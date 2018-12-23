# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys

from .data import CMS_VERSION_MATRIX, DJANGO_VERSION_MATRIX

try:
    from configparser import ConfigParser  # Python 3.
except ImportError:
    from ConfigParser import ConfigParser  # Python 2.


SECTION = 'djangocms_installer'


def parse_config_file(parser, stdin_args):
    """Parse config file.

    Returns a list of additional args.
    """
    config_args = []

    # Temporary switch required args and save them to restore.
    required_args = []
    for action in parser._actions:
        if action.required:
            required_args.append(action)
            action.required = False

    parsed_args = parser.parse_args(stdin_args)

    # Restore required args.
    for action in required_args:
        action.required = True

    if not parsed_args.config_file:
        return config_args

    config = ConfigParser()
    if not config.read(parsed_args.config_file):
        sys.stderr.write('Config file "{0}" doesn\'t exists\n'.format(parsed_args.config_file))
        sys.exit(7)  # It isn't used anywhere.

    config_args = _convert_config_to_stdin(config, parser)
    return config_args


def dump_config_file(filename, args, parser=None):
    """Dump args to config file."""
    config = ConfigParser()
    config.add_section(SECTION)
    if parser is None:
        for attr in args:
            config.set(SECTION, attr, args.attr)
    else:
        keys_empty_values_not_pass = (
            '--extra-settings', '--languages', '--requirements', '--template', '--timezone')

        # positionals._option_string_actions
        for action in parser._actions:
            if action.dest in ('help', 'config_file', 'config_dump', 'project_name'):
                continue

            keyp = action.option_strings[0]
            option_name = keyp.lstrip('-')
            option_value = getattr(args, action.dest)
            if any([i for i in keys_empty_values_not_pass if i in action.option_strings]):
                if action.dest == 'languages':
                    if len(option_value) == 1 and option_value[0] == 'en':
                        config.set(SECTION, option_name, '')
                    else:
                        config.set(SECTION, option_name, ','.join(option_value))
                else:
                    config.set(SECTION, option_name, option_value if option_value else '')
            elif action.choices == ('yes', 'no'):
                config.set(SECTION, option_name, 'yes' if option_value else 'no')
            elif action.dest == 'templates':
                config.set(SECTION, option_name, option_value if option_value else 'no')
            elif action.dest == 'cms_version':
                version = ('stable' if option_value == CMS_VERSION_MATRIX['stable']
                           else option_value)
                config.set(SECTION, option_name, version)
            elif action.dest == 'django_version':
                version = ('stable' if option_value == DJANGO_VERSION_MATRIX['stable']
                           else option_value)
                config.set(SECTION, option_name, version)
            elif action.const:
                config.set(SECTION, option_name, 'true' if option_value else 'false')
            else:
                config.set(SECTION, option_name, str(option_value))
    with open(filename, 'w') as fp:
        config.write(fp)


def _convert_config_to_stdin(config, parser):
    """Convert config options to stdin args.

    Especially boolean values, for more information
    @see https://docs.python.org/3.4/library/configparser.html#supported-datatypes
    """
    keys_empty_values_not_pass = (
        '--extra-settings', '--languages', '--requirements', '--template', '--timezone')
    args = []
    for key, val in config.items(SECTION):
        keyp = '--{0}'.format(key)
        action = parser._option_string_actions[keyp]

        if action.const:
            try:
                if config.getboolean(SECTION, key):
                    args.append(keyp)
            except ValueError:
                args.extend([keyp, val])  # Pass it as is to get the error from ArgumentParser.
        elif any([i for i in keys_empty_values_not_pass if i in action.option_strings]):
            # Some keys with empty values shouldn't be passed into args to use their defaults
            # from ArgumentParser.
            if val != '':
                args.extend([keyp, val])
        else:
            args.extend([keyp, val])

    return args
