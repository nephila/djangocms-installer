import keyword
import re
import sys
from argparse import Action

import dj_database_url

from .data import DRIVERS

project_name_rx = re.compile(r"^[a-z0-9_A-Z]+$")


class DbAction(Action):
    def __call__(self, parser, namespace, values, option_string):
        parsed = dj_database_url.parse(values)
        if parsed.get("ENGINE", None):
            if DRIVERS[parsed["ENGINE"]] == "postgis":
                sys.stdout.write(
                    "postgis installation is not supported at the moment.\n"
                    "You need to install and configure the backend.\n"
                )
            setattr(namespace, self.dest, values)
            setattr(namespace, "{}_parsed".format(self.dest), parsed)
            setattr(namespace, "{}_driver".format(self.dest), DRIVERS[parsed["ENGINE"]])
        else:
            raise ValueError("Database URL not recognized, try again")


def validate_project(project_name):
    """
    Check the defined project name against keywords, builtins and existing
    modules to avoid name clashing
    """
    if not project_name_rx.search(project_name):
        return None
    if keyword.iskeyword(project_name):
        return None
    if project_name in dir(__builtins__):
        return None
    try:
        __import__(project_name)
        return None
    except ImportError:
        return project_name
