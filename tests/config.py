import copy
import os
import sys
import tempfile
from argparse import Namespace
from unittest.mock import patch

from six import StringIO
from tzlocal import get_localzone

from djangocms_installer import config
from djangocms_installer.config import data
from djangocms_installer.install import check_install
from djangocms_installer.utils import less_than_version, supported_versions

from .base import BaseTestClass, get_stable_django, unittest


class TestConfig(BaseTestClass):
    def test_default_config(self):
        dj_version, dj_match = get_stable_django(latest=True)

        conf_data = config.parse(
            ["--db=postgres://user:pwd@host/dbname", "-q", "-p" + self.project_dir, "example_prj"]
        )

        self.assertEqual(conf_data.project_name, "example_prj")

        self.assertEqual(conf_data.cms_version, "3.8")
        self.assertEqual(conf_data.django_version, dj_version)
        self.assertEqual(conf_data.i18n, "yes")
        self.assertEqual(conf_data.reversion, "yes")
        self.assertEqual(conf_data.permissions, "no")
        self.assertEqual(conf_data.use_timezone, "yes")
        self.assertEqual(conf_data.db, "postgres://user:pwd@host/dbname")

        self.assertEqual(conf_data.no_db_driver, False)
        self.assertEqual(conf_data.no_deps, False)
        self.assertEqual(conf_data.no_sync, False)
        self.assertEqual(conf_data.plugins, False)
        self.assertEqual(conf_data.requirements_file, None)

    def test_cli_config(self):
        with self.assertRaises(SystemExit):
            dj_version = "1.8"
            config.parse(
                [
                    "-q",
                    "--db=postgres://user:pwd@host/dbname",
                    "--cms-version=stable",
                    "--django-version={}".format(dj_version),
                    "--i18n=no",
                    "--reversion=no",
                    "--permissions=no",
                    "--use-tz=no",
                    "-tEurope/Rome",
                    "-len-CA",
                    "-lde",
                    "-lit",
                    "-p" + self.project_dir,
                    "example_prj",
                ]
            )

        dj_version, dj_match = get_stable_django()
        cms_version = "develop"
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--django-version={}".format(dj_version),
                "--cms-version={}".format(cms_version),
                "--i18n=no",
                "--reversion=no",
                "--permissions=no",
                "--use-tz=no",
                "-tEurope/Rome",
                "-len",
                "-lde",
                "-lit",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertEqual(conf_data.project_name, "example_prj")

        self.assertEqual(str(conf_data.cms_version), data.DJANGOCMS_DEVELOP)
        self.assertEqual(str(conf_data.django_version), dj_version)
        self.assertEqual(conf_data.i18n, "yes")
        self.assertEqual(conf_data.reversion, "no")
        self.assertEqual(conf_data.permissions, "no")
        self.assertEqual(conf_data.use_timezone, "no")
        self.assertEqual(conf_data.timezone, "Europe/Rome")
        self.assertEqual(conf_data.languages, ["en", "de", "it"])
        self.assertEqual(conf_data.project_directory, self.project_dir)
        self.assertEqual(conf_data.db, "postgres://user:pwd@host/dbname")
        self.assertEqual(conf_data.db_driver, "psycopg2")

        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--django-version={}".format(dj_version),
                "--cms-version={}".format(cms_version),
                "--i18n=no",
                "--reversion=no",
                "--permissions=no",
                "--use-tz=no",
                "-tEurope/Rome",
                "-len,de,it",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertEqual(conf_data.project_name, "example_prj")

        self.assertEqual(str(conf_data.cms_version), data.DJANGOCMS_DEVELOP)
        self.assertEqual(str(conf_data.django_version), dj_version)
        self.assertEqual(conf_data.i18n, "yes")
        self.assertEqual(conf_data.reversion, "no")
        self.assertEqual(conf_data.permissions, "no")
        self.assertEqual(conf_data.use_timezone, "no")
        self.assertEqual(conf_data.timezone, "Europe/Rome")
        self.assertEqual(conf_data.languages, ["en", "de", "it"])
        self.assertEqual(conf_data.project_directory, self.project_dir)
        self.assertEqual(conf_data.db, "postgres://user:pwd@host/dbname")
        self.assertEqual(conf_data.db_driver, "psycopg2")

    def test_version_misdj_match(self):
        with self.assertRaises(SystemExit):
            config.parse(
                [
                    "-q",
                    "--db=postgres://user:pwd@host/dbname",
                    "--cms-version=stable",
                    "--django-version=1.4",
                    "--i18n=no",
                    "--reversion=no",
                    "--permissions=no",
                    "--use-tz=no",
                    "-tEurope/Rome",
                    "-len",
                    "-lde",
                    "-lit",
                    "-p" + self.project_dir,
                    "example_prj",
                ]
            )

    def test_cli_config_commaseparated_languages(self):
        conf_data = config.parse(
            ["-q", "--db=postgres://user:pwd@host/dbname", "-len,de,it", "-p" + self.project_dir, "example_prj"]
        )

        self.assertEqual(conf_data.languages, ["en", "de", "it"])

    def test_cli_config_missing_param(self):
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                with self.assertRaises(SystemExit) as e:
                    conf_data = config.parse(["-q"])
                    self.assertEqual(conf_data.languages, ["en"])
        self.assertEqual(e.exception.code, 2)

    def test_cli_config_input(self):
        templates = tempfile.mkdtemp()
        prj_dir = "param_w_input"
        user_input = [
            "sqlite://localhost/project.db",  # db
            "stable",  # cms_version
            "stable",  # django_version
            "yes",  # i18n
            "",  # reversion
            "en",  # languages
            "",  # timezone
            "yes",  # use_timezone
            "yes",  # permissions
            "yes",  # bootstrap
            "not_exist",  # templates
            templates,  # templates
            "yes",  # starting_page
        ]
        with patch("builtins.input", side_effect=user_input):
            conf_data = config.parse(["-w", "-t=Europe/Rome", "-len", "-lde", "-eno", prj_dir])
        self.assertEqual(conf_data.languages, ["en"])
        self.assertEqual(conf_data.use_timezone, "yes")
        self.assertEqual(conf_data.timezone, "Europe/Rome")
        self.assertEqual(conf_data.permissions, "yes")
        self.assertEqual(conf_data.i18n, "yes")
        self.assertEqual(conf_data.django_version, data.DJANGO_STABLE)
        self.assertEqual(conf_data.cms_version, data.DJANGOCMS_STABLE)
        self.assertEqual(conf_data.db, "sqlite://localhost/project.db")
        self.assertEqual(conf_data.bootstrap, True)
        self.assertEqual(conf_data.reversion, "no")
        self.assertEqual(conf_data.starting_page, True)
        self.assertEqual(conf_data.templates, templates)
        self.assertEqual(conf_data.templates, templates)

    def test_cli_config_comma_languages_with_space(self):
        conf_data = config.parse(
            ["-q", "--db=postgres://user:pwd@host/dbname", "-len , de , it", "-p" + self.project_dir, "example_prj"]
        )

        self.assertEqual(conf_data.languages, ["en", "de", "it"])

    def test_invalid_choices(self):
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                with self.assertRaises(SystemExit) as error:
                    config.parse(
                        [
                            "-q",
                            "--db=postgres://user:pwd@host/dbname",
                            "--cms-version=2.6",
                            "--django-version=1.1",
                            "--i18n=no",
                            "-p" + self.project_dir,
                            "example_prj",
                        ]
                    )
        self.assertEqual(error.exception.code, 2)
        self.assertTrue(self.stderr.getvalue().find("--cms-version/-v: invalid choice: '2.6'") > -1)

    def test_invalid_project_name(self):
        with patch("sys.stdout", self.stdout):
            stderr_tmp = StringIO()
            with patch("sys.stderr", stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    config.parse(["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, "test"])
            self.assertEqual(error.exception.code, 3)
            self.assertTrue(stderr_tmp.getvalue().find('Project name "test" is not valid') > -1)

            stderr_tmp = StringIO()
            with patch("sys.stderr", stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    config.parse(["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, "assert"])
            self.assertEqual(error.exception.code, 3)
            self.assertTrue(stderr_tmp.getvalue().find('Project name "assert" is not valid') > -1)

            stderr_tmp = StringIO()
            with patch("sys.stderr", stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    config.parse(["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, "values"])
            self.assertEqual(error.exception.code, 3)
            self.assertTrue(stderr_tmp.getvalue().find('Project name "values" is not valid') > -1)

            stderr_tmp = StringIO()
            with patch("sys.stderr", stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    config.parse(
                        ["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, "project-name"]
                    )
            self.assertEqual(error.exception.code, 3)
            self.assertTrue(stderr_tmp.getvalue().find('Project name "project-name" is not valid') > -1)

            stderr_tmp = StringIO()
            with patch("sys.stderr", stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    config.parse(
                        ["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, "project.name"]
                    )
            self.assertEqual(error.exception.code, 3)
            self.assertTrue(stderr_tmp.getvalue().find('Project name "project.name" is not valid') > -1)

            stderr_tmp = StringIO()
            with patch("sys.stderr", stderr_tmp):
                with self.assertRaises(SystemExit) as error:
                    config.parse(
                        ["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, "project?name"]
                    )
            self.assertEqual(error.exception.code, 3)
            self.assertTrue(stderr_tmp.getvalue().find('Project name "project?name" is not valid') > -1)

    def test_invalid_project_path(self):
        prj_dir = "example_prj"
        existing_path = os.path.join(self.project_dir, prj_dir)
        os.makedirs(existing_path)
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse(
                        ["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, prj_dir, "-s"]
                    )
                    self.assertEqual(conf_data.project_path, existing_path)
        self.assertEqual(error.exception.code, 4)
        out = self.stderr.getvalue()
        expected = 'Path "{}/{}" already exists, please choose a different one'.format(self.project_dir, prj_dir)
        self.assertTrue(out.find(expected) > -1)

    def test_invalid_project_dir(self):
        prj_dir = "example_prj"
        existing_path = os.path.join(self.project_dir, "a_file")
        with open(existing_path, "w") as f:
            f.write("")
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                with self.assertRaises(SystemExit) as error:
                    conf_data = config.parse(
                        ["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, prj_dir]
                    )
                    self.assertEqual(conf_data.project_path, existing_path)
        self.assertEqual(error.exception.code, 4)
        self.assertTrue(
            self.stderr.getvalue().find('Path "%s" already exists and is not empty' % self.project_dir) > -1
        )

    def test_invalid_project_dir_skip(self):
        prj_dir = "example_prj"
        existing_path = os.path.join(self.project_dir, "a_file")
        with open(existing_path, "w") as f:
            f.write("")
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                config.parse(["-q", "-s", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, prj_dir])
        self.assertFalse(
            self.stderr.getvalue().find('Path "%s" already exists and is not empty' % self.project_dir) > -1
        )

    def test_valid_project_dir(self):
        prj_dir = "example_prj"
        existing_path = os.path.join(self.project_dir, ".hidden_file")
        with open(existing_path, "w") as f:
            f.write("")
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                config.parse(["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, prj_dir])
        self.assertFalse(
            self.stderr.getvalue().find('Path "%s" already exists and is not empty' % self.project_dir) > -1
        )

    def test_invalid_django_settings_module(self):
        prj_dir = "example_prj"
        existing_path = os.path.join(self.project_dir, ".hidden_file")
        with open(existing_path, "w") as f:
            f.write("")
        os.environ["DJANGO_SETTINGS_MODULE"] = "some_module.settings"
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                with self.assertRaises(SystemExit) as error:
                    config.parse(["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, prj_dir])
        self.assertEqual(error.exception.code, 10)
        self.assertTrue(self.stderr.getvalue().find("DJANGO_SETTINGS_MODULE") > -1)
        self.assertTrue(self.stderr.getvalue().find("some_module.settings") > -1)

    def test_valid_django_settings_module(self):
        prj_dir = "example_prj"
        existing_path = os.path.join(self.project_dir, ".hidden_file")
        with open(existing_path, "w") as f:
            f.write("")
        os.environ["DJANGO_SETTINGS_MODULE"] = "example_prj.settings"
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                config.parse(["-q", "--db=postgres://user:pwd@host/dbname", "-p" + self.project_dir, prj_dir])
        self.assertFalse(self.stderr.getvalue().find("DJANGO_SETTINGS_MODULE") > -1)
        self.assertFalse(self.stderr.getvalue().find("some_module.settings") > -1)

    def test_latest_version(self):
        self.assertEqual(less_than_version("2.4"), "2.5")
        self.assertEqual(less_than_version("3"), "3.1")
        self.assertEqual(less_than_version("3.0.1"), "3.1.1")

    def test_supported_versions(self):
        dj_version, dj_match = get_stable_django(latest=True)

        self.assertEqual(supported_versions("stable", "stable"), (dj_version, "3.8"))
        self.assertEqual(supported_versions("stable", "3.1.10"), (dj_version, None))
        self.assertEqual(supported_versions("stable", "beta"), (dj_version, data.DJANGOCMS_BETA))
        self.assertEqual(supported_versions("stable", "develop"), (dj_version, data.DJANGOCMS_DEVELOP))
        self.assertEqual(supported_versions("lts", "stable"), ("2.2", "3.8"))
        self.assertEqual(supported_versions("lts", "lts"), ("2.2", "3.8"))

        with self.assertRaises(RuntimeError):
            supported_versions("stable", "2.4"), ("1.5", "2.4")
        with self.assertRaises(RuntimeError):
            supported_versions("1.5", "stable"), ("1.8", "3.1")

        with self.assertRaises(RuntimeError):
            self.assertEqual(supported_versions("1.9", "stable"), ("1.9", "3.5"))
            self.assertEqual(supported_versions("1.8", "stable"), ("1.8", "3.5"))
            self.assertEqual(supported_versions("1.9", "3.5"), ("1.9", "3.5"))
            self.assertEqual(supported_versions("1.8", "lts"), ("1.8", "3.7"))
            self.assertEqual(supported_versions("1.8.3", "stable"), (None, "3.6"))

    def test_requirements(self):
        """
        Test for different configuration and package versions
        """
        dj_version, dj_match = get_stable_django(lts=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--cms-version=3.7",
                "--django-version={}".format(dj_version),
                "--i18n=no",
                "-f",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )
        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_37) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor>=4.0") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style>=2.0") > -1)
        self.assertTrue(conf_data.requirements.find("django-filer") > -1)
        self.assertTrue(conf_data.requirements.find("cmsplugin-filer") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-file") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") > -1)
        self.assertTrue(conf_data.requirements.find("psycopg2") > -1)

        dj_version, dj_match = get_stable_django(latest=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=stable",
                "--django-version={}".format(dj_version),
                "--reversion=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_38) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("cmsplugin-filer") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor>=4.0") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-bootstrap4") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-file") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-flash") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-googlemap") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-inherit") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-link") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-picture") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-style") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-teaser") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-video") > -1)
        self.assertTrue(conf_data.requirements.find("psycopg2") > -1)

        dj_version, dj_match = get_stable_django(lts=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=develop",
                "--django-version={}".format(dj_version),
                "-f",
                "--reversion=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style") > -1)
        self.assertTrue(conf_data.requirements.find("django-filer") > -1)
        self.assertTrue(conf_data.requirements.find("cmsplugin-filer") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-bootstrap4") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-file") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-flash") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-googlemap") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-inherit") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-link") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-picture") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-style") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-teaser") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-video") > -1)
        self.assertTrue(conf_data.requirements.find("psycopg2") > -1)

        with self.assertRaises(SystemExit):
            dj_version = "1.8"
            conf_data = config.parse(
                [
                    "-q",
                    "--db=postgres://user:pwd@host/dbname",
                    "--i18n=no",
                    "--cms-version=develop",
                    "--django-version={}".format(dj_version),
                    "-f",
                    "--reversion=yes",
                    "-p" + self.project_dir,
                    "example_prj",
                ]
            )

        dj_version, dj_match = get_stable_django(latest=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=develop",
                "--django-version={}".format(dj_version),
                "-f",
                "--reversion=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("django-treebeard") > -1)

        dj_version, dj_match = get_stable_django()
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=develop",
                "--django-version={}".format(dj_version),
                "-f",
                "--reversion=yes",
                "-z=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("https://github.com/divio/djangocms-link") > -1)
        self.assertTrue(conf_data.requirements.find("https://github.com/divio/djangocms-style") > -1)
        self.assertTrue(conf_data.requirements.find("https://github.com/divio/djangocms-googlemap") > -1)
        self.assertTrue(conf_data.requirements.find("https://github.com/divio/djangocms-snippet") > -1)
        self.assertTrue(conf_data.requirements.find("https://github.com/divio/djangocms-video") > -1)
        self.assertTrue(conf_data.requirements.find("https://github.com/divio/djangocms-bootstrap4") > -1)
        self.assertTrue(conf_data.requirements.find("https://github.com/divio/djangocms-admin-style") > -1)
        self.assertTrue(conf_data.requirements.find("https://github.com/divio/djangocms-text-ckeditor") > -1)
        self.assertTrue(conf_data.requirements.find("pytz") > -1)

        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=3.7",
                "--django-version={}".format(dj_version),
                "-f",
                "--reversion=yes",
                "-z=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_37) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor>=4.0") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style") > -1)
        self.assertTrue(conf_data.requirements.find("pytz") > -1)

        dj_version, dj_match = get_stable_django(lts=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=3.7",
                "--django-version={}".format(dj_version),
                "-f",
                "--reversion=yes",
                "-z=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_37) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor>=4.0") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style") > -1)
        self.assertTrue(conf_data.requirements.find("pytz") > -1)

        dj_version, dj_match = get_stable_django(lts=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=develop",
                "--django-version={}".format(dj_version),
                "--reversion=yes",
                "-z=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-teaser") == -1)
        self.assertTrue(conf_data.requirements.find("south") == -1)

        dj_version, dj_match = get_stable_django()
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=develop",
                "--django-version={}".format(dj_version),
                "--reversion=yes",
                "--no-plugins",
                "-z=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style/archive/master") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-teaser") == -1)
        self.assertTrue(conf_data.requirements.find("south") == -1)

        dj_version, dj_match = get_stable_django(lts=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--i18n=no",
                "--cms-version=develop",
                "--django-version={}".format(dj_version),
                "--reversion=yes",
                "--no-plugins",
                "-z=yes",
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style/archive/master.zip") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-teaser/archive/master.zip") == -1)
        self.assertTrue(conf_data.requirements.find("south") == -1)

        dj_version, dj_match = get_stable_django(lts=True)
        requirements_21 = [
            "-q",
            "--db=postgres://user:pwd@host/dbname",
            "--i18n=no",
            "--cms-version=develop",
            "--django-version={}".format(dj_version),
            "--reversion=yes",
            "--no-plugins",
            "-z=yes",
            "-p" + self.project_dir,
            "example_prj",
        ]

        conf_data = config.parse(requirements_21)

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_DEVELOP) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)
        self.assertFalse(conf_data.requirements.find("django-reversion") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-text-ckeditor") == -1)
        self.assertTrue(conf_data.requirements.find("djangocms-admin-style/archive/master.zip") > -1)
        self.assertTrue(conf_data.requirements.find("djangocms-teaser/archive/master.zip") == -1)
        self.assertTrue(conf_data.requirements.find("south") == -1)
        self.assertTrue(conf_data.requirements.find("psycopg2") > -1)

        dj_version, dj_match = get_stable_django(lts=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--cms-version=lts",
                "--django-version={}".format(dj_version),
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_38) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)

        dj_version, dj_match = get_stable_django(latest=True)
        conf_data = config.parse(
            [
                "-q",
                "--db=postgres://user:pwd@host/dbname",
                "--cms-version=stable",
                "--django-version={}".format(dj_version),
                "-p" + self.project_dir,
                "example_prj",
            ]
        )

        self.assertTrue(conf_data.requirements.find(config.data.DJANGOCMS_38) > -1)
        self.assertTrue(conf_data.requirements.find(dj_match) > -1)

    def test_bootstrap(self):
        """
        Verify handling of bootstrap parameter
        """
        conf_data = config.parse(["-q", "-p" + self.project_dir, "example_prj"])
        self.assertFalse(conf_data.bootstrap)

        conf_data = config.parse(["--bootstrap=yes", "-q", "-p" + self.project_dir, "example_prj"])
        self.assertTrue(conf_data.bootstrap)

    def test_starting_page(self):
        """
        Verify handling of starting-page parameter
        """
        conf_data = config.parse(["-q", "-p" + self.project_dir, "example_prj"])
        self.assertFalse(conf_data.starting_page)

        conf_data = config.parse(["--starting-page=yes", "-q", "-p" + self.project_dir, "example_prj"])
        self.assertTrue(conf_data.starting_page)

    def test_auto_i18n(self):
        """
        Verify setting automatic i18n support if multiple languages
        """
        conf_data = config.parse(["-q", "-len,de" "--i18n=no", "-p" + self.project_dir, "example_prj"])
        self.assertTrue(conf_data.i18n)

    def test_utc(self):
        """
        Verify handling UTC default
        """
        default_tz = get_localzone()

        conf_data = config.parse(["-q", "-p" + self.project_dir, "example_prj"])
        self.assertEqual(str(conf_data.timezone), default_tz.zone)

        conf_data = config.parse(["-q", "--utc", "-p" + self.project_dir, "example_prj"])
        self.assertEqual(conf_data.timezone, "UTC")

    @patch("tzlocal.get_localzone")
    def test_timezone(self, mock_get_localzone):
        """
        Verify handling problem with detecting timezone
        """
        mock_get_localzone.return_value = "local"
        conf_data = config.parse(["-q", "-p" + self.project_dir, "example_prj"])
        self.assertEqual(str(conf_data.timezone), "UTC")

    def test_templates(self):
        """-
        Verify handling of valid (existing) and invalid (non-existing) templates directory parameter
        """
        conf_data = config.parse(["--templates=/foo/bar", "-q", "-p" + self.project_dir, "example_prj"])
        self.assertFalse(conf_data.templates)

        tpl_path = os.path.join(os.path.dirname(__file__), "test_templates")

        conf_data = config.parse(["--templates=%s" % tpl_path, "-q", "-p" + self.project_dir, "example_prj"])
        self.assertEqual(conf_data.templates, tpl_path)

    def suspend_test_check_install(self):
        import pip

        # discard the argparser errors
        with patch("sys.stdout", self.stdout):
            with patch("sys.stderr", self.stderr):
                # clean the virtualenv
                try:
                    pip.main(["uninstall", "-y", "psycopg2"])
                except pip.exceptions.UninstallationError:
                    # package not installed, all is fine
                    pass
                try:
                    pip.main(["uninstall", "-y", "pillow"])
                except pip.exceptions.UninstallationError:
                    # package not installed, all is fine
                    pass
                try:
                    pip.main(["uninstall", "-y", "mysql-python"])
                except pip.exceptions.UninstallationError:
                    # package not installed, all is fine
                    pass

                # Check postgres / pillow
                conf_data = config.parse(
                    [
                        "-q",
                        "--db=postgres://user:pwd@host/dbname",
                        "--django-version=1.8",
                        "--i18n=no",
                        "-f",
                        "-p" + self.project_dir,
                        "example_prj",
                    ]
                )
                with self.assertRaises(EnvironmentError) as context_error:
                    check_install(conf_data)
                self.assertTrue(str(context_error.exception).find("Pillow is not installed") > -1)
                self.assertTrue(str(context_error.exception).find("PostgreSQL driver is not installed") > -1)

                # Check mysql
                conf_data = config.parse(
                    [
                        "-q",
                        "--db=mysql://user:pwd@host/dbname",
                        "--django-version=1.8",
                        "--i18n=no",
                        "-f",
                        "-p" + self.project_dir,
                        "example_prj",
                    ]
                )
                with self.assertRaises(EnvironmentError) as context_error:
                    check_install(conf_data)
                self.assertTrue(str(context_error.exception).find("MySQL driver is not installed") > -1)

    def test_show_plugins(self):
        sys.stdout = StringIO()
        try:
            config.show_plugins()
        finally:
            sys.stdout = sys.__stdout__

    def test_show_requirements(self):
        sys.stdout = StringIO()
        dj_version, dj_match = get_stable_django()

        try:
            conf_data = config.parse(
                [
                    "-q",
                    "--db=mysql://user:pwd@host/dbname",
                    "--django-version={}".format(dj_version),
                    "--i18n=no",
                    "-f",
                    "-p" + self.project_dir,
                    "example_prj",
                ]
            )
            config.show_requirements(conf_data)
        finally:
            sys.stdout = sys.__stdout__


