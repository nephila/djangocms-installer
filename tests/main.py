#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tempfile
import shutil

from aldryn_installer import main
from . import BaseTestClass, PatchStd

class TestMain(BaseTestClass):

    def test_main_invocation(self):
        with PatchStd(self.stdout, self.stderr):
            self.project_dir = tempfile.mkdtemp()
            sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                   '-len',
                                   '-q', '-u', '-p'+self.project_dir, 'test_project']
            main.execute()
            # Checking we successfully completed the whole process
            self.assertTrue("Get into '%s' directory and type 'python manage.py runserver' to start your project" % self.project_dir in self.stdout.getvalue())

    def test_two_langs_invocation(self):
        with PatchStd(self.stdout, self.stderr):
            self.project_dir = tempfile.mkdtemp()
            sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                   '-len', '-lfr',
                                   '-q', '-u', '-p'+self.project_dir, 'test_project']
            main.execute()
            # Checking we successfully completed the whole process
            self.assertTrue("Get into '%s' directory and type 'python manage.py runserver' to start your project" % self.project_dir in self.stdout.getvalue())

    def manual_test_develop(self):
        with PatchStd(self.stdout, self.stderr):
            self.project_dir = tempfile.mkdtemp()
            sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                   '-len', '--cms-version=develop',
                                   '-q', '-u', '-p'+self.project_dir, 'test_project']
            main.execute()
            # Checking we successfully completed the whole process
            self.assertTrue("Get into '%s' directory and type 'python manage.py runserver' to start your project" % self.project_dir in self.stdout.getvalue())

    def manual_test_django_1_4(self):
        with PatchStd(self.stdout, self.stderr):
            self.project_dir = tempfile.mkdtemp()
            sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                   '-len', '--django-version=1.4',
                                   '-q', '-u', '-p'+self.project_dir, 'test_project']
            main.execute()
            # Checking we successfully completed the whole process
            self.assertTrue("Get into '%s' directory and type 'python manage.py runserver' to start your project" % self.project_dir in self.stdout.getvalue())

    def manual_test_django_1_5(self):
        with PatchStd(self.stdout, self.stderr):
            self.project_dir = tempfile.mkdtemp()
            sys.argv = ['main'] + ['--db=sqlite://localhost/test.db',
                                   '-len', '--django-version=1.5',
                                   '-q', '-u', '-p'+self.project_dir, 'test_project']
            main.execute()
            # Checking we successfully completed the whole process
            self.assertTrue("Get into '%s' directory and type 'python manage.py runserver' to start your project" % self.project_dir in self.stdout.getvalue())
