# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

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
        raise ValueError('invalid default answer: "%s"' % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = compat.input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write('Please answer with "yes" or "no" '
                             '(or "y" or "n").\n')


def supported_versions(django, cms):
    """
    Convert numeric and literal version information to numeric format
    """
    cms_version = None
    django_version = None
    try:
        cms_version = float(cms)
    except ValueError:
        try:
            cms_version = CMS_VERSION_MATRIX[cms]
        except KeyError:
            pass

    try:
        django_version = float(django)
    except ValueError:
        try:
            django_version = DJANGO_VERSION_MATRIX[django]
        except KeyError:
            pass
    try:
        if (
                cms_version and django_version and
                not (VERSION_MATRIX[cms_version][0] <= django_version <=
                     VERSION_MATRIX[cms_version][1])
        ):
            raise RuntimeError(
                'Django and django CMS versions doesn\'t match: '
                'Django %s is not supported by django CMS %s' % (django_version, cms_version)
            )
    except KeyError:
        raise RuntimeError(
            'Django and django CMS versions doesn\'t match: '
            'Django %s is not supported by django CMS %s' % (django_version, cms_version)
        )
    return django_version, cms_version


def less_than_version(value):
    """
    Converts the current version to the next one for inserting into requirements
    in the ' < version' format
    """
    items = list(map(int, str(value).split(".")))
    if len(items) == 1:
        items.append(0)
    items[1] += 1
    return ".".join(map(str, items))


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
