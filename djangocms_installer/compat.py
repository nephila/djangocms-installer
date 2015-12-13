# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import subprocess

import six

if six.PY3:
    input = input

    def clean(value):
        if value:
            return value.strip()
        else:
            return value

    unicode = str

else:
    input = raw_input  # NOQA

    def clean(value):
        if value:
            return value.strip().decode('utf-8')
        else:
            return value

    unicode = unicode  # NOQA

if 'check_output' not in dir(subprocess):
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get('args')
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f
