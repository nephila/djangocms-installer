# -*- coding: utf-8 -*-
import six

CONFIGURABLE_OPTIONS = ['--db', '--cms-version', '--django-version', '--i18n',
                        '--reversion', '--languages', '--timezone', '--use-tz',
                        '--permissions', '--bootstrap', '--starting-page']

DJANGOCMS_DEVELOP = 'https://github.com/divio/django-cms/archive/develop.zip'
DJANGOCMS_BETA = 'https://github.com/divio/django-cms/archive/042f4953f6d2db66fd15e4cb748ab4b279f57947.zip'
DJANGOCMS_LATEST = '2.4'

DJANGO_DEVELOP = 'https://github.com/django/django/archive/master.zip'
DJANGO_LATEST = '1.5'  # this is not true, but it's the most recent version
                       # compatible with all the CMS versions

DEFAULT_REQUIREMENTS = """
django-classy-tags>=0.3.4.1
south>=0.7.2
html5lib
Pillow>=2
django-sekizai>=0.7
"""

DJANGOCMS_2_REQUIREMENTS = """
django-mptt>=0.5.1,<0.5.3
"""

DJANGOCMS_3_REQUIREMENTS = """
django-mptt>=0.6
djangocms-text-ckeditor>=2.0.5
djangocms-admin-style
git+https://github.com/divio/djangocms-column.git#egg=djangocms-column
git+https://github.com/divio/djangocms-style.git#egg=djangocms-style
"""

DJANGO_16_REVERSION = "django-reversion>=1.8"
DJANGO_15_REVERSION = "django-reversion>=1.7,<1.8"
DJANGO_14_REVERSION = "django-reversion<1.7"

FILER_REQUIREMENTS_CMS3 = """
easy_thumbnails
https://github.com/stefanfoulis/django-filer/archive/develop.zip
https://github.com/stefanfoulis/cmsplugin_filer/archive/develop.zip
"""
FILER_REQUIREMENTS_CMS2 = """
easy_thumbnails
django-filer
cmsplugin_filer
"""

PLUGIN_LIST_TEXT = """
djangocms_installer will install and configure the following plugins:
 * djangocms-text-ckeditor (Text plugin)
 * cms.plugins.file (File plugin)
 * cms.plugins.flash (Flash plugin)
 * cms.plugins.googlemap (GoogleMap plugin)
 * cms.plugins.inherit (Inherit plugin)
 * cms.plugins.link (Link plugin)
 * cms.plugins.picture (Picture plugin)
 * cms.plugins.teaser (Teaser plugin)
 * cms.plugins.video (Video plugin)
 * djangocms_style (Style plugin)
 * djangocms_column (Style plugin)
                     
It will optionally install cmsplugin-filer plugins (if requested during
configuration):
 * cmsplugin_filer_file (File plugin, replaces cms.plugins.file)
 * cmsplugin_filer_folder (Folder plugin)
 * cmsplugin_filer_image (Image plugin, replaces cms.plugins.picture)
 * cmsplugin_filer_link (Link plugin, replaces cms.plugins.link)
 * cmsplugin_filer_teaser (Teaser plugin, replaces cms.plugins.teaser)
 * cmsplugin_filer_video (Video plugin, replaces cms.plugins.video)
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
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
"""
