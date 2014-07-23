# -*- coding: utf-8 -*-
CONFIGURABLE_OPTIONS = ['--db', '--cms-version', '--django-version', '--i18n',
                        '--reversion', '--languages', '--timezone', '--use-tz',
                        '--permissions', '--bootstrap', '--templates',
                        '--starting-page']

DJANGOCMS_DEVELOP = '-e git+https://github.com/divio/django-cms@develop#egg=django-cms'
DJANGOCMS_RC = 'https://github.com/divio/django-cms/archive/3.0c2.zip'
DJANGOCMS_BETA = 'https://github.com/divio/django-cms/archive/3.0.0.beta3.zip'
DJANGOCMS_LATEST = '3.0'

DJANGO_DEVELOP = 'https://github.com/django/django/archive/master.zip'
# this is not true, but it's the most recent version
# compatible with all the CMS versions
DJANGO_LATEST = '1.5'
DJANGO_LATEST_CMS_3 = '1.6'

DEFAULT_REQUIREMENTS = """
django-classy-tags>=0.3.4.1
south>=0.7.2
html5lib
Pillow>=2
django-sekizai>=0.7
six
"""

DJANGOCMS_2_REQUIREMENTS = """
django-mptt>=0.5.1,<0.5.3
"""

DJANGOCMS_3_REQUIREMENTS = """
django-mptt>=0.6
djangocms-text-ckeditor>=2.1.4
djangocms-admin-style
djangocms-column
djangocms-style
djangocms-flash
djangocms-googlemap
djangocms-inherit
"""

PLUGIN_REQUIREMENTS = """
djangocms-file
djangocms-link
djangocms-picture
djangocms-teaser
djangocms-video
"""

DJANGO_16_REVERSION = "django-reversion>=1.8"
DJANGO_15_REVERSION = "django-reversion>=1.7,<1.8"
DJANGO_14_REVERSION = "django-reversion<1.7"

FILER_REQUIREMENTS_CMS3 = """
easy_thumbnails
django-filer>=0.9.6
cmsplugin-filer>=0.9.9
"""
FILER_REQUIREMENTS_CMS2 = """
easy_thumbnails
django-filer<=0.9.6
cmsplugin_filer
"""

PLUGIN_LIST_TEXT = """
djangocms_installer will install and configure the following plugins:
 * djangocms-text-ckeditor (Text plugin)
 * djangocms-file (File plugin)
 * djangocms-flash (Flash plugin)
 * djangocms-googlemap (GoogleMap plugin)
 * djangocms-inherit (Inherit plugin)
 * djangocms-link (Link plugin)
 * djangocms-picture (Picture plugin)
 * djangocms-teaser (Teaser plugin)
 * djangocms-video (Video plugin)
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
"""
STATICFILES_DEFAULT = """STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)"""

BASE_DIR = """
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
"""
