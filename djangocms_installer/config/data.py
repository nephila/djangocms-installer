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
DJANGOCMS_RC = 'https://github.com/divio/django-cms/archive/develop.zip?{bust}'.format(
    **bust
)
DJANGOCMS_BETA = DJANGOCMS_DEVELOP
DJANGOCMS_34 = 'django-cms>=3.4,<3.5'
DJANGOCMS_35 = 'django-cms>=3.5,<3.6'
DJANGOCMS_36 = 'django-cms>=3.6,<3.7'

if sys.version_info >= (3, 4):
    DJANGOCMS_SUPPORTED = ('3.4', '3.5', '3.6', 'stable', 'lts', 'develop')
    DJANGOCMS_STABLE = '3.6'
    DJANGOCMS_LTS = '3.4'
else:
    DJANGOCMS_SUPPORTED = ('3.4', '3.5', '3.6', 'stable', 'lts', 'develop')
    DJANGOCMS_STABLE = '3.6'
    DJANGOCMS_LTS = '3.4'
DJANGOCMS_DEFAULT = DJANGOCMS_STABLE

DJANGO_DEVELOP = 'https://github.com/django/django/archive/master.zip?{bust}'.format(**bust)
DJANGO_BETA = 'https://github.com/django/django/archive/master.zip?{bust}'.format(**bust)
if sys.version_info >= (3, 5):

    DJANGO_SUPPORTED = ('1.8', '1.9', '1.10', '1.11', '2.0', '2.1', 'stable', 'lts')
    DJANGO_STABLE = '1.11'
    DJANGO_LTS = '1.11'
elif sys.version_info >= (3, 4):
    DJANGO_SUPPORTED = ('1.8', '1.9', '1.10', '1.11', '2.0', 'stable', 'lts')
    DJANGO_STABLE = '1.11'
    DJANGO_LTS = '1.11'
else:
    DJANGO_SUPPORTED = ('1.8', '1.9', '1.10', '1.11', 'stable', 'lts')
    DJANGO_STABLE = '1.11'
    DJANGO_LTS = '1.11'
DJANGO_DEFAULT = DJANGO_STABLE

CMS_VERSION_MATRIX = {
    'stable': DJANGOCMS_STABLE,
    'lts': DJANGOCMS_LTS,
    'rc': '3.6',
    'beta': '3.6',
    'develop': '3.6',
}
DJANGO_VERSION_MATRIX = {
    'stable': DJANGO_STABLE,
    'lts': DJANGO_LTS,
    'rc': '1.11',
    'beta': '1.11',
    'develop': '1.11'
}
VERSION_MATRIX = {
    '3.4': ('1.8', '1.11'),
    '3.5': ('1.8', '1.11'),
    '3.6': ('1.11', '2.1'),
}
PACKAGE_MATRIX = {
    '3.4': DJANGOCMS_34,
    '3.5': DJANGOCMS_35,
    '3.6': DJANGOCMS_36,
}

REQUIREMENTS = {
    'default': [
        'django-classy-tags>=0.7',
        'html5lib>=1.0.1',
        'Pillow>=3.0',
        'django-sekizai>=0.9',
        'six',
        'pytz',
    ],
    'django-1.8': [
        'django-polymorphic<2.0',
        'django-mptt<0.9',
    ],
    'django-1.9': [
        'django-polymorphic<2.0',
        'django-mptt<0.9',
    ],
    'django-1.10': [
        'django-polymorphic<2.0',
        'django-mptt<0.9',
    ],
    'django-1.11': [
        'django-mptt>0.9',
    ],
    'django-2.0': [
        'django-mptt>0.9',
    ],
    'django-2.1': [
        'django-mptt>0.9',
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
    'reversion-django-1.11': [
        'django-reversion>=2.0,<2.1',
    ],
    'cms-3.4': [
        'djangocms-admin-style>=1.2,<1.3',
        'django-treebeard>=4.0,<5.0',
    ],
    'cms-3.5': [
        'djangocms-admin-style>=1.2,<1.3',
        'django-treebeard>=4.0,<5.0',
    ],
    'cms-3.6': [
        'djangocms-admin-style>=1.2,<1.3',
        'django-treebeard>=4.0,<5.0',
    ],
    'cms-master': [
        'https://github.com/divio/djangocms-admin-style/archive/master.zip?{bust}'.format(**bust),
        'django-treebeard>=4.0,<5.0',
    ],
    'plugins-3.4': [
        'djangocms-text-ckeditor>3.6,<3.7',
        'djangocms-link>=1.8,<2.2',
        'djangocms-style>=1.7,<2.1',
        'djangocms-googlemap>=0.5,<1.2',
        'djangocms-snippet>=1.9,<2.1',
        'djangocms-video>=2.0,<2.1',
        'djangocms-column>=1.6,<1.9',
        'djangocms-file>=2.0,<2.2',
        'djangocms-picture>=2.0,<2.1',
    ],
    'plugins-3.5': [
        'djangocms-text-ckeditor>3.6,<3.7',
        'djangocms-link>=2.1,<2.2',
        'djangocms-snippet>=2.1,<2.2',
        'djangocms-googlemap>=1.1,<1.2',
        'djangocms-snippet>=2.0,<2.1',
        'djangocms-video>=2.0,<2.1',
        'djangocms-column>=1.7,<1.9',
        'djangocms-file>=2.0,<2.2',
        'djangocms-picture>=2.0,<2.1',
    ],
    'plugins-3.6': [
        'djangocms-text-ckeditor>=3.7,<3.8',
        'djangocms-link>=2.3',
        'djangocms-style>=2.1',
        'djangocms-googlemap>=1.2',
        'djangocms-snippet>=2.1,<2.2',
        'djangocms-video>=2.0,<2.1',
        'djangocms-column>=1.9',
        'djangocms-file>=2.2,<3.0',
        'djangocms-picture>=2.0,<2.1',
    ],
    'plugins-master': [
        'https://github.com/divio/djangocms-text-ckeditor/archive/master.zip?{bust}'
        ''.format(**bust),
        'https://github.com/divio/djangocms-file/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-link/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-style/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-googlemap/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-snippet/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-picture/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-video/archive/master.zip?{bust}'.format(**bust),
        'https://github.com/divio/djangocms-column/archive/master.zip?{bust}'.format(**bust),
    ],
    'plugins-basic': [
    ],
    'plugins-basic-master': [
    ],
    'filer': [
        'easy_thumbnails',
        'django-filer>=1.3',
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
 * djangocms-file (File plugin)
 * djangocms-picture (Image plugin)
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
import os  # isort:skip
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
