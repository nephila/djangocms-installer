#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import tempfile

from aldryn_installer import config
from aldryn_installer.install import check_install
from aldryn_installer.utils import less_than_version
from . import BaseTestClass, PatchStd


class TestConfig(BaseTestClass):
    def test_default_config(self):
        self._remove_project_dir()
        conf_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                  '-q', '-p'+self.project_dir, 'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(conf_data.cms_version, 2.4)
        self.assertEqual(conf_data.django_version, 1.5)
        self.assertEqual(conf_data.i18n, 'yes')
        self.assertEqual(conf_data.reversion, 'yes')
        self.assertEqual(conf_data.permissions, 'yes')
        self.assertEqual(conf_data.use_timezone, 'yes')
        self.assertEqual(conf_data.db, 'postgres://user:pwd@host/dbname')

        self.assertEqual(conf_data.no_db_driver, False)
        self.assertEqual(conf_data.no_deps, False)
        self.assertEqual(conf_data.no_sync, False)
        self.assertEqual(conf_data.plugins, False)
        self.assertEqual(conf_data.requirements_file, None)

    def test_cli_config(self):
        self._remove_project_dir()
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--cms-version=develop',
            '--django-version=1.4',
            '--i18n=no',
            '--reversion=no',
            '--permissions=no',
            '--use-tz=no',
            '-tEurope/Rome',
            '-len', '-lde', '-lit',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(conf_data.cms_version, 3.0)
        self.assertEqual(conf_data.django_version, 1.4)
        self.assertEqual(conf_data.i18n, 'no')
        self.assertEqual(conf_data.reversion, 'no')
        self.assertEqual(conf_data.permissions, 'no')
        self.assertEqual(conf_data.use_timezone, 'no')
        self.assertEqual(conf_data.timezone, 'Europe/Rome')
        self.assertEqual(conf_data.languages, ['en', 'de', 'it'])
        self.assertEqual(conf_data.project_directory, self.project_dir)
        self.assertEqual(conf_data.db, 'postgres://user:pwd@host/dbname')
        self.assertEqual(conf_data.db_driver, 'psycopg2')

    def test_invalid_choices(self):
        self._remove_project_dir()
        with PatchStd(self.stdout, self.stderr):
            with self.assertRaises(SystemExit) as error:
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '--cms-version=2.6',
                    '--django-version=1.1',
                    '--i18n=no',
                    '-p'+self.project_dir,
                    'example_prj'])
                self.assertTrue(str(error.exception).find('--cms-version/-v: invalid choice: "2.6"') > -1)

    def test_invalid_project_name(self):
        with PatchStd(self.stdout, self.stderr):
            with self.assertRaises(SystemExit) as error:
                self._remove_project_dir()
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '-p'+self.project_dir,
                    'test'])
                self.assertTrue(str(error.exception).find('Project name "test" is not valid') > -1)

            with self.assertRaises(SystemExit) as error:
                self._remove_project_dir()
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '-p'+self.project_dir,
                    'assert'])
                self.assertTrue(str(error.exception).find('Project name "assert" is not valid') > -1)

            with self.assertRaises(SystemExit) as error:
                self._remove_project_dir()
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '-p'+self.project_dir,
                    'values'])
                self.assertTrue(str(error.exception).find('Project name "assert" is not valid') > -1)

    def test_invalid_project_path(self):
        self._remove_project_dir()
        prj_dir = 'example_prj'
        existing_path = os.path.join(self.project_dir, prj_dir)
        os.makedirs(existing_path)
        with PatchStd(self.stdout, self.stderr):
            with self.assertRaises(SystemExit) as error:
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '-p'+self.project_dir,
                    prj_dir])
                self.assertTrue(str(error.exception).find('Path "%s" already exists' % existing_path) > -1)

    def test_whitespace_project_path(self):
        self._remove_project_dir()
        prj_dir = 'example_prj'
        existing_path = os.path.join(self.project_dir, prj_dir)
        os.makedirs(existing_path)
        with PatchStd(self.stdout, self.stderr):
            with self.assertRaises(SystemExit) as error:
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '-p'+self.project_dir,
                    prj_dir])
                self.assertEqual(conf_data.project_path, existing_path)

    def test_latest_version(self):
        self.assertEqual(less_than_version('2.4'), '2.5')
        self.assertEqual(less_than_version('3'), '3.1')
        self.assertEqual(less_than_version('3.0.1'), '3.1.1')

    def test_requirements(self):
        self._remove_project_dir()
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--django-version=1.4',
            '--i18n=no',
            '-f',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find('django-cms<2.5') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.5') > -1)
        self.assertTrue(conf_data.requirements.find('django-filer') > -1)
        self.assertTrue(conf_data.requirements.find('cmsplugin_filer') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion<1.7') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') == -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=stable',
            '--django-version=stable',
            '-f',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find('django-cms<2.5') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.6') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') == -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.7') > -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=beta',
            '-f',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_BETA) > -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=develop',
            '-f',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') > -1)

    def test_check_install(self):
        try:
            import PIL
            self.skipTest('Virtualenv installed, cannot run this test')
        except ImportError:
            pass
        # discard the argparser errors
        with PatchStd(self.stdout, self.stderr):
            self._remove_project_dir()
            conf_data = config.parse([
                '-q',
                '--db=postgres://user:pwd@host/dbname',
                '--django-version=1.4',
                '--i18n=no',
                '-f',
                '-p'+self.project_dir,
                'example_prj'])

            with self.assertRaises(EnvironmentError) as error:
                check_install(conf_data)
            self.assertTrue(str(error.exception).find('Pillow is not installed') > -1)
            self.assertTrue(str(error.exception).find('PostgreSQL driver is not installed') > -1)

            conf_data = config.parse([
                '-q',
                '--db=mysql://user:pwd@host/dbname',
                '--django-version=1.4',
                '--i18n=no',
                '-f',
                '-p'+self.project_dir,
                'example_prj'])

            with self.assertRaises(EnvironmentError) as error:
                check_install(conf_data)

                self.assertTrue(str(error.exception).find('MySQL  driver is not installed') > -1)
