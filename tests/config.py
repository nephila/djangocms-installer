# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import copy
import os
import sys
from argparse import Namespace

from mock import patch
from six import StringIO, text_type
from tzlocal import get_localzone
import six

from djangocms_installer import config
from djangocms_installer.config.data import CMS_VERSION_MATRIX, DJANGO_VERSION_MATRIX
from djangocms_installer.install import check_install
from djangocms_installer.utils import less_than_version, supported_versions

from .base import BaseTestClass, unittest


class TestConfig(BaseTestClass):
    def test_default_config(self):
        conf_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                  '-q', '-p'+self.project_dir, 'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(conf_data.cms_version, 3.2)
        self.assertEqual(conf_data.django_version, 1.8)
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
        dj_version = '1.8'
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--cms-version=stable',
            '--django-version={0}'.format(dj_version),
            '--i18n=no',
            '--reversion=no',
            '--permissions=no',
            '--use-tz=no',
            '-tEurope/Rome',
            '-len-CA', '-lde', '-lit',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(conf_data.cms_version, 3.2)
        self.assertEqual(conf_data.django_version, 1.8)
        self.assertEqual(conf_data.i18n, 'yes')
        self.assertEqual(conf_data.reversion, 'no')
        self.assertEqual(conf_data.permissions, 'no')
        self.assertEqual(conf_data.use_timezone, 'no')
        self.assertEqual(conf_data.timezone, 'Europe/Rome')
        self.assertEqual(conf_data.languages, ['en-ca', 'de', 'it'])
        self.assertEqual(conf_data.project_directory, self.project_dir)
        self.assertEqual(conf_data.db, 'postgres://user:pwd@host/dbname')
        self.assertEqual(conf_data.db_driver, 'psycopg2')

        dj_version = '1.8'
        cms_version = '3.2'
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--cms-version=stable',
            '--django-version={0}'.format(dj_version),
            '--cms-version={0}'.format(cms_version),
            '--i18n=no',
            '--reversion=no',
            '--permissions=no',
            '--use-tz=no',
            '-tEurope/Rome',
            '-len', '-lde', '-lit',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(str(conf_data.cms_version), cms_version)
        self.assertEqual(str(conf_data.django_version), dj_version)
        self.assertEqual(conf_data.i18n, 'yes')
        self.assertEqual(conf_data.reversion, 'no')
        self.assertEqual(conf_data.permissions, 'no')
        self.assertEqual(conf_data.use_timezone, 'no')
        self.assertEqual(conf_data.timezone, 'Europe/Rome')
        self.assertEqual(conf_data.languages, ['en', 'de', 'it'])
        self.assertEqual(conf_data.project_directory, self.project_dir)
        self.assertEqual(conf_data.db, 'postgres://user:pwd@host/dbname')
        self.assertEqual(conf_data.db_driver, 'psycopg2')

        dj_version = '1.8'
        cms_version = '3.2'
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--cms-version=stable',
            '--django-version={0}'.format(dj_version),
            '--cms-version={0}'.format(cms_version),
            '--i18n=no',
            '--reversion=no',
            '--permissions=no',
            '--use-tz=no',
            '-tEurope/Rome',
            '-len',
            '-p' + self.project_dir,
            'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(str(conf_data.cms_version), cms_version)
        self.assertEqual(str(conf_data.django_version), dj_version)
        self.assertEqual(conf_data.i18n, 'no')
        self.assertEqual(conf_data.reversion, 'no')
        self.assertEqual(conf_data.permissions, 'no')
        self.assertEqual(conf_data.use_timezone, 'no')
        self.assertEqual(conf_data.timezone, 'Europe/Rome')
        self.assertEqual(conf_data.languages, ['en'])
        self.assertEqual(conf_data.project_directory, self.project_dir)
        self.assertEqual(conf_data.db, 'postgres://user:pwd@host/dbname')
        self.assertEqual(conf_data.db_driver, 'psycopg2')

    def test_version_mismatch(self):
        with self.assertRaises(SystemExit):
            conf_data = config.parse([
                '-q',
                '--db=postgres://user:pwd@host/dbname',
                '--cms-version=stable',
                '--django-version=1.4',
                '--i18n=no',
                '--reversion=no',
                '--permissions=no',
                '--use-tz=no',
                '-tEurope/Rome',
                '-len', '-lde', '-lit',
                '-p'+self.project_dir,
                'example_prj'])

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
        if six.PY3:
            self.assertTrue(self.stderr.getvalue().find('--cms-version/-v: invalid choice: \'2.6\'') > -1)
        else:
            self.assertTrue(self.stderr.getvalue().find('--cms-version/-v: invalid choice: u\'2.6\'') > -1)

    def test_invalid_project_name(self):
        with patch('sys.stdout', self.stdout):
            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'test'])
            self.assertTrue(stderr_tmp.getvalue().find('Project name "test" is not a valid app name') > -1)

            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'assert'])
            self.assertTrue(stderr_tmp.getvalue().find('Project name "assert" is not a valid app name') > -1)

            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'values'])
            self.assertTrue(stderr_tmp.getvalue().find('Project name "values" is not a valid app name') > -1)

            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'project-name'])
            self.assertTrue(stderr_tmp.getvalue().find('Project name "project-name" is not a valid app name') > -1)

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
        self.assertTrue(self.stderr.getvalue().find('Path "%s" already exists and is not empty' % self.project_dir) > -1)

    def test_invalid_project_dir(self):
        prj_dir = 'example_prj'
        existing_path = os.path.join(self.project_dir, 'a_file')
        with open(existing_path, 'w') as f:
            f.write('')
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        prj_dir])
                    self.assertEqual(conf_data.project_path, existing_path)
        self.assertTrue(self.stderr.getvalue().find('Path "%s" already exists and is not empty' % self.project_dir) > -1)

    def test_invalid_project_dir_skip(self):
        prj_dir = 'example_prj'
        existing_path = os.path.join(self.project_dir, 'a_file')
        with open(existing_path, 'w') as f:
            f.write('')
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                conf_data = config.parse([
                    '-q', '-s',
                    '--db=postgres://user:pwd@host/dbname',
                    '-p'+self.project_dir,
                    prj_dir])
        self.assertFalse(self.stderr.getvalue().find('Path "%s" already exists and is not empty' % self.project_dir) > -1)

    def test_valid_project_dir(self):
        prj_dir = 'example_prj'
        existing_path = os.path.join(self.project_dir, '.hidden_file')
        with open(existing_path, 'w') as f:
            f.write('')
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '-p'+self.project_dir,
                    prj_dir])
        self.assertFalse(self.stderr.getvalue().find('Path "%s" already exists and is not empty' % self.project_dir) > -1)

    def test_latest_version(self):
        self.assertEqual(less_than_version('2.4'), '2.5')
        self.assertEqual(less_than_version('3'), '3.1')
        self.assertEqual(less_than_version('3.0.1'), '3.1.1')

    def test_supported_versions(self):
        self.assertEqual(supported_versions('stable', 'stable'), (1.8, 3.2))
        self.assertEqual(supported_versions('stable', '3.1.10'), (1.8, None))
        self.assertEqual(supported_versions('stable', 'rc'), (1.8, 3.3))
        self.assertEqual(supported_versions('stable', 'beta'), (1.8, 3.3))
        self.assertEqual(supported_versions('stable', 'develop'), (1.8, 3.3))

        with self.assertRaises(RuntimeError):
            supported_versions('stable', '2.4'), (1.5, 2.4)
        with self.assertRaises(RuntimeError):
            supported_versions('1.5', 'stable'), (1.8, 3.1)

        self.assertEqual(supported_versions('1.9', 'stable'), (1.9, 3.2))
        self.assertEqual(supported_versions('1.8', 'stable'), (1.8, 3.2))
        self.assertEqual(supported_versions('1.8.3', 'stable'), (None, 3.2))
        self.assertEqual(supported_versions('beta', 'stable'), (1.9, 3.2))
        self.assertEqual(supported_versions('develop', 'stable'), (1.9, 3.2))

    def test_requirements(self):
        """
        Test for different configuration and package versions
        """
        dj_version = '1.8'
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--cms-version=3.2',
            '--django-version={0}'.format(dj_version),
            '--i18n=no',
            '--apphooks-reload',
            '-f',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find('django-cms<3.3') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.9') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.10,<1.11') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor>=2.8.1') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style>=1.1.1') > -1)
        self.assertTrue(conf_data.requirements.find('django-filer') > -1)
        self.assertTrue(conf_data.requirements.find('cmsplugin-filer') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(conf_data.requirements.find('aldryn-apphook-reload') == -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=stable',
            '--django-version=stable',
            '--reversion=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find('django-cms<3.3') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.9') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.10,<1.11') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor>=2.8') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style>=1.1.1') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-column') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-file') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-flash') == -1)
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
            '--apphooks-reload',
            '--reversion=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.9') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.10,<1.11') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') > -1)
        self.assertTrue(conf_data.requirements.find('django-filer') > -1)
        self.assertTrue(conf_data.requirements.find('cmsplugin-filer') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-column') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-file') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-flash') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-googlemap') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-inherit') > -1)
        #self.assertTrue(conf_data.requirements.find('djangocms-link') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-picture') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-style') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-teaser') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-video') == -1)
        self.assertTrue(conf_data.requirements.find('aldryn-apphook-reload') == -1)

        dj_version = '1.8'
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=develop',
            '--django-version={0}'.format(dj_version),
            '-f',
            '--reversion=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.9') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.10,<1.11') > -1)
        self.assertTrue(conf_data.requirements.find('django-mptt') == -1)
        self.assertTrue(conf_data.requirements.find('django-treebeard') > -1)

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
        self.assertTrue(conf_data.requirements.find('Django<1.9') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.10,<1.11') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') > -1)
        self.assertTrue(conf_data.requirements.find('pytz') > -1)

        dj_version = '1.8'
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=develop',
            '--django-version={0}'.format(dj_version),
            '--reversion=yes',
            '-z=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.9') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.10,<1.11') > -1)
        self.assertTrue(conf_data.requirements.find('https://github.com/divio/djangocms-text-ckeditor/archive/develop.zip') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style>=1.1.1') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-teaser') > -1)
        self.assertTrue(conf_data.requirements.find('south') == -1)

        dj_version = '1.8'
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=develop',
            '--django-version={0}'.format(dj_version),
            '--reversion=yes',
            '--no-plugins',
            '-z=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.9') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.10,<1.11') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor/archive/master.zip') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style/archive/master.zip') == -1)
        self.assertTrue(conf_data.requirements.find('djangocms-teaser/archive/master.zip') == -1)
        self.assertTrue(conf_data.requirements.find('south') == -1)

    def disabled_test_aldryn_compatibility(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '--cms-version=2.4',
                        '--django-version=stable',
                        #'-a',
                        '-p'+self.project_dir,
                        'example_prj'])
                try:
                    self.assertEqual(error.exception.code, 5)
                except AttributeError:
                    self.assertEqual(error.exception, 5)

    def test_boostrap(self):
        """
        Verify handling of bootstrap parameter
        """
        conf_data = config.parse([
            '-q',
            '-p'+self.project_dir,
            'example_prj'])
        self.assertFalse(conf_data.bootstrap)

        conf_data = config.parse([
            '--bootstrap=yes', '-q',
            '-p'+self.project_dir,
            'example_prj'])
        self.assertTrue(conf_data.bootstrap)

    def test_starting_page(self):
        """
        Verify handling of starting-page parameter
        """
        conf_data = config.parse([
            '-q',
            '-p'+self.project_dir,
            'example_prj'])
        self.assertFalse(conf_data.starting_page)

        conf_data = config.parse([
            '--starting-page=yes', '-q',
            '-p'+self.project_dir,
            'example_prj'])
        self.assertTrue(conf_data.starting_page)

    def test_auto_i18n(self):
        """
        Verify setting automatic i18n support if multiple languages
        """
        conf_data = config.parse([
            '-q', '-len,de'
            '--i18n=no',
            '-p' + self.project_dir,
            'example_prj'])
        self.assertTrue(conf_data.i18n)

    def test_utc(self):
        """
        Verify handling UTC default
        """
        default_tz = get_localzone()

        conf_data = config.parse([
            '-q',
            '-p'+self.project_dir,
            'example_prj'])
        self.assertEqual(text_type(conf_data.timezone), default_tz.zone)

        conf_data = config.parse([
            '-q', '--utc',
            '-p'+self.project_dir,
            'example_prj'])
        self.assertEqual(conf_data.timezone, 'UTC')

    def test_templates(self):
        """
        Verify handling of valid (existing) and invalid (non-existing) templates directory parameter
        """
        conf_data = config.parse([
            '--templates=/foo/bar', '-q',
            '-p'+self.project_dir,
            'example_prj'])
        self.assertFalse(conf_data.templates)

        tpl_path = os.path.join(os.path.dirname(__file__), 'test_templates')

        conf_data = config.parse([
            '--templates=%s' % tpl_path, '-q',
            '-p'+self.project_dir,
            'example_prj'])
        self.assertEqual(conf_data.templates, tpl_path)

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
                    '--django-version=1.8',
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
                    '--django-version=1.8',
                    '--i18n=no',
                    '-f',
                    '-p'+self.project_dir,
                    'example_prj'])
                with self.assertRaises(EnvironmentError) as context_error:
                    check_install(conf_data)
                self.assertTrue(str(context_error.exception).find('MySQL driver is not installed') > -1)

    def test_show_plugins(self):
        sys.stdout = StringIO()
        try:
            config.show_plugins()
        finally:
            sys.stdout = sys.__stdout__

    def test_show_requirements(self):
        sys.stdout = StringIO()
        dj_version = '1.8'
        try:
            conf_data = config.parse([
                '-q',
                '--db=mysql://user:pwd@host/dbname',
                '--django-version={0}'.format(dj_version),
                '--i18n=no',
                '-f',
                '-p'+self.project_dir,
                'example_prj'])
            config.show_requirements(conf_data)
        finally:
            sys.stdout = sys.__stdout__