class TestBaseConfig(unittest.TestCase):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_dir = os.path.join(base_dir, "tests/fixtures/configs")
    args = ["--config-file", "-s", "-q", "example_prj"]
    django_version = data.DJANGO_VERSION_MATRIX["stable"]
    config_fixture = Namespace(
        **{
            "bootstrap": False,
            "cms_version": data.CMS_VERSION_MATRIX["stable"],
            "db": "sqlite://localhost/project.db",
            "django_version": django_version,
            "dump_reqs": False,
            "extra_settings": None,
            "filer": True,
            "i18n": "yes",
            "languages": ["en"],
            "no_db_driver": False,
            "no_deps": False,
            "noinput": True,
            "no_sync": False,
            "no_user": False,
            "permissions": "yes",
            "pip_options": "",
            "plugins": False,
            "project_directory": os.path.abspath("."),
            "project_name": "example_prj",
            "requirements_file": None,
            "reversion": "yes",
            "skip_project_dir_check": True,
            "starting_page": False,
            "template": None,
            "templates": False,
            "timezone": get_localzone().zone,
            "use_timezone": "yes",
            "utc": False,
            "no_plugins": False,
            "verbose": False,
            "wizard": False,
            "delete_project_dir": False,
        }
    )

    def __init__(self, *args, **kwargs):
        self.config_not_exists = self.conf("config-dump.ini")
        super().__init__(*args, **kwargs)

    def tearDown(self):
        if os.path.isfile(self.config_not_exists):
            os.remove(self.config_not_exists)

    def conf(self, filename):
        return os.path.join(self.config_dir, filename)

    def unused(self, config_data):
        """Remove not configurable keys."""
        for attr in (
            "config_dump",
            "config_file",
            "db_driver",
            "db_parsed",
            "project_path",
            "settings_path",
            "urlconf_path",
        ):
            delattr(config_data, attr)
        # When `requirements` arg is used then requirements attr isn't set.
        if hasattr(config_data, "requirements"):
            delattr(config_data, "requirements")

    def test_parse_config_file(self, *args):
        """Tests .config.__init__._parse_config_file function."""
        dj_version, __ = get_stable_django(latest=True)
        dj_lts_version, __ = get_stable_django(lts=True)

        with self.assertRaises(SystemExit) as error:
            config.parse(self.args[0:1] + [self.conf("config-not-exists.ini")] + self.args[1:])
            self.assertEqual(7, error.exception.code)

        args = self.args[0:1] + [self.conf("config-01.ini")] + self.args[1:]
        config_data = config.parse(args)
        self.unused(config_data)
        self.assertEqual(self.config_fixture, config_data)  # Check if config value and changed value equals.

        test_data = [
            (
                "config-02.ini",
                None,
                (
                    ("cms_version", "3.7"),
                    ("db", "postgres://user:pwd@host:54321/dbname"),
                    ("django_version", dj_lts_version),
                ),
            ),
            (
                "config-03.ini",
                None,
                (
                    ("cms_version", "3.8"),
                    ("i18n", "no"),
                    ("django_version", dj_version),
                ),
            ),
            ("config-04.ini", None, (("cms_version", "3.8"), ("use_timezone", "no"))),
            ("config-05.ini", None, (("cms_version", "3.8"), ("timezone", "Europe/London"))),
            ("config-06.ini", None, (("cms_version", "3.8"), ("reversion", "no"))),
            (
                "config-07.ini",
                None,
                (("cms_version", "3.8"), ("permissions", "no"), ("django_version", dj_lts_version)),
            ),
            (
                "config-08.ini",
                None,
                (("cms_version", "3.7"), ("i18n", "no"), ("languages", ["ru"]), ("django_version", dj_lts_version)),
            ),
            (
                "config-09.ini",
                None,
                (
                    ("cms_version", "3.8"),
                    ("i18n", "yes"),
                    ("languages", ["en", "ru"]),
                    ("django_version", dj_lts_version),
                ),
            ),
            ("config-10.ini", "django_version", dj_lts_version),
            ("config-11.ini", None, (("project_directory", "/test/me"), ("cms_version", "3.7"))),
            ("config-12.ini", None, (("bootstrap", True), ("django_version", dj_lts_version))),
            ("config-13.ini", "templates", "."),
            ("config-14.ini", "starting_page", True),
            ("config-15.ini", "plugins", True),
            ("config-16.ini", "dump_reqs", True),
            ("config-17.ini", "noinput", True),
            ("config-18.ini", "filer", True),
            ("config-19.ini", "requirements_file", "/test/reqs"),
            ("config-20.ini", "no_deps", True),
            ("config-21.ini", "no_db_driver", True),
            ("config-22.ini", "no_sync", True),
            ("config-23.ini", "no_user", True),
            ("config-24.ini", "template", "/test/template"),
            ("config-25.ini", "extra_settings", "/test/extra_settings"),
            ("config-26.ini", "skip_project_dir_check", True),
            ("config-27.ini", "utc", True),
            ("config-28.ini", "no_plugins", True),
            ("config-30.ini", "verbose", True),
            ("config-32.ini", "delete_project_dir", True),
        ]
        fixture = copy.copy(self.config_fixture)
        for filename, key, val in test_data:
            if type(val) == tuple:
                for subkey, subval in val:
                    setattr(fixture, subkey, subval)  # Change value.
            else:
                setattr(fixture, key, val)  # Change value.
            args = self.args[0:1] + [self.conf(filename)] + self.args[1:]  # Load new config.
            config_data = config.parse(args)
            self.unused(config_data)
            self.assertEqual(fixture, config_data)  # Check if config value and changed value equals.

    @patch("sys.stdout")
    @patch("sys.stderr")
    def test_dump_config_file(self, *args):
        """Tests .config.ini.dump_config_file function."""
        config_exists = self.conf("config-01.ini")

        with self.assertRaises(SystemExit) as error:
            config.parse(["--config-dump", config_exists] + self.args[1:] + ["-p", "."])
            self.assertEqual(8, error.exception.code)

        config.parse(["--config-dump", self.config_not_exists] + self.args[1:] + ["-p", "."])
        self.assertTrue(os.path.isfile(self.config_not_exists))

        fixture = copy.copy(self.config_fixture)
        fixture.timezone = get_localzone().zone
        # Load dumped config.
        args = self.args[0:1] + [self.config_not_exists] + self.args[1:]
        config_data = config.parse(args)
        self.unused(config_data)
        self.assertEqual(fixture, config_data)
