import os
import subprocess
import sys
from shutil import rmtree
from subprocess import CalledProcessError
from tempfile import mkdtemp
from unittest.mock import patch

from djangocms_installer import config, install, main

from .base import IsolatedTestClass, get_stable_django


class TestMain(IsolatedTestClass):
    def test_requirements_invocation(self):
        dj_version, dj_match = get_stable_django(latest=True)

        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                sys.argv = ["main"] + [
                    "--db=sqlite://localhost/test.db",
                    "-len",
                    "--cms-version=stable",
                    "-R",
                    "-q",
                    "-u",
                    "-p" + self.project_dir,
                    "example_prj",
                ]
                main.execute()
        stdout = self.stdout.getvalue()
        self.assertTrue(stdout.find(dj_match) > -1)
        self.assertFalse(stdout.find("django-reversion") > -1)
        self.assertTrue(stdout.find("djangocms-text-ckeditor") > -1)
        self.assertTrue(stdout.find("djangocms-admin-style") > -1)
        self.assertTrue(stdout.find("djangocms-bootstrap4") > -1)
        self.assertTrue(stdout.find("djangocms-file") > -1)
        self.assertTrue(stdout.find("djangocms-flash") == -1)
        self.assertTrue(stdout.find("djangocms-googlemap") > -1)
        self.assertTrue(stdout.find("djangocms-inherit") == -1)
        self.assertTrue(stdout.find("djangocms-link") > -1)
        self.assertTrue(stdout.find("djangocms-picture") > -1)
        self.assertTrue(stdout.find("djangocms-style") > -1)
        self.assertTrue(stdout.find("cmsplugin-filer") == -1)
        self.assertTrue(stdout.find("djangocms-teaser") == -1)
        self.assertTrue(stdout.find("djangocms-video") > -1)

    def cleanup_ask(self):
        dj_version, dj_match = get_stable_django()

        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                conf_data = config.parse(
                    [
                        "-q",
                        "--db=postgres://user:pwd@host/dbname",
                        "--i18n=no",
                        "--django-version=%s" % dj_version,
                        "-f",
                        "-p" + self.project_dir,
                        "example_prj",
                    ]
                )
                install.cleanup_directory(conf_data)
                self.assertFalse(os.path.exists(self.project_dir))

    def cleanup_skip(self):
        dj_version, dj_match = get_stable_django()

        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                conf_data = config.parse(
                    [
                        "-q",
                        "-s",
                        "--db=postgres://user:pwd@host/dbname",
                        "--i18n=no",
                        "--django-version=%s" % dj_version,
                        "-f",
                        "-p" + self.project_dir,
                        "example_prj",
                    ]
                )
                install.cleanup_directory(conf_data)
                self.assertTrue(os.path.exists(self.project_dir))

    def test_main_invocation(self):
        dj_version, dj_match = get_stable_django()
        base_dir = mkdtemp()
        project_dir = os.path.join(base_dir, "example_prj")
        original_dir = os.getcwd()
        os.chdir(base_dir)
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                sys.argv = ["main"] + [
                    "--db=sqlite://localhost/test.db",
                    "-len",
                    "--cms-version=stable",
                    "--django=%s" % dj_version,
                    "-q",
                    "-u",
                    "--verbose",
                    "example_prj",
                ]
                main.execute()
                self.assertTrue(os.path.exists(os.path.join(project_dir, "static")))
                self.assertTrue(os.path.exists(os.path.join(project_dir, "requirements.txt")))
                self.assertTrue(os.path.exists(os.path.join(project_dir, "example_prj", "static")))
                with open(os.path.join(project_dir, "requirements.txt")) as req_file:
                    text = req_file.read()
                    self.assertTrue(text.find("djangocms-text-ckeditor") > -1)
                # Checking we successfully completed the whole process
                self.assertTrue("Successfully installed " in self.stdout.getvalue())
                self.assertTrue(
                    (
                        'Get into "%s" directory and type "python manage.py runserver" to start your project'
                        % project_dir
                    )
                    in self.stdout.getvalue()
                )
        os.chdir(original_dir)
        rmtree(base_dir)

    def test_base_invocation(self):
        base_dir = mkdtemp()
        project_dir = os.path.join(base_dir, "example_prj")
        original_dir = os.getcwd()
        os.chdir(base_dir)
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                sys.argv = ["main"] + ["--cms-version=stable", "example_prj"]
                main.execute()
                self.assertTrue(os.path.exists(os.path.join(project_dir, "static")))
                self.assertTrue(os.path.exists(os.path.join(project_dir, "requirements.txt")))
                self.assertTrue(os.path.exists(os.path.join(project_dir, "example_prj", "static")))
                with open(os.path.join(project_dir, "requirements.txt")) as req_file:
                    text = req_file.read()
                    self.assertTrue(text.find("djangocms-text-ckeditor") > -1)
                self.assertTrue(
                    (
                        'Get into "%s" directory and type "python manage.py runserver" to start your project'
                        % project_dir
                    )
                    in self.stdout.getvalue()
                )
        os.chdir(project_dir)
        with patch("sys.stdout", self.stdout):
            out = subprocess.check_output(
                ["sqlite3", "project.db", 'SELECT COUNT(*) FROM auth_user WHERE username="admin"']
            )
            self.assertEqual(bytes(out), bytes(b"1\n"))
        os.chdir(original_dir)
        rmtree(base_dir)

    def test_two_langs_invocation(self):
        dj_version, dj_match = get_stable_django()

        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                sys.argv = ["main"] + [
                    "--db=sqlite://localhost/test.db",
                    "-len-GB",
                    "-lfr-fr",
                    "--cms-version=stable",
                    "--verbose",
                    "--django=%s" % dj_version,
                    "-q",
                    "-u",
                    "-p" + self.project_dir,
                    "example_prj",
                ]
                try:
                    main.execute()
                    # Checking we successfully completed the whole process
                    self.assertTrue(
                        (
                            'Get into "%s" directory and type "python manage.py runserver" to start your project'
                            % self.project_dir
                        )
                        in self.stdout.getvalue()
                    )
                except Exception as e:
                    print(e)

    def test_develop(self):
        dj_version, dj_match = get_stable_django(lts=True)

        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                sys.argv = ["main"] + [
                    "--db=sqlite://localhost/test.db",
                    "-len",
                    "--cms-version=develop",
                    "--django=%s" % dj_version,
                    "-q",
                    "-u",
                    "-p" + self.project_dir,
                    "example_prj",
                ]
                main.execute()
                # Checking we successfully completed the whole process
                self.assertTrue(
                    (
                        'Get into "%s" directory and type "python manage.py runserver" to start your project'
                        % self.project_dir
                    )
                    in self.stdout.getvalue()
                )

    def test_cleanup(self):
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                with self.assertRaises((CalledProcessError, EnvironmentError)):
                    sys.argv = ["main"] + [
                        "--db=postgres://user:pwd@host/dbname",
                        "-len",
                        "--no-db-driver",
                        "-c",
                        "-q",
                        "-u",
                        "-p" + self.project_dir,
                        "example_prj",
                    ]
                    main.execute()
        self.assertFalse(os.path.exists(self.project_dir))

    def test_no_cleanup(self):
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                with self.assertRaises((CalledProcessError, EnvironmentError)):
                    sys.argv = ["main"] + [
                        "--db=postgres://user:pwd@host/dbname",
                        "-len",
                        "--no-db-driver",
                        "-q",
                        "-u",
                        "-p" + self.project_dir,
                        "example_prj",
                    ]
                    main.execute()
        self.assertTrue(os.path.exists(self.project_dir))

    def test_i18n_urls(self):
        base_dir = mkdtemp()
        project_dir = os.path.join(base_dir, "example_prj")
        original_dir = os.getcwd()
        os.chdir(base_dir)
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                sys.argv = ["main"] + [
                    "--i18n=yes",
                    "--cms-version=stable",
                    "example_prj",
                ]
                main.execute()
                self.assertTrue(os.path.exists(os.path.join(project_dir, "example_prj", "urls.py")))
                with open(os.path.join(project_dir, "example_prj", "urls.py")) as urls_file:
                    urls = urls_file.read()
                    self.assertTrue(urls.find("urlpatterns += i18n_patterns(") > -1)
        os.chdir(original_dir)
        rmtree(base_dir)

    def test_noi18n_urls(self):
        base_dir = mkdtemp()
        project_dir = os.path.join(base_dir, "example_prj")
        original_dir = os.getcwd()
        os.chdir(base_dir)
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                sys.argv = ["main"] + [
                    "--i18n=no",
                    "--cms-version=stable",
                    "example_prj",
                ]
                main.execute()
                self.assertTrue(os.path.exists(os.path.join(project_dir, "example_prj", "urls.py")))
                with open(os.path.join(project_dir, "example_prj", "urls.py")) as urls_file:
                    urls = urls_file.read()
                    self.assertTrue(urls.find("urlpatterns += i18n_patterns(") == -1)
        os.chdir(original_dir)
        rmtree(base_dir)
