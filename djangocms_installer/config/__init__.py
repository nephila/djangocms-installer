# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import argparse
import locale
import os.path
import sys
import warnings

import six
from tzlocal import get_localzone

from . import data, ini
from .. import compat, utils
from ..utils import less_than_version, supported_versions
from .internal import DbAction, validate_project


def parse(args):
    """
    Define the available arguments
    """
    parser = argparse.ArgumentParser(description='Bootstrap a django CMS project.')
    parser.add_argument('--config-file', dest='config_file', action='store',
                        default=None,
                        help='Configuration file for djangocms_installer')
    parser.add_argument('--config-dump', dest='config_dump', action='store',
                        default=None,
                        help='Dump configuration file with current args')
    parser.add_argument('--db', '-d', dest='db', action=DbAction,
                        default='sqlite://localhost/project.db',
                        help='Database configuration (in URL format)')
    parser.add_argument('--i18n', '-i', dest='i18n', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Activate Django I18N / L10N setting; this is '
                                            'automatically activated if more than '
                                            'language is provided')
    parser.add_argument('--use-tz', '-z', dest='use_timezone', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Activate Django timezone support')
    parser.add_argument('--timezone', '-t', dest='timezone',
                        required=False, default=get_localzone(),
                        action='store', help='Optional default time zone')
    parser.add_argument('--reversion', '-e', dest='reversion', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Install and configure reversion support')
    parser.add_argument('--permissions', dest='permissions', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Activate CMS permission management')
    parser.add_argument('--pip-options', help='pass custom pip options', default='')
    parser.add_argument('--languages', '-l', dest='languages', action='append',
                        help='Languages to enable. Option can be provided multiple times, or as a '
                             'comma separated list. Only language codes supported by Django can '
                             'be used here')
    parser.add_argument('--django-version', dest='django_version', action='store',
                        choices=data.DJANGO_SUPPORTED,
                        default='stable', help='Django version')
    parser.add_argument('--cms-version', '-v', dest='cms_version', action='store',
                        choices=data.DJANGOCMS_SUPPORTED,
                        default='stable', help='django CMS version')
    parser.add_argument('--parent-dir', '-p', dest='project_directory',
                        required=True, default='',
                        action='store', help='Optional project parent directory')
    parser.add_argument('--bootstrap', dest='bootstrap', action='store',
                        choices=('yes', 'no'),
                        default='no', help='Use Twitter Bootstrap Theme')
    parser.add_argument('--templates', dest='templates', action='store',
                        default='no', help='Use custom template set')
    parser.add_argument('--starting-page', dest='starting_page', action='store',
                        choices=('yes', 'no'),
                        default='no', help='Load a starting page with examples after installation '
                                           '(english language only). Choose "no" if you use a '
                                           'custom template set.')
    parser.add_argument(dest='project_name', action='store',
                        help='Name of the project to be created')

    # Command that lists the supported plugins in verbose description
    parser.add_argument('--list-plugins', '-P', dest='plugins', action='store_true',
                        help='List plugins that\'s going to be installed and configured')

    # Command that lists the supported plugins in verbose description
    parser.add_argument('--dump-requirements', '-R', dest='dump_reqs', action='store_true',
                        help='It dumps the requirements that would be installed according to '
                             'parameters given. Together with --requirements argument is useful '
                             'for customizing the virtualenv')

    # Advanced options. These have a predefined default and are not managed
    # by config wizard.
    # parser.add_argument('--aldryn', '-a', dest='aldryn', action='store_true',
    #                    default=False, help='Use Aldryn-boilerplate as project template')
    parser.add_argument('--no-input', '-q', dest='noinput', action='store_true',
                        default=False, help='Don\'t run the configuration wizard, just use the '
                                            'provided values')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        default=False, help='Be more verbose and don\' swallow subcommands output')
    parser.add_argument('--apphooks-reload', '-k', dest='apphooks_reload', action='store_true',
                        default=False, help='Use apphooks-reload middleware')
    parser.add_argument('--filer', '-f', dest='filer', action='store_true',
                        default=False, help='Install and configure django-filer plugins')
    parser.add_argument('--requirements', '-r', dest='requirements_file', action='store',
                        default=None, help='Externally defined requirements file')
    parser.add_argument('--no-deps', '-n', dest='no_deps', action='store_true',
                        default=False, help='Don\'t install package dependencies')
    parser.add_argument('--no-plugins', dest='no_plugins', action='store_true',
                        default=False, help='Don\'t install plugins')
    parser.add_argument('--no-db-driver', dest='no_db_driver', action='store_true',
                        default=False, help='Don\'t install database package')
    parser.add_argument('--no-sync', '-m', dest='no_sync', action='store_true',
                        default=False, help='Don\'t run syncdb / migrate after bootstrapping')
    parser.add_argument('--no-user', '-u', dest='no_user', action='store_true',
                        default=False, help='Don\'t create the admin user')
    parser.add_argument('--template', dest='template', action='store',
                        default=None, help='The path or URL to load the django project '
                                           'template from.')
    parser.add_argument('--extra-settings', dest='extra_settings', action='store',
                        default=None, help='The path to an file that contains extra settings.')
    parser.add_argument('--skip-empty-check', '-s', dest='skip_project_dir_check',
                        action='store_true',
                        default=False, help='Skip the check if project dir is empty.')
    parser.add_argument('--utc', dest='utc',
                        action='store_true',
                        default=False, help='Use UTC timezone.')

    if '--utc' in args:
        for action in parser._positionals._actions:
            if action.dest == 'timezone':
                action.default = 'UTC'

    # If config_args then pretend that config args came from the stdin and run parser again.
    config_args = ini.parse_config_file(parser, args)
    args = parser.parse_args(config_args + args)

    # First of all, check if the project name is valid
    if not validate_project(args.project_name):
        sys.stderr.write(
            'Project name "{0}" is not a valid app name, or it\'s already defined. '
            'Please use only numbers, letters and underscores.\n'.format(args.project_name)
        )
        sys.exit(3)

    # Checking the given path
    setattr(args, 'project_path',
            os.path.join(args.project_directory, args.project_name).strip())
    if not args.skip_project_dir_check:
        if (os.path.exists(args.project_directory) and
                [path for path in os.listdir(args.project_directory) if not path.startswith('.')]):
            sys.stderr.write(
                'Path "{0}" already exists and is not empty, please choose a different one\n'
                'If you want to use this path anyway use the -s flag to skip this check.\n'
                ''.format(args.project_directory)
            )
            sys.exit(4)

    if os.path.exists(args.project_path):
        sys.stderr.write(
            'Path "{0}" already exists, please choose a different one\n'.format(args.project_path)
        )
        sys.exit(4)

    if args.config_dump and os.path.isfile(args.config_dump):
        sys.stdout.write(
            'Cannot dump because given configuration file "{0}" exists.\n'.format(args.config_dump)
        )
        sys.exit(8)

    args = _manage_args(parser,  args)

    # what do we want here?!
    # * if languages are given as multiple arguments, let's use it as is
    # * if no languages are given, use a default and stop handling it further
    # * if languages are given as a comma-separated list, split it and use the
    #   resulting list.

    if not args.languages:
        try:
            args.languages = [locale.getdefaultlocale()[0].split('_')[0]]
        except:
            args.languages = ['en']
    elif isinstance(args.languages, six.string_types):
        args.languages = args.languages.split(',')
    elif len(args.languages) == 1 and isinstance(args.languages[0], six.string_types):
        args.languages = args.languages[0].split(',')

    args.languages = [lang.strip().lower() for lang in args.languages]
    if len(args.languages) > 1:
        args.i18n = 'yes'
    args.aldryn = False

    # Convert version to numeric format for easier checking
    try:
        django_version, cms_version = supported_versions(args.django_version,
                                                         args.cms_version)
    except RuntimeError as e:
        sys.stderr.write(compat.unicode(e))
        sys.exit(6)
    if django_version is None:
        sys.stderr.write(
            'Please provide a Django supported version: {0}. Only Major.Minor '
            'version selector is accepted\n'.format(', '.join(data.DJANGO_SUPPORTED))
        )
        sys.exit(6)
    if django_version is None:
        sys.stderr.write(
            'Please provide a django CMS supported version: {0}. Only Major.Minor '
            'version selector is accepted\n'.format(', '.join(data.DJANGOCMS_SUPPORTED))
        )
        sys.exit(6)

    if not getattr(args, 'requirements_file'):
        requirements = []

        # django CMS version check
        if args.cms_version == 'develop':
            requirements.append(data.DJANGOCMS_DEVELOP)
            warnings.warn(data.VERSION_WARNING.format('develop', 'django CMS'))
        elif args.cms_version == 'rc':  # pragma: no cover
            requirements.append(data.DJANGOCMS_RC)
        elif args.cms_version == 'beta':  # pragma: no cover
            requirements.append(data.DJANGOCMS_BETA)
            warnings.warn(data.VERSION_WARNING.format('beta', 'django CMS'))
        else:
            requirements.append('django-cms<{0}'.format(less_than_version(cms_version)))

        if cms_version >= 3.2:
            requirements.extend(data.REQUIREMENTS['cms-3.2'])

        if not args.no_db_driver:
            requirements.append(args.db_driver)
        if not args.no_plugins:
            if args.filer:
                requirements.extend(data.REQUIREMENTS['plugins-common'])
                requirements.extend(data.REQUIREMENTS['filer'])
            else:
                requirements.extend(data.REQUIREMENTS['plugins-common'])
                requirements.extend(data.REQUIREMENTS['plugins-basic'])
            if cms_version >= 3.3 or cms_version == 'rc':
                requirements.extend(data.REQUIREMENTS['ckeditor-3.3'])
            else:
                requirements.extend(data.REQUIREMENTS['ckeditor-3.2'])
        if args.aldryn:  # pragma: no cover
            requirements.extend(data.REQUIREMENTS['aldryn'])

        # Django version check
        if args.django_version == 'develop':  # pragma: no cover
            requirements.append(data.DJANGO_DEVELOP)
            warnings.warn(data.VERSION_WARNING.format('develop', 'Django'))
        elif args.django_version == 'beta':  # pragma: no cover
            requirements.append(data.DJANGO_BETA)
            warnings.warn(data.VERSION_WARNING.format('beta', 'Django'))
        else:
            requirements.append('Django<{0}'.format(less_than_version(django_version)))

        # Timezone support
        if args.use_timezone:
            requirements.append('pytz')

        # Requirements dependendent on django version
        # if django_version < 1.7:
        #    requirements.extend(data.REQUIREMENTS['django-legacy'])

        # Reversion package version depends on django version
        if args.reversion:
            if django_version == 1.8:
                requirements.extend(data.REQUIREMENTS['reversion-django-1.8'])
            elif django_version == 1.9:
                requirements.extend(data.REQUIREMENTS['reversion-django-1.9'])

        if django_version == 1.8:
            requirements.extend(data.REQUIREMENTS['django-1.8'])
        elif django_version == 1.9:
            requirements.extend(data.REQUIREMENTS['django-1.9'])

        requirements.extend(data.REQUIREMENTS['default'])

        setattr(args, 'requirements', '\n'.join(requirements).strip())

    # Convenient shortcuts
    setattr(args, 'cms_version', cms_version)
    setattr(args, 'django_version', django_version)
    setattr(args, 'settings_path',
            os.path.join(args.project_directory, args.project_name, 'settings.py').strip())
    setattr(args, 'urlconf_path',
            os.path.join(args.project_directory, args.project_name, 'urls.py').strip())

    if args.config_dump:
        ini.dump_config_file(args.config_dump, args, parser)

    return args


def get_settings():
    module = __import__(str('djangocms_installer.config'), globals(), locals(), [str('settings')])
    return module.settings


def write_default(config):
    pass


def show_plugins():
    """
    Shows a descriptive text about supported plugins
    """
    sys.stdout.write(compat.unicode(data.PLUGIN_LIST_TEXT))


def show_requirements(args):
    """
    Prints the list of requirements according to the arguments provided
    """
    sys.stdout.write(compat.unicode(args.requirements))


def _manage_args(parser,  args):
    """
    Checks and validate provided input
    """
    for item in data.CONFIGURABLE_OPTIONS:
        action = parser._option_string_actions[item]
        choices = default = ''
        input_value = getattr(args, action.dest)
        new_val = None
        # cannot count this until we find a way to test input
        if not args.noinput:  # pragma: no cover
            if action.choices:
                choices = ' (choices: {0})'.format(', '.join(action.choices))
            if input_value:
                if type(input_value) == list:
                    default = ' [default {0}]'.format(', '.join(input_value))
                else:
                    default = ' [default {0}]'.format(input_value)

            while not new_val:
                prompt = '{0}{1}{2}: '.format(action.help, choices, default)
                if action.choices in ('yes', 'no'):
                    new_val = utils.query_yes_no(prompt)
                else:
                    new_val = compat.input(prompt)
                new_val = compat.clean(new_val)
                if not new_val and input_value:
                    new_val = input_value
                if new_val and action.dest == 'templates':
                    if new_val != 'no' and not os.path.isdir(new_val):
                        sys.stdout.write('Given directory does not exists, retry\n')
                        new_val = False
                if new_val and action.dest == 'db':
                    action(parser, args, new_val, action.option_strings)
                    new_val = getattr(args, action.dest)
        else:
            if not input_value and action.required:
                raise ValueError(
                    'Option {0} is required when in no-input mode'.format(action.dest)
                )
            new_val = input_value
            if action.dest == 'db':
                action(parser, args, new_val, action.option_strings)
                new_val = getattr(args, action.dest)
        if action.dest == 'templates' and (new_val == 'no' or not os.path.isdir(new_val)):
            new_val = False
        if action.dest in ('bootstrap', 'starting_page'):
            new_val = (new_val == 'yes')
        setattr(args, action.dest, new_val)
    return args
