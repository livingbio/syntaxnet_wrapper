from __future__ import unicode_literals, print_function
import re
import sys
import signal
from os import path

import tensorflow as tf

from google.protobuf import text_format
from tensorflow.python.platform import gfile

from dragnn.protos import spec_pb2
from dragnn.python import graph_builder
from dragnn.python import spec_builder
from syntaxnet import sentence_pb2
from syntaxnet.util import check

import dragnn.python.load_dragnn_cc_impl
import syntaxnet.load_parser_ops


def length_to_bytes(length):
    if length <= 0x7f:
        return [length]
    else:
        return [length % 0x80 + 0x80, (length - 0x80) // 0x80 + 1]


def gen_char_corpus(sentence):
    char = bytearray([18])
    byte_sent = sentence.encode('utf8')
    len_sent = len(byte_sent)
    char.extend(length_to_bytes(len_sent))
    char.extend(byte_sent)
    pos = 0
    for ch in sentence:
        byte_ch = ch.encode('utf8')
        chlen = len(byte_ch)
        end_pos = pos + chlen - 1
        itemlen = 6 + chlen + int(pos > 0x7f) + int(end_pos > 0x7f)

        char.extend([26, itemlen, 10, chlen])
        char.extend(byte_ch)
        char.append(16)
        char.extend(length_to_bytes(pos))
        char.append(24)
        char.extend(length_to_bytes(end_pos))
        pos += chlen
    return bytes(char)


def gen_seg_corpus(words, sep=' '):
    sentence = sep.join(words)
    char = bytearray([18])
    byte_sent = sentence.encode('utf8')
    char.extend(length_to_bytes(len(byte_sent)))
    char.extend(byte_sent)
    pos = 0
    non_first_word = 0
    for w in words:
        byte_word = w.encode('utf8')
        len_word = len(byte_word)
        end_pos = pos + len_word - 1
        itemlen = 8 + len_word + int(pos > 0x7f) + int(end_pos > 0x7f)

        char.extend([26, itemlen, 10, len_word])
        char.extend(byte_word)
        char.append(16)
        char.extend(length_to_bytes(pos))
        char.append(24)
        char.extend(length_to_bytes(end_pos))
        char.append(64)
        char.append(non_first_word)
        non_first_word = 1
        pos += len_word + len(sep)
    return bytes(char)


def post_parse(processed_sentence):
    parsed_sents = []
    for serialized_sentence in processed_sentence:
        sentence = sentence_pb2.Sentence()
        sentence.ParseFromString(serialized_sentence)
        sent = []
        for i, token in enumerate(sentence.token):
            item = {'pos': '_', 'ptb': '_', 'head': -1}
            for field, value in sorted(token.ListFields())[::-1]:
                if field.json_name == 'tag':
                    attrs = re.findall('(\w+): +\"([\w\+]+)\" +(\w+): +\"([\w\+\$]+)\"', token.tag)
                    for _, name, _, val in attrs:
                        if name == 'fPOS':
                            pos, ptb = val.split('++')
                            item['pos'] = pos
                            item['ptb'] = ptb
                        else:
                            item[name] = val
                elif field.json_name == 'word':
                    item['name'] = value
                else:
                    if field.json_name == 'label' and value == 'punct':
                        item['pos'] = 'PUNCT'
                        if 'name' in item:
                            item['ptb'] = item['name'][0]
                        else:
                            item['ptb'] = '.'
                    item[field.json_name] = value
            sent.append(item)
        parsed_sents.append(sent)
    return parsed_sents


if __name__ == '__main__':
    model_name = sys.argv[1]
    basedir = path.join(path.dirname(__file__), 'models', 'syntaxnet')
    exec_dir = path.join(basedir, 'bazel-bin', 'dragnn', 'tools', 'parse-to-conll.runfiles', '__main__')
    model_dir = path.join(basedir, 'dragnn', 'conll17', model_name)
    seg_dir = path.join(basedir, 'dragnn', 'conll17', model_name, 'segmenter')
    assert path.isdir(model_dir)
    assert path.isdir(seg_dir)
    assert path.isdir(exec_dir)

    parser_master_spec = path.join(model_dir, 'parser_spec.textproto')
    parser_checkpoint_file = path.join(model_dir, 'checkpoint')
    parser_resource_dir = model_dir
    segmenter_master_spec = path.join(seg_dir, 'spec.textproto')
    segmenter_checkpoint_file = path.join(seg_dir, 'checkpoint')
    segmenter_resource_dir = seg_dir
    component_beam_sizes = [('char_lstm', '16'), ('lookahead', '16'),
                            ('tagger', '32'), ('parser', '64')]

    master_spec = spec_pb2.MasterSpec()
    with gfile.FastGFile(parser_master_spec) as fin:
        text_format.Parse(fin.read(), master_spec)
    spec_builder.complete_master_spec(master_spec, None, parser_resource_dir)

    g = tf.Graph()
    with g.as_default(), tf.device('/device:CPU:0'):
        hyperparam_config = spec_pb2.GridPoint()
        hyperparam_config.use_moving_average = True
        builder = graph_builder.MasterBuilder(master_spec, hyperparam_config)
        annotator = builder.add_annotation()
        builder.add_saver()

    sess = tf.Session(graph=g)
    with g.as_default():
        with sess.as_default():
            sess.run(tf.global_variables_initializer())
            sess.run('save/restore_all', {'save/Const:0': parser_checkpoint_file})

    def stdin_handler(signum, frame):
        line = sys.stdin.readline()[:-1].decode('utf8')
        char_corpus = [gen_seg_corpus(line.split())]
        feed_dict = {annotator['input_batch']: char_corpus}
        for comp, beam_size in component_beam_sizes:
            feed_dict['%s/InferenceBeamSize:0' % comp] = beam_size
        results = sess.run(annotator['annotations'], feed_dict=feed_dict)
        parsed = post_parse(results)

        sys.stdout.write('\n## result start\n')
        sys.stdout.flush()
        for sent in parsed:
            for i, word in enumerate(sent):
                conll = '\t'.join([str(i + 1), word['name'], '_', word['pos'], word['ptb'], '_',
                                   str(word['head'] + 1), word['label'], '_', '_'])
                print(conll.encode('utf8'))
            print()
        sys.stdout.write('\n## result end\n')
        sys.stdout.flush()

    def abort_handler(signum, frame):
        sess.close()
        sys.exit(0)

    signal.signal(signal.SIGALRM, stdin_handler)
    signal.signal(signal.SIGABRT, abort_handler)

    while True:
        sys.stdout.write('\n## input content:\n')
        sys.stdout.flush()
        signal.alarm(1800)
        signal.pause()
