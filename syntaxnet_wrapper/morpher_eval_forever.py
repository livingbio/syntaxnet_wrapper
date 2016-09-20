# -*- coding: utf-8 -*-
import os
import os.path
import sys
import signal

import tempfile
import tensorflow as tf

from tensorflow.python.platform import gfile

from google.protobuf import text_format

from syntaxnet import structured_graph_builder
from syntaxnet.ops import gen_parser_ops
from syntaxnet import task_spec_pb2

morpher_hidden_layer_sizes = '64'
morpher_arg_prefix = 'brain_morpher'
# graph_builder = 'structured'
slim_model = True
batch_size = 1
beam_size = 8
max_steps = 1000
resource_dir = sys.argv[1]
context_path = sys.argv[2]
morpher_model_path = os.path.join(resource_dir, 'morpher-params')


def RewriteContext(task_context):
    context = task_spec_pb2.TaskSpec()
    with gfile.FastGFile(task_context) as fin:
        text_format.Merge(fin.read(), context)
    for resource in context.input:
        for part in resource.part:
            if part.file_pattern != '-':
                part.file_pattern = os.path.join(resource_dir, part.file_pattern)
    with tempfile.NamedTemporaryFile(delete=False) as fout:
        fout.write(str(context))
        return fout.name


sess = tf.Session()

task_context = RewriteContext(context_path)
feature_sizes, domain_sizes, embedding_dims, num_actions = sess.run(
    gen_parser_ops.feature_size(task_context=task_context, arg_prefix=morpher_arg_prefix))
hidden_layer_sizes = map(int, morpher_hidden_layer_sizes.split(','))
morpher = structured_graph_builder.StructuredGraphBuilder(
    num_actions, feature_sizes, domain_sizes, embedding_dims,
    hidden_layer_sizes, gate_gradients=True, arg_prefix=morpher_arg_prefix,
    beam_size=beam_size, max_steps=max_steps)
morpher.AddEvaluation(task_context, batch_size, corpus_name='stdin',
                      evaluation_max_steps=max_steps)

morpher.AddSaver(slim_model)
sess.run(morpher.inits.values())
morpher.saver.restore(sess, morpher_model_path)

sink_documents = tf.placeholder(tf.string)
sink = gen_parser_ops.document_sink(sink_documents, task_context=task_context,
                                    corpus_name='stdout-conll')


def stdin_handler(signum, frame):
    tf_eval_epochs, tf_eval_metrics, tf_documents = sess.run([
        morpher.evaluation['epochs'],
        morpher.evaluation['eval_metrics'],
        morpher.evaluation['documents'],
    ])

    sys.stdout.write('\n## result start\n')
    sys.stdout.flush()

    if len(tf_documents):
        sess.run(sink, feed_dict={sink_documents: tf_documents})

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
    signal.pause()
