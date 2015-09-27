#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import djangocms_installer
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open('requirements.txt').readlines()
test_requirements = []

# Add Python 2.6-specific dependencies
if sys.version_info[:2] < (2, 7):
    test_requirements.append('unittest2')


setup(
    name='djangocms-installer',
    version=djangocms_installer.__version__,
    description='Command to easily bootstrap django CMS projects',
    long_description=readme + '\n\n' + history,
    author='Iacopo Spalletti',
    author_email='i.spalletti@nephila.it',
    url='https://github.com/nephila/djangocms-installer',
    packages=find_packages(),
    package_dir={'djangocms_installer': 'djangocms_installer'},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'djangocms = djangocms_installer.main:execute',
        ]
    },
    license='BSD',
    zip_safe=False,
    keywords='djangocms-installer',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Topic :: Software Development',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
