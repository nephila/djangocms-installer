# -*- coding: utf-8 -*-
from __future__ import print_function
from copy import copy, deepcopy
import glob
import os
import re
import requests
try:
    from shlex import quote as shlex_quote
except ImportError:
    from pipes import quote as shlex_quote
import shutil
import subprocess
import sys
import tempfile
import zipfile
from six import BytesIO


from ..compat import iteritems
from ..utils import chdir
from ..config import data, get_settings


def create_project(config_data):
    """
    Call django-admin to create the project structure
    """

    env = deepcopy(dict(os.environ))
    env['DJANGO_SETTINGS_MODULE'] = (
        '{0}.settings'.format(config_data.project_name))
    env['PYTHONPATH'] = os.pathsep.join(map(shlex_quote, sys.path))
    kwargs = {}
    args = []
    if config_data.template:
        kwargs['template'] = config_data.template
    args.append(config_data.project_name)
    if config_data.project_directory:
        args.append(config_data.project_directory)
        if not os.path.exists(config_data.project_directory):
            os.makedirs(config_data.project_directory)
    subprocess.check_call(' '.join([sys.executable, os.path.join(os.path.dirname(sys.executable), 'django-admin.py'), 'startproject'] + args),
                          shell=True)



def copy_files(config_data):
    """
    It's a little rude actually: it just overwrites the django-generated urls.py
    with a custom version and put other files in the project directory.
    """
    urlconf_path = os.path.join(os.path.dirname(__file__), '../config/urls.py')
    share_path = os.path.join(os.path.dirname(__file__), '../share')
    template_path = os.path.join(share_path, 'templates')
    if config_data.aldryn:
        media_project = os.path.join(config_data.project_directory, 'dist', 'media')
        static_main = False
        static_project = os.path.join(config_data.project_directory, 'dist', 'static')
        template_target = os.path.join(config_data.project_directory, 'templates')
        tmpdir = tempfile.mkdtemp()
        aldrynzip = requests.get(data.ALDRYN_BOILERPLATE)
        zip_open = zipfile.ZipFile(BytesIO(aldrynzip.content))
        zip_open.extractall(path=tmpdir)
        for component in os.listdir(os.path.join(tmpdir, 'aldryn-boilerplate-standard-master')):
            src = os.path.join(tmpdir, 'aldryn-boilerplate-standard-master', component)
            dst = os.path.join(config_data.project_directory, component)
            if os.path.isfile(src):
                shutil.copy(src, dst)
            else:
                shutil.copytree(src, dst)
        shutil.rmtree(tmpdir)
    else:
        media_project = os.path.join(config_data.project_directory, 'media')
        static_main = os.path.join(config_data.project_path, 'static')
        static_project = os.path.join(config_data.project_directory, 'static')
        template_target = os.path.join(config_data.project_path, 'templates')
        if config_data.templates and os.path.isdir(config_data.templates):
            template_path = config_data.templates
        elif config_data.bootstrap:
            template_path = os.path.join(template_path, 'bootstrap')
        else:
            template_path = os.path.join(template_path, 'basic')

    shutil.copy(urlconf_path, config_data.urlconf_path)
    if media_project:
        os.makedirs(media_project)
    if static_main:
        os.makedirs(static_main)
    if not os.path.exists(static_project):
        os.makedirs(static_project)
    if not os.path.exists(template_target):
        os.makedirs(template_target)
    for filename in glob.glob(os.path.join(template_path, '*.html')):
        if os.path.isfile(filename):
            shutil.copy(filename, template_target)

    if config_data.starting_page:
        for filename in glob.glob(os.path.join(share_path, 'starting_page.*')):
            if os.path.isfile(filename):
                shutil.copy(filename, os.path.join(config_data.project_path, '..'))


