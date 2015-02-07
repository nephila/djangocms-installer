# -*- coding: utf-8 -*-
import logging
import os
import six
import sys


from . import config, django, install


def execute():
    # Log info and above to console
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    config_data = config.parse(sys.argv[1:])
    try:
        if config_data.plugins:
            config.show_plugins()
        elif config_data.dump_reqs:
            config.show_requirements(config_data)
        else:
            sys.stdout.write("Creating the project\n"
                             "Please wait while I install dependencies\n")
            if not config_data.no_deps:
                if config_data.requirements_file:
                    install.requirements(config_data.requirements_file, True)
                else:
                    install.requirements(config_data.requirements)
            sys.stdout.write("Dependencies installed\n"
                             "Creating the project")
            install.check_install(config_data)
            django.create_project(config_data)
            django.patch_settings(config_data)
            django.copy_files(config_data)
            if not config_data.no_sync:
                django.setup_database(config_data)
            if config_data.starting_page:
                django.load_starting_page(config_data)
            if config_data.aldryn:
                sys.stdout.write("Project created!\n")
                sys.stdout.write("aldryn boilerplate requires action before "
                                 "you can actually run the project.\n"
                                 "See documentation at "
                                 "http://aldryn-boilerplate.readthedocs.org/"
                                 "for more information.\n")
            else:
                sys.stdout.write("All done!\n")
                sys.stdout.write("Get into '%s' directory and type "
                                 "'python manage.py runserver' to start your "
                                 "project\n" % os.path.abspath(config_data.project_directory))
    except Exception as e:
        # Clean up your own mess
        install.cleanup_directory(config_data)
        if six.PY3:
            tb = sys.exc_info()[2]
            raise EnvironmentError("%s\nDocumentation available at "
                                   "http://djangocms-installer.rtfd.org\n" % e).with_traceback(tb)
        else:
            raise
