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
        requirements = install.parse(config_data)
        sys.exit(0)
        install.requirements(requirements)
        django.create_project(config)
        django.patch_settings(config)
        django.setup_database(config)
        config.write_default(config)
