# -*- coding: utf-8 -*-
import sys
import argparse

import dj_database_url

from .. import compat, utils
from . import data


def parse(args):
    """
    Define the available arguments
    """
    parser = argparse.ArgumentParser(description='Bootstrap a django CMS project.')
    parser.add_argument('--db', '-d', dest='db', action='store',
                        help='Database configuration (in URL format)')
    parser.add_argument('--south', '-s', dest='south', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='install south in the environment')
    parser.add_argument('--i18n', '-i', dest='i18n', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='activate Django I18N / L10N setting')
    parser.add_argument('--django-version', dest='django_version', action='store',
                        choices=('1.4', '1.5', 'latest', 'beta'),
                        default='latest', help='Django version')
    parser.add_argument('--cms-version', '-v', dest='cms_version', action='store',
                        choices=('2.4', '2.3', 'beta', 'latest', 'develop'),
                        default='latest', help='django CMS version')
    parser.add_argument(dest='project_name', action='store',
                        help='name of the project to be created')

    # Command that lists the supported plugins in verbose description
    parser.add_argument('--list-plugins', '-l', dest='plugins', action='store_true',
                        help="list plugins that's going to be installed and configured")

    # Advanced options. These have a predefined default and are not managed
    # by config wizard.
    parser.add_argument('--no-input', '-q', dest='noinput', action='store_true',
                        default=False, help="don't run the configuration wizard, just use the provided values")
    parser.add_argument('--filer', '-f', dest='filer', action='store_true',
                        default=False, help='install and configure django-filer plugins')
    parser.add_argument('--requirements', '-r', dest='requirements', action='store',
                        default=None, help='externally defined requirements file')
    parser.add_argument('--no-deps', '-n', dest='no_deps', action='store_true',
                        default=False, help="Don't install package dependencies")
    parser.add_argument('--no-db-driver', dest='no_db_driver', action='store_true',
                        default=False, help="Don't install database package")
    parser.add_argument('--no-sync', '-m', dest='no_sync', action='store_true',
                        default=False, help="Don't run syncdb / migrate after bootstrapping")

    args = parser.parse_args(args)

    if not args.noinput:
        for item in data.CONFIGURABLE_OPTIONS:
            action = parser._option_string_actions[item]
            choices = default = ""
            input_value = getattr(args, action.dest)
            new_val = None
            if action.choices:
                choices = " [choices: %s]" % ", ".join(action.choices)
            if input_value:
                default = " default %s" % input_value

            while not new_val:
                prompt = "%s%s%s: " % (action.help, choices, default)
                if action.choices in ('yes', 'no'):
                    new_val = utils.query_yes_no(prompt)
                else:
                    new_val = compat.input(prompt)
                new_val = _validate(new_val, action)
    return args


def _validate(value, action):
    cleaned = compat.clean(value)
    if action.dest == 'db':
        try:
            return dj_database_url.parse(cleaned)
        except Exception:
            sys.out.write("Database URL not recognized, try again")
            return False
    else:
        if not cleaned and action.default:
            cleaned = action.default
        return cleaned


def write_default(config):
    pass


def show_plugins():
    """
    Shows a descriptive text about supported plugins
    """
    sys.stdout.write(data.PLUGIN_LIST_TEXT)

