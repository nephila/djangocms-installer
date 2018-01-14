# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from decimal import Decimal, InvalidOperation
from distutils.version import LooseVersion

from six import text_type

from . import compat
from .config.data import CMS_VERSION_MATRIX, DJANGO_VERSION_MATRIX, VERSION_MATRIX


def query_yes_no(question, default=None):  # pragma: no cover
    """
    Ask a yes/no question via `raw_input()` and return their answer.

    :param question: A string that is presented to the user.
    :param default: The presumed answer if the user just hits <Enter>.
                    It must be "yes" (the default), "no" or None (meaning
                    an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    Code borrowed from cookiecutter
    https://github.com/audreyr/cookiecutter/blob/master/cookiecutter/prompt.py
    """
    valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError('invalid default answer: "{0}"'.format(default))

    while True:
        sys.stdout.write(question + prompt)
        choice = compat.input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write('Please answer with "yes" or "no" (or "y" or "n").\n')


def supported_versions(django, cms):
    """
    Convert numeric and literal version information to numeric format
    """
    cms_version = None
    django_version = None

    try:
        cms_version = Decimal(cms)
    except (ValueError, InvalidOperation):
        try:
            cms_version = CMS_VERSION_MATRIX[str(cms)]
        except KeyError:
            pass

    try:
        django_version = Decimal(django)
    except (ValueError, InvalidOperation):
        try:
            django_version = DJANGO_VERSION_MATRIX[str(django)]
        except KeyError:  # pragma: no cover
            pass

    try:
        if (
                cms_version and django_version and
                not (LooseVersion(VERSION_MATRIX[compat.unicode(cms_version)][0]) <=
                     LooseVersion(compat.unicode(django_version)) <=
                     LooseVersion(VERSION_MATRIX[compat.unicode(cms_version)][1]))
        ):
            raise RuntimeError(
                'Django and django CMS versions doesn\'t match: '
                'Django {0} is not supported by django CMS {1}'.format(django_version, cms_version)
            )
    except KeyError:
        raise RuntimeError(
            'Django and django CMS versions doesn\'t match: '
            'Django {0} is not supported by django CMS {1}'.format(django_version, cms_version)
        )
    return (
        compat.unicode(django_version) if django_version else django_version,
        compat.unicode(cms_version) if cms_version else cms_version
    )


def less_than_version(value):
    """
    Converts the current version to the next one for inserting into requirements
    in the ' < version' format
    """
    items = list(map(int, str(value).split('.')))
    if len(items) == 1:
        items.append(0)
    items[1] += 1
    if value == '1.11':
        return '2.0'
    else:
        return '.'.join(map(str, items))


class chdir(object):
    """
    Context manager for changing the current working directory
    """
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def format_val(val):
    """
    Returns val as integer or as escaped string according to its value
    :param val: any value
    :return: formatted string
    """
    val = text_type(val)
    if val.isdigit():
        return int(val)
    else:
        return '\'{0}\''.format(val)
