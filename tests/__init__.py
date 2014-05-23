#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import tempfile
import shutil

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from six import StringIO


class BaseTestClass(unittest.TestCase):
    stdout = None
    stderr = None
    project_dir = None

    def _remove_project_dir(self):
        if self.project_dir:
            shutil.rmtree(self.project_dir)
            self.project_dir = None

    def _create_project_dir(self):
        if 'USE_SHM' in os.environ:
            if os.path.exists('/run/shm'):
                self.project_dir = tempfile.mkdtemp(dir='/run/shm')
            elif os.path.exists('/dev/shm'):
                self.project_dir = tempfile.mkdtemp(dir='/dev/shm')
            else:
                self.project_dir = tempfile.mkdtemp()
        else:
            self.project_dir = tempfile.mkdtemp()

    def tearDown(self):
        self._remove_project_dir()
        self.stdout = None
        self.stderr = None

    def setUp(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self._create_project_dir()
