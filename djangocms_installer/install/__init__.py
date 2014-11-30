# -*- coding: utf-8 -*-
import os.path

import pip
from pip.exceptions import InstallationError
from pip.status_codes import SUCCESS


def check_install(config_data):
    """
    Here we do some **really** basic environment sanity checks.

    Basically we test for the more delicate and failing-prone dependencies:
     * database driver
     * Pillow image format support

    Many other errors will go undetected
    """
    errors = []
    size = 128, 128

    # PIL tests
    try:
        from PIL import Image

        try:
            im = Image.open(os.path.join(os.path.dirname(__file__), "../share/test_image.png"))
            im.thumbnail(size)
        except IOError:
            errors.append("Pillow is not compiled with PNG support, see 'Libraries installation issues' documentation section: http://djangocms-installer.readthedocs.org/en/latest/libraries.html.")
        try:
            im = Image.open(os.path.join(os.path.dirname(__file__), "../share/test_image.jpg"))
            im.thumbnail(size)
        except IOError:
            errors.append("Pillow is not compiled with JPEG support, see 'Libraries installation issues' documentation section: http://djangocms-installer.readthedocs.org/en/latest/libraries.html")
    except ImportError:
        errors.append("Pillow is not installed check for installation errors and see 'Libraries installation issues' documentation section: http://djangocms-installer.readthedocs.org/en/latest/libraries.html")

    # PostgreSQL test
    if config_data.db_driver == 'psycopg2' and not config_data.no_db_driver:  # pragma: no cover
        try:
            import psycopg2  # NOQA
        except ImportError:
            errors.append("PostgreSQL driver is not installed, but you configured a PostgreSQL database, please check your installation and see 'Libraries installation issues' documentation section: http://djangocms-installer.readthedocs.org/en/latest/libraries.html")

    # MySQL test
    if config_data.db_driver == 'MySQL-python' and not config_data.no_db_driver:  # pragma: no cover
        try:
            import MySQLdb  # NOQA
        except ImportError:
            errors.append("MySQL driver is not installed, but you configured a MySQL database, please check your installation and see 'Libraries installation issues' documentation section: http://djangocms-installer.readthedocs.org/en/latest/libraries.html")
    if errors:
        raise EnvironmentError("\n".join(errors))


def requirements(requirements, is_file=False):
    if is_file:
        args = ['install', '-q', '-r', requirements]
    else:
        args = ['install', '-q', ]
        args.extend(requirements.split())
    exit_status = pip.main(args)
    if exit_status != SUCCESS:
        raise InstallationError("Error while installing requirements. Check pip log file for error details.")
    return True
