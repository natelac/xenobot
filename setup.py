import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name='xenobot',
        version='0.1.0',
        description='Discord server logging',
        author='Nathaniel Lacelle',
        author_email='natelac@umich.edu',
        long_description=read('README.md'),
        install_requires=['discord'],
        python_requires='>=3.8',
      )
