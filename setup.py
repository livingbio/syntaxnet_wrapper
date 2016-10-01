from setuptools import setup
from setuptools.command.install import install
import sys
import subprocess
from os import path
import os
import pip
import stat
import site
from distutils.sysconfig import get_python_lib

model_list = ['Arabic', 'Basque', 'Bulgarian', 'Catalan', 'Chinese', 'Croatian',
    'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'Finnish', 'French',
    'Galician', 'German', 'Gothic', 'Greek', 'Hebrew', 'Hindi', 'Hungarian',
    'Indonesian', 'Irish', 'Italian', 'Kazakh', 'Latin', 'Latvian', 'Norwegian',
    'Persian', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Slovenian',
    'Spanish', 'Swedish', 'Tamil', 'Turkish', ]


class InstallClass(install):
    def run(self):
        install.run(self)
        sys.path.reverse()
        import syntaxnet_wrapper
        syntaxnet_wrapper_dir = syntaxnet_wrapper.__path__[0]
        subprocess.call(['make'], cwd=syntaxnet_wrapper_dir)


class InstallTarClass(install):
    def run(self):
        pip.main(['install', 'https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0rc0-cp27-none-linux_x86_64.whl'])
        install.run(self)
        package_dir = [p for p in sys.path if p.endswith('site-packages')][0]
        package_dir = path.join(package_dir, 'syntaxnet_wrapper')
        print 'Start downloading syntaxnet.tgz...'
        subprocess.call(['wget', '-q', 'https://gliacloud.blob.core.windows.net/nlp/syntaxnet.tgz'], cwd=package_dir)
        print 'Start extracting syntaxnet.tgz...'
        subprocess.call(['tar', 'xzf', 'syntaxnet.tgz'], cwd=package_dir)
        model_dir = path.join(package_dir, 'models/syntaxnet/syntaxnet/models/parsey_universal')
        model_url = 'http://download.tensorflow.org/models/parsey_universal/{}.zip'
        print 'Start downloading pretrained models...'
        for model_name in model_list:
            subprocess.call(['wget', '-q', model_url.format(model_name)], cwd=model_dir)
            subprocess.call(['unzip', '-n', '-qq', '{}.zip'.format(model_name)], cwd=model_dir)
            os.unlink(path.join(model_dir, '{}.zip'.format(model_name)))
            dir_name = path.join(model_dir, model_name)
            os.chmod(dir_name, os.stat(dir_name).st_mode | stat.S_IROTH | stat.S_IXOTH)
            for fn in os.listdir(dir_name):
                fpath = path.join(dir_name, fn)
                os.chmod(fpath, os.stat(fpath).st_mode | stat.S_IROTH)
            print model_name, 'model is installed.'

setup(name='syntaxnet_wrapper',
      version='0.3.1',
      description='A Python Wrapper for Google SyntaxNet',
      url='https://github.com/livingbio/syntaxnet_wrapper',
      author='Ping Chu Hung',
      author_email='banyhong@gliacloud.com',
      license='MIT',
      packages=['syntaxnet_wrapper'],
      zip_safe=False,
      install_requires=[
          'protobuf==3.0.0b2',
          'asciitree',
      ],
      cmdclass={
          'install': InstallClass,
          'install_tar': InstallTarClass,
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      package_data={'syntaxnet_wrapper': ['makefile']}
)
