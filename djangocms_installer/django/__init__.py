import glob
import os
import re
import shutil
import subprocess
import sys
import textwrap
from copy import copy, deepcopy
from distutils.version import LooseVersion
from shlex import quote as shlex_quote

from ..config import data, get_settings
from ..utils import chdir, format_val


def create_project(config_data):
    """
    Call django-admin to create the project structure

    :param config_data: configuration data
    """
    env = deepcopy(dict(os.environ))
    env["DJANGO_SETTINGS_MODULE"] = str("{}.settings".format(config_data.project_name))
    env["PYTHONPATH"] = str(os.pathsep.join(map(shlex_quote, sys.path)))
    kwargs = {}
    args = []
    if config_data.template:
        kwargs["template"] = config_data.template
    args.append(config_data.project_name)
    if config_data.project_directory:
        args.append(config_data.project_directory)
        if not os.path.exists(config_data.project_directory):
            os.makedirs(config_data.project_directory)
    base_cmd = "django-admin.py"
    start_cmds = [os.path.join(os.path.dirname(sys.executable), base_cmd)]
    start_cmd_pnodes = ["Scripts"]
    start_cmds.extend([os.path.join(os.path.dirname(sys.executable), pnode, base_cmd) for pnode in start_cmd_pnodes])
    start_cmd = [base_cmd]
    for p in start_cmds:
        if os.path.exists(p):
            start_cmd = [sys.executable, p]
            break
    cmd_args = start_cmd + ["startproject"] + args
    if config_data.verbose:
        sys.stdout.write("Project creation command: {}\n".format(" ".join(cmd_args)))
    try:
        output = subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
        sys.stdout.write(output.decode("utf-8"))
    except subprocess.CalledProcessError as e:  # pragma: no cover
        raise RuntimeError(e.output.decode("utf-8"))


def copy_files(config_data):
    """
    It's a little rude actually: it just overwrites the django-generated urls.py
    with a custom version and put other files in the project directory.

    :param config_data: configuration data
    """
    if config_data.i18n == "yes":
        urlconf_path = os.path.join(os.path.dirname(__file__), "../config/urls_i18n.py")
    else:
        urlconf_path = os.path.join(os.path.dirname(__file__), "../config/urls_noi18n.py")
    share_path = os.path.join(os.path.dirname(__file__), "../share")
    template_path = os.path.join(share_path, "templates")

    media_project = os.path.join(config_data.project_directory, "media")
    static_main = os.path.join(config_data.project_path, "static")
    static_project = os.path.join(config_data.project_directory, "static")
    template_target = os.path.join(config_data.project_path, "templates")
    if config_data.templates and os.path.isdir(config_data.templates):
        template_path = config_data.templates
    elif config_data.bootstrap:
        template_path = os.path.join(template_path, "bootstrap")
    else:
        template_path = os.path.join(template_path, "basic")

    shutil.copy(urlconf_path, config_data.urlconf_path)
    if media_project:
        os.makedirs(media_project)
    if static_main:
        os.makedirs(static_main)
    if not os.path.exists(static_project):
        os.makedirs(static_project)
    if not os.path.exists(template_target):
        os.makedirs(template_target)
    for filename in glob.glob(os.path.join(template_path, "*.html")):
        if os.path.isfile(filename):
            shutil.copy(filename, template_target)

    if config_data.noinput and not config_data.no_user:
        script_path = os.path.join(share_path, "create_user.py")
        if os.path.isfile(script_path):
            shutil.copy(script_path, os.path.join(config_data.project_path, ".."))

    if config_data.starting_page:
        for filename in glob.glob(os.path.join(share_path, "starting_page.*")):
            if os.path.isfile(filename):
                shutil.copy(filename, os.path.join(config_data.project_path, ".."))


