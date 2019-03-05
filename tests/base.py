# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import copy

from six import StringIO


SYSTEM_ACTIVATE = os.path.join(os.path.dirname(sys.executable), 'activate_this.py')


class BaseTestClass(unittest.TestCase):
    stdout = None
    stderr = None
    project_dir = None
    verbose = False

    def _remove_project_dir(self):
        if (
            self.project_dir and os.path.exists(self.project_dir) and
            not os.environ.get('INSTALLER_TEST_KEEP_VIRTUALENV')
        ):
            shutil.rmtree(self.project_dir)
            self.project_dir = None

    def _create_project_dir(self):
        if os.environ.get('USE_SHM', 'no') == 'yes':
            if os.path.exists('/run/shm'):
                self.project_dir = tempfile.mkdtemp(dir='/run/shm')
            elif os.path.exists('/dev/shm'):
                self.project_dir = tempfile.mkdtemp(dir='/dev/shm')
            else:
                self.project_dir = tempfile.mkdtemp()
        else:
            self.project_dir = tempfile.mkdtemp()

    def tearDown(self):
        self._remove_project_dir()
        self.stdout = None
        self.stderr = None
        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            del os.environ['DJANGO_SETTINGS_MODULE']
        sys.path = self.syspath

    def setUp(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self._create_project_dir()
        self.syspath = sys.path


class IsolatedTestClass(BaseTestClass):
    virtualenv_dir = None
    activate_this = ''

    def _remove_project_dir(self):
        super(IsolatedTestClass, self)._remove_project_dir()
        if (
            self.virtualenv_dir and not os.environ.get('INSTALLER_TEST_VIRTUALENV', False) and
            not os.environ.get('INSTALLER_TEST_KEEP_VIRTUALENV')
        ):
            if self.verbose:
                print('remove virtualenv', self.virtualenv_dir)
            shutil.rmtree(self.virtualenv_dir)
            self.virtualenv_dir = None

    def _create_project_dir(self):
        super(IsolatedTestClass, self)._create_project_dir()
        if os.environ.get('INSTALLER_TEST_VIRTUALENV', False):
            self.virtualenv_dir = os.environ.get('INSTALLER_TEST_VIRTUALENV')
        else:
            self.virtualenv_dir = tempfile.mkdtemp()
        if self.verbose:
            print('creating virtualenv', self.virtualenv_dir)

    def tearDown(self):
        if self.verbose:
            print('deactivating virtualenv', self.virtualenv_dir)
        if os.path.exists(SYSTEM_ACTIVATE):
            try:
                execfile(SYSTEM_ACTIVATE, dict(__file__=SYSTEM_ACTIVATE))
            except NameError:
                with open(SYSTEM_ACTIVATE) as f:
                    code = compile(f.read(), SYSTEM_ACTIVATE, 'exec')
                exec(code, dict(__file__=SYSTEM_ACTIVATE))
            sys.executable = os.path.join(os.path.dirname(SYSTEM_ACTIVATE), 'python')
        super(IsolatedTestClass, self).tearDown()
        modules = copy(sys.modules)
        for module in modules:
            if 'django' in module:
                del sys.modules[module]

    def setUp(self):
        super(IsolatedTestClass, self).setUp()
        if os.path.exists(SYSTEM_ACTIVATE):
            subprocess.check_call([
                'virtualenv', '--always-copy', '-q', '--python=%s' % sys.executable,
                self.virtualenv_dir
            ])
            activate_temp = os.path.join(self.virtualenv_dir, 'bin', 'activate_this.py')
            try:
                execfile(activate_temp, dict(__file__=activate_temp))
            except NameError:
                with open(activate_temp) as f:
                    code = compile(f.read(), activate_temp, 'exec')
                exec(code, dict(__file__=activate_temp))
            if self.verbose:
                print('activating virtualenv', self.virtualenv_dir)
            sys.executable = os.path.join(self.virtualenv_dir, 'bin', 'python')
            os.environ['VIRTUAL_ENV'] = self.virtualenv_dir


def get_latest_django(latest_stable=False):
    if sys.version_info < (3, 4) and not latest_stable:
        dj_ver = '1.8'
        match = 'Django<1.9'
    elif sys.version_info < (3, 4) and latest_stable:
        dj_ver = '1.11'
        match = 'Django<2.0'
    elif sys.version_info < (3, 5):
        dj_ver = '2.0'
        match = 'Django<2.1'
    else:
        dj_ver = '2.1'
        match = 'Django<2.2'
    return dj_ver, match
