# -*- coding: utf-8 -*-
import sys
import os
import re
import subprocess

from ..config import data


def create_project(config_data):
    try:
        if config_data.project_directory:
            if not os.path.exists(config_data.project_directory):
                os.makedirs(config_data.project_directory)
            subprocess.check_call(["django-admin.py", "startproject",
                                   config_data.project_name,
                                   config_data.project_directory])
        else:
            subprocess.check_call(["django-admin.py", "startproject",
                                   config_data.project_name])
        setattr(config_data, 'project_path',
                os.path.join(config_data.project_directory, config_data.project_name))
        setattr(config_data, 'settings_path',
                os.path.join(config_data.project_directory, config_data.project_name,
                             'settings.py'))
    except subprocess.CalledProcessError as message:
        raise EnvironmentError(message)


def patch_settings(config_data):
    print(config_data)
    with open(config_data.settings_path, 'r') as fd_original:
        original = fd_original.read()

    original = original.replace("# -*- coding: utf-8 -*-\n", "")
    original = data.DEFAULT_PROJECT_HEADER + original
    original = original.replace("MEDIA_URL = ''", "MEDIA_URL = '/media/'")
    original = original.replace("MEDIA_ROOT = ''", "MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')")
    original = original.replace("STATIC_ROOT = ''", "STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')")
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
        original = original.replace("TIME_ZONE = 'America/Chicago'", "TIME_ZONE = '%s'" % config_data.timezone)

    middleware = re.compile(r"^MIDDLEWARE_CLASSES[^\)]+\)", re.DOTALL | re.MULTILINE)
    original = middleware.sub('', original)

    installed = re.compile(r"^INSTALLED_APPS[^\)]+\)", re.DOTALL | re.MULTILINE)
    original = installed.sub('', original)

    with open("test.py", "w") as fd_dest:
        fd_dest.write(original)


def setup_database(config_data):
    pass