def patch_settings(config_data):
    """
    Modify the settings file created by Django injecting the django CMS
    configuration

    :param config_data: configuration data
    """
    import django

    current_django_version = LooseVersion(django.__version__)
    declared_django_version = LooseVersion(config_data.django_version)

    if not os.path.exists(config_data.settings_path):  # pragma: no cover
        sys.stderr.write(
            "Error while creating target project, "
            "please check the given configuration: {}\n".format(config_data.settings_path)
        )
        return sys.exit(5)

    if current_django_version.version[:2] != declared_django_version.version[:2]:
        sys.stderr.write(
            "Currently installed Django version {} differs from the declared {}. "
            "Please check the given `--django-version` installer argument, your virtualenv "
            "configuration and any package forcing a different Django version"
            "\n".format(current_django_version, declared_django_version)
        )
        return sys.exit(9)

    overridden_settings = (
        "MIDDLEWARE_CLASSES",
        "MIDDLEWARE",
        "INSTALLED_APPS",
        "TEMPLATE_LOADERS",
        "TEMPLATE_CONTEXT_PROCESSORS",
        "TEMPLATE_DIRS",
        "LANGUAGES",
    )
    extra_settings = ""

    with open(config_data.settings_path) as fd_original:
        original = fd_original.read()

    # extra settings reading
    if config_data.extra_settings and os.path.exists(config_data.extra_settings):
        with open(config_data.extra_settings) as fd_extra:
            extra_settings = fd_extra.read()

    original = original.replace("# -*- coding: utf-8 -*-\n", "")

    DATA_DIR = "DATA_DIR = os.path.dirname(os.path.dirname(__file__))\n"  # noqa
    STATICFILES_DIR = "os.path.join(BASE_DIR, '{}', 'static'),".format(config_data.project_name)  # noqa

    original = data.DEFAULT_PROJECT_HEADER + DATA_DIR + original
    original += "MEDIA_URL = '/media/'\n"
    original += "MEDIA_ROOT = os.path.join(DATA_DIR, 'media')\n"
    original += "STATIC_ROOT = os.path.join(DATA_DIR, 'static')\n"
    original += """
STATICFILES_DIRS = (
    {}
)
""".format(
        STATICFILES_DIR
    )
    original = original.replace("# -*- coding: utf-8 -*-\n", "")

    # I18N
    if config_data.i18n == "no":
        original = original.replace("I18N = True", "I18N = False")
        original = original.replace("L10N = True", "L10N = False")

    # TZ
    if config_data.use_timezone == "no":
        original = original.replace("USE_TZ = True", "USE_TZ = False")

    if config_data.languages:
        original = original.replace(
            "LANGUAGE_CODE = 'en-us'",
            "LANGUAGE_CODE = '{}'".format(config_data.languages[0]),
        )
    if config_data.timezone:
        original = original.replace("TIME_ZONE = 'UTC'", "TIME_ZONE = '{}'".format(config_data.timezone))

    for item in overridden_settings:
        item_re = re.compile(r"{} = [^\]]+\]".format(item), re.DOTALL | re.MULTILINE)
        original = item_re.sub("", original)
    # TEMPLATES is special, so custom regexp needed
    item_re = re.compile(r"TEMPLATES = .+\},\n\s+\},\n]$", re.DOTALL | re.MULTILINE)
    original = item_re.sub("", original)
    # DATABASES is a dictionary, so different regexp needed
    item_re = re.compile(r"DATABASES = [^\}]+\}[^\}]+\}", re.DOTALL | re.MULTILINE)
    original = item_re.sub("", original)
    if original.find("SITE_ID") == -1:
        original += "SITE_ID = 1\n\n"

    original += _build_settings(config_data)
    # Append extra settings at the end of the file
    original += "\n" + extra_settings

    with open(config_data.settings_path, "w") as fd_dest:
        fd_dest.write(original)


def _build_settings(config_data):
    """
    Build the django CMS settings dictionary

    :param config_data: configuration data
    """
    spacer = "    "
    text = []
    settings_data = get_settings()

    settings_data.MIDDLEWARE_CLASSES.insert(0, settings_data.APPHOOK_RELOAD_MIDDLEWARE_CLASS)

    processors = settings_data.TEMPLATE_CONTEXT_PROCESSORS + settings_data.TEMPLATE_CONTEXT_PROCESSORS_3
    text.append(
        data.TEMPLATES_1_8.format(
            loaders=(",\n" + spacer * 4).join(
                [
                    "'{}'".format(var)
                    for var in settings_data.TEMPLATE_LOADERS
                    if (LooseVersion(config_data.django_version) < LooseVersion("2.0") or "eggs" not in var)
                ]
            ),
            processors=(",\n" + spacer * 4).join(["'{}'".format(var) for var in processors]),
            dirs="os.path.join(BASE_DIR, '{}', 'templates'),".format(config_data.project_name),
        )
    )

    text.append(
        "MIDDLEWARE = [\n{}{}\n]".format(
            spacer,
            (",\n" + spacer).join(["'{}'".format(var) for var in settings_data.MIDDLEWARE_CLASSES]),
        )
    )

    apps = list(settings_data.INSTALLED_APPS)
    apps = list(settings_data.CMS_3_HEAD) + apps
    apps.extend(settings_data.TREEBEARD_APPS)
    apps.extend(settings_data.CMS_3_APPLICATIONS)

    if not config_data.no_plugins:
        apps.extend(settings_data.FILER_PLUGINS_3)

    text.append(
        "INSTALLED_APPS = [\n{}{}\n]".format(
            spacer,
            (",\n" + spacer).join(["'{}'".format(var) for var in apps] + ["'{}'".format(config_data.project_name)]),
        )
    )

    text.append(
        "LANGUAGES = (\n{0}{1}\n{0}{2}\n)".format(
            spacer,
            "## Customize this",
            ("\n" + spacer).join(["('{0}', gettext('{0}')),".format(item) for item in config_data.languages]),  # NOQA
        )
    )

    cms_langs = deepcopy(settings_data.CMS_LANGUAGES)
    for lang in config_data.languages:
        lang_dict = {"code": lang, "name": lang}
        lang_dict.update(copy(cms_langs["default"]))
        cms_langs[1].append(lang_dict)
    cms_text = ["CMS_LANGUAGES = {"]
    cms_text.append("{}{}".format(spacer, "## Customize this"))
    for key, value in cms_langs.items():
        if key == "default":
            cms_text.append("{0}'{1}': {{".format(spacer, key))
            for config_name, config_value in value.items():
                cms_text.append("{}'{}': {},".format(spacer * 2, config_name, config_value))
            cms_text.append("{0}}},".format(spacer))
        else:
            cms_text.append("{}{}: [".format(spacer, key))
            for lang in value:
                cms_text.append("{0}{{".format(spacer * 2))
                for config_name, config_value in lang.items():
                    if config_name == "code":
                        cms_text.append("{}'{}': '{}',".format(spacer * 3, config_name, config_value))  # NOQA
                    elif config_name == "name":
                        cms_text.append("{}'{}': gettext('{}'),".format(spacer * 3, config_name, config_value))  # NOQA
                    else:
                        cms_text.append("{}'{}': {},".format(spacer * 3, config_name, config_value))
                cms_text.append("{0}}},".format(spacer * 2))
            cms_text.append("{}],".format(spacer))
    cms_text.append("}")

    text.append("\n".join(cms_text))

    if config_data.bootstrap:
        cms_templates = "CMS_TEMPLATES_BOOTSTRAP"
    else:
        cms_templates = "CMS_TEMPLATES"

    text.append(
        "CMS_TEMPLATES = (\n{0}{1}\n{0}{2}\n)".format(
            spacer,
            "## Customize this",
            (",\n" + spacer).join(["('{}', '{}')".format(*item) for item in getattr(settings_data, cms_templates)]),
        )
    )

    text.append("X_FRAME_OPTIONS = 'SAMEORIGIN'")
    text.append("CMS_PERMISSION = {}".format(settings_data.CMS_PERMISSION))
    text.append("CMS_PLACEHOLDER_CONF = {}".format(settings_data.CMS_PLACEHOLDER_CONF))

    database = [
        "'{}': {}".format(key, format_val(val))
        for key, val in sorted(config_data.db_parsed.items(), key=lambda x: x[0])
    ]  # NOQA
    text.append(
        textwrap.dedent(
            """
        DATABASES = {{
            'default': {{
                {0}
            }}
        }}"""
        )
        .strip()
        .format((",\n" + spacer * 2).join(database))
    )  # NOQA

    if config_data.filer:
        text.append(
            "THUMBNAIL_PROCESSORS = (\n{}{}\n)".format(
                spacer,
                (",\n" + spacer).join(["'{}'".format(var) for var in settings_data.THUMBNAIL_PROCESSORS]),
            )
        )
    return "\n\n".join(text)


