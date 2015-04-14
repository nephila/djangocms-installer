====================
django CMS Installer
====================


.. image:: https://img.shields.io/pypi/v/djangocms-installer.svg
        :target: https://pypi.python.org/pypi/djangocms-installer
        :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/nephila/djangocms-installer.svg
        :target: https://travis-ci.org/nephila/djangocms-installer
        :alt: Latest Travis CI build status

.. image:: https://img.shields.io/pypi/dm/djangocms-installer.svg
        :target: https://pypi.python.org/pypi/djangocms-installer
        :alt: Monthly downloads

.. image:: https://coveralls.io/repos/nephila/djangocms-installer/badge.png
        :target: https://coveralls.io/r/nephila/djangocms-installer
        :alt: Test coverage

Command to easily bootstrap django CMS projects

* Free software: BSD license

Features
--------

``djangocms-installer`` is a console wizard to help bootstrapping a django CMS
project.

Refer to `django CMS Tutorial <http://django-cms.readthedocs.org/en/latest/introduction/index.html>`_
on how to properly setup your first django CMS project.

.. note:: It used to be called **aldryn-installer**, but since version 0.2.0
          it's been renamed **djangocms-installer** for clarity.

Installation
------------

#. Create an empty virtualenv::

    virtualenv /virtualenv/path/my_project

#. Install `djangocms-installer`::

    pip install djangocms-installer

   or::

    pip install -e git+https://github.com/nephila/djangocms-installer#egg=djangocms-installer

Documentation
-------------

See http://djangocms-installer.readthedocs.org

Supported versions
------------------

The current supported version matrix is the following:

+----------------+-------------+-------------+-------------+-------------+-------------+
|                | Django 1.4  | Django 1.5  | Django 1.6  | Django 1.7  | Django 1.8  |
+----------------+-------------+-------------+-------------+-------------+-------------+
| django CMS 2.4 | Supported   | Supported   | Unsupported | Unsupported | Unsupported |
+----------------+-------------+-------------+-------------+-------------+-------------+
| django CMS 3.0 | Supported   | Supported   | Supported   | Supported   | Unsupported |
+----------------+-------------+-------------+-------------+-------------+-------------+
| django CMS 3.1 | Unsupported | Unsupported | Supported   | Supported   | WiP         |
+----------------+-------------+-------------+-------------+-------------+-------------+
| django CMS dev | Unsupported | Unsupported | Supported   | Supported   | WiP         |
+----------------+-------------+-------------+-------------+-------------+-------------+

Any beta and develop version of Django and django CMS, by its very nature,
it's not supported, while it still may work.

``djangocms-installer`` tries to support beta versions of django CMS when they
will be considered sufficiently stable by the upstream project.

Warning
-------

``djangocms-installer`` assumes that ``django-admin.py`` is installed in the same directory
as python executable, which is the standard virtualenv layout.

Caveats
-------

While this wizard try to handle most of the things for you, it doesn't check for
all the proper native (non python) libraries to be installed.
Before running this, please check you have the proper header and libraries
installed and available for packages to be installed.

Libraries you would want to check:

* libjpeg (for JPEG support in ``Pillow``)
* zlib (for PNG support in ``Pillow``)
* postgresql (for ``psycopg``)
* libmysqlclient (for ``Mysql-Python``)
* python-dev (for compilation and linking)

For additional information, check http://djangocms-installer.readthedocs.org/en/latest/libraries.html


Windows support
---------------

The installer is tested on Windows 7 with Python versions 3.4.2 and 2.7.8 installed using
official MSI packages available at http://python.org.

Please check that the ``.py`` extension is associated correctly with Python interpreter::

    c:\> assoc .py
    .py=Python.File

    c:\>ftype Python.File
    Python.File="C:\Windows\py.exe" "%1" %*

