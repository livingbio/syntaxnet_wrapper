from __future__ import print_function
from setuptools import setup
from setuptools.command.install import install
import sys
import subprocess


class InstallClass(install):
    def run(self):
        install.run(self)
        subprocess.call(['pip', 'install', 'tensorflow', 'virtualenv', 'protobuf', 'asciitree', 'mock'])
        sys.path.reverse()


setup(name='syntaxnet_wrapper',
      version='0.4.1',
      description='A Python Wrapper for Google SyntaxNet',
      url='https://github.com/livingbio/syntaxnet_wrapper',
      author='Ping Chu Hung',
      author_email='banyhong@gliacloud.com',
      license='MIT',
      packages=['syntaxnet_wrapper'],
      zip_safe=False,
      install_requires=[
          'tensorflow',
          'virtualenv',
          'protobuf',
          'asciitree',
          'mock',
      ],
      cmdclass={
          'install': InstallClass,
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      package_data={'syntaxnet_wrapper': ['makefile']}
)