def patch_settings(config_data):
    """
    Modify the settings file created by Django injecting the django CMS
    configuration
    """
    overridden_settings = ('MIDDLEWARE_CLASSES', 'INSTALLED_APPS',
                           'TEMPLATE_LOADERS', 'TEMPLATE_CONTEXT_PROCESSORS',
                           'TEMPLATE_DIRS', 'LANGUAGES')
    extra_settings = ''

    if not os.path.exists(config_data.settings_path):
        sys.stdout.write("Error while creating target project, please check the given configuration: %s" % config_data.settings_path)
        return sys.exit(5)

    with open(config_data.settings_path, 'r') as fd_original:
        original = fd_original.read()

    # extra settings reading
    if config_data.extra_settings and os.path.exists(config_data.extra_settings):
        with open(config_data.extra_settings, 'r') as fd_extra:
            extra_settings = fd_extra.read()

    original = original.replace("# -*- coding: utf-8 -*-\n", "")

    if config_data.aldryn:
        DATA_DIR = "DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')\n"
        STATICFILES_DIR = 'os.path.join(BASE_DIR, \'static\'),'
    else:
        DATA_DIR = "DATA_DIR = os.path.dirname(os.path.dirname(__file__))\n"
        STATICFILES_DIR = 'os.path.join(BASE_DIR, \'%s\', \'static\'),' % config_data.project_name

    if original.find('BASE_DIR') == -1:
        original = data.DEFAULT_PROJECT_HEADER + data.BASE_DIR + DATA_DIR + original
    else:
        original = data.DEFAULT_PROJECT_HEADER + DATA_DIR + original
    if original.find('MEDIA_URL') > -1:
        original = original.replace("MEDIA_URL = ''", "MEDIA_URL = '/media/'")
    else:
        original += "MEDIA_URL = '/media/'\n"
    if original.find('MEDIA_ROOT') > -1:
        original = original.replace("MEDIA_ROOT = ''", "MEDIA_ROOT = os.path.join(DATA_DIR, 'media')")
    else:
        original += "MEDIA_ROOT = os.path.join(DATA_DIR, 'media')\n"
    if original.find('STATIC_ROOT') > -1:
        original = original.replace("STATIC_ROOT = ''", "STATIC_ROOT = os.path.join(DATA_DIR, 'static')")
    else:
        original += "STATIC_ROOT = os.path.join(DATA_DIR, 'static')\n"
    if original.find('STATICFILES_DIRS') > -1:
        original = original.replace(data.STATICFILES_DEFAULT, """
STATICFILES_DIRS = (
    %s
)
""" % STATICFILES_DIR)
    else:
        original += """
STATICFILES_DIRS = (
    %s
)
""" % STATICFILES_DIR
    original = original.replace("# -*- coding: utf-8 -*-\n", "")

    # I18N
    if config_data.i18n == 'no':
        original = original.replace("I18N = True", "I18N = False")
        original = original.replace("L10N = True", "L10N = False")

    # TZ
    if config_data.use_timezone == 'no':
        original = original.replace("USE_TZ = True", "USE_TZ = False")

    if config_data.languages:
        original = original.replace("LANGUAGE_CODE = 'en-us'", "LANGUAGE_CODE = '%s'" % config_data.languages[0])
    if config_data.timezone:
        # This is for Django 1.6 which changed the default timezone
        original = original.replace("TIME_ZONE = 'UTC'", "TIME_ZONE = '%s'" % config_data.timezone)
        # This is for older django versions
        original = original.replace("TIME_ZONE = 'America/Chicago'", "TIME_ZONE = '%s'" % config_data.timezone)

    for item in overridden_settings:
        item_re = re.compile(r"%s = [^\)]+\)" % item, re.DOTALL | re.MULTILINE)
        original = item_re.sub('', original)
    # DATABASES is a dictionary, so different regexp needed
    item_re = re.compile(r"DATABASES = [^\}]+\}[^\}]+\}", re.DOTALL | re.MULTILINE)
    original = item_re.sub('', original)
    if original.find('SITE_ID') == -1:
        original += "SITE_ID = 1\n\n"

    original += _build_settings(config_data)
    # Append extra settings at the end of the file
    original += ("\n" + extra_settings)

    with open(config_data.settings_path, "w") as fd_dest:
        fd_dest.write(original)


