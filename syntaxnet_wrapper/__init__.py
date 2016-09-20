import subprocess
import os
import six
import time
import signal

from shutil import copyfile
from os.path import join, dirname, abspath, isfile
from fcntl import fcntl, F_SETFL, F_GETFD

__all__ = ['parser', 'tagger']


class SyntaxNetWrapper(object):
    def __del__(self):
        self.din.close()
        try:
            self.process.send_signal(signal.SIGABRT)
            self.process.kill()
            self.process.wait()
        except OSError:
            pass

    def __init__(self, run_filename, model_name):
        self.model_name = model_name
        if model_name == 'English-Parsey':
            model_path = 'models/syntaxnet'
            context_path = 'models/syntaxnet/syntaxnet/models/parsey_mcparseface/context.pbtxt'
        else:
            model_path = 'models/syntaxnet/syntaxnet/models/parsey_universal/{!s}'.format(model_name)
            context_path = 'models/syntaxnet/syntaxnet/models/parsey_universal/context.pbtxt'
        pwd = dirname(abspath(__file__))
        model_path = join(pwd, model_path)
        rundir = join(pwd, 'models/syntaxnet/bazel-bin/syntaxnet/parser_eval.runfiles')
        context_path = join(pwd, context_path)
        command = ['python', run_filename, model_path, context_path]

        copyfile(join(pwd, run_filename), join(rundir, run_filename))

        print command, rundir
        env = os.environ.copy()
        subproc_args = {'stdin': subprocess.PIPE, 'stdout': subprocess.PIPE,
                        'stderr': subprocess.STDOUT, 'cwd': rundir,
                        'env': env, 'close_fds': True}
        self.process = subprocess.Popen(command, shell=False, **subproc_args)
        self.out = self.process.stdout
        self.din = self.process.stdin
        fcntl(self.out.fileno(), F_SETFL, fcntl(self.out.fileno(), F_GETFD) | os.O_NONBLOCK)

    def isReady(self):
        '''A blocking function to wait for NiuParser program ready.
        '''
        timeout = 0
        print 'check module is ready'
        while True:
            try:
                result = self.out.readline().decode('utf-8').strip()
                print result
                if result == '## input content:':
                    print 'ready'
                    return True
            except Exception as e:
                time.sleep(0.1)
                timeout += 1
                if timeout > 100:
                    raise Exception('error')


    def query(self, text, returnRaw=False):
        self.isReady()  # blocked until ready
        self.din.write(text.encode('utf8') + six.b('\n'))
        self.din.flush()
        self.process.send_signal(signal.SIGALRM)
        results = []
        result = None
        start = 0
        timeout = 0 
        while True:
            try:
                result = self.out.readline().decode('utf8')[:-1]

                if result == '## result end':
                    break

                if start:
                    results.append(result)

                if result == '## result start':
                    start = 1
            except:
                time.sleep(0.1)
                pass

        if returnRaw:
            return '\n'.join(results).strip()
        return [r.split('\t') for r in results[:-1]]

    def list_models(self):
        pwd = dirname(abspath(__file__))
        model_path = os.path.join(pwd, 'models/syntaxnet/syntaxnet/models/parsey_universal')
        files = os.listdir(model_path)
        models = []
        for fn in files:
            if os.path.isdir(os.path.join(model_path, fn)):
                models.append(fn)
        models.append('English-Parsey')
        return sorted(models)


class SyntaxNetMorpher(SyntaxNetWrapper):
    def __init__(self, model_name='English'):
        super(SyntaxNetMorpher, self).__init__('morpher_eval_forever.py', model_name)


class SyntaxNetTagger(SyntaxNetWrapper):
    def __init__(self, model_name='English-Parsey', **kwargs):
        if model_name == 'English-Parsey':
            self.morpher = None
        elif 'morpher' in kwargs:
            self.morpher = kwargs['morpher']
        else:
            self.morpher = SyntaxNetMorpher(model_name)
        super(SyntaxNetTagger, self).__init__('tagger_eval_forever.py', model_name)

    def query(self, text, returnRaw=False):
        if self.morpher:
            text = self.morpher.query(text, returnRaw=True)
        return super(SyntaxNetTagger, self).query(text, returnRaw)


class SyntaxNetParser(SyntaxNetWrapper):
    def __init__(self, model_name='English-Parsey', **kwargs):
        if 'tagger' in kwargs:
            self.tagger = kwargs['tagger']
            self.morpher = self.tagger.morpher
        else:
            if model_name == 'English-Parsey':
                self.morpher = None
            elif 'morpher' in kwargs:
                self.morpher = kwargs['morpher']
            else:
                self.morpher = SyntaxNetMorpher(model_name)
            self.tagger = SyntaxNetTagger(model_name, morpher=self.morpher)
        super(SyntaxNetParser, self).__init__('parser_eval_forever.py', model_name)

    def query(self, text, returnRaw=False):
        text = self.tagger.query(text, returnRaw=True)
        return super(SyntaxNetParser, self).query(text, returnRaw)


language_code_to_model_name = {
    'ar': 'Arabic',
    'eu': 'Basque',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'zh': 'Chinese',
    'zh-tw': 'Chinese',
    'zh-cn': 'Chinese',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English-Parsey',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'de': 'German',
    'el': 'Greek',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'kk': 'Kazakh',
    'la': 'Latin',
    'lv': 'Latvian',
    'no': 'Norwegian',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'tr': 'Turkish',
}


class Tagger(object):
    cached = {}

    def __del__(self):
        for code in self.cached:
            tmp = self.cached[code]
            self.cached[code] = None
            del tmp

    def __getitem__(self, code):
        if code not in language_code_to_model_name:
            raise ValueError('Invalid language code for tagger: {}'.format(code))
        lang = language_code_to_model_name[code]
        if code in self.cached:
            return self.cached[code]
        self.cached[code] = SyntaxNetTagger(lang)
        return self.cached[code]

tagger = Tagger()


class Parser(object):
    cached = {}

    def __del__(self):
        for code in self.cached:
            tmp = self.cached[code]
            self.cached[code] = None
            del tmp

    def __getitem__(self, code):
        if code not in language_code_to_model_name:
            raise ValueError('Invalid language code for parser: {}'.format(code))
        lang = language_code_to_model_name[code]
        if code in self.cached:
            return self.cached[code]
        self.cached[code] = SyntaxNetParser(lang, tagger=tagger[code])
        return self.cached[code]

parser = Parser()
