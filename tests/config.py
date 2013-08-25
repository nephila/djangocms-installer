#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_aldryn-installer
----------------------------------

Tests for `aldryn-installer` module.
"""
import sys
from aldryn_installer.config import data

PY3 = sys.version > '3'

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


import aldryn_installer.config


class TestAldrynInstaller(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestConfig(unittest.TestCase):
    def test_default_config(self):
        config = aldryn_installer.config.parse(["--db=mysql://user:pwd@host/dbname",
                                                "-q", "test_project"])

        self.assertEqual(config.project_name, 'test_project')

        self.assertEqual(config.cms_version, 'latest')
        self.assertEqual(config.django_version, 'latest')
        self.assertEqual(config.i18n, 'yes')
        self.assertEqual(config.db, "mysql://user:pwd@host/dbname")

        self.assertEqual(config.no_db_driver, False)
        self.assertEqual(config.no_deps, False)
        self.assertEqual(config.no_sync, False)
        self.assertEqual(config.plugins, False)
        self.assertEqual(config.requirements_file, None)

    def test_cli_config(self):
        config = aldryn_installer.config.parse([
            "-q",
            "--db=mysql://user:pwd@host/dbname",
            "--cms-version=2.4",
            "--django-version=1.5",
            "--i18n=no",
            "test_project"])

        self.assertEqual(config.project_name, 'test_project')

        self.assertEqual(config.cms_version, '2.4')
        self.assertEqual(config.django_version, '1.5')
        self.assertEqual(config.i18n, 'no')
        self.assertEqual(config.db, "mysql://user:pwd@host/dbname")
        self.assertEqual(config.db_driver, "MySQL-python")

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
                "--i18n=no",
                "test_project"])
            self.assertTrue(str(error.exception).find("--cms-version/-v: invalid choice: '2.6'") > -1)

        sys.stderr = saved_stderr

    def test_latest_version(self):
        self.assertEqual(data.less_than_version('2.4'), "2.5")
        self.assertEqual(data.less_than_version('3'), "3.1")
        self.assertEqual(data.less_than_version('3.0.1'), "3.1.1")

    def test_requirements(self):
        config = aldryn_installer.config.parse([
            "-q",
            "--db=mysql://user:pwd@host/dbname",
            "--django-version=1.4",
            "--i18n=no",
            "-f",
            "test_project"])

        self.assertTrue(config.requirements.find("django-cms<2.5") > -1)
        self.assertTrue(config.requirements.find("Django<1.5") > -1)
        self.assertTrue(config.requirements.find("django-filer") > -1)
        self.assertTrue(config.requirements.find("cmsplugin_filer") > -1)

        config = aldryn_installer.config.parse([
            "-q",
            "--db=mysql://user:pwd@host/dbname",
            "--i18n=no",
            "--cms-version=latest",
            "--django-version=latest",
            "-f",
            "test_project"])

        self.assertTrue(config.requirements.find("django-cms<2.5") > -1)
        self.assertTrue(config.requirements.find("Django<1.6") > -1)

        config = aldryn_installer.config.parse([
            "-q",
            "--db=mysql://user:pwd@host/dbname",
            "--i18n=no",
            "--cms-version=beta",
            "--django-version=beta",
            "-f",
            "test_project"])

        self.assertTrue(config.requirements.find(data.DJANGOCMS_BETA) > -1)
        self.assertTrue(config.requirements.find(data.DJANGO_BETA) > -1)

        config = aldryn_installer.config.parse([
            "-q",
            "--db=mysql://user:pwd@host/dbname",
            "--i18n=no",
            "--cms-version=develop",
            "--django-version=develop",
            "-f",
            "test_project"])

        self.assertTrue(config.requirements.find(data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(config.requirements.find(data.DJANGO_DEVELOP) > -1)
