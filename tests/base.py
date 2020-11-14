import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import copy

from six import StringIO

SYSTEM_ACTIVATE = os.path.join(os.path.dirname(sys.executable), "activate_this.py")


class BaseTestClass(unittest.TestCase):
    stdout = None
    stderr = None
    project_dir = None
    verbose = False

    def _remove_project_dir(self):
        if (
            self.project_dir
            and os.path.exists(self.project_dir)
            and not os.environ.get("INSTALLER_TEST_KEEP_VIRTUALENV")
        ):
            shutil.rmtree(self.project_dir)
            self.project_dir = None

    def _create_project_dir(self):
        if os.environ.get("USE_SHM", "no") == "yes":
            if os.path.exists("/run/shm"):
                self.project_dir = tempfile.mkdtemp(dir="/run/shm")
            elif os.path.exists("/dev/shm"):
                self.project_dir = tempfile.mkdtemp(dir="/dev/shm")
            else:
                self.project_dir = tempfile.mkdtemp()
        else:
            self.project_dir = tempfile.mkdtemp()

    def tearDown(self):
        self._remove_project_dir()
        self.stdout = None
        self.stderr = None
        if "DJANGO_SETTINGS_MODULE" in os.environ:
            del os.environ["DJANGO_SETTINGS_MODULE"]
        sys.path = self.syspath

    def setUp(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self._create_project_dir()
        self.syspath = sys.path


class IsolatedTestClass(BaseTestClass):
    virtualenv_dir = None
    activate_this = ""

    def _remove_project_dir(self):
        super()._remove_project_dir()
        if (
            self.virtualenv_dir
            and not os.environ.get("INSTALLER_TEST_VIRTUALENV", False)
            and not os.environ.get("INSTALLER_TEST_KEEP_VIRTUALENV")
        ):
            if self.verbose:
                print("remove virtualenv", self.virtualenv_dir)
            shutil.rmtree(self.virtualenv_dir)
            self.virtualenv_dir = None

    def _create_project_dir(self):
        super()._create_project_dir()
        if os.environ.get("INSTALLER_TEST_VIRTUALENV", False):
            self.virtualenv_dir = os.environ.get("INSTALLER_TEST_VIRTUALENV")
        else:
            self.virtualenv_dir = tempfile.mkdtemp()
        if self.verbose:
            print("creating virtualenv", self.virtualenv_dir)

    def tearDown(self):
        if self.verbose:
            print("deactivating virtualenv", self.virtualenv_dir)
        if os.path.exists(SYSTEM_ACTIVATE):
            with open(SYSTEM_ACTIVATE) as f:
                code = compile(f.read(), SYSTEM_ACTIVATE, "exec")
            # fmt: off
            exec(code, dict(__file__=SYSTEM_ACTIVATE))
            # fmt: on
            sys.executable = os.path.join(os.path.dirname(SYSTEM_ACTIVATE), "python")
        super().tearDown()
        modules = copy(sys.modules)
        for module in modules:
            if "django" in module:
                del sys.modules[module]

    def setUp(self):
        super().setUp()
        if os.path.exists(SYSTEM_ACTIVATE):
            subprocess.check_call(
                ["virtualenv", "--always-copy", "-q", "--python=%s" % sys.executable, self.virtualenv_dir]
            )
            activate_temp = os.path.join(self.virtualenv_dir, "bin", "activate_this.py")
            with open(activate_temp) as f:
                code = compile(f.read(), activate_temp, "exec")
            # fmt: off
            exec(code, dict(__file__=activate_temp))
            # fmt: on
            if self.verbose:
                print("activating virtualenv", self.virtualenv_dir)
            sys.executable = os.path.join(self.virtualenv_dir, "bin", "python")
            os.environ["VIRTUAL_ENV"] = self.virtualenv_dir


def get_stable_django(latest=False, lts=False):
    """
    Get django version compatible with all the supported django CMS and python versions.

    Takes into account arguments and python version.

    Default to lower common version.

    :param latest: Latest stable version
    :param lts: Latest lts version
    """
    if latest and not sys.version_info < (3, 6) and not lts:
        dj_ver = "3.1"
        match = "Django<3.2"
    else:
        dj_ver = "2.2"
        match = "Django<2.3"
    return dj_ver, match


def get_stable_djangocms():
    """
    Get django CMS version compatible with all the supported django and python versions.

    Takes into account arguments and python version.
    """
    dj_ver = "3.8"
    match = "django-cms<3.9"
    return dj_ver, match
