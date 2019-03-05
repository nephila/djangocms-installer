# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import subprocess
import sys
from shutil import rmtree
from subprocess import CalledProcessError
from tempfile import mkdtemp

from mock import patch
from six import binary_type

from djangocms_installer import config, install, main

from .base import IsolatedTestClass, get_latest_django, unittest


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
        self.assertTrue(stdout.find('Django<2.0') > -1)
        self.assertFalse(stdout.find('django-reversion') > -1)
        self.assertTrue(stdout.find('djangocms-text-ckeditor') > -1)
        self.assertTrue(stdout.find('djangocms-admin-style') > -1)
        self.assertTrue(stdout.find('djangocms-column') > -1)
        self.assertTrue(stdout.find('djangocms-file') > -1)
        self.assertTrue(stdout.find('djangocms-flash') == -1)
        self.assertTrue(stdout.find('djangocms-googlemap') > -1)
        self.assertTrue(stdout.find('djangocms-inherit') == -1)
        self.assertTrue(stdout.find('djangocms-link') > -1)
        self.assertTrue(stdout.find('djangocms-picture') > -1)
        self.assertTrue(stdout.find('djangocms-style') > -1)
        self.assertTrue(stdout.find('djangocms-snippet') > -1)
        self.assertTrue(stdout.find('cmsplugin-filer') == -1)
        self.assertTrue(stdout.find('djangocms-teaser') == -1)
        self.assertTrue(stdout.find('djangocms-video') > -1)

    def cleanup_ask(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                conf_data = config.parse([
                    '-q',
                    '--db=postgres://user:pwd@host/dbname',
                    '--i18n=no',
                    '--django-version=1.11',
                    '-f',
                    '-p'+self.project_dir,
                    'example_prj'])
                install.cleanup_directory(conf_data)
                self.assertFalse(os.path.exists(self.project_dir))

    def cleanup_skip(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                conf_data = config.parse([
                    '-q',
                    '-s',
                    '--db=postgres://user:pwd@host/dbname',
                    '--i18n=no',
                    '--django-version=1.11',
                    '-f',
                    '-p'+self.project_dir,
                    'example_prj'])
                install.cleanup_directory(conf_data)
                self.assertTrue(os.path.exists(self.project_dir))

    def test_main_invocation(self):
        dj_version, dj_match = get_latest_django(latest_stable=True)
        base_dir = mkdtemp()
        project_dir = os.path.join(base_dir, 'example_prj')
        original_dir = os.getcwd()
        os.chdir(base_dir)
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len', '--cms-version=stable', '--django=%s' % dj_version,
                                       '-q', '-u', '--verbose',
                                       'example_prj']
                main.execute()
                self.assertTrue(os.path.exists(os.path.join(project_dir, 'static')))
                self.assertTrue(os.path.exists(os.path.join(project_dir, 'requirements.txt')))
                self.assertTrue(os.path.exists(os.path.join(project_dir, 'example_prj', 'static')))
                with open(os.path.join(project_dir, 'requirements.txt'), 'r') as req_file:
                    text = req_file.read()
                    self.assertTrue(text.find('djangocms-text-ckeditor') > -1)
                # Checking we successfully completed the whole process
                self.assertTrue('Successfully installed ' in self.stdout.getvalue())
                self.assertTrue(('Get into "%s" directory and type "python manage.py runserver" to start your project' % project_dir) in self.stdout.getvalue())
        os.chdir(original_dir)
        rmtree(base_dir)

    def test_base_invocation(self):
        base_dir = mkdtemp()
        project_dir = os.path.join(base_dir, 'example_prj')
        original_dir = os.getcwd()
        os.chdir(base_dir)
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['example_prj']
                main.execute()
                self.assertTrue(os.path.exists(os.path.join(project_dir, 'static')))
                self.assertTrue(os.path.exists(os.path.join(project_dir, 'requirements.txt')))
                self.assertTrue(os.path.exists(os.path.join(project_dir, 'example_prj', 'static')))
                with open(os.path.join(project_dir, 'requirements.txt'), 'r') as req_file:
                    text = req_file.read()
                    self.assertTrue(text.find('djangocms-text-ckeditor') > -1)
                self.assertTrue(('Get into "%s" directory and type "python manage.py runserver" to start your project' % project_dir) in self.stdout.getvalue())
        os.chdir(project_dir)
        with patch('sys.stdout', self.stdout):
            out = subprocess.check_output(['sqlite3', 'project.db', 'SELECT COUNT(*) FROM auth_user WHERE username="admin"'])
            self.assertEqual(binary_type(out), binary_type(b'1\n'))
        os.chdir(original_dir)
        rmtree(base_dir)

    def test_two_langs_invocation(self):
        dj_version, dj_match = get_latest_django(latest_stable=True)
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len-GB', '-lfr-fr', '--cms-version=stable',
                                       '--django=%s' % dj_version,
                                       '-q', '-u', '-p'+self.project_dir,
                                       'example_prj']
                main.execute()
                # Checking we successfully completed the whole process
                self.assertTrue(('Get into "%s" directory and type "python manage.py runserver" to start your project' % self.project_dir) in self.stdout.getvalue())

    @unittest.skipIf(sys.version_info < (3.5,),
                     reason='django 2.1 does not support python < 3.5')
    def test_develop(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                       '-len', '--cms-version=develop', '--django=2.1',
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
                                           '-len', '--no-db-driver', '-c',
                                           '-q', '-u', '-p'+self.project_dir,
                                           'example_prj']
                    main.execute()
        self.assertFalse(os.path.exists(self.project_dir))

    def test_no_cleanup(self):
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                with self.assertRaises((CalledProcessError, EnvironmentError)):
                    sys.argv = ['main'] + ['--db=postgres://user:pwd@host/dbname',
                                           '-len', '--no-db-driver',
                                           '-q', '-u', '-p' + self.project_dir,
                                           'example_prj']
                    main.execute()
        self.assertTrue(os.path.exists(self.project_dir))

    def test_i18n_urls(self):
        base_dir = mkdtemp()
        project_dir = os.path.join(base_dir, 'example_prj')
        original_dir = os.getcwd()
        os.chdir(base_dir)
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--i18n=yes', 'example_prj']
                main.execute()
                self.assertTrue(
                    os.path.exists(
                        os.path.join(project_dir, 'example_prj', 'urls.py')
                    )
                )
                with open(os.path.join(project_dir, 'example_prj', 'urls.py'),
                          'r') as urls_file:
                    urls = urls_file.read()
                    self.assertTrue(
                        urls.find('urlpatterns += i18n_patterns(') > -1
                    )
        os.chdir(original_dir)
        rmtree(base_dir)

    def test_noi18n_urls(self):
        base_dir = mkdtemp()
        project_dir = os.path.join(base_dir, 'example_prj')
        original_dir = os.getcwd()
        os.chdir(base_dir)
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                sys.argv = ['main'] + ['--i18n=no', 'example_prj']
                main.execute()
                self.assertTrue(
                    os.path.exists(
                        os.path.join(project_dir, 'example_prj', 'urls.py')
                    )
                )
                with open(os.path.join(project_dir, 'example_prj', 'urls.py'),
                          'r') as urls_file:
                    urls = urls_file.read()
                    self.assertTrue(
                        urls.find('urlpatterns += i18n_patterns(') == -1
                    )
        os.chdir(original_dir)
        rmtree(base_dir)
