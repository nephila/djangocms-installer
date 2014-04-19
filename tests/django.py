#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
import six
import sqlite3
from . import unittest
import re

from djangocms_installer import config, django, install
from . import BaseTestClass


class TestDjango(BaseTestClass):

    def test_create_project(self):
        config_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                    '--cms-version=develop',
                                    '-q', '-p'+self.project_dir, 'example_prj'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        self.assertTrue(os.path.exists(os.path.join(self.project_dir, 'example_prj')))

    def test_patch_16(self):
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en',
                                    '--django-version=1.6',
                                    '--cms-version=3.0',
                                    '-q', '-u', '-zno', '--i18n=no',
                                    '-p'+self.project_dir, 'example_path_16'])

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
        self.assertTrue(project.settings.MEDIA_ROOT, os.path.join(config_data.project_directory, 'media'))
        self.assertEqual(project.settings.MEDIA_URL, '/media/')

        self.assertTrue('cmsplugin_filer_image' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_file' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_folder' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_link' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_teaser' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_utils' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_video' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_text_ckeditor' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_admin_style' in project.settings.INSTALLED_APPS)
        self.assertTrue('filer' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_column' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_file' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_flash' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_googlemap' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_inherit' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_link' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_picture' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_style' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_teaser' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_video' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.context_processors.cms_settings' in project.settings.TEMPLATE_CONTEXT_PROCESSORS)
        self.assertTrue('cms.context_processors.media' not in project.settings.TEMPLATE_CONTEXT_PROCESSORS)

        self.assertEqual(len(re.findall('BASE_DIR = ', settings)), 1)
        self.assertEqual(len(re.findall('STATIC_ROOT', settings)), 1)
        self.assertEqual(len(re.findall('MEDIA_ROOT =', settings)), 1)
        self.assertEqual(len(re.findall('STATICFILES_DIRS', settings)), 2)

    @unittest.skipIf(sys.version_info >= (3, 0),
                     reason="django CMS 2.4 does not support python3")
    def test_patch_24_standard(self):
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en',
                                    '--django-version=1.5',
                                    '--cms-version=2.4',
                                    '-q', '-u', '-zno', '--i18n=no',
                                    '-p'+self.project_dir, 'example_path_24_s'])

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
        self.assertTrue(project.settings.MEDIA_ROOT, os.path.join(config_data.project_directory, 'media'))
        self.assertEqual(project.settings.MEDIA_URL, '/media/')
        self.assertTrue('cms.context_processors.cms_settings' not in project.settings.TEMPLATE_CONTEXT_PROCESSORS)
        self.assertTrue('cms.context_processors.media' in project.settings.TEMPLATE_CONTEXT_PROCESSORS)
        self.assertTrue('djangocms_file' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_flash' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_googlemap' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_inherit' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_link' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_picture' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_teaser' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_video' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.file' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.flash' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.googlemap' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.inherit' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.link' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.picture' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.teaser' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.text' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.twitter' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.video' in project.settings.INSTALLED_APPS)

    @unittest.skipIf(sys.version_info >= (3, 0),
                     reason="django CMS 2.4 does not support python3")
    def test_patch_24_filer(self):
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en',
                                    '--django-version=1.5',
                                    '--cms-version=2.4',
                                    '-f', '-q', '-u', '-zno', '--i18n=no',
                                    '-p'+self.project_dir, 'example_path_24_f'])

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
        self.assertTrue(project.settings.MEDIA_ROOT, os.path.join(config_data.project_directory, 'media'))
        self.assertEqual(project.settings.MEDIA_URL, '/media/')
        self.assertTrue('djangocms_file' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_flash' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_googlemap' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_inherit' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_link' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_picture' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_teaser' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_video' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_image' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.flash' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.googlemap' in project.settings.INSTALLED_APPS)
        self.assertTrue('cms.plugins.inherit' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_file' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_folder' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_link' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_teaser' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_utils' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_video' in project.settings.INSTALLED_APPS)

    def test_patch(self):
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en',
                                    '--django-version=1.5',
                                    '--cms-version=3.0',
                                    '-f', '-q', '-u', '-zno', '--i18n=no',
                                    '-p'+self.project_dir, 'example_path_patch'])
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
        self.assertTrue(project.settings.MEDIA_ROOT, os.path.join(config_data.project_directory, 'media'))
        self.assertEqual(project.settings.MEDIA_URL, '/media/')
        #
        ## checking for standard CMS settings
        self.assertTrue('sekizai.context_processors.sekizai' in project.settings.TEMPLATE_CONTEXT_PROCESSORS)
        self.assertTrue('cms.middleware.toolbar.ToolbarMiddleware' in project.settings.MIDDLEWARE_CLASSES)
        self.assertTrue(project.settings.CMS_LANGUAGES['default']['redirect_on_fallback'])
        self.assertEqual(project.settings.CMS_LANGUAGES[1][0]['code'], 'en')

        ## checking for filer (optional) settings
        self.assertTrue('filer' in project.settings.INSTALLED_APPS)
        self.assertTrue('easy_thumbnails' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_image' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_file' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_folder' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_link' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_teaser' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_utils' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_video' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_text_ckeditor' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_admin_style' in project.settings.INSTALLED_APPS)
        self.assertTrue('filer' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_column' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_file' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_flash' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_googlemap' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_inherit' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_link' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_picture' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_style' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_teaser' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_video' not in project.settings.INSTALLED_APPS)
        self.assertTrue(hasattr(project.settings, 'THUMBNAIL_PROCESSORS'))
        self.assertTrue('cms.context_processors.cms_settings' in project.settings.TEMPLATE_CONTEXT_PROCESSORS)
        self.assertTrue('cms.context_processors.media' not in project.settings.TEMPLATE_CONTEXT_PROCESSORS)

        ## basic urlconf check
        self.assertTrue('cms.urls' in urlconf)
        self.assertTrue('staticfiles_urlpatterns' in urlconf)

        sys.path.remove(config_data.project_directory)
        del project
        del(sys.modules["%s.settings" % config_data.project_name])

    @unittest.skip("Currently unsupported test")
    def test_database_setup_filer(self):
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '-f', '-q', '-u',
                                    '--cms-version=3.0',
                                    '-p'+self.project_dir, 'cms_project'])
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

    def test_database_setup(self):
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '-q', '-u', '--cms-version=3.0',
                                    '-p'+self.project_dir, 'cms_project'])
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

