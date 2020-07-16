import os
import sys
from decimal import Decimal, InvalidOperation
from distutils.version import LooseVersion

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
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError('invalid default answer: "{}"'.format(default))

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()

        if default is not None and choice == "":
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
            cms_version
            and django_version
            and not (
                LooseVersion(VERSION_MATRIX[str(cms_version)][0])
                <= LooseVersion(str(django_version))
                <= LooseVersion(VERSION_MATRIX[str(cms_version)][-1])
            )
        ):
            raise RuntimeError(
                "Django and django CMS versions doesn't match: "
                "Django {} is not supported by django CMS {}".format(django_version, cms_version)
            )
    except KeyError:
        raise RuntimeError(
            "Django and django CMS versions doesn't match: "
            "Django {} is not supported by django CMS {}".format(django_version, cms_version)
        )
    return (
        str(django_version) if django_version else django_version,
        str(cms_version) if cms_version else cms_version,
    )


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


class chdir:  # noqa
    """
    Context manager for changing the current working directory
    """

    def __init__(self, new_path):
        self.new_path = new_path

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def format_val(val):
    """
    Returns val as integer or as escaped string according to its value
    :param val: any value
    :return: formatted string
    """
    val = str(val)
    if val.isdigit():
        return int(val)
    else:
        return "'{}'".format(val)
