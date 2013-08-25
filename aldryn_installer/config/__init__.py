# -*- coding: utf-8 -*-
import sys
import argparse

import dj_database_url

from .. import compat, utils
from . import data
from aldryn_installer.config.internal import DbAction


def parse(args):
    """
    Define the available arguments
    """
    parser = argparse.ArgumentParser(description='Bootstrap a django CMS project.')
    parser.add_argument('--db', '-d', dest='db', action=DbAction,
                        help='Database configuration (in URL format)')
    parser.add_argument('--i18n', '-i', dest='i18n', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Activate Django I18N / L10N setting')
    parser.add_argument('--reversion', '-e', dest='reversion', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Install and configure reversion support')
    parser.add_argument('--django-version', dest='django_version', action='store',
                        choices=('1.4', '1.5', 'latest', 'beta', 'develop'),
                        default='latest', help='Django version')
    parser.add_argument('--cms-version', '-v', dest='cms_version', action='store',
                        choices=('2.4', 'latest', 'beta', 'develop'),
                        default='latest', help='django CMS version')
    parser.add_argument(dest='project_name', action='store',
                        help='Name of the project to be created')

    # Command that lists the supported plugins in verbose description
    parser.add_argument('--list-plugins', '-l', dest='plugins', action='store_true',
                        help="List plugins that's going to be installed and configured")

    # Advanced options. These have a predefined default and are not managed
    # by config wizard.
    parser.add_argument('--no-input', '-q', dest='noinput', action='store_true',
                        default=False, help="Don't run the configuration wizard, just use the provided values")
    parser.add_argument('--filer', '-f', dest='filer', action='store_true',
                        default=False, help='Install and configure django-filer plugins')
    parser.add_argument('--requirements', '-r', dest='requirements_file', action='store',
                        default=None, help='Externally defined requirements file')
    parser.add_argument('--no-deps', '-n', dest='no_deps', action='store_true',
                        default=False, help="Don't install package dependencies")
    parser.add_argument('--no-db-driver', dest='no_db_driver', action='store_true',
                        default=False, help="Don't install database package")
    parser.add_argument('--no-sync', '-m', dest='no_sync', action='store_true',
                        default=False, help="Don't run syncdb / migrate after bootstrapping")

    args = parser.parse_args(args)

    for item in data.CONFIGURABLE_OPTIONS:
        action = parser._option_string_actions[item]
        choices = default = ""
        input_value = getattr(args, action.dest)
        new_val = None
        if not args.noinput:
            if action.choices:
                choices = " (choices: %s)" % ", ".join(action.choices)
            if input_value:
                default = " [default %s]" % input_value

            while not new_val:
                prompt = "%s%s%s: " % (action.help, choices, default)
                if action.choices in ('yes', 'no'):
                    new_val = utils.query_yes_no(prompt)
                else:
                    new_val = compat.input(prompt)
                new_val = compat.clean(new_val)
                if not new_val and input_value:
                    new_val = input_value
        else:
            if not input_value:
                raise ValueError("Option %s is required when in no-input mode" % action.dest)
            new_val = input_value
        setattr(args, action.dest, new_val)
        if not getattr(args, 'requirements_file'):
            requirements = [data.DEFAULT_REQUIREMENTS]
            cms_version = 3
            django_version = 1.5

            if not args.no_db_driver:
                requirements.append(args.db_driver)
            if args.filer:
                requirements.append(data.FILER_REQUIREMENTS)

            ## Django version check
            if args.django_version == 'develop':
                requirements.append(data.DJANGO_DEVELOP)
            elif args.django_version == 'beta':
                requirements.append(data.DJANGO_BETA)
            else:
                if args.django_version == 'latest':
                    requirements.append("Django<%s" % data.less_than_version(data.DJANGO_LATEST))
                else:
                    requirements.append("Django<%s" % data.less_than_version(args.django_version))
                    if data.less_than_version(args.django_version) <= "1.5":
                        django_version = 1.4

            ## Reversion package version depends on django version
            if args.reversion:
                if django_version < 1.5:
                    requirements.append(data.DJANGO_14_REVERSION)
                else:
                    requirements.append(data.DJANGO_15_REVERSION)

            ## Django cms version check
            if args.cms_version == 'develop':
                requirements.append(data.DJANGOCMS_DEVELOP)
            elif args.cms_version == 'beta':
                requirements.append(data.DJANGOCMS_BETA)
            else:
                if args.cms_version == 'latest':
                    requirements.append("django-cms<%s" % data.less_than_version(data.DJANGOCMS_LATEST))
                else:
                    requirements.append("django-cms<%s" % data.less_than_version(args.cms_version))
                if(args.cms_version == 'latest' or
                        data.less_than_version(args.cms_version) < "3.0"):
                    cms_version = 2.4
            if cms_version >= 3:
                requirements.append(data.DJANGOCMS_3_REQUIREMENTS)

            setattr(args, "requirements", "\n".join(requirements).strip())
    return args


def write_default(config):
    pass


def show_plugins():
    """
    Shows a descriptive text about supported plugins
    """
    sys.stdout.write(data.PLUGIN_LIST_TEXT)

