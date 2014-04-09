#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import tempfile
from mock import patch
from six import StringIO

from djangocms_installer import config
from djangocms_installer.install import check_install
from djangocms_installer.utils import less_than_version

from . import BaseTestClass


class TestConfig(BaseTestClass):
    def test_default_config(self):
        conf_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                  '-q', '-p'+self.project_dir, 'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(conf_data.cms_version, 3.0)
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

    def test_cli_config_commaseparated_languages(self):
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '-len,de,it',
            '-p'+self.project_dir,
            'example_prj'
        ])

        self.assertEqual(conf_data.languages, ['en', 'de', 'it'])

    def test_cli_config_comma_languages_with_space(self):
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '-len , de , it',
            '-p'+self.project_dir,
            'example_prj'
        ])

        self.assertEqual(conf_data.languages, ['en', 'de', 'it'])

    def test_invalid_choices(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '--cms-version=2.6',
                        '--django-version=1.1',
                        '--i18n=no',
                        '-p'+self.project_dir,
                        'example_prj'])
        self.assertTrue(self.stderr.getvalue().find("--cms-version/-v: invalid choice: '2.6'") > -1)

    def test_invalid_project_name(self):
        #with patch('sys.stdout', self.stdout):
            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'test'])
            self.assertTrue(stderr_tmp.getvalue().find("Project name 'test' is not valid") > -1)

            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'assert'])
            self.assertTrue(stderr_tmp.getvalue().find("Project name 'assert' is not valid") > -1)

            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'values'])
            self.assertTrue(stderr_tmp.getvalue().find("Project name 'values' is not valid") > -1)

    def test_invalid_project_path(self):
        prj_dir = 'example_prj'
        existing_path = os.path.join(self.project_dir, prj_dir)
        os.makedirs(existing_path)
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        prj_dir])
                    self.assertEqual(conf_data.project_path, existing_path)
        self.assertTrue(self.stderr.getvalue().find("Path '%s' already exists" % existing_path) > -1)

    def test_latest_version(self):
        self.assertEqual(less_than_version('2.4'), '2.5')
        self.assertEqual(less_than_version('3'), '3.1')
        self.assertEqual(less_than_version('3.0.1'), '3.1.1')

    def test_requirements(self):
        """
        Test for different configuration and package versions
        """
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--django-version=1.4',
            '--i18n=no',
            '-f',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find('django-cms<3.1') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.5') > -1)
        self.assertTrue(conf_data.requirements.find('django-filer') > -1)
        self.assertTrue(conf_data.requirements.find('cmsplugin-filer') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=2.4',
            '--django-version=stable',
            '-f',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find('six') > -1)
        self.assertTrue(conf_data.requirements.find('django-cms<2.5') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.6') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-column') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-file') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-flash') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-googlemap') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-inherit') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-link') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-picture') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-style') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-teaser') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-video') == -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.7') > -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=stable',
            '--django-version=stable',
            '--reversion=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find('django-cms<3.1') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.7') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-column') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-file') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-flash') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-googlemap') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-inherit') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-link') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-picture') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-style') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-teaser') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-video') > -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=develop',
            '--django-version=stable',
            '-f',
            '--reversion=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.7') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') > -1)
        self.assertTrue(conf_data.requirements.find('django-filer') > -1)
        self.assertTrue(conf_data.requirements.find('cmsplugin-filer') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-column') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-file') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-flash') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-googlemap') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-inherit') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-link') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-picture') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-style') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-teaser') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-video') == -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=develop',
            '--django-version=1.4',
            '-f',
            '--reversion=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.5') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8') > -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=develop',
            '--django-version=stable',
            '-f',
            '--reversion=yes',
            '-z=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.7') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8') > -1)
        self.assertTrue(conf_data.requirements.find('pytz') > -1)

    def suspend_test_check_install(self):
        import pip
        # discard the argparser errors
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                # clean the virtualenv
                try:
                    pip.main(['uninstall', '-y', 'psycopg2'])
                except pip.exceptions.UninstallationError:
                    ## package not installed, all is fine
                    pass
                try:
                    pip.main(['uninstall', '-y', 'pillow'])
                except pip.exceptions.UninstallationError:
                    ## package not installed, all is fine
                    pass
                try:
                    pip.main(['uninstall', '-y', 'mysql-python'])
                except pip.exceptions.UninstallationError:
                    ## package not installed, all is fine
                    pass

                # Check postgres / pillow
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '--django-version=1.4',
                    '--i18n=no',
                    '-f',
                    '-p'+self.project_dir,
                    'example_prj'])
                with self.assertRaises(EnvironmentError) as context_error:
                    check_install(conf_data)
                self.assertTrue(str(context_error.exception).find('Pillow is not installed') > -1)
                self.assertTrue(str(context_error.exception).find('PostgreSQL driver is not installed') > -1)

                # Check mysql
                conf_data = config.parse([
                    '-q',
                    '--db=mysql://user:pwd@host/dbname',
                    '--django-version=1.4',
                    '--i18n=no',
                    '-f',
                    '-p'+self.project_dir,
                    'example_prj'])
                with self.assertRaises(EnvironmentError) as context_error:
                    check_install(conf_data)
                self.assertTrue(str(context_error.exception).find('MySQL driver is not installed') > -1)
