TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
    "django.template.loaders.eggs.Loader",
)

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]


TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.template.context_processors.i18n",
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    "django.template.context_processors.media",
    "django.template.context_processors.csrf",
    "django.template.context_processors.tz",
    "sekizai.context_processors.sekizai",
    "django.template.context_processors.static",
]

TEMPLATE_CONTEXT_PROCESSORS_3 = [
    "cms.context_processors.cms_settings",
]

TEMPLATE_DIRS = ()

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "cms",
    "menus",
    "sekizai",
)

MPTT_APPS = ("mptt",)

TREEBEARD_APPS = ("treebeard",)

FILER_PLUGINS_3 = (
    "filer",
    "easy_thumbnails",
    "djangocms_bootstrap4",
    "djangocms_bootstrap4.contrib.bootstrap4_alerts",
    "djangocms_bootstrap4.contrib.bootstrap4_badge",
    "djangocms_bootstrap4.contrib.bootstrap4_card",
    "djangocms_bootstrap4.contrib.bootstrap4_carousel",
    "djangocms_bootstrap4.contrib.bootstrap4_collapse",
    "djangocms_bootstrap4.contrib.bootstrap4_content",
    "djangocms_bootstrap4.contrib.bootstrap4_grid",
    "djangocms_bootstrap4.contrib.bootstrap4_jumbotron",
    "djangocms_bootstrap4.contrib.bootstrap4_link",
    "djangocms_bootstrap4.contrib.bootstrap4_listgroup",
    "djangocms_bootstrap4.contrib.bootstrap4_media",
    "djangocms_bootstrap4.contrib.bootstrap4_picture",
    "djangocms_bootstrap4.contrib.bootstrap4_tabs",
    "djangocms_bootstrap4.contrib.bootstrap4_utilities",
    "djangocms_file",
    "djangocms_icon",
    "djangocms_link",
    "djangocms_picture",
    "djangocms_style",
    "djangocms_googlemap",
    "djangocms_video",
)

CMS_3_HEAD = ("djangocms_admin_style",)

CMS_3_APPLICATIONS = ("djangocms_text_ckeditor",)

REVERSION_APPLICATIONS = ("reversion",)
SOUTH_APPLICATIONS = ("south",)

CMS_TEMPLATES = (
    ("fullwidth.html", "Fullwidth"),
    ("sidebar_left.html", "Sidebar Left"),
    ("sidebar_right.html", "Sidebar Right"),
)

CMS_TEMPLATES_BOOTSTRAP = (
    ("page.html", "Page"),
    ("feature.html", "Page with Feature"),
)

LANGUAGES = ()

CMS_LANGUAGES = {
    1: [],
    "default": {"redirect_on_fallback": True, "public": True, "hide_untranslated": False},
}
CMS_PERMISSION = True
CMS_PLACEHOLDER_CONF = {}

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

URLCONF = {}

APPHOOK_RELOAD_MIDDLEWARE_CLASS = "cms.middleware.utils.ApphookReloadMiddleware"
