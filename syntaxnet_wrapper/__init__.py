import subprocess
import os
import six
import time
from shutil import copyfile
from os.path import join, dirname, abspath, isfile
from fcntl import fcntl, F_SETFL, F_GETFD

__all__ = ['SyntaxNetParser', 'SyntaxNetTagger']


class SyntaxNetTagger(object):
    def __del__(self):
        self.din.close()
        try:
            self.process.kill()
            self.process.wait()
        except OSError:
            pass

    def __init__(self, model_name='English'):
        model_path = 'models/syntaxnet/syntaxnet/models/parsey_universal/{!s}'.format(model_name)
        run_filename = 'tagger_eval_forever.py'
        pwd = dirname(abspath(__file__))
        model_path = join(pwd, model_path)
        rundir = join(pwd, 'models/syntaxnet/bazel-bin/syntaxnet/parser_eval.runfiles')
        context_path = join(pwd, 'models/syntaxnet/syntaxnet/models/parsey_universal/context.pbtxt')
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
            time.sleep(0.01)
            timeout += 1
            try:
                result = self.out.readline().decode('utf8')[:-1]
                # print result
            except:
                result = ''
            if timeout > 1000:
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


class SyntaxNetParser(object):
    def __del__(self):
        del self.tagger
        self.din.close()
        try:
            self.process.kill()
            self.process.wait()
        except OSError:
            pass

    def __init__(self, model_name='English', **kwargs):
        model_path = 'models/syntaxnet/syntaxnet/models/parsey_universal/{!s}'.format(model_name)
        if 'tagger' in kwargs:
            self.tagger = kwargs['tagger']
        else:
            self.tagger = SyntaxNetTagger(model_name)
        run_filename = 'parser_eval_forever.py'
        pwd = dirname(abspath(__file__))
        model_path = join(pwd, model_path)
        rundir = join(pwd, 'models/syntaxnet/bazel-bin/syntaxnet/parser_eval.runfiles')
        context_path = join(pwd, 'models/syntaxnet/syntaxnet/models/parsey_universal/context.pbtxt')
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
            time.sleep(0.01)
            timeout += 1
            try:
                result = self.out.readline().decode('utf8')[:-1]
                # print result
            except:
                result = ''
            if timeout > 1000:
                break

    def query(self, text, returnRaw=False):
        tagged_text = self.tagger.query(text, returnRaw=True)
        self.din.write(tagged_text.encode('utf8') + six.b('\n'))
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
        return [r.split('\t') for r in results]
