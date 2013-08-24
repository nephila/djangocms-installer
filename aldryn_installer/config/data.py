# -*- coding: utf-8 -*-
CONFIGURABLE_OPTIONS = ['--db', '--cms-version', '--django-version', '--i18n',
                        '--south']

DEFAULT_REQUIREMENTS = """
django-classy-tags>=0.3.4.1
south>=0.7.2
html5lib
django-mptt>=0.5.1,<0.5.3
django-sekizai>=0.7
djangocms-admin-style
djangocms-text-ckeditor>=2.0
-e git+git://github.com/KristianOellegaard/django-hvad.git#egg=hvad
-e git+git://github.com/divio/djangocms-column.git#egg=djangocms-column
-e git+git://github.com/divio/djangocms-style.git#egg=djangocms-style
"""

FILER_REQUIREMENTS = """
easy_thumbnails
django-filer
cmsplugin_filer
"""

PLUGIN_LIST_TEXT = """
aldryn_installer will install and configure the following plugins:
 * djangocms-text-ckeditor (Text plugin)
 * cms.plugins.file (File plugin)
 * cms.plugins.flash (Flash plugin)
 * cms.plugins.googlemap (GoogleMap plugin)
 * cms.plugins.inherit (Inherit plugin)
 * cms.plugins.link (Link plugin)
 * cms.plugins.picture (Picture plugin)
 * cms.plugins.teaser (Teaser plugin)
 * cms.plugins.video (Video plugin)
 * djangocms-style (Style plugin)
                     
It will optionally install cmsplugin-filer plugins (if requested during
configuration):
 * cmsplugin_filer_file (File plugin, replaces cms.plugins.file)
 * cmsplugin_filer_folder (Folder plugin)
 * cmsplugin_filer_image (Image plugin, replaces cms.plugins.picture)
 * cmsplugin_filer_link (Link plugin, replaces cms.plugins.link)
 * cmsplugin_filer_teaser (Teaser plugin, replaces cms.plugins.teaser)
 * cmsplugin_filer_video (Video plugin, replaces cms.plugins.video)
"""