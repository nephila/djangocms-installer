# -*- coding: utf-8 -*-
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
    input = raw_input

    def clean(value):
        if value:
            return value.strip().decode("utf-8")
        else:
            return value

    unicode = unicode

iteritems = six.iteritems

StringIO = six.StringIO
