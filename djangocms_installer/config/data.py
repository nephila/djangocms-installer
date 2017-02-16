# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys
import time

bust = {'bust': time.time()}

CONFIGURABLE_OPTIONS = ['--db', '--cms-version', '--django-version', '--i18n',
                        '--reversion', '--languages', '--timezone', '--use-tz',
                        '--permissions', '--bootstrap', '--templates',
                        '--starting-page']

DJANGOCMS_DEVELOP = 'https://github.com/divio/django-cms/archive/develop.zip?{bust}'.format(
    **bust
)
DJANGOCMS_RC = 'https://github.com/divio/django-cms/archive/release/3.4.x.zip?{bust}'.format(
    **bust
)
DJANGOCMS_BETA = 'https://github.com/divio/django-cms/archive/3.0.0.beta3.zip'

if sys.version_info >= (3, 5):
    DJANGOCMS_SUPPORTED = ('3.2', '3.3', '3.4', 'stable', 'lts', 'develop')
    DJANGOCMS_STABLE = '3.4'
    DJANGOCMS_LTS = '3.4'
else:
    DJANGOCMS_SUPPORTED = ('3.2', '3.3', '3.4', 'stable', 'lts', 'develop')
    DJANGOCMS_STABLE = '3.4'
    DJANGOCMS_LTS = '3.4'

DJANGO_DEVELOP = 'https://github.com/django/django/archive/master.zip?{bust}'.format(**bust)
DJANGO_BETA = 'https://github.com/django/django/archive/master.zip?{bust}'.format(**bust)
if sys.version_info >= (3, 5):
    DJANGO_SUPPORTED = ('1.8', '1.9', '1.10', 'stable', 'lts')
    DJANGO_STABLE = '1.10'
    DJANGO_LTS = '1.8'
elif sys.version_info >= (3, 4):
    DJANGO_SUPPORTED = ('1.8', '1.9', '1.10', 'stable', 'lts')
    DJANGO_STABLE = '1.10'
    DJANGO_LTS = '1.8'
elif sys.version_info >= (3, 3):
    DJANGO_SUPPORTED = ('1.8', 'stable', 'lts')
    DJANGO_STABLE = '1.8'
    DJANGO_LTS = '1.8'
else:
    DJANGO_SUPPORTED = ('1.8', '1.9', '1.10', 'stable', 'lts')
    DJANGO_STABLE = '1.10'
    DJANGO_LTS = '1.8'

CMS_VERSION_MATRIX = {
    'stable': DJANGOCMS_STABLE,
    'lts': DJANGOCMS_LTS,
    'rc': '3.5',
    'beta': '3.5',
    'develop': '3.5'
}
DJANGO_VERSION_MATRIX = {
    'stable': DJANGO_STABLE,
    'lts': DJANGO_LTS,
    'rc': '1.11',
    'beta': '1.11',
    'develop': '1.11'
}
VERSION_MATRIX = {
    '3.2': ('1.8', '1.9'),
    '3.3': ('1.8', '1.9'),
    '3.4': ('1.8', '1.10'),
    '3.5': ('1.8', '1.10'),
}

REQUIREMENTS = {
    'default': [
        'django-classy-tags>=0.7',
        'html5lib>=0.999999,<0.99999999',
        'Pillow>=3.0',
        'django-sekizai>=0.9',
        'six',
    ],
    'django-1.8': [
    ],
    'django-1.9': [
    ],
    'django-1.10': [
    ],
    'reversion-django-1.8': [
        'django-reversion>=1.10,<1.11',
    ],
    'reversion-django-1.9': [
        'django-reversion>=1.10,<2.0',
    ],
    'reversion-django-1.10': [
        'django-reversion>=2.0,<2.1',
    ],
    'cms-3.2': [
        'djangocms-admin-style>=1.1.1,<1.3',
        'django-treebeard>=4.0,<5.0',
    ],
    'cms-3.3': [
        'djangocms-admin-style>=1.2,<1.3',
        'django-treebeard>=4.0,<5.0',
    ],
    'cms-3.4': [
        'djangocms-admin-style>=1.2,<1.3',
        'django-treebeard>=4.0,<5.0',
    ],
    'cms-master': [
        'https://github.com/divio/djangocms-admin-style/archive/master.zip?{bust}'.format(**bust),
        'django-treebeard>=4.0,<5.0',
    ],
    'plugins-3.2': [
        'djangocms-text-ckeditor>=2.8.1,<3.0',
        'djangocms-link>=1.8,<2.0',
        'djangocms-style>=1.7,<2.0',
        'djangocms-googlemap>=0.5,<1.0',
        'djangocms-snippet>=1.9,<2.0',
        'djangocms-video>=1.1,<2.0',
        'djangocms-column>=1.6,<1.7',
    ],
    'plugins-3.3': [
        'djangocms-text-ckeditor>=3.2.1',
        'djangocms-link>=1.8',
        'djangocms-style>=1.7',
        'djangocms-googlemap>=0.5',
        'djangocms-snippet>=1.9',
        'djangocms-video>=2.0',
        'djangocms-column>=1.6',
    ],
    'plugins-3.4': [
        'djangocms-text-ckeditor>=3.2.1',
        'djangocms-link>=1.8',
        'djangocms-style>=1.7',
        'djangocms-googlemap>=0.5',
        'djangocms-snippet>=1.9',
        'djangocms-video>=2.0',
        'djangocms-column>=1.6',
    ],
    'plugins-master': [
        'https://github.com/divio/djangocms-text-ckeditor/archive/master.zip?{bust}'
        ''.format(**bust),
        'https://github.com/divio/djangocms-link/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-style/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-googlemap/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-snippet/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-video/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-column/archive/master.zip?{bust}'.format(**bust),
    ],
    'plugins-basic': [
        'djangocms-file>=1.0,<1.1',
        'djangocms-picture>=0.2.0,<0.3',
        'djangocms-teaser>=0.2.0,<0.3',
    ],
    'plugins-basic-master': [
        'https://github.com/divio/djangocms-file/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-picture/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-teaser/archive/master.zip?{bust}'.format(**bust),
    ],
    'filer': [
        'easy_thumbnails',
        'django-filer>=1.2',
        'cmsplugin-filer>=1.1',
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
djangocms installer will install and configure the following plugins:
 * djangocms-text-ckeditor (Text plugin)
 * djangocms-link (Link plugin)
 * cmsplugin_filer_file (File plugin, replaces djangocms-file)
 * cmsplugin_filer_folder (Folder plugin)
 * cmsplugin_filer_image (Image plugin, replaces djangocms-picture)
 * djangocms-style (Style plugin)
 * djangocms-snippet (Snippet plugin)
 * djangocms-googlemap (GoogleMap plugin)
 * djangocms-video (Video plugin)
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

VERSION_WARNING = '{0} version of {1} is not supported and it may not work as expected'
