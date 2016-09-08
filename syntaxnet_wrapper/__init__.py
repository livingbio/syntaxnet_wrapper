import subprocess
import os
import six
import time
from shutil import copyfile
from os.path import join, dirname, abspath, isfile
from fcntl import fcntl, F_SETFL, F_GETFD

__all__ = ['SyntaxNetParser', 'SyntaxNetTagger', 'SyntaxNetMorpher']


class SyntaxNetWrapper(object):
    def __del__(self):
        self.din.close()
        try:
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
        self.isReady()  # blocked until ready
        self.isReady()  # blocked until ready

    def isReady(self):
        '''A blocking function to wait for NiuParser program ready.
        '''
        result = ''
        timeout = 0
        while not result.endswith(u'/word-map.'):
            time.sleep(0.001)
            timeout += 1
            try:
                result = self.out.readline().decode('utf8')[:-1]
                # print result
            except:
                result = ''
            if timeout > 2000:
                break

    def query(self, text, returnRaw=False):
        self.din.write(text.encode('utf8') + six.b('\n'))
        self.din.flush()
        results = []
        result = None
        while not result:
            try:
                result = self.out.readline().decode('utf8')[:-1]
            except:
                result = None
        results.append(result)
        try:
            while True:
                results.append(self.out.readline().decode('utf8')[:-1])
        except:
            pass
        if returnRaw:
            return '\n'.join(results)
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
