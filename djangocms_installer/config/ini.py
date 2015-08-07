# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

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
        sys.stderr.write("Config file '%s' doesn't exists\n" % parsed_args.config_file)
        sys.exit(7)  # It isn't used anythere.

    config_args = _convert_config_to_stdin(config, parser)
    return config_args


def _convert_config_to_stdin(config, parser):
    """Convert config options to stdin args.

    Especially boolean values, for more information
    @see https://docs.python.org/3.4/library/configparser.html#supported-datatypes
    """
    keys_empty_values_not_pass = (
        '--extra-settings', '--languages', '--requirements', '--template', '--timezone')
    args = []
    for key, val in config.items(SECTION):
        keyp = '--%s' % key
        action = parser._option_string_actions[keyp]

        if action.const:
            try:
                if config.getboolean(SECTION, key):
                    args.append(keyp)
            except ValueError:
                args.extend([keyp, val])  # Pass it as is to get the error from ArgumentParser.
        elif any([i for i in keys_empty_values_not_pass if i in action.option_strings]):
            # Some keys with empty values shouldn't be passed into args to use their defaults from ArgumentParser.
            if val != '':
                args.extend([keyp, val])
        else:
            args.extend([keyp, val])

    return args