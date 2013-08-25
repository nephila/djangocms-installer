#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
import tempfile

from aldryn_installer import config, django

PY3 = sys.version > '3'

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestDjango(unittest.TestCase):
    def test_create_project(self):
        tmp_dir = tempfile.mkdtemp()
        conf_data = config.parse(['--db=mysql://user:pwd@host/dbname',
                                  '-q', '-p'+tmp_dir, 'test_project'])
        django.create_project(conf_data)
        self.assertTrue(os.path.exists(os.path.join(tmp_dir, 'test_project')))