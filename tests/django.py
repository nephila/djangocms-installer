#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
import six
import sqlite3
from . import unittest

from aldryn_installer import config, django, install
from . import BaseTestClass


class TestDjango(BaseTestClass):

    def test_create_project(self):
        self._remove_project_dir()
        config_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                    '--cms-version=develop',
                                    '-q', '-p'+self.project_dir, 'example_prj'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        self.assertTrue(os.path.exists(os.path.join(self.project_dir, 'example_prj')))

    def test_patch(self):
        self._remove_project_dir()
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en',
                                    '--cms-version=develop',
                                    '-f', '-q', '-u', '-zno', '--i18n=no',
                                    '-p'+self.project_dir, 'example_patch'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        settings = open(config_data.settings_path).read()
        urlconf = open(config_data.urlconf_path).read()

        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name,
                             globals(), locals(), ['settings'])

        ## checking for django options
        self.assertFalse(project.settings.USE_L10N)
        self.assertFalse(project.settings.USE_TZ)
        self.assertEqual(project.settings.LANGUAGE_CODE, 'en')
        #
        ## checking for standard CMS settings
        self.assertTrue('sekizai.context_processors.sekizai' in project.settings.TEMPLATE_CONTEXT_PROCESSORS)
        self.assertTrue('cms.middleware.toolbar.ToolbarMiddleware' in project.settings.MIDDLEWARE_CLASSES)
        self.assertTrue(project.settings.CMS_LANGUAGES['default']['redirect_on_fallback'])
        self.assertEqual(project.settings.CMS_LANGUAGES[1][0]['code'], 'en')

        ## checking for filer (optional) settings
        self.assertTrue('filer' in project.settings.INSTALLED_APPS)
        self.assertTrue('easy_thumbnails' in project.settings.INSTALLED_APPS)
        self.assertTrue(hasattr(project.settings, 'THUMBNAIL_PROCESSORS'))

        ## basic urlconf check
        self.assertTrue('cms.urls' in urlconf)
        self.assertTrue('staticfiles_urlpatterns' in urlconf)

        sys.path.remove(config_data.project_directory)
        self._remove_project_dir()
        del project
        del(sys.modules["%s.settings" % config_data.project_name])

    @unittest.skipIf(six.PY3, "Filer not compatible with Python 3, skipping")
    def test_setup_database_filer(self):
        self._remove_project_dir()
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '-f', '-q', '-u',
                                    '--cms-version=develop',
                                    '-p'+self.project_dir, 'aldryn_project'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        django.setup_database(config_data)
        project_db = sqlite3.connect(os.path.join(config_data.project_directory, 'test.db'))

        # Checking content type table to check for correct applications setup
        query = project_db.execute('SELECT * FROM django_content_type WHERE app_label="cms" AND model="page"')
        self.assertEqual(query.fetchone()[1], 'page')
        query = project_db.execute('SELECT * FROM django_content_type WHERE app_label="filer" AND model="image"')
        self.assertEqual(query.fetchone()[1], 'image')

        # No data in CMS tables at setup time, but if query succeed database
        # schema should be fine
        query = project_db.execute('SELECT * FROM cms_page')
        self.assertTrue(query)

    def test_setup_database(self):
        self._remove_project_dir()
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '-q', '-u', '--cms-version=develop',
                                    '-p'+self.project_dir, 'aldryn_project'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        django.setup_database(config_data)
        project_db = sqlite3.connect(os.path.join(config_data.project_directory, 'test.db'))

        # Checking content type table to check for correct applications setup
        query = project_db.execute('SELECT * FROM django_content_type WHERE app_label="cms" AND model="page"')
        self.assertEqual(query.fetchone()[1], 'page')

        # No data in CMS tables at setup time, but if query succeed database
        # schema should be fine
        query = project_db.execute('SELECT * FROM cms_page')
        self.assertTrue(query)