def _build_settings(config_data):
    """
    Build the django CMS settings dictionary
    """
    spacer = "    "
    text = []
    vars = get_settings()

    if config_data.django_version < 1.6:
        vars.MIDDLEWARE_CLASSES.extend(vars.MIDDLEWARE_CLASSES_DJANGO_15)

    text.append("TEMPLATE_LOADERS = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in vars.TEMPLATE_LOADERS])))

    text.append("MIDDLEWARE_CLASSES = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in vars.MIDDLEWARE_CLASSES])))

    if config_data.cms_version < 3:
        processors = vars.TEMPLATE_CONTEXT_PROCESSORS + vars.TEMPLATE_CONTEXT_PROCESSORS_2
    else:
        processors = vars.TEMPLATE_CONTEXT_PROCESSORS + vars.TEMPLATE_CONTEXT_PROCESSORS_3
    text.append("TEMPLATE_CONTEXT_PROCESSORS = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in processors])))

    if config_data.aldryn:
        text.append("TEMPLATE_DIRS = (\n%s%s\n)" % (
            spacer, "os.path.join(BASE_DIR, 'templates'),"))
    else:
        text.append("TEMPLATE_DIRS = (\n%s%s\n)" % (
            spacer, "os.path.join(BASE_DIR, '%s', 'templates')," % config_data.project_name))

    apps = list(vars.INSTALLED_APPS)
    if config_data.cms_version == 2.4:
        apps.extend(vars.CMS_2_APPLICATIONS)
        apps.extend(vars.MPTT_APPS)
        MIGRATION_MODULES = ()
    elif config_data.cms_version == 3.0:
        apps = list(vars.CMS_3_HEAD) + apps
        apps.extend(vars.MPTT_APPS)
        apps.extend(vars.CMS_3_APPLICATIONS)
        if config_data.filer:
            MIGRATION_MODULES = vars.MIGRATION_MODULES_BASE_FILER
        else:
            MIGRATION_MODULES = vars.MIGRATION_MODULES_BASE
    else:
        apps = list(vars.CMS_3_HEAD) + apps
        apps.extend(vars.TREEBEARD_APPS)
        apps.extend(vars.CMS_3_APPLICATIONS)
        if config_data.filer:
            MIGRATION_MODULES = vars.MIGRATION_MODULES_3_1_FILER
        else:
            MIGRATION_MODULES = vars.MIGRATION_MODULES_3_1

    if config_data.cms_version == 2.4:
        if config_data.filer:
            apps.extend(vars.FILER_PLUGINS_2)
        else:
            apps.extend(vars.STANDARD_PLUGINS_2)
    else:
        if config_data.filer:
            apps.extend(vars.FILER_PLUGINS_3)
        else:
            apps.extend(vars.STANDARD_PLUGINS_3)
    if config_data.django_version <= 1.6:
        apps.extend(vars.SOUTH_APPLICATIONS)

    if config_data.aldryn:
        apps.extend(vars.ALDRYN_APPLICATIONS)
    if config_data.reversion:
        apps.extend(vars.REVERSION_APPLICATIONS)
    text.append("INSTALLED_APPS = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in apps] + ["'%s'" % config_data.project_name])))

    text.append("LANGUAGES = (\n%s%s\n%s%s\n)" % (
        spacer, "## Customize this",
        spacer, ("\n" + spacer).join(["('%s', gettext('%s'))," % (item, item) for item in config_data.languages])))

    cms_langs = deepcopy(vars.CMS_LANGUAGES)
    for lang in config_data.languages:
        lang_dict = {'code': lang, 'name': lang}
        lang_dict.update(copy(cms_langs['default']))
        cms_langs[1].append(lang_dict)
    cms_text = ["CMS_LANGUAGES = {"]
    cms_text.append("%s%s" % (spacer, "## Customize this",))
    for key, value in iteritems(cms_langs):
        if key == 'default':
            cms_text.append("%s'%s': {" % (spacer, key))
            for config_name, config_value in iteritems(value):
                cms_text.append("%s'%s': %s," % (spacer * 2, config_name, config_value))
            cms_text.append("%s}," % spacer)
        else:
            cms_text.append("%s%s: [" % (spacer, key))
            for lang in value:
                cms_text.append("%s{" % (spacer * 2))
                for config_name, config_value in iteritems(lang):
                    if config_name == 'code':
                        cms_text.append("%s'%s': '%s'," % (spacer * 3, config_name, config_value))
                    elif config_name == 'name':
                        cms_text.append("%s'%s': gettext('%s')," % (spacer * 3, config_name, config_value))
                    else:
                        cms_text.append("%s'%s': %s," % (spacer * 3, config_name, config_value))
                cms_text.append("%s}," % (spacer * 2))
            cms_text.append("%s]," % spacer)
    cms_text.append("}")

    text.append("\n".join(cms_text))

    if config_data.bootstrap:
        cms_templates = 'CMS_TEMPLATES_BOOTSTRAP'
    else:
        cms_templates = 'CMS_TEMPLATES'

    text.append("CMS_TEMPLATES = (\n%s%s\n%s%s\n)" % (
        spacer, "## Customize this",
        spacer, (",\n" + spacer).join(["('%s', '%s')" % item for item in getattr(vars, cms_templates)])))

    text.append("CMS_PERMISSION = %s" % vars.CMS_PERMISSION)
    text.append("CMS_PLACEHOLDER_CONF = %s" % vars.CMS_PLACEHOLDER_CONF)

    text.append("DATABASES = {\n%s'default':\n%s%s\n}" % (spacer, spacer * 2, config_data.db_parsed))

    if config_data.django_version >= 1.7:
        text.append("MIGRATION_MODULES = {\n%s%s\n}" % (
            spacer, (",\n" + spacer).join(["'%s': '%s'" % item for item in MIGRATION_MODULES])))

    if config_data.filer:
        text.append("THUMBNAIL_PROCESSORS = (\n%s%s\n)" % (
            spacer, (",\n" + spacer).join(["'%s'" % var for var in vars.THUMBNAIL_PROCESSORS])))
        if config_data.django_version <= 1.6:
            text.append("SOUTH_MIGRATION_MODULES = {\n%s%s\n}" % (
                spacer, (",\n" + spacer).join(["'%s': '%s'" % item for item in vars.SOUTH_MIGRATION_MODULES])))
    return "\n\n".join(text)


def setup_database(config_data):
    with chdir(config_data.project_directory):
        env = deepcopy(dict(os.environ))
        env['DJANGO_SETTINGS_MODULE'] = (
            '{0}.settings'.format(config_data.project_name))
        env['PYTHONPATH'] = os.pathsep.join(map(shlex_quote, sys.path))

        if config_data.django_version < 1.7:
            try:
                import south  # NOQA
                subprocess.check_call([sys.executable, "-W", "ignore",
                                       "manage.py", "syncdb", "--all",
                                       "--noinput"], env=env)
                subprocess.check_call([sys.executable, "-W", "ignore",
                                       "manage.py", "migrate", "--fake"],
                                      env=env)
            except ImportError:
                subprocess.check_call([sys.executable, "-W", "ignore",
                                       "manage.py", "syncdb", "--noinput"],
                                      env=env)
                print("south not installed, migrations skipped")
        else:
            subprocess.check_call([sys.executable, "-W", "ignore",
                                  "manage.py", "migrate", "--noinput"],
                                  env=env)
        if not config_data.no_user and not config_data.noinput:
            print("\n\nCreating admin user")
            subprocess.check_call([sys.executable, "-W", "ignore",
                                   "manage.py", "createsuperuser"],
                                  env=env)


def load_starting_page(config_data):
    """
    Load starting page into the CMS
    """
    with chdir(config_data.project_directory):
        env = deepcopy(dict(os.environ))
        env['DJANGO_SETTINGS_MODULE'] = (
            '{0}.settings'.format(config_data.project_name))
        env['PYTHONPATH'] = os.pathsep.join(map(shlex_quote, sys.path))
        subprocess.check_call([sys.executable, "starting_page.py"],
                              env=env)
        for ext in ['py', 'pyc', 'json']:
            try:
                os.remove('starting_page.%s' % ext)
            except OSError:
                pass
