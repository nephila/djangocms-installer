# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

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

iteritems = six.iteritems

StringIO = six.StringIO
