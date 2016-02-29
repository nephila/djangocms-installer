# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from subprocess import CalledProcessError

from mock import patch

from djangocms_installer import config, install, main

from .base import IsolatedTestClass, dj_ver, unittest


class TestMain(IsolatedTestClass):

    def test_requirements_invocation(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len', '--cms-version=stable', '-R',
                                       '-q', '-u', '-p'+self.project_dir,
                                       'example_prj']
                main.execute()
        stdout = self.stdout.getvalue()
        if sys.version_info < (2, 7):
            self.assertTrue(stdout.find('Django<1.7') > -1)
            self.assertTrue(stdout.find('django-reversion>=1.8,<1.9') > -1)
        else:
            self.assertTrue(stdout.find('Django<1.9') > -1)
            self.assertTrue(stdout.find('django-reversion>=1.8.7,<1.9') > -1)
        self.assertTrue(stdout.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(stdout.find('djangocms-admin-style') > -1)
        self.assertTrue(stdout.find('djangocms-column') > -1)
        self.assertTrue(stdout.find('djangocms-file') > -1)
        self.assertTrue(stdout.find('djangocms-flash') == -1)
        self.assertTrue(stdout.find('djangocms-googlemap') > -1)
        self.assertTrue(stdout.find('djangocms-inherit') > -1)
        self.assertTrue(stdout.find('djangocms-link') > -1)
        self.assertTrue(stdout.find('djangocms-picture') > -1)
        self.assertTrue(stdout.find('djangocms-style') > -1)
        self.assertTrue(stdout.find('djangocms-teaser') > -1)
        self.assertTrue(stdout.find('djangocms-video') > -1)

    def cleanup_ask(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '--i18n=no',
                    '--cms-version=2.4',
                    '--django-version=1.7',
                    '-f',
                    '-p'+self.project_dir,
                    'example_prj'])
                install.cleanup_directory(conf_data)
                self.assertFalse(os.path.exists(self.project_dir))

    def test_main_invocation(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len', '--cms-version=stable', '--django=%s' % dj_ver,
                                       '-q', '-u', '-p'+self.project_dir, '--verbose',
                                       'example_prj']
                main.execute()
                self.assertTrue(os.path.exists(os.path.join(self.project_dir, 'static')))
                self.assertTrue(os.path.exists(os.path.join(self.project_dir, 'requirements.txt')))
                self.assertTrue(os.path.exists(os.path.join(self.project_dir, 'example_prj', 'static')))
                with open(os.path.join(self.project_dir, 'requirements.txt'), 'r') as req_file:
                    text = req_file.read()
                    self.assertTrue(text.find('djangocms-text-ckeditor') > -1)
                # Checking we successfully completed the whole process
                self.assertTrue('Successfully installed ' in self.stdout.getvalue())
                self.assertTrue(('Get into "%s" directory and type "python manage.py runserver" to start your project' % self.project_dir) in self.stdout.getvalue())

    def test_two_langs_invocation(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len-GB', '-lfr-fr', '--cms-version=stable',
                                       '--django=%s' % dj_ver,
                                       '-q', '-u', '-p'+self.project_dir,
                                       'example_prj']
                main.execute()
                # Checking we successfully completed the whole process
                self.assertTrue(('Get into "%s" directory and type "python manage.py runserver" to start your project' % self.project_dir) in self.stdout.getvalue())

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='django CMS develop does not support python 2.6')
    def test_develop(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len', '--cms-version=develop', '--django=1.8',
                                       '-q', '-u', '-p'+self.project_dir,
                                       'example_prj']
                main.execute()
                # Checking we successfully completed the whole process
                self.assertTrue(('Get into "%s" directory and type "python manage.py runserver" to start your project' % self.project_dir) in self.stdout.getvalue())

    def test_cleanup(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                with self.assertRaises((CalledProcessError, EnvironmentError)):
                    sys.argv = ['main'] + ['--db=postgres://user:pwd@host/dbname',
                                           '-len', '--no-db-driver',
                                           '-q', '-u', '-p'+self.project_dir,
                                           'example_prj']
                    main.execute()
        self.assertFalse(os.path.exists(self.project_dir))

    @unittest.skipIf(sys.version_info >= (3, 0),
                     reason='django 1.4 does not support python3')
    def test_django_1_4(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len', '--django-version=1.4',
                                       '--cms-version=3.0',
                                       '-q', '-u', '-p'+self.project_dir,
                                       'example_prj']
                main.execute()
                # Checking we successfully completed the whole process
                self.assertTrue(('Get into "%s" directory and type "python manage.py runserver" to start your project' % self.project_dir) in self.stdout.getvalue())

    @unittest.skipIf(sys.version_info >= (3, 0),
                     reason='django 1.5 does not support python3')
    def test_django_1_5(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len', '--django-version=1.5',
                                       '--cms-version=3.0',
                                       '-q', '-u', '-p'+self.project_dir,
                                       'example_prj']
                main.execute()
                # Checking we successfully completed the whole process
                self.assertTrue(('Get into "%s" directory and type "python manage.py runserver" to start your project' % self.project_dir) in self.stdout.getvalue())
