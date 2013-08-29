#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from aldryn_installer import config
from aldryn_installer.install import check_install
from aldryn_installer.utils import less_than_version
from . import BaseTestClass, PatchStd


class TestConfig(BaseTestClass):
    def test_default_config(self):
        conf_data = config.parse(["--db=postgres://user:pwd@host/dbname",
                                  "-q", "test_project"])

        self.assertEqual(conf_data.project_name, 'test_project')

        self.assertEqual(conf_data.cms_version, 2.4)
        self.assertEqual(conf_data.django_version, 1.5)
        self.assertEqual(conf_data.i18n, 'yes')
        self.assertEqual(conf_data.reversion, 'yes')
        self.assertEqual(conf_data.permissions, 'yes')
        self.assertEqual(conf_data.use_timezone, 'yes')
        self.assertEqual(conf_data.db, "postgres://user:pwd@host/dbname")

        self.assertEqual(conf_data.no_db_driver, False)
        self.assertEqual(conf_data.no_deps, False)
        self.assertEqual(conf_data.no_sync, False)
        self.assertEqual(conf_data.plugins, False)
        self.assertEqual(conf_data.requirements_file, None)

    def test_cli_config(self):
        conf_data = config.parse([
            "-q",
            "--db=postgres://user:pwd@host/dbname",
            "--cms-version=develop",
            "--django-version=1.4",
            "--i18n=no",
            "--reversion=no",
            "--permissions=no",
            "--use-tz=no",
            "-tEurope/Rome",
            "-len", "-lde", "-lit",
            "-p/tmp/test",
            "test_project"])

        self.assertEqual(conf_data.project_name, 'test_project')

        self.assertEqual(conf_data.cms_version, 3.0)
        self.assertEqual(conf_data.django_version, 1.4)
        self.assertEqual(conf_data.i18n, 'no')
        self.assertEqual(conf_data.reversion, 'no')
        self.assertEqual(conf_data.permissions, 'no')
        self.assertEqual(conf_data.use_timezone, 'no')
        self.assertEqual(conf_data.timezone, 'Europe/Rome')
        self.assertEqual(conf_data.languages, ['en', 'de', 'it'])
        self.assertEqual(conf_data.project_directory, '/tmp/test')
        self.assertEqual(conf_data.db, "postgres://user:pwd@host/dbname")
        self.assertEqual(conf_data.db_driver, "psycopg2")

    def test_invalid_choices(self):
        with PatchStd(self.stdout, self.stderr):
            with self.assertRaises(SystemExit) as error:
                conf_data = config.parse([
                    "-q",
                    "--db=postgres://user:pwd@host/dbname",
                    "--cms-version=2.6",
                    "--django-version=1.1",
                    "--i18n=no",
                    "test_project"])
                self.assertTrue(str(error.exception).find("--cms-version/-v: invalid choice: '2.6'") > -1)

    def test_latest_version(self):
        self.assertEqual(less_than_version('2.4'), "2.5")
        self.assertEqual(less_than_version('3'), "3.1")
        self.assertEqual(less_than_version('3.0.1'), "3.1.1")

    def test_requirements(self):
        conf_data = config.parse([
            "-q",
            "--db=postgres://user:pwd@host/dbname",
            "--django-version=1.4",
            "--i18n=no",
            "-f",
            "test_project"])

        self.assertTrue(conf_data.requirements.find("django-cms<2.5") > -1)
        self.assertTrue(conf_data.requirements.find("Django<1.5") > -1)
        self.assertTrue(conf_data.requirements.find("django-filer") > -1)
        self.assertTrue(conf_data.requirements.find("cmsplugin_filer") > -1)
        self.assertTrue(conf_data.requirements.find("django-reversion<1.7") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") == -1)

        conf_data = config.parse([
            "-q",
            "--db=postgres://user:pwd@host/dbname",
            "--i18n=no",
            "--cms-version=stable",
            "--django-version=stable",
            "-f",
            "test_project"])

        self.assertTrue(conf_data.requirements.find("django-cms<2.5") > -1)
        self.assertTrue(conf_data.requirements.find("Django<1.6") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style") == -1)
        self.assertTrue(conf_data.requirements.find("django-reversion>=1.7") > -1)

        conf_data = config.parse([
            "-q",
            "--db=postgres://user:pwd@host/dbname",
            "--i18n=no",
            "--cms-version=beta",
            "-f",
            "test_project"])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_BETA) > -1)

        conf_data = config.parse([
            "-q",
            "--db=postgres://user:pwd@host/dbname",
            "--i18n=no",
            "--cms-version=develop",
            "-f",
            "test_project"])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style") > -1)

    def test_check_install(self):
        try:
            import PIL
            self.skipTest("Virtualenv installed, cannot run this test")
        except ImportError:
            pass
        # discard the argparser errors
        with PatchStd(self.stdout, self.stderr):
            conf_data = config.parse([
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--django-version=1.4",
                "--i18n=no",
                "-f",
                "test_project"])

            with self.assertRaises(EnvironmentError) as error:
                check_install(conf_data)
            self.assertTrue(str(error.exception).find("Pillow is not installed") > -1)
            self.assertTrue(str(error.exception).find("PostgreSQL driver is not installed") > -1)

            conf_data = config.parse([
                "-q",
                "--db=mysql://user:pwd@host/dbname",
                "--django-version=1.4",
                "--i18n=no",
                "-f",
                "test_project"])

            with self.assertRaises(EnvironmentError) as error:
                check_install(conf_data)

                self.assertTrue(str(error.exception).find("MySQL  driver is not installed") > -1)
