#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import shutil

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

if sys.version_info[0] > 2:
    from io import StringIO
else:
    from StringIO import StringIO


class PatchStd(object):
    """Context manager for patching stdout / stderr"""
    stdout = None
    stderr = None
    saved_out = None
    saved_err = None

    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr

    def __enter__(self):
        self.saved_out = sys.stdout
        self.saved_err = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def __exit__(self, etype, value, traceback):
        sys.stdout = self.saved_out
        sys.stderr = self.saved_err


class BaseTestClass(unittest.TestCase):
    stdout = None
    stderr = None
    project_dir = None

    def tearDown(self):
        if self.project_dir:
            shutil.rmtree(self.project_dir)
        self.stdout = None
        self.stderr = None

    def setUp(self):
        self.stdout = StringIO()
        self.stderr = StringIO()