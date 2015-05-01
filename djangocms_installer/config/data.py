# -*- coding: utf-8 -*-
from __future__ import print_function
import time

CONFIGURABLE_OPTIONS = ['--db', '--cms-version', '--django-version', '--i18n',
                        '--reversion', '--languages', '--timezone', '--use-tz',
                        '--permissions', '--bootstrap', '--templates',
                        '--starting-page']

DJANGOCMS_DEVELOP = 'https://github.com/divio/django-cms/archive/develop.zip?%s' % time.time()  ## to avoid getting this from caches or mirrors
DJANGOCMS_RC = 'https://github.com/divio/django-cms/archive/3.0c2.zip'
DJANGOCMS_BETA = 'https://github.com/divio/django-cms/archive/3.0.0.beta3.zip'
DJANGOCMS_SUPPORTED = ('2.4', '3.0', '3.1', 'stable', 'develop')

DJANGO_DEVELOP = 'https://github.com/django/django/archive/master.zip?%s' % time.time()  ## to avoid getting this from caches or mirrors
DJANGO_SUPPORTED = ('1.4', '1.5', '1.6', '1.7', 'stable')

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


DEFAULT_REQUIREMENTS = """
django-classy-tags>=0.3.4.1
html5lib
Pillow<=2.8
django-sekizai>=0.7
six
"""

DJANGO_16_REQUIREMENTS = """
south>=1.0.0
"""

DJANGOCMS_2_REQUIREMENTS = """
django-mptt>=0.5.1,<0.5.3
"""

DJANGOCMS_3_REQUIREMENTS = """
django-mptt<0.7
"""
DJANGOCMS_3_1_REQUIREMENTS = """
django-treebeard>=2.0
"""

PLUGINS_REQUIREMENTS_BASIC = """
djangocms-admin-style
djangocms-column
djangocms-flash
djangocms-googlemap
djangocms-inherit
djangocms-style
djangocms-text-ckeditor>=2.3.0
"""

PLUGINS_REQUIREMENTS_NON_FILER = """
djangocms-file
djangocms-link
djangocms-picture
djangocms-teaser
djangocms-video
"""

PLUGINS_REQUIREMENTS_BASIC_DJANGO_17 = """
https://github.com/divio/djangocms-admin-style/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-column/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-flash/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-googlemap/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-inherit/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-style/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-text-ckeditor/archive/master.zip?%(bust)s
""" % {'bust': time.time()}

PLUGINS_REQUIREMENTS_NON_FILER_DJANGO_17 = """
https://github.com/divio/djangocms-file/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-link/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-picture/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-teaser/archive/master.zip?%(bust)s
https://github.com/divio/djangocms-video/archive/master.zip?%(bust)s
""" % {'bust': time.time()}


DJANGO_17_REVERSION = "django-reversion>=1.8.2,<1.8.6"
ALDRYN_REQUIREMENTS = """
django-compressor
"""
DJANGO_16_REVERSION = "django-reversion>=1.8,<1.8.6"
DJANGO_15_REVERSION = "django-reversion>=1.7,<1.8"
DJANGO_14_REVERSION = "django-reversion<1.7"

FILER_REQUIREMENTS_CMS3 = """
easy_thumbnails
https://github.com/stefanfoulis/django-filer/archive/develop.zip
cmsplugin-filer>=0.9.9
"""
FILER_REQUIREMENTS_CMS2 = """
easy_thumbnails
django-filer<=0.9.6
cmsplugin_filer
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
