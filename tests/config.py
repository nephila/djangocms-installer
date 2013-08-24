#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_aldryn-installer
----------------------------------

Tests for `aldryn-installer` module.
"""
import sys

PY3 = sys.version > '3'

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO

try:
    import unittest2 as unittest
except ImportError:
    import unittest


import aldryn_installer.config


class TestAldrynInstaller(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestConfig(unittest.TestCase):
    def test_default_config(self):
        config = aldryn_installer.config.parse(["-q", "test_project"])

        self.assertEqual(config.project_name, 'test_project')

        self.assertEqual(config.cms_version, 'latest')
        self.assertEqual(config.django_version, 'latest')
        self.assertEqual(config.south, 'yes')
        self.assertEqual(config.i18n, 'yes')
        self.assertEqual(config.db, None)

        self.assertEqual(config.no_db_driver, False)
        self.assertEqual(config.no_deps, False)
        self.assertEqual(config.no_sync, False)
        self.assertEqual(config.plugins, False)
        self.assertEqual(config.requirements, None)

    def test_cli_config(self):
        config = aldryn_installer.config.parse([
            "-q",
            "--db=mysql://user:pwd@host/dbname",
            "--cms-version=2.4",
            "--django-version=1.5",
            "--south=no",
            "--i18n=no",
            "test_project"])

        self.assertEqual(config.project_name, 'test_project')

        self.assertEqual(config.cms_version, '2.4')
        self.assertEqual(config.django_version, '1.5')
        self.assertEqual(config.south, 'no')
        self.assertEqual(config.i18n, 'no')
        self.assertEqual(config.db, 'mysql://user:pwd@host/dbname')

    def test_invalud_choices(self):
        saved_stderr = sys.stderr
        err = StringIO()
        sys.stderr = err
        with self.assertRaises(SystemExit) as error:
            config = aldryn_installer.config.parse([
                "-q",
                "--db=mysql://user:pwd@host/dbname",
                "--cms-version=2.6",
                "--django-version=1.1",
                "--south=no",
                "--i18n=no",
                "test_project"])
            self.assertTrue(str(error.exception).find("--cms-version/-v: invalid choice: '2.6'") > -1)

        sys.stderr = saved_stderr