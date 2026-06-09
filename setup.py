#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


setup(
    name='qaforge',
    use_scm_version={
        'local_scheme': 'dirty-tag',
        'write_to': 'src/qaforge/_version.py',
        'fallback_version': '0.0.4',
    },
    license='MIT',
    description='QA automation toolkit: helpers for requests, JSON, CSV, YAML, databases and data generation.',
    long_description='{}\n{}'.format(
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst')),
    ),
    author='Priscilla Rodrigues Martins',
    author_email='angeleyes.ffx@hotmail.com',
    url='https://github.com/angeleyesffx/qaforge',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://qaforge.readthedocs.io/',
        'Changelog': 'https://qaforge.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/angeleyesffx/qaforge/issues',
    },
    keywords=['qa', 'automation', 'testing', 'toolkit'],
    python_requires='>=3.9',
    install_requires=[
        'Jinja2~=3.1',
        'PyMySQL~=1.0',
        'psycopg2-binary~=2.9',
        'pyyaml~=6.0',
        'requests~=2.28',
    ],
    setup_requires=[
        'setuptools_scm>=3.3.1',
    ],
    entry_points={
        'console_scripts': [
            'qaforge = qaforge.cli:main',
        ]
    },
)