class TestBaseConfig(unittest.TestCase):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_dir = os.path.join(base_dir, 'tests/fixtures/configs')
    args = ['--config-file', '-s', '-q', 'example_prj']
    config_fixture = Namespace(**{
        'bootstrap': False,
        'cms_version': CMS_VERSION_MATRIX['stable'],
        'db': 'sqlite://localhost/project.db',
        'django_version': DJANGO_VERSION_MATRIX['stable'],
        'dump_reqs': False,
        'extra_settings': None,
        'filer': False,
        'i18n': 'yes',
        'languages': ['en'],
        'no_db_driver': False,
        'no_deps': False,
        'noinput': True,
        'no_sync': False,
        'no_user': False,
        'permissions': 'yes',
        'pip_options': '',
        'plugins': False,
        'project_directory': '.',
        'project_name': 'example_prj',
        'requirements_file': None,
        'reversion': 'yes',
        'skip_project_dir_check': True,
        'starting_page': False,
        'template': None,
        'templates': False,
        'timezone': get_localzone(),
        'use_timezone': 'yes',
        'utc': False,
        'no_plugins': False,
        'apphooks_reload': False,
        'verbose': False,
    })

    def __init__(self, *args, **kwargs):
        self.config_not_exists = self.conf('config-dump.ini')
        super(TestBaseConfig, self).__init__(*args, **kwargs)

    def tearDown(self):
        if os.path.isfile(self.config_not_exists):
            os.remove(self.config_not_exists)

    def conf(self, filename):
        return os.path.join(self.config_dir, filename)

    def unused(self, config_data):
        """Remove not configurable keys."""
        for attr in ('aldryn', 'config_dump', 'config_file', 'db_driver', 'db_parsed',
                     'project_path', 'settings_path', 'urlconf_path'):
            delattr(config_data, attr)
        # When `requirements` arg is used then requirements attr isn't set.
        if hasattr(config_data, 'requirements'):
            delattr(config_data, 'requirements')

    def test_parse_config_file(self, *args):
        """Tests .config.__init__._parse_config_file function."""
        with self.assertRaises(SystemExit) as error:
            config.parse(self.args[0:1] + [self.conf('config-not-exists.ini')] + self.args[1:])
            self.assertEqual(7, error.exception.code)

        args = self.args[0:1] + [self.conf('config-01.ini')] + self.args[1:]
        config_data = config.parse(args)
        self.unused(config_data)
        self.assertEqual(self.config_fixture, config_data)

        test_data = [
            ('config-02.ini', 'db', 'postgres://user:pwd@host:54321/dbname'),
            ('config-03.ini', 'i18n', 'no'),
            ('config-04.ini', 'use_timezone', 'no'),
            ('config-05.ini', 'timezone', 'Europe/London'),
            ('config-06.ini', 'reversion', 'no'),
            ('config-07.ini', 'permissions', 'no'),
            ('config-08.ini', None, (('i18n', 'no'), ('languages', ['ru']))),
            ('config-09.ini', None, (('i18n', 'yes'), ('languages', ['en', 'ru']))),
            ('config-10.ini', 'django_version', 1.8),
            ('config-11.ini', 'project_directory', '/test/me'),
            ('config-12.ini', 'bootstrap', True),
            ('config-13.ini', 'templates', '.'),
            ('config-14.ini', 'starting_page', True),
            ('config-15.ini', 'plugins', True),
            ('config-16.ini', 'dump_reqs', True),
            ('config-17.ini', 'noinput', True),
            ('config-18.ini', 'filer', True),
            ('config-19.ini', 'requirements_file', '/test/reqs'),
            ('config-20.ini', 'no_deps', True),
            ('config-21.ini', 'no_db_driver', True),
            ('config-22.ini', 'no_sync', True),
            ('config-23.ini', 'no_user', True),
            ('config-24.ini', 'template', '/test/template'),
            ('config-25.ini', 'extra_settings', '/test/extra_settings'),
            ('config-26.ini', 'skip_project_dir_check', True),
            ('config-27.ini', 'utc', True),
            ('config-28.ini', 'no_plugins', True),
            ('config-29.ini', 'apphooks_reload', True),
            ('config-30.ini', 'verbose', True),
        ]
        fixture = copy.copy(self.config_fixture)
        for filename, key, val in test_data:
            if type(val) == tuple:
                for subkey, subval in val:
                    setattr(fixture, subkey, subval)  # Change value.
            else:
                setattr(fixture, key, val)  # Change value.
            args = self.args[0:1] + [self.conf(filename)] + self.args[1:]  # Load new config.
            config_data = config.parse(args)
            self.unused(config_data)
            self.assertEqual(fixture, config_data)  # Check if config value and changed value equals.

    @patch('sys.stdout')
    @patch('sys.stderr')
    def test_dump_config_file(self, *args):
        """Tests .config.ini.dump_config_file function."""
        config_exists = self.conf('config-01.ini')

        with self.assertRaises(SystemExit) as error:
            config.parse(['--config-dump', config_exists] + self.args[1:] + ['-p', '.'])
            self.assertEqual(8, error.exception.code)

        config.parse(['--config-dump', self.config_not_exists] + self.args[1:] + ['-p', '.'])
        self.assertTrue(os.path.isfile(self.config_not_exists))

        fixture = copy.copy(self.config_fixture)
        setattr(fixture, 'timezone', get_localzone().zone)
        # Load dumped config.
        args = self.args[0:1] + [self.config_not_exists] + self.args[1:]
        config_data = config.parse(args)
        self.unused(config_data)
        self.assertEqual(fixture, config_data)
