# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import locale
import os.path
import six
import sys
import warnings

from tzlocal import get_localzone

from . import data
from .internal import DbAction, validate_project
from .. import compat, utils
from ..utils import less_than_version, supported_versions


def parse(args):
    """
    Define the available arguments
    """
    parser = argparse.ArgumentParser(description='Bootstrap a django CMS project.')
    parser.add_argument('--db', '-d', dest='db', action=DbAction,
                        default='sqlite://localhost/project.db',
                        help='Database configuration (in URL format)')
    parser.add_argument('--i18n', '-i', dest='i18n', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Activate Django I18N / L10N setting')
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
    parser.add_argument('--languages', '-l', dest='languages', action='append',
                        help='Languages to enable. Option can be provided multiple times, or as a comma separated list. '
                        'Only language codes supported by Django can be used here')
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
                        default='no', help='Load a starting page with examples after installation. Choose "no" if you use a custom template set.')
    parser.add_argument(dest='project_name', action='store',
                        help='Name of the project to be created')

    # Command that lists the supported plugins in verbose description
    parser.add_argument('--list-plugins', '-P', dest='plugins', action='store_true',
                        help="List plugins that's going to be installed and configured")

    # Command that lists the supported plugins in verbose description
    parser.add_argument('--dump-requirements', '-R', dest='dump_reqs', action='store_true',
                        help="It dumps the requirements that would be installed according to parameters given."
                             "Together with --requirements argument is useful for customizing the virtualenv")

    # Advanced options. These have a predefined default and are not managed
    # by config wizard.
    #parser.add_argument('--aldryn', '-a', dest='aldryn', action='store_true',
    #                    default=False, help="Use Aldryn-boilerplate as project template")
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
    parser.add_argument('--no-user', '-u', dest='no_user', action='store_true',
                        default=False, help="Don't create the admin user")
    parser.add_argument('--template', dest='template', action='store',
                        default=None, help="The path or URL to load the django project template from.")
    parser.add_argument('--extra-settings', dest='extra_settings', action='store',
                        default=None, help="The path to an file that contains extra settings.")
    parser.add_argument('--skip-empty-check', '-s', dest='skip_project_dir_check',
                        action='store_true',
                        default=False, help="Skip the check if project dir is empty.")
    parser.add_argument('--utc', dest='utc',
                        action='store_true',
                        default=False, help="Use UTC timezone.")

    if '--utc' in args:
        for action in parser._positionals._actions:
            if action.dest == 'timezone':
                action.default = 'UTC'
    args = parser.parse_args(args)

    # First of all, check if the project name is valid
    if not validate_project(args.project_name):
        sys.stderr.write(u"Project name '%s' is not a valid app name, "
                         u"or it's already defined. "
                         u"Please use only numbers, letters and underscores.\n"
                         % args.project_name)
        sys.exit(3)

    # Checking the given path
    setattr(args, 'project_path',
            os.path.join(args.project_directory, args.project_name).strip())
    if not args.skip_project_dir_check:
        if (os.path.exists(args.project_directory) and
                [path for path in os.listdir(args.project_directory) if not path.startswith('.')]):
            sys.stderr.write("Path '%s' already exists and is not empty, "
                             "please choose a different one\nIf you want to use this path anyway "
                             "use the -s flag to skip this check." % args.project_directory)
            sys.exit(4)

    if os.path.exists(args.project_path):
        sys.stderr.write("Path '%s' already exists, "
                         "please choose a different one\n" % args.project_path)
        sys.exit(4)

    for item in data.CONFIGURABLE_OPTIONS:
        action = parser._option_string_actions[item]
        choices = default = ""
        input_value = getattr(args, action.dest)
        new_val = None
        if not args.noinput:
            if action.choices:
                choices = " (choices: %s)" % ", ".join(action.choices)
            if input_value:
                if type(input_value) == list:
                    default = " [default %s]" % ", ".join(input_value)
                else:
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
                if new_val and action.dest == 'templates':
                    if new_val != 'no' and not os.path.isdir(new_val):
                        sys.stdout.write('Given directory does not exists, retry\n')
                        new_val = False
                if new_val and action.dest == 'db':
                    action(parser, args, new_val, action.option_strings)
                    new_val = getattr(args, action.dest)
        else:
            if not input_value and action.required:
                raise ValueError("Option %s is required when in no-input mode" % action.dest)
            new_val = input_value
            if action.dest == 'db':
                action(parser, args, new_val, action.option_strings)
                new_val = getattr(args, action.dest)
        if action.dest == 'templates' and (new_val == 'no' or not os.path.isdir(new_val)):
            new_val = False
        if action.dest in ('bootstrap', 'starting_page'):
            new_val = (new_val == 'yes')
        setattr(args, action.dest, new_val)

    # what do we want here?!
    # * if languages are given as multiple arguments, let's use it as is
    # * if no languages are given, use a default and stop handling it further
    # * if languages are given as a comma-separated list, split it and use the
    #   resulting list.

    if not args.languages:
        args.languages = [locale.getdefaultlocale()[0].split("_")[0]]
    elif isinstance(args.languages, six.string_types):
        args.languages = args.languages.split(",")
    elif len(args.languages) == 1 and isinstance(args.languages[0],
                                                 six.string_types):
        args.languages = args.languages[0].split(",")

    args.languages = [lang.strip() for lang in args.languages]
    args.aldryn = False

    # Convert version to numeric format for easier checking
    try:
        django_version, cms_version = supported_versions(args.django_version,
                                                         args.cms_version)
    except RuntimeError as e:
        sys.stderr.write(compat.unicode(e))
        sys.exit(6)
    if django_version is None:
        sys.stderr.write("Please provide a Django supported version: %s. Only Major.Minor version selector is accepted\n" % ", ".join(data.DJANGO_SUPPORTED))
        sys.exit(6)
    if django_version is None:
        sys.stderr.write("Please provide a django CMS supported version: %s. Only Major.Minor version selector is accepted\n" % ", ".join(data.DJANGOCMS_SUPPORTED))
        sys.exit(6)

    if not getattr(args, 'requirements_file'):
        requirements = []

        # django CMS version check
        if args.cms_version == 'develop':
            requirements.append(data.DJANGOCMS_DEVELOP)
            warnings.warn(data.VERSION_WARNING % ('develop', 'django CMS'))
        elif args.cms_version == 'rc':
            requirements.append(data.DJANGOCMS_RC)
        elif args.cms_version == 'beta':
            requirements.append(data.DJANGOCMS_BETA)
            warnings.warn(data.VERSION_WARNING % ('beta', 'django CMS'))
        else:
            requirements.append("django-cms<%s" % less_than_version(cms_version))

        if cms_version == 3:
            requirements.append(data.DJANGOCMS_3_REQUIREMENTS)
        elif cms_version >= 3:
            requirements.append(data.DJANGOCMS_3_1_REQUIREMENTS)
        else:
            requirements.append(data.DJANGOCMS_2_REQUIREMENTS)

        if not args.no_db_driver:
            requirements.append(args.db_driver)
        if args.filer:
            if cms_version >= 3:
                if django_version < 1.7:
                    requirements.append(data.PLUGINS_REQUIREMENTS_BASIC)
                    requirements.append(data.FILER_REQUIREMENTS_CMS3)
                else:
                    requirements.append(data.PLUGINS_REQUIREMENTS_BASIC_DJANGO_17)
                    requirements.append(data.FILER_REQUIREMENTS_CMS3)
            else:
                requirements.append(data.FILER_REQUIREMENTS_CMS2)
        elif cms_version >= 3:
            if django_version < 1.7:
                requirements.append(data.PLUGINS_REQUIREMENTS_BASIC)
                requirements.append(data.PLUGINS_REQUIREMENTS_NON_FILER)
            else:
                requirements.append(data.PLUGINS_REQUIREMENTS_BASIC_DJANGO_17)
                requirements.append(data.PLUGINS_REQUIREMENTS_NON_FILER_DJANGO_17)
        if args.aldryn:
            requirements.append(data.ALDRYN_REQUIREMENTS)

        # Django version check
        if args.django_version == 'develop':
            requirements.append(data.DJANGO_DEVELOP)
            warnings.warn(data.VERSION_WARNING % ('develop', 'Django'))
        elif args.django_version == 'beta':
            requirements.append(data.DJANGO_BETA)
            warnings.warn(data.VERSION_WARNING % ('beta', 'Django'))
        else:
            requirements.append("Django<%s" % less_than_version(django_version))

        # Timezone support
        if args.use_timezone:
            requirements.append('pytz')

        # Requirements dependendent on django version
        if django_version < 1.7:
            requirements.append(data.DJANGO_16_REQUIREMENTS)

        # Reversion package version depends on django version
        if args.reversion:
            if django_version < 1.5:
                requirements.append(data.DJANGO_14_REVERSION)
            elif django_version == 1.5:
                requirements.append(data.DJANGO_15_REVERSION)
            elif django_version == 1.6:
                requirements.append(data.DJANGO_16_REVERSION)
            else:
                requirements.append(data.DJANGO_17_REVERSION)

        requirements.extend([data.DEFAULT_REQUIREMENTS])

        setattr(args, "requirements", "\n".join(requirements).strip())
    if cms_version < 3 and args.aldryn:
        sys.stderr.write("Aldryn Boilerplate is not compatible with django CMS versions < 3\n")
        sys.exit(5)

    # Convenient shortcuts
    setattr(args, "cms_version", cms_version)
    setattr(args, "django_version", django_version)
    setattr(args, 'settings_path',
            os.path.join(args.project_directory, args.project_name, 'settings.py').strip())
    setattr(args, 'urlconf_path',
            os.path.join(args.project_directory, args.project_name, 'urls.py').strip())

    return args


def get_settings():
    module = __import__('djangocms_installer.config', globals(), locals(), ['settings'])
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
