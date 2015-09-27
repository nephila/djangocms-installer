# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys

from .main import execute

if __name__ == '__main__':
    status = execute()
    if status:
        sys.exit(status)
