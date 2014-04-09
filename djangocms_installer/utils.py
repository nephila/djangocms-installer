# -*- coding: utf-8 -*-
import os
import sys

from . import compat


def query_yes_no(question, default=None):
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
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = compat.input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please answer with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def supported_versions(django, cms):
    """
    Convert numeric and literal version information to numeric format
    """
    cms_version = 3
    django_version = 1.5
    try:
        cms_version = float(cms)
    except ValueError:
        if cms == 'stable':
            cms_version = 3.0
        elif django == 'rc':
            django_version = 3.0
        elif django == 'beta':
            django_version = 3.0
        elif django == 'develop':
            django_version = 3.0

    try:
        django_version = float(django)
    except ValueError:
        if django == 'stable':
            if cms_version == 3.0:
                django_version = 1.6
            else:
                django_version = 1.5
        elif django == 'beta':
            django_version = 1.6
        elif django == 'develop':
            django_version = 1.7

    return django_version, cms_version


def less_than_version(value):
    """
    Converts the current version to the next one for inserting into requirements
    in the ' < version' format
    """
    items = list(map(int, value.split(".")))
    if len(items) == 1:
        items.append(0)
    items[1] += 1
    return ".".join(map(str, items))


class chdir(object):
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
