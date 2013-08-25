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

requirements = open('requirements.txt').readlines()
test_requirements = []

# Add Python 2.6-specific dependencies
if sys.version_info[:2] < (2, 7):
    requirements.append('argparse')
    test_requirements.append('unittest2')
# Add Python 2.6 and 2.7-specific dependencies
if sys.version < '3':
    test_requirements.append('mock')


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
    install_requires=requirements,
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
    test_requirements=test_requirements
)