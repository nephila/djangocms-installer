# -*- coding: utf-8 -*-
import sys
import logging


from . import config, install, django


def execute():
    # Log info and above to console
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    config_data = config.parse(sys.argv[1:])
    if config_data.plugins:
        config.show_plugins()
    else:
        if not config_data.no_deps:
            if config_data.requirements_file:
                install.requirements(config_data.requirements_file, True)
            else:
                install.requirements(config_data.requirements)
        install.check_install(config_data)
        django.create_project(config_data)
        django.patch_settings(config_data)
        django.copy_files(config_data)
        if not config_data.no_sync:
            django.setup_database(config_data)
        print("All done!")
        print("Get into '%s' directory and type 'python manage.py runserver' "
              "to start your project" % config_data.project_directory)