def setup_database(config_data):
    """
    Run the migrate command to create the database schema

    :param config_data: configuration data
    """
    with chdir(config_data.project_directory):
        env = deepcopy(dict(os.environ))
        env["DJANGO_SETTINGS_MODULE"] = str("{}.settings".format(config_data.project_name))
        env["PYTHONPATH"] = str(os.pathsep.join(map(shlex_quote, sys.path)))
        commands = []

        commands.append([sys.executable, "-W", "ignore", "manage.py", "migrate"])

        if config_data.verbose:
            sys.stdout.write("Database setup commands: {}\n".format(", ".join([" ".join(cmd) for cmd in commands])))
        for command in commands:
            try:
                output = subprocess.check_output(command, env=env, stderr=subprocess.STDOUT)
                sys.stdout.write(output.decode("utf-8"))
            except subprocess.CalledProcessError as e:  # pragma: no cover
                if config_data.verbose:
                    sys.stdout.write(e.output.decode("utf-8"))
                raise

        if not config_data.no_user:
            sys.stdout.write("Creating admin user\n")
            if config_data.noinput:
                create_user(config_data)
            else:  # pragma: no cover
                subprocess.check_call(
                    " ".join([sys.executable, "-W", "ignore", "manage.py", "createsuperuser"]),
                    shell=True,
                    stderr=subprocess.STDOUT,
                )


def create_user(config_data):
    """
    Create admin user without user input

    :param config_data: configuration data
    """
    with chdir(os.path.abspath(config_data.project_directory)):
        env = deepcopy(dict(os.environ))
        env["DJANGO_SETTINGS_MODULE"] = str("{}.settings".format(config_data.project_name))
        env["PYTHONPATH"] = str(os.pathsep.join(map(shlex_quote, sys.path)))
        subprocess.check_call([sys.executable, "create_user.py"], env=env, stderr=subprocess.STDOUT)
        for ext in ["py", "pyc"]:
            try:
                os.remove("create_user.{}".format(ext))
            except OSError:
                pass


def load_starting_page(config_data):
    """
    Load starting page into the CMS

    :param config_data: configuration data
    """
    with chdir(os.path.abspath(config_data.project_directory)):
        env = deepcopy(dict(os.environ))
        env["DJANGO_SETTINGS_MODULE"] = str("{}.settings".format(config_data.project_name))
        env["PYTHONPATH"] = str(os.pathsep.join(map(shlex_quote, sys.path)))
        subprocess.check_call([sys.executable, "starting_page.py"], env=env, stderr=subprocess.STDOUT)
        for ext in ["py", "pyc", "json"]:
            try:
                os.remove("starting_page.{}".format(ext))
            except OSError:
                pass
