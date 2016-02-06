# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import os
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
            sys.stdout.write('Creating the project\n'
                             'Please wait while I install dependencies\n')
            if not config_data.no_deps:
                if config_data.requirements_file:
                    install.requirements(
                        config_data.requirements_file, config_data.pip_options, True,
                        verbose=config_data.verbose
                    )
                else:
                    install.requirements(
                        config_data.requirements, config_data.pip_options,
                        verbose=config_data.verbose
                    )
            sys.stdout.write('Dependencies installed\nCreating the project\n')
            install.check_install(config_data)
            django.create_project(config_data)
            django.patch_settings(config_data)
            django.copy_files(config_data)
            if not config_data.no_sync:
                django.setup_database(config_data)
            if config_data.starting_page:
                django.load_starting_page(config_data)
            if not config_data.requirements_file:
                install.write_requirements(config_data)
            if config_data.aldryn:  # pragma: no cover
                sys.stdout.write('Project created!\n')
                sys.stdout.write('aldryn boilerplate requires action before '
                                 'you can actually run the project.\n'
                                 'See documentation at '
                                 'http://aldryn-boilerplate.readthedocs.org/'
                                 'for more information.\n')
            else:
                sys.stdout.write('All done!\n')
                sys.stdout.write(
                    'Get into "{0}" directory and type "python manage.py runserver" to start your '
                    'project\n'.format(os.path.abspath(config_data.project_directory))
                )
    except Exception:
        # Clean up your own mess
        install.cleanup_directory(config_data)
        doc_message = 'Check documentation at http://djangocms-installer.rtfd.org'
        exception_message = '\n\n{0}\n\n{1}\n\n{0}\n\n'.format('*' * len(doc_message), doc_message)
        sys.stdout.write(exception_message)
        raise
