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


setup(name='syntaxnet_wrapper',
      version='0.2.1',
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
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      package_data={'syntaxnet_wrapper': ['models.tgz', 'makefile']}
)
