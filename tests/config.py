# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys

from mock import patch
from six import StringIO, text_type
from tzlocal import get_localzone

from djangocms_installer import config
from djangocms_installer.install import check_install
from djangocms_installer.utils import less_than_version, supported_versions

from .base import BaseTestClass


class TestConfig(BaseTestClass):
    def test_default_config(self):
        conf_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                  '-q', '-p'+self.project_dir, 'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(conf_data.cms_version, 3.1)
        self.assertEqual(conf_data.django_version, 1.7)
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
            '--cms-version=stable',
            '--django-version=1.7',
            '--i18n=no',
            '--reversion=no',
            '--permissions=no',
            '--use-tz=no',
            '-tEurope/Rome',
            '-len', '-lde', '-lit',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertEqual(conf_data.project_name, 'example_prj')

        self.assertEqual(conf_data.cms_version, 3.1)
        self.assertEqual(conf_data.django_version, 1.7)
        self.assertEqual(conf_data.i18n, 'no')
        self.assertEqual(conf_data.reversion, 'no')
        self.assertEqual(conf_data.permissions, 'no')
        self.assertEqual(conf_data.use_timezone, 'no')
        self.assertEqual(conf_data.timezone, 'Europe/Rome')
        self.assertEqual(conf_data.languages, ['en', 'de', 'it'])
        self.assertEqual(conf_data.project_directory, self.project_dir)
        self.assertEqual(conf_data.db, 'postgres://user:pwd@host/dbname')
        self.assertEqual(conf_data.db_driver, 'psycopg2')

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--cms-version=stable',
            '--django-version=1.4',
            '--cms-version=3.0',
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
        self.assertTrue(self.stderr.getvalue().find("--cms-version/-v: invalid choice: '2.6'") > -1)

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
            self.assertTrue(stderr_tmp.getvalue().find("Project name 'test' is not a valid app name") > -1)

            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'assert'])
            self.assertTrue(stderr_tmp.getvalue().find("Project name 'assert' is not a valid app name") > -1)

            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'values'])
            self.assertTrue(stderr_tmp.getvalue().find("Project name 'values' is not a valid app name") > -1)

            stderr_tmp = StringIO()
            with patch('sys.stderr', stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse([
                        '-q',
                        '--db=postgres://user:pwd@host/dbname',
                        '-p'+self.project_dir,
                        'project-name'])
            self.assertTrue(stderr_tmp.getvalue().find("Project name 'project-name' is not a valid app name") > -1)

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
        self.assertTrue(self.stderr.getvalue().find("Path '%s' already exists and is not empty" % self.project_dir) > -1)

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
        self.assertTrue(self.stderr.getvalue().find("Path '%s' already exists and is not empty" % self.project_dir) > -1)

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
        self.assertFalse(self.stderr.getvalue().find("Path '%s' already exists and is not empty" % self.project_dir) > -1)

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
        self.assertFalse(self.stderr.getvalue().find("Path '%s' already exists and is not empty" % self.project_dir) > -1)

    def test_latest_version(self):
        self.assertEqual(less_than_version('2.4'), '2.5')
        self.assertEqual(less_than_version('3'), '3.1')
        self.assertEqual(less_than_version('3.0.1'), '3.1.1')

    def test_supported_versions(self):
        self.assertEqual(supported_versions('stable', 'stable'), (1.7, 3.1))
        self.assertEqual(supported_versions('stable', '3.0'), (1.7, 3.0))
        self.assertEqual(supported_versions('stable', '3.0.10'), (1.7, None))
        self.assertEqual(supported_versions('stable', 'rc'), (1.7, 3.2))
        self.assertEqual(supported_versions('stable', 'beta'), (1.7, 3.2))
        self.assertEqual(supported_versions('stable', 'develop'), (1.7, 3.2))

        with self.assertRaises(RuntimeError):
            supported_versions('stable', '2.4'), (1.5, 2.4)
            supported_versions('1.5', 'stable'), (1.7, 3.1)

        self.assertEqual(supported_versions('1.5', '2.4'), (1.5, 2.4))
        self.assertEqual(supported_versions('1.6', 'stable'), (1.6, 3.1))
        self.assertEqual(supported_versions('1.6.9', 'stable'), (None, 3.1))
        self.assertEqual(supported_versions('1.7', 'stable'), (1.7, 3.1))
        self.assertEqual(supported_versions('beta', 'stable'), (1.8, 3.1))
        self.assertEqual(supported_versions('develop', 'stable'), (1.8, 3.1))

    def test_requirements(self):
        """
        Test for different configuration and package versions
        """
        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--django-version=1.6',
            '--i18n=no',
            '-f',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find('django-cms<3.2') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.7') > -1)
        self.assertTrue(conf_data.requirements.find('django-filer') > -1)
        self.assertTrue(conf_data.requirements.find('cmsplugin-filer') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8,<1.8.6') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=2.4',
            '--django-version=1.5',
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

        self.assertTrue(conf_data.requirements.find('django-cms<3.2') > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.8') > -1)
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
        self.assertTrue(conf_data.requirements.find('Django<1.8') > -1)
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
            '--django-version=1.6',
            '-f',
            '--reversion=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.7') > -1)
        self.assertTrue(conf_data.requirements.find('django-mptt') == -1)
        self.assertTrue(conf_data.requirements.find('django-treebeard') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8,<1.8.6') > -1)

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
        self.assertTrue(conf_data.requirements.find('Django<1.8') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8') > -1)
        self.assertTrue(conf_data.requirements.find('pytz') > -1)

        conf_data = config.parse([
            '-q',
            '--db=postgres://user:pwd@host/dbname',
            '--i18n=no',
            '--cms-version=develop',
            '--django-version=1.7',
            '--reversion=yes',
            '-z=yes',
            '-p'+self.project_dir,
            'example_prj'])

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find('Django<1.8') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-text-ckeditor/archive/master.zip') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-admin-style/archive/master.zip') > -1)
        self.assertTrue(conf_data.requirements.find('djangocms-teaser/archive/master.zip') > -1)
        self.assertTrue(conf_data.requirements.find('django-reversion>=1.8.2') > -1)
        self.assertTrue(conf_data.requirements.find('south') == -1)

        # conf_data = config.parse([
        #     '-q',
        #     '--db=postgres://user:pwd@host/dbname',
        #     '--cms-version=stable',
        #     '--django-version=stable',
        #     #'-a',
        #     '-p'+self.project_dir,
        #     'example_prj'])
        # self.assertTrue(conf_data.requirements.find('django-compressor') > -1)

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

    def test_show_plugins(self):
        sys.stdout = StringIO()
        try:
            config.show_plugins()
        finally:
            sys.stdout = sys.__stdout__

    def test_show_requirements(self):
        sys.stdout = StringIO()
        try:
            conf_data = config.parse([
                '-q',
                '--db=mysql://user:pwd@host/dbname',
                '--django-version=1.7',
                '--i18n=no',
                '-f',
                '-p'+self.project_dir,
                'example_prj'])
            config.show_requirements(conf_data)
        finally:
            sys.stdout = sys.__stdout__
