# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import os.path
import shutil
import subprocess
import sys

from djangocms_installer.utils import query_yes_no

logger = logging.getLogger('')


def check_install(config_data):
    """
    Here we do some **really** basic environment sanity checks.

    Basically we test for the more delicate and failing-prone dependencies:
     * database driver
     * Pillow image format support

    Many other errors will go undetected
    """
    errors = []

    # PIL tests
    try:
        from PIL import Image

        try:
            im = Image.open(os.path.join(os.path.dirname(__file__), '../share/test_image.png'))
            im.load()
        except IOError:  # pragma: no cover
            errors.append(
                'Pillow is not compiled with PNG support, see "Libraries installation issues" '
                'documentation section: https://djangocms-installer.readthedocs.io/en/latest/'
                'libraries.html.'
            )
        try:
            im = Image.open(os.path.join(os.path.dirname(__file__), '../share/test_image.jpg'))
            im.load()
        except IOError:  # pragma: no cover
            errors.append(
                'Pillow is not compiled with JPEG support, see "Libraries installation issues" '
                'documentation section: https://djangocms-installer.readthedocs.io/en/latest/'
                'libraries.html'
            )
    except ImportError:  # pragma: no cover
        errors.append(
            'Pillow is not installed check for installation errors and see "Libraries installation'
            ' issues" documentation section: https://djangocms-installer.readthedocs.io/en/latest/'
            'libraries.html'
        )

    # PostgreSQL test
    if config_data.db_driver == 'psycopg2' and not config_data.no_db_driver:  # pragma: no cover
        try:
            import psycopg2  # NOQA
        except ImportError:
            errors.append(
                'PostgreSQL driver is not installed, but you configured a PostgreSQL database, '
                'please check your installation and see "Libraries installation issues" '
                'documentation section: https://djangocms-installer.readthedocs.io/en/latest/'
                'libraries.html'
            )

    # MySQL test
    if config_data.db_driver == 'mysqlclient' and not config_data.no_db_driver:  # pragma: no cover  # NOQA
        try:
            import MySQLdb  # NOQA
        except ImportError:
            errors.append(
                'MySQL driver is not installed, but you configured a MySQL database, please check '
                'your installation and see "Libraries installation issues" documentation section: '
                'https://djangocms-installer.readthedocs.io/en/latest/libraries.html'
            )
    if errors:  # pragma: no cover
        raise EnvironmentError('\n'.join(errors))


def requirements(req_file, pip_options='', is_file=False, verbose=False):
    args = ['install']
    if not verbose:
        args.append('-q')
    if pip_options:
        args.extend([opt for opt in pip_options.split(' ') if opt])
    if is_file:  # pragma: no cover
        args += ['-r', req_file]
    else:
        args.extend(['{0}'.format(package) for package in req_file.split()])
    cmd = [sys.executable, '-mpip'] + args
    if verbose:
        sys.stdout.write('python path: {0}\n'.format(sys.executable))
        sys.stdout.write('packages install command: {0}\n'.format(' '.join(cmd)))
    try:
        subprocess.check_output(['python', '-msite'], stderr=subprocess.STDOUT)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        sys.stdout.write(output.decode('utf-8'))
    except Exception as e:
        logger.error('cmd : %s :%s' % (e.cmd, e.output))
        raise

    return True


def write_requirements(config_data):
    with open(os.path.join(config_data.project_directory, 'requirements.txt'), 'w') as reqfile:
        reqfile.write(config_data.requirements)


def cleanup(requirements):  # pragma: no cover
    import pip

    args = ['uninstall', '-q', '-y']
    args.extend(requirements.split())
    pip.main(args)
    return True


def cleanup_directory(config_data):
    """
    Asks user for removal of project directory and eventually removes it
    """
    if os.path.exists(config_data.project_directory):
        choice = False
        if config_data.noinput is False and not config_data.verbose:
            choice = query_yes_no(
                'The installation failed.\n'
                'Do you want to clean up by removing {0}?\n'
                '\tWarning: this will delete all files in:\n'
                '\t\t{0}\n'
                'Do you want to cleanup?'.format(
                    os.path.abspath(config_data.project_directory)
                ),
                'no'
            )
        else:
            sys.stdout.write('The installation has failed.\n')
        if config_data.skip_project_dir_check is False and (choice or
                                                            (config_data.noinput and
                                                             config_data.delete_project_dir)):
            sys.stdout.write('Removing everything under {0}\n'.format(
                os.path.abspath(config_data.project_directory)
            ))
            shutil.rmtree(config_data.project_directory, True)
