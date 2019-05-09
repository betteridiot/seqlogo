from setuptools.command.test import test as TestCommand
from setuptools import setup
import os
import sys
from os import path

__version__ = '5.29.4'

def readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


class PyTest(TestCommand):
    user_args = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        if errno:
            sys.exit(errno)
        else:
            errno = pytest.main(['-Wignore'])
            sys.exit(errno)


setup(
    name='seqlogo',
    version=__version__,
    description='Python port of the R Bioconductor `seqlogo` package ',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/betteridiot/seqlogo',
    author='Marcus D. Sherman',
    author_email='mdsherman@betteridiot.tech',
    license='BSD 3-Clause',
    install_requires=[
        'numpy',
        'pandas',
        'weblogo',
        'ghostscript',
        'pytest'
    ],
    tests_require=['pytest'],
    cmdclass = {'test' : PyTest},
    packages=['seqlogo', 'seqlogo.tests'],
    package_dir={'seqlogo': './seqlogo'},
    package_data={'seqlogo': ['docs/*']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    keywords='sequence logo seqlogo bioinformatics genomics weblogo',
    include_package_data=True,
    zip_safe=False
)

