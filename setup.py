#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='aldryn-installer',
    version='0.1.0',
    description='Command to easily bootstrap django CMS projects',
    long_description=readme + '\n\n' + history,
    author='Iacopo Spalletti',
    author_email='i.spalletti@nephila.it',
    url='https://github.com/nephila/aldryn-installer',
    packages=[
        'aldryn_installer',
    ],
    package_dir={'aldryn-installer': 'aldryn_installer'},
    include_package_data=True,
    install_requires=[
        'pip',
        'dj-database-url'
    ],
    entry_points={
        'console_scripts': [
            'aldryn-installer = aldrin_installer.main:execute',
        ]
    },
    license="BSD",
    zip_safe=False,
    keywords='aldryn-installer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)