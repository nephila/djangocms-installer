# -*- coding: utf-8 -*-
import tempfile
import os.path

import pip


def check_install(config_data):
    """
    Here we do some **really* basic sanity check for the environment.

    Bsically we test for the more delicate and failing-prone dependencies:
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
        except IOError as e:
            #errors.append(e.strerror)
            errors.append("Pillow is not compiled with PNG support, see 'Libraries installation issues' documentation section.")
        try:
            im = Image.open(os.path.join(os.path.dirname(__file__), "../share/test_image.jpg"))
            im.thumbnail(size)
        except IOError as e:
            #errors.append(e.strerror)
            errors.append("Pillow is not compiled with JPEG support, see 'Libraries installation issues' documentation section.")
    except ImportError:
        errors.append("Pillow is not installed check for installation errors and see 'Libraries installation issues' documentation section.")

    # PostgreSQL test
    if config_data.db_driver == 'psycopg2' and not config_data.no_db_driver:
        try:
            import psycopg2
        except ImportError:
            errors.append("PostgreSQL driver is not installed, but you configured a PostgreSQL database, please check your installation and see 'Libraries installation issues' documentation section.")

    # MySQL test
    if config_data.db_driver == 'MySQL-python' and not config_data.no_db_driver:
        try:
            import MySQLdb
        except ImportError:
            errors.append("MySQL driver is not installed, but you configured a MySQL database, please check your installation and see 'Libraries installation issues' documentation section.")
    if errors:
        raise EnvironmentError("\n".join(errors))


def requirements(requirements, is_file=False):
    if is_file:
        args = ['install', '-q', '-r', requirements]
    else:
        args = ['install', '-q', ]
        args.extend(requirements.split())
    command = pip.main(args)
