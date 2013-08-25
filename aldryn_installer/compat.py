# -*- coding: utf-8 -*-
import sys
PY3 = sys.version > '3'
if PY3:
    input = input
    iteritems = lambda d: iter(d.items())

    def clean(value): return value.strip()

else:
    input = raw_input
    iteritems = lambda d: d.iteritems()

    def clean(value):
        if value:
            return value.strip().decode("utf-8")
        else:
            return value