# -*- coding: utf-8 -*-
from __future__ import print_function
import time

CONFIGURABLE_OPTIONS = ['--db', '--cms-version', '--django-version', '--i18n',
                        '--reversion', '--languages', '--timezone', '--use-tz',
                        '--permissions', '--bootstrap', '--templates',
                        '--starting-page']

DJANGOCMS_DEVELOP = 'https://github.com/divio/django-cms/archive/develop.zip?%s' % time.time()
DJANGOCMS_RC = 'https://github.com/divio/django-cms/archive/3.0c2.zip'
DJANGOCMS_BETA = 'https://github.com/divio/django-cms/archive/3.0.0.beta3.zip'
DJANGOCMS_SUPPORTED = ('2.4', '3.0', '3.1', 'stable', 'develop')

DJANGO_DEVELOP = 'https://github.com/django/django/archive/master.zip?%s' % time.time()
DJANGO_BETA = 'https://github.com/django/django/archive/master.zip?%s' % time.time()
DJANGO_SUPPORTED = ('1.4', '1.5', '1.6', '1.7', '1.8', 'stable')

CMS_VERSION_MATRIX = {
    'stable': 3.1,
    'rc': 3.2,
    'beta': 3.2,
    'develop': 3.2
}
DJANGO_VERSION_MATRIX = {
    'stable': 1.7,
    'rc': 1.8,
    'beta': 1.8,
    'develop': 1.8
}
VERSION_MATRIX = {
    2.4: (1.4, 1.5),
    3.0: (1.4, 1.7),
    3.1: (1.6, 1.8),
    3.2: (1.6, 1.8),
}

REQUIREMENTS = {
    'default': [
        'django-classy-tags>=0.3.4.1',
        'html5lib',
        'Pillow>=2.3',
        'django-sekizai>=0.7',
        'six',
    ],
    'django-legacy': [
        'south>=1.0.0',
    ],
    'reversion-django-1.4': [
        'django-reversion<1.7',
    ],
    'reversion-django-1.5': [
        'django-reversion>=1.7,<1.8',
    ],
    'reversion-django-1.6': [
        'django-reversion>=1.8,<1.8.6',
    ],
    'reversion-django-1.7': [
        'django-reversion>=1.8.2,<1.8.6',
    ],
    'reversion-django-1.8': [
        'django-reversion>=1.8.7',
    ],
    'cms-2.x': [
        'django-mptt>=0.5.1,<0.5.3',
    ],
    'cms-3.0': [
        'django-mptt<0.7',
    ],

    'cms-3.x': [
        'django-treebeard>=2.0',
    ],
    'plugins-common': [
        'djangocms-admin-style',
        'djangocms-column',
        'djangocms-flash',
        'djangocms-googlemap',
        'djangocms-inherit',
        'djangocms-style',
        'djangocms-text-ckeditor>=2.3.0',
    ],
    'plugins-basic': [
        'djangocms-file',
        'djangocms-link',
        'djangocms-picture',
        'djangocms-teaser',
        'djangocms-video',
    ],
    'plugins-common-master': [
        'https://github.com/divio/djangocms-admin-style/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-column/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-flash/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-googlemap/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-inherit/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-link/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-style/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-text-ckeditor/archive/master.zip?%(bust)s' % {'bust': time.time()},
    ],
    'plugins-basic-master': [
        'https://github.com/divio/djangocms-file/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-picture/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-teaser/archive/master.zip?%(bust)s' % {'bust': time.time()},
        'https://github.com/divio/djangocms-video/archive/master.zip?%(bust)s' % {'bust': time.time()},
    ],
    'aldryn': [
        'django-compressor',
    ],
    'filer': [
        'easy_thumbnails',
        'https://github.com/stefanfoulis/django-filer/archive/develop.zip',
        'cmsplugin-filer>=0.9.9',
    ],
    'filer-cms-2.x': [
        'easy_thumbnails',
        'django-filer<=0.9.6',
        'cmsplugin-filer',
    ],
}

TEMPLATES_1_8 = """
TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [{dirs}],
        'OPTIONS': {{
            'context_processors': [
                {processors}
            ],
            'loaders': [
                {loaders}
            ],
        }},
    }},
]
"""

PLUGIN_LIST_TEXT = """
djangocms_installer will install and configure the following plugins:
 * djangocms_column (Column plugin)
 * djangocms-file (File plugin)
 * djangocms-flash (Flash plugin)
 * djangocms-googlemap (GoogleMap plugin)
 * djangocms-inherit (Inherit plugin)
 * djangocms-link (Link plugin)
 * djangocms-picture (Picture plugin)
 * djangocms_style (Style plugin)
 * djangocms-teaser (Teaser plugin)
 * djangocms-text-ckeditor (Text plugin)
 * djangocms-video (Video plugin)

It will optionally install cmsplugin-filer plugins (if requested during
configuration):
 * cmsplugin_filer_file (File plugin, replaces djangocms-file)
 * cmsplugin_filer_folder (Folder plugin)
 * cmsplugin_filer_image (Image plugin, replaces djangocms-picture)
 * djangocms-link (Link plugin)
 * cmsplugin_filer_teaser (Teaser plugin, replaces djangocms-teaser)
 * cmsplugin_filer_video (Video plugin, replaces djangocms-video)
"""

DRIVERS = {
    'django.db.backends.postgresql_psycopg2': 'psycopg2',
    'django.db.backends.postgresql_postgis': 'postgis',
    'django.db.backends.mysql': 'MySQL-python',
    'django.db.backends.sqlite3': '',
}

DEFAULT_PROJECT_HEADER = """# -*- coding: utf-8 -*-
import os
gettext = lambda s: s
"""
STATICFILES_DEFAULT = """STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)"""

BASE_DIR = """
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
"""

ALDRYN_BOILERPLATE = 'https://github.com/aldryn/aldryn-boilerplate/archive/master.zip'

VERSION_WARNING = '%s version of %s is not supported and it may not work as expected'
