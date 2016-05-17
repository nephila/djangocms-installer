# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys
import time

bust = {'bust': time.time()}

CONFIGURABLE_OPTIONS = ['--db', '--cms-version', '--django-version', '--i18n',
                        '--reversion', '--languages', '--timezone', '--use-tz',
                        '--permissions', '--bootstrap', '--templates',
                        '--starting-page']

DJANGOCMS_DEVELOP = 'https://github.com/divio/django-cms/archive/develop.zip?%s' % time.time()
DJANGOCMS_RC = 'https://github.com/divio/django-cms/archive/develop.zip?%s' % time.time()
DJANGOCMS_BETA = 'https://github.com/divio/django-cms/archive/3.0.0.beta3.zip'

if sys.version_info < (2, 7):
    DJANGOCMS_SUPPORTED = ('2.4', '3.0', '3.1', '3.2', 'stable', 'develop')
    DJANGOCMS_STABLE = 3.2
elif sys.version_info >= (3, 5):
    DJANGOCMS_SUPPORTED = ('3.0', '3.1', '3.2', 'stable', 'rc', 'develop')
    DJANGOCMS_STABLE = 3.2
else:
    DJANGOCMS_SUPPORTED = ('2.4', '3.0', '3.1', '3.2', 'stable', 'rc', 'develop')
    DJANGOCMS_STABLE = 3.2

DJANGO_DEVELOP = 'https://github.com/django/django/archive/master.zip?%s' % time.time()
DJANGO_BETA = 'https://github.com/django/django/archive/master.zip?%s' % time.time()
if sys.version_info < (2, 7):
    DJANGO_SUPPORTED = ('1.4', '1.5', '1.6', 'stable')
    DJANGO_STABLE = 1.6
elif sys.version_info >= (3, 5):
    DJANGO_SUPPORTED = ('1.8', '1.9', 'stable')
    DJANGO_STABLE = 1.8
elif sys.version_info >= (3, 4):
    DJANGO_SUPPORTED = ('1.5', '1.6', '1.7', '1.8', '1.9', 'stable')
    DJANGO_STABLE = 1.8
elif sys.version_info >= (3, 3):
    DJANGO_SUPPORTED = ('1.5', '1.6', '1.7', '1.8', 'stable')
    DJANGO_STABLE = 1.8
else:
    DJANGO_SUPPORTED = ('1.4', '1.5', '1.6', '1.7', '1.8', '1.9', 'stable')
    DJANGO_STABLE = 1.8

CMS_VERSION_MATRIX = {
    'stable': DJANGOCMS_STABLE,
    'rc': 3.3,
    'beta': 3.3,
    'develop': 3.3
}
DJANGO_VERSION_MATRIX = {
    'stable': DJANGO_STABLE,
    'rc': 1.9,
    'beta': 1.9,
    'develop': 1.9
}
VERSION_MATRIX = {
    2.4: (1.4, 1.5),
    3.0: (1.4, 1.7),
    3.1: (1.6, 1.8),
    3.2: (1.6, 1.9),
    3.3: (1.8, 1.9),
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
    'django-1.4': [
    ],
    'django-1.5': [
    ],
    'django-1.6': [
    ],
    'django-1.7': [
    ],
    'django-1.8': [
        'django-mptt<0.9',
    ],
    'django-1.9': [
        'django-mptt<0.9',
    ],
    'reversion-django-1.4': [
        'django-reversion<1.7',
    ],
    'reversion-django-1.5': [
        'django-reversion>=1.7,<1.8',
    ],
    'reversion-django-1.6': [
        'django-reversion>=1.8,<1.9',
    ],
    'reversion-django-1.7': [
        'django-reversion>=1.8.2,<1.9',
    ],
    'reversion-django-1.8': [
        'django-reversion>=1.8.7,<1.9',
    ],
    'reversion-django-1.9': [
        'django-reversion>=1.10,<1.11',
    ],
    'cms-2.x': [
        'django-mptt>=0.5.1,<0.5.3',
    ],
    'cms-3.0': [
        'django-mptt<0.8',
    ],
    'cms-3.1': [
        'django-treebeard>=2.0',
    ],
    'cms-3.2': [
        'django-treebeard>=2.0',
    ],
    'ckeditor-3.0': [
        'djangocms-admin-style<0.3',
        'djangocms-text-ckeditor<2.7.0',
    ],
    'ckeditor-3.1': [
        'djangocms-admin-style<1.0',
        'djangocms-text-ckeditor<2.8.0',
    ],
    'ckeditor-3.2': [
        'djangocms-admin-style>=1.0.6',
        'djangocms-text-ckeditor>=2.8.1',
    ],
    'ckeditor-3.3': [
        'djangocms-admin-style>=1.1.1',
        'https://github.com/divio/djangocms-text-ckeditor/archive/develop.zip'
    ],
    'plugins-common': [
        'djangocms-column',
        'djangocms-googlemap',
        'djangocms-inherit',
        'djangocms-style',
        'djangocms-link',
    ],
    'plugins-basic': [
        'djangocms-file',
        'djangocms-picture',
        'djangocms-teaser',
        'djangocms-video',
    ],
    'plugins-common-master': [
        'https://github.com/divio/djangocms-column/archive/master.zip?%(bust)s' % bust,
        'https://github.com/divio/djangocms-googlemap/archive/master.zip?%(bust)s' % bust,
        'https://github.com/divio/djangocms-inherit/archive/master.zip?%(bust)s' % bust,
        'https://github.com/divio/djangocms-link/archive/master.zip?%(bust)s' % bust,
        'https://github.com/divio/djangocms-style/archive/master.zip?%(bust)s' % bust,
    ],
    'plugins-basic-master': [
        'https://github.com/divio/djangocms-file/archive/master.zip?%(bust)s' % bust,
        'https://github.com/divio/djangocms-picture/archive/master.zip?%(bust)s' % bust,
        'https://github.com/divio/djangocms-teaser/archive/master.zip?%(bust)s' % bust,
        'https://github.com/divio/djangocms-video/archive/master.zip?%(bust)s' % bust,
    ],
    'aldryn': [
        'django-compressor',
    ],
    'filer': [
        'easy_thumbnails',
        'django-filer>=0.9.12',
        'cmsplugin-filer>=0.10.2',
    ],
    'filer-cms-2.x': [
        'easy_thumbnails',
        'django-filer<=0.9.6',
        'cmsplugin-filer',
    ],
    'apphooks-reload': [
        'aldryn-apphook-reload>=0.2.2'
    ]
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
    'django.db.backends.mysql': 'mysqlclient',
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
