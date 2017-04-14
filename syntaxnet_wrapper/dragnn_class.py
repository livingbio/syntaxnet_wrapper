import subprocess
import os
import stat
import six
import signal

from fcntl import fcntl, F_SETFL, F_GETFD
import time
from datetime import datetime, timedelta
import logging
from os.path import join, dirname, abspath

logger = logging.getLogger()
pwd = dirname(abspath(__file__))
PIDFILE_PATH = os.path.join(pwd, 'pids')


class TimeoutException(Exception):
    pass


class DragnnWrapper(object):

    def __del__(self):
        self.stop()

    def clean_zombie_process(self):
        for pidfile in os.listdir(PIDFILE_PATH):
            if not pidfile.endswith('.pid') or pidfile.count('_') != 2:
                continue
            pid, model, clsname = pidfile.split('_')
            try:
                os.kill(int(pid), 0)
                os.unlink(os.path.join(PIDFILE_PATH, pidfile))
            except:
                logger.info('kill zombie process {}'.format(pid))
                self.kill_process(pidfile)

    def kill_process(self, pidfile):
        try:
            with open(os.path.join(PIDFILE_PATH, pidfile)) as f:
                pid = f.read().strip()
                try:
                    os.kill(int(pid), 9)
                except Exception as e:
                    logger.info(e)
            os.unlink(os.path.join(PIDFILE_PATH, pidfile))
        except Exception as e:
            logger.info(e)

    def make_pidfile(self):
        if not os.path.isdir(PIDFILE_PATH):
            os.mkdir(PIDFILE_PATH)
        pidfilename = os.path.join(PIDFILE_PATH, "{}.pid".format(self.name))
        for fn in os.listdir(PIDFILE_PATH):
            if not fn.endswith('.pid') or fn.count('_') != 2:
                continue
            pid, model, clsname = fn.split('_')
            if clsname == self.__class__.__name__ + '.pid' and model == self.model_name:
                self.kill_process(fn)
        with open(pidfilename, 'w+') as f:
            f.write(str(self.process.pid))
        os.chmod(pidfilename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

    @property
    def name(self):
        return u"{}_{}_{}".format(os.getpid(), self.model_name, self.__class__.__name__)

    def start(self):
        rundir = join(pwd, 'models', 'syntaxnet', 'bazel-bin', 'dragnn', 'tools', 'parse-to-conll.runfiles', '__main__')
        command = ['python', self.run_filename, self.model_name]

        env = os.environ.copy()
        env['PYTHONPATH'] = rundir
        subproc_args = {'stdin': subprocess.PIPE, 'stdout': subprocess.PIPE,
                        'stderr': subprocess.STDOUT, 'cwd': pwd,
                        'env': env, 'close_fds': True}
        self.process = subprocess.Popen(command, shell=False, **subproc_args)
        self.out = self.process.stdout
        self.din = self.process.stdin
        fcntl(self.out.fileno(), F_SETFL, fcntl(self.out.fileno(), F_GETFD) | os.O_NONBLOCK)
        self.make_pidfile()

    def stop(self):
        self.din.close()
        try:
            import signal  # wordaround for AttributeError("'NoneType' object has no attribute 'SIGTERM'",)
            os.kill(self.process.pid, signal.SIGTERM)
            self.process.send_signal(signal.SIGTERM)
            self.process.kill()
            self.process.wait()
        except OSError:
            pass

    def __init__(self, run_filename, model_name):
        self.model_name = model_name
        self.run_filename = run_filename
        self.start()

    def restart(self):
        self.stop()
        self.start()

    def wait_for(self, text, timeout=5):
        result = []
        start_time = datetime.now()
        while True:
            try:
                line = self.out.readline().decode('utf-8').strip()
                if text == line:
                    return result
                result.append(line)
            except:
                # read timeout
                time.sleep(0.1)
            finally:
                now = datetime.now()
                if(now - start_time) > timedelta(0, timeout):
                    raise TimeoutException()

    def __query(self, text, returnRaw=False):
        self.wait_for('## input content:')

        # push data
        self.din.write(text.encode('utf8') + six.b('\n'))
        self.din.flush()
        self.process.send_signal(signal.SIGALRM)

        self.wait_for('## result start')
        results = self.wait_for('## result end')

        if returnRaw:
            return '\n'.join(results).strip() + "\n"
        return [r.split('\t') for r in results[:-2]]

    def query(self, text, returnRaw=False):
        for i in xrange(3):
            try:
                return self.__query(text, returnRaw)
            except Exception:
                # retart process
                self.restart()

    def list_models(self):
        pwd = dirname(abspath(__file__))
        model_path = os.path.join(pwd, 'models', 'syntaxnet', 'dragnn', 'conll17')
        files = os.listdir(model_path)
        models = []
        for fn in files:
            if os.path.isdir(os.path.join(model_path, fn)):
                models.append(fn)
        return sorted(models)


class DragnnParser(DragnnWrapper):

    def __init__(self, model_name='English', **kwargs):
        super(DragnnParser, self).__init__('dragnn_parse_forever.py', model_name)

    def query(self, text, returnRaw=False):
        return super(DragnnParser, self).query(text, returnRaw)
