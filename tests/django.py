# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os.path
import re
import sqlite3
import sys
import textwrap

from mock import patch

from djangocms_installer import config, django, install

from .base import IsolatedTestClass, get_latest_django, unittest

cms_stable = '3.6'


class TestDjango(IsolatedTestClass):
    templates_basic = set(
        (
            ('fullwidth.html', 'Fullwidth'),
            ('sidebar_left.html', 'Sidebar Left'),
            ('sidebar_right.html', 'Sidebar Right'),
        )
    )
    templates_bootstrap = set(
        (
            ('page.html', 'Page'),
            ('feature.html', 'Page with Feature')
        )
    )

    def test_create_project(self):
        dj_version, dj_match = get_latest_django(latest_stable=True)
        config_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                    '--cms-version=%s' % cms_stable, '--django=%s' % dj_version,
                                    '-q', '-p' + self.project_dir, 'example_prj'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        self.assertTrue(os.path.exists(os.path.join(self.project_dir, 'example_prj')))

    def test_django_admin_errors(self):
        dj_version, dj_match = get_latest_django(latest_stable=True)
        config_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                    '--cms-version=%s' % cms_stable, '--django=%s' % dj_version,
                                    '-q', '-p' + self.project_dir, 'example_prj'])
        install.requirements(config_data.requirements)
        config_data.project_name = 'example.prj'
        with self.assertRaises(RuntimeError) as e:
            django.create_project(config_data)
        self.assertTrue('\'example.prj\' is not a valid project name.' in str(e.exception))

    def test_copy_data(self):
        """
        Test correct file copying with different switches
        """
        dj_version, dj_match = get_latest_django(latest_stable=True)
        # Basic template
        config_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                    '--cms-version=%s' % cms_stable, '--django=%s' % dj_version,
                                    '-q', '-p' + self.project_dir, 'test_copy_data_1'])
        os.makedirs(config_data.project_path)
        django.copy_files(config_data)
        starting_page_py = os.path.join(config_data.project_directory, 'starting_page.py')
        starting_page_json = os.path.join(config_data.project_directory, 'starting_page.json')
        basic_template = os.path.join(config_data.project_path, 'templates', 'fullwidth.html')
        boostrap_template = os.path.join(config_data.project_path, 'templates', 'feature.html')
        self.assertFalse(os.path.exists(starting_page_py))
        self.assertFalse(os.path.exists(starting_page_json))
        self.assertFalse(os.path.exists(boostrap_template))
        self.assertTrue(os.path.exists(basic_template))

        # Bootstrap template
        self._create_project_dir()
        config_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                    '--django=%s' % dj_version,
                                    '--cms-version=%s' % cms_stable, '--bootstrap=yes',
                                    '-q', '-p' + self.project_dir, 'test_copy_data_2'])
        os.makedirs(config_data.project_path)
        django.copy_files(config_data)
        starting_page_py = os.path.join(config_data.project_directory, 'starting_page.py')
        starting_page_json = os.path.join(config_data.project_directory, 'starting_page.json')
        basic_template = os.path.join(config_data.project_path, 'templates', 'fullwidth.html')
        boostrap_template = os.path.join(config_data.project_path, 'templates', 'feature.html')
        self.assertFalse(os.path.exists(starting_page_py))
        self.assertFalse(os.path.exists(starting_page_json))
        self.assertTrue(os.path.exists(boostrap_template))
        self.assertFalse(os.path.exists(basic_template))

        # Custom template
        self._create_project_dir()
        tpl_path = os.path.join(os.path.dirname(__file__), 'test_templates')
        config_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                    '--django=%s' % dj_version,
                                    '--cms-version=%s' % cms_stable, '--templates=%s' % tpl_path,
                                    '-q', '-p' + self.project_dir, 'example_prj'])
        os.makedirs(config_data.project_path)
        django.copy_files(config_data)
        basic_template = os.path.join(config_data.project_path, 'templates', 'fullwidth.html')
        boostrap_template = os.path.join(config_data.project_path, 'templates', 'feature.html')
        custom_template = os.path.join(config_data.project_path, 'templates', 'left.html')
        self.assertTrue(os.path.exists(custom_template))
        self.assertFalse(os.path.exists(boostrap_template))
        self.assertFalse(os.path.exists(basic_template))

        # Starting page
        self._create_project_dir()
        config_data = config.parse(['--db=postgres://user:pwd@host/dbname',
                                    '--django=%s' % dj_version,
                                    '--cms-version=%s' % cms_stable, '--starting-page=yes',
                                    '-q', '-p' + self.project_dir, 'example_prj'])
        os.makedirs(config_data.project_path)
        django.copy_files(config_data)
        starting_page_py = os.path.join(config_data.project_directory, 'starting_page.py')
        starting_page_json = os.path.join(config_data.project_directory, 'starting_page.json')
        self.assertTrue(os.path.exists(starting_page_py))
        self.assertTrue(os.path.exists(starting_page_json))

    def test_patch_111_settings(self):
        dj_version, dj_match = get_latest_django(latest_stable=True, latest_1_x=True)

        extra_path = os.path.join(os.path.dirname(__file__), 'data', 'extra_settings.py')
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en', '--extra-settings=%s' % extra_path,
                                    '--cms-version=%s' % cms_stable,
                                    '--django-version=%s' % dj_version,
                                    '--timezone=Europe/Moscow',
                                    '-q', '-u', '-zno', '--i18n=no',
                                    '-p' + self.project_dir, 'example_path_111_settings'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertEqual(project.settings.MEDIA_ROOT,
                         os.path.join(config_data.project_directory, 'media'))
        self.assertEqual(project.settings.MEDIA_URL, '/media/')

        # Data from external settings files
        self.assertIsNotNone(getattr(project.settings, 'MIDDLEWARE', None))
        self.assertIsNone(getattr(project.settings, 'MIDDLEWARE_CLASSES', None))

    def test_patch_111_36_settings(self):
        dj_version, dj_match = get_latest_django(latest_1_x=True)

        extra_path = os.path.join(os.path.dirname(__file__), 'data', 'extra_settings.py')
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en', '--extra-settings=%s' % extra_path,
                                    '--django-version=%s' % dj_version,
                                    '--cms-version=3.6', '--timezone=Europe/Moscow',
                                    '-q', '-u', '-zno', '--i18n=no',
                                    '-p' + self.project_dir, 'test_patch_111_36_settings'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertEqual(project.settings.MEDIA_ROOT,
                         os.path.join(config_data.project_directory, 'media'))
        self.assertEqual(project.settings.MEDIA_URL, '/media/')

        # Data from external settings file
        self.assertEqual(project.settings.CUSTOM_SETTINGS_VAR, True)
        self.assertEqual(project.settings.CMS_PERMISSION, False)
        self.assertEqual(set(project.settings.CMS_TEMPLATES), self.templates_basic)
        self.assertIsNotNone(getattr(project.settings, 'MIDDLEWARE', None))
        self.assertIsNone(getattr(project.settings, 'MIDDLEWARE_CLASSES', None))

    def test_patch_django_111_36(self):
        dj_version, dj_match = get_latest_django(latest_1_x=True)

        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en', '--bootstrap=yes',
                                    '--django-version=%s' % dj_version,
                                    '--cms-version=3.6', '--timezone=Europe/Moscow',
                                    '-q', '-u', '-zno', '--i18n=no',
                                    '-p' + self.project_dir, 'test_patch_django_111_36'])

        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        settings = open(config_data.settings_path).read()
        urlconf = open(config_data.urlconf_path).read()

        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertEqual(
            project.settings.MEDIA_ROOT, os.path.join(config_data.project_directory, 'media')
        )
        self.assertEqual(project.settings.MEDIA_URL, '/media/')

        self.assertEqual(project.settings.TIME_ZONE, 'Europe/Moscow')
        self.assertTrue('cmsplugin_filer_image' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_file' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_folder' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_link' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_teaser' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_utils' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_video' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_text_ckeditor' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_admin_style' in project.settings.INSTALLED_APPS)
        self.assertTrue('filer' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_bootstrap4' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_file' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_flash' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_googlemap' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_inherit' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_link' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_picture' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_style' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_teaser' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_video' in project.settings.INSTALLED_APPS)
        self.assertTrue(
            config.get_settings().APPHOOK_RELOAD_MIDDLEWARE_CLASS in
            project.settings.MIDDLEWARE
        )
        self.assertEqual(set(project.settings.CMS_TEMPLATES), self.templates_bootstrap)

        self.assertTrue(project.settings.TEMPLATES)
        self.assertEqual(len(re.findall('BASE_DIR = ', settings)), 1)
        self.assertEqual(len(re.findall('STATIC_ROOT', settings)), 1)
        self.assertEqual(len(re.findall('MEDIA_ROOT =', settings)), 1)
        self.assertEqual(len(re.findall('STATICFILES_DIRS', settings)), 1)

    def test_patch_django_111_develop(self):
        extra_path = os.path.join(os.path.dirname(__file__), 'data', 'extra_settings.py')
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en', '--extra-settings=%s' % extra_path,
                                    '--django-version=1.11', '-f',
                                    '--cms-version=develop', '--timezone=Europe/Moscow',
                                    '-q', '-u', '-zno', '--i18n=no',
                                    '-p' + self.project_dir, 'test_patch_django_111_develop'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertTrue(project.settings.TEMPLATES)
        self.assertFalse(getattr(project.settings, 'TEMPLATES_DIR', False))
        self.assertTrue(
            config.get_settings().APPHOOK_RELOAD_MIDDLEWARE_CLASS in
            project.settings.MIDDLEWARE
        )

    @unittest.skipIf(sys.version_info[:2] not in ((3, 5), (3, 6), (3, 7),),
                     reason='django 2.1 only supports python 3.5, 3.6 and 3.7')
    def test_patch_django_22_rc(self):
        extra_path = os.path.join(os.path.dirname(__file__), 'data', 'extra_settings.py')
        params = [
            '--db=sqlite://localhost/test.db', '--lang=en', '--extra-settings=%s' % extra_path,
            '--django-version=2.2', '-f', '--cms-version=rc', '--timezone=Europe/Moscow',
            '-q', '-u', '-zno', '--i18n=no', '-p' + self.project_dir,
            'test_patch_django_22_rc'
        ]
        config_data = config.parse(params)
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertTrue(project.settings.TEMPLATES)
        self.assertFalse(getattr(project.settings, 'TEMPLATES_DIR', False))
        self.assertTrue(
            config.get_settings().APPHOOK_RELOAD_MIDDLEWARE_CLASS in
            project.settings.MIDDLEWARE
        )

    @unittest.skipIf(sys.version_info[:2] not in ((3, 5), (3, 6), (3, 7),),
                     reason='django 2.1 only supports python 3.5, 3.6 and 3.7')
    def test_patch_django_21_develop(self):
        extra_path = os.path.join(os.path.dirname(__file__), 'data', 'extra_settings.py')
        params = [
            '--db=sqlite://localhost/test.db', '--lang=en', '--extra-settings=%s' % extra_path,
            '--django-version=2.1', '-f', '--cms-version=develop', '--timezone=Europe/Moscow',
            '-q', '-u', '-zno', '--i18n=no', '-p' + self.project_dir,
            'test_patch_django_21_develop'
        ]
        config_data = config.parse(params)
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertTrue(project.settings.TEMPLATES)
        self.assertFalse(getattr(project.settings, 'TEMPLATES_DIR', False))
        self.assertTrue(
            config.get_settings().APPHOOK_RELOAD_MIDDLEWARE_CLASS in
            project.settings.MIDDLEWARE
        )

    @unittest.skipIf(sys.version_info[:2] not in ((3, 5), (3, 6), (3, 7),),
                     reason='django 2.0 only supports python 3.5, 3.6 and 3.7')
    def test_patch_django_20_develop(self):
        extra_path = os.path.join(os.path.dirname(__file__), 'data', 'extra_settings.py')
        params = [
            '--db=sqlite://localhost/test.db', '--lang=en', '--extra-settings=%s' % extra_path,
            '--django-version=2.0', '-f', '--cms-version=develop', '--timezone=Europe/Moscow',
            '-q', '-u', '-zno', '--i18n=no', '-p' + self.project_dir,
            'test_patch_django_20_develop'
        ]
        config_data = config.parse(params)
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertTrue(project.settings.TEMPLATES)
        self.assertFalse(getattr(project.settings, 'TEMPLATES_DIR', False))
        self.assertTrue(
            config.get_settings().APPHOOK_RELOAD_MIDDLEWARE_CLASS in
            project.settings.MIDDLEWARE
        )

    def test_patch_django_111_no_plugins(self):
        extra_path = os.path.join(os.path.dirname(__file__), 'data', 'extra_settings.py')
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en', '--extra-settings=%s' % extra_path,
                                    '--django-version=1.11', '-f', '--no-plugins',
                                    '--cms-version=%s' % cms_stable, '--timezone=Europe/Moscow',
                                    '-q', '-u', '-zno', '--i18n=no',
                                    '-p' + self.project_dir, 'test_patch_django_111_no_plugins'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertTrue(project.settings.TEMPLATES)
        self.assertFalse(getattr(project.settings, 'TEMPLATES_DIR', False))
        self.assertFalse('djangocms_file' in project.settings.INSTALLED_APPS)
        self.assertFalse('djangocms_flash' in project.settings.INSTALLED_APPS)
        self.assertFalse('djangocms_googlemap' in project.settings.INSTALLED_APPS)
        self.assertFalse('djangocms_inherit' in project.settings.INSTALLED_APPS)
        self.assertFalse('djangocms_link' in project.settings.INSTALLED_APPS)
        self.assertFalse('djangocms_picture' in project.settings.INSTALLED_APPS)
        self.assertFalse('djangocms_teaser' in project.settings.INSTALLED_APPS)
        self.assertFalse('djangocms_video' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.file' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.flash' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.googlemap' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.inherit' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.link' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.picture' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.teaser' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.text' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.twitter' in project.settings.INSTALLED_APPS)
        self.assertFalse('cms.plugins.video' in project.settings.INSTALLED_APPS)

    def test_patch(self):
        dj_version, dj_match = get_latest_django(latest_stable=True)

        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--lang=en',
                                    '--cms-version=%s' % cms_stable,
                                    '--django-version=%s' % dj_version,
                                    '--timezone=Europe/Moscow',
                                    '-f', '-q', '-u', '-zno', '--i18n=no',
                                    '-p' + self.project_dir, 'example_path_patch'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        settings = open(config_data.settings_path).read()
        urlconf = open(config_data.urlconf_path).read()

        # settings is importable even in non django environment
        sys.path.append(config_data.project_directory)

        project = __import__(config_data.project_name, globals(), locals(), [str('settings')])

        # checking for django options
        self.assertFalse(project.settings.USE_L10N)
        self.assertFalse(project.settings.USE_TZ)
        self.assertEqual(project.settings.TIME_ZONE, 'Europe/Moscow')
        self.assertEqual(project.settings.LANGUAGE_CODE, 'en')
        self.assertTrue(project.settings.MEDIA_ROOT,
                        os.path.join(config_data.project_directory, 'media'))
        self.assertEqual(project.settings.MEDIA_URL, '/media/')
        #
        # checking for standard CMS settings
        self.assertTrue(
            'sekizai.context_processors.sekizai' in
            project.settings.TEMPLATES[0]['OPTIONS']['context_processors']
        )
        self.assertTrue(
            'cms.middleware.toolbar.ToolbarMiddleware' in project.settings.MIDDLEWARE
        )
        self.assertTrue(project.settings.CMS_LANGUAGES['default']['redirect_on_fallback'])
        self.assertEqual(project.settings.CMS_LANGUAGES[1][0]['code'], 'en')

        # checking mptt / treebeard
        self.assertFalse('mptt' in project.settings.INSTALLED_APPS)
        self.assertTrue('treebeard' in project.settings.INSTALLED_APPS)

        # checking for filer (optional) settings
        self.assertTrue('filer' in project.settings.INSTALLED_APPS)
        self.assertTrue('easy_thumbnails' in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_image' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_file' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_folder' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_link' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_teaser' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_utils' not in project.settings.INSTALLED_APPS)
        self.assertTrue('cmsplugin_filer_video' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_text_ckeditor' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_admin_style' in project.settings.INSTALLED_APPS)
        self.assertTrue('filer' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_file' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_flash' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_googlemap' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_inherit' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_link' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_picture' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_style' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_teaser' not in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_video' in project.settings.INSTALLED_APPS)
        self.assertTrue('djangocms_bootstrap4' in project.settings.INSTALLED_APPS)
        self.assertTrue(hasattr(project.settings, 'THUMBNAIL_PROCESSORS'))
        self.assertTrue(
            'cms.context_processors.cms_settings' in
            project.settings.TEMPLATES[0]['OPTIONS']['context_processors']
        )
        self.assertTrue(
            'cms.context_processors.media' not in
            project.settings.TEMPLATES[0]['OPTIONS']['context_processors']
        )

        # basic urlconf check
        self.assertTrue('cms.urls' in urlconf)
        self.assertTrue('staticfiles_urlpatterns' in urlconf)

        sys.path.remove(config_data.project_directory)
        del project
        del (sys.modules["%s.settings" % config_data.project_name])

    def test_database_setup_filer(self):
        dj_version, dj_match = get_latest_django(latest_stable=True)

        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--cms-version=%s' % cms_stable,
                                    '-f', '-q', '-u', '--django-version=%s' % dj_version,
                                    '-p' + self.project_dir, 'cms_project'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        django.setup_database(config_data)
        project_db = sqlite3.connect(os.path.join(config_data.project_directory, 'test.db'))

        # Checking content type table to check for correct applications setup
        query = project_db.execute(
            'SELECT * FROM django_content_type WHERE app_label="cms" AND model="page"'
        )
        row = query.fetchone()
        self.assertTrue('page' in row)
        self.assertTrue('cms' in row)

        # No data in CMS tables at setup time, but if query succeed database
        # schema should be fine
        query = project_db.execute('SELECT * FROM cms_page')
        self.assertTrue(query)

        # No data in auth tables at setup time due to the no-input
        query = project_db.execute('SELECT * FROM auth_user')
        self.assertTrue(query)

        # No data in CMS tables at setup time, but if query succeed database
        # schema should be fine
        query = project_db.execute('SELECT * FROM cms_page')
        self.assertTrue(query)

        # Check filer data
        query = project_db.execute(
            'SELECT * FROM django_content_type WHERE app_label="filer" AND model="image"'
        )
        row = query.fetchone()
        self.assertTrue('filer' in row)
        self.assertTrue('image' in row)

    def test_starting_page(self):
        dj_version, dj_match = get_latest_django(latest_stable=True)

        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '--cms-version=%s' % cms_stable,
                                    '-q', '-u', '--django-version=%s' % dj_version,
                                    '--starting-page=yes',
                                    '-p' + self.project_dir, 'cms_project'])
        install.requirements(config_data.requirements)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        django.setup_database(config_data)
        django.load_starting_page(config_data)
        project_db = sqlite3.connect(os.path.join(config_data.project_directory, 'test.db'))

        # Check loaded data
        query = project_db.execute('SELECT * FROM cms_page')
        row = query.fetchone()
        self.assertTrue('fullwidth.html' in row)

        query = project_db.execute('SELECT * FROM cms_title')
        row = query.fetchone()
        self.assertTrue('Home' in row)

        query = project_db.execute('SELECT * FROM cms_cmsplugin')
        row = query.fetchone()
        self.assertTrue('TextPlugin' in row)

    def test_force_django(self):
        config_data = config.parse(['--db=sqlite://localhost/test.db',
                                    '-q', '-u', '--django-version=1.11',
                                    '--cms-version=3.6', '--starting-page=yes',
                                    '-p' + self.project_dir, 'cms_project'])
        install.requirements(config_data.requirements)
        install.requirements('django<1.9')
        django.create_project(config_data)
        with patch('sys.stdout', self.stdout):
            with patch('sys.stderr', self.stderr):
                with self.assertRaises(SystemExit) as error:
                    django.patch_settings(config_data)
        self.assertEqual(error.exception.code, 9)
        self.assertTrue(self.stderr.getvalue().find(
            'Currently installed Django version 1.8.19 differs from the declared 1.11'
        ) > -1)


class TestBaseDjango(unittest.TestCase):
    def test_build_settings(self):
        """Tests django.__init__._build_settings function."""
        dj_version, dj_match = get_latest_django(latest_stable=True)
        config_data = config.parse(['--db=postgres://user:pwd@host:5432/dbname',
                                    '--cms-version=%s' % cms_stable, '--django=%s' % dj_version,
                                    '-q', '-p .', 'example_prj'])
        settings = django._build_settings(config_data)
        self.assertTrue(textwrap.dedent('''
            DATABASES = {
                'default': {
                    'CONN_MAX_AGE': 0,
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'HOST': 'host',
                    'NAME': 'dbname',
                    'PASSWORD': 'pwd',
                    'PORT': 5432,
                    'USER': 'user'
                }
            }''').strip() in settings)
