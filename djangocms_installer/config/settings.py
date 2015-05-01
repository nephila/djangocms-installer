# -*- coding: utf-8 -*-
from __future__ import print_function
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
    'django.middleware.doc.XViewMiddleware',
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
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    'django.core.context_processors.csrf',
    "django.core.context_processors.tz",
    "sekizai.context_processors.sekizai",
    "django.core.context_processors.static",
]
TEMPLATE_CONTEXT_PROCESSORS_2 = [
    "cms.context_processors.media",
]
TEMPLATE_CONTEXT_PROCESSORS_3 = [
    "cms.context_processors.cms_settings",
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
    'djangocms_flash',
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
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
)

CMS_3_HEAD = (
    'djangocms_admin_style',
    'djangocms_text_ckeditor',
)

CMS_3_APPLICATIONS = (
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

SOUTH_MIGRATION_MODULES = (
    ('easy_thumbnails', 'easy_thumbnails.south_migrations'),
    ('djangocms_text_ckeditor', 'djangocms_text_ckeditor.south_migrations'),
)

MIGRATION_MODULES_COMMON = (
    ('djangocms_column', 'djangocms_column.migrations_django'),
    ('djangocms_flash', 'djangocms_flash.migrations_django'),
    ('djangocms_googlemap', 'djangocms_googlemap.migrations_django'),
    ('djangocms_inherit', 'djangocms_inherit.migrations_django'),
    ('djangocms_link', 'djangocms_link.migrations_django'),
    ('djangocms_style', 'djangocms_style.migrations_django'),
)

MIGRATION_MODULES_STANDARD = (
    ('djangocms_file', 'djangocms_file.migrations_django'),
    ('djangocms_picture', 'djangocms_picture.migrations_django'),
    ('djangocms_teaser', 'djangocms_teaser.migrations_django'),
    ('djangocms_video', 'djangocms_video.migrations_django'),
)

MIGRATION_MODULES_FILER = (
    ('filer', 'filer.migrations_django'),
    ('cmsplugin_filer_image', 'cmsplugin_filer_image.migrations_django'),
    ('cmsplugin_filer_file', 'cmsplugin_filer_file.migrations_django'),
    ('cmsplugin_filer_folder', 'cmsplugin_filer_folder.migrations_django'),
    ('cmsplugin_filer_teaser', 'cmsplugin_filer_teaser.migrations_django'),
    ('cmsplugin_filer_utils', 'cmsplugin_filer_utils.migrations_django'),
    ('cmsplugin_filer_video', 'cmsplugin_filer_video.migrations_django'),
)

MIGRATION_MODULES_BASE = (
    ('cms', 'cms.migrations_django'),
    ('menus', 'menus.migrations_django'),
) + MIGRATION_MODULES_COMMON + MIGRATION_MODULES_STANDARD

MIGRATION_MODULES_BASE_FILER = (
    ('cms', 'cms.migrations_django'),
    ('menus', 'menus.migrations_django'),
) + MIGRATION_MODULES_COMMON + MIGRATION_MODULES_FILER

MIGRATION_MODULES_3_1 = MIGRATION_MODULES_COMMON + MIGRATION_MODULES_STANDARD

MIGRATION_MODULES_3_1_FILER = MIGRATION_MODULES_COMMON + MIGRATION_MODULES_FILER