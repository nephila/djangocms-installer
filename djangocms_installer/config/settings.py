# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

MIDDLEWARE_CLASSES_DJANGO_15 = [
    'django.middleware.transaction.TransactionMiddleware',
]


TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'sekizai.context_processors.sekizai',
    'django.core.context_processors.static',
]
TEMPLATE_CONTEXT_PROCESSORS_2 = [
    'cms.context_processors.media',
]
TEMPLATE_CONTEXT_PROCESSORS_3 = [
    'cms.context_processors.cms_settings',
]

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
)

MPTT_APPS = (
    'mptt',
)

TREEBEARD_APPS = (
    'treebeard',
)

STANDARD_PLUGINS_2 = (
    'cms.plugins.file',
    'cms.plugins.flash',
    'cms.plugins.googlemap',
    'cms.plugins.inherit',
    'cms.plugins.link',
    'cms.plugins.picture',
    'cms.plugins.teaser',
    'cms.plugins.text',
    'cms.plugins.twitter',
    'cms.plugins.video',
)
STANDARD_PLUGINS_3 = (
    'djangocms_file',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
)

FILER_PLUGINS_2 = (
    'filer',
    'easy_thumbnails',
    'cmsplugin_filer_image',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_utils',
    'cmsplugin_filer_video',
    'cms.plugins.flash',
    'cms.plugins.googlemap',
    'cms.plugins.inherit',
    'djangocms_link',
)

FILER_PLUGINS_3 = (
    'filer',
    'easy_thumbnails',
    'cmsplugin_filer_image',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_utils',
    'cmsplugin_filer_video',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
)

CMS_3_HEAD = (
    'djangocms_admin_style',
)

CMS_3_APPLICATIONS = (
    'djangocms_text_ckeditor',
    'djangocms_style',
    'djangocms_column',
)

CMS_2_APPLICATIONS = (
    'cms.plugins.text',
)

REVERSION_APPLICATIONS = (
    'reversion',
)
SOUTH_APPLICATIONS = (
    'south',
)

ALDRYN_APPLICATIONS = (
    'compressor',
)

CMS_TEMPLATES = (
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right')
)

CMS_TEMPLATES_BOOTSTRAP = (
    ('page.html', 'Page'),
    ('feature.html', 'Page with Feature'),
)

LANGUAGES = (
)

CMS_LANGUAGES = {
    1: [
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    }
}
CMS_PERMISSION = True
CMS_PLACEHOLDER_CONF = {}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

URLCONF = {

}

APPHOOK_RELOAD_APPLICATIONS = [
    'aldryn_apphook_reload'
]
APPHOOK_RELOAD_MIDDLEWARE_CLASS_OLD = 'aldryn_apphook_reload.middleware.ApphookReloadMiddleware'
APPHOOK_RELOAD_MIDDLEWARE_CLASS = 'cms.middleware.utils.ApphookReloadMiddleware'

MIGRATIONS_CHECK_MODULES = (
    'cms',
    'menus',
    'filer',
    'cmsplugin_filer_image',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_utils',
    'cmsplugin_filer_video',
    'djangocms_text_ckeditor',
    'djangocms_column',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_style',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
)
