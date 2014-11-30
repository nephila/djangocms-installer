# -*- coding: utf-8 -*-
import sys

from .main import execute

if __name__ == '__main__':
    status = execute()
    if status:
        sys.exit(status)
