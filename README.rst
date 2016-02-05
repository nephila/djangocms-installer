====================
django CMS Installer
====================

.. image:: https://img.shields.io/pypi/v/djangocms-installer.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-installer
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/djangocms-installer.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-installer
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/djangocms-installer.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-installer
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/djangocms-installer.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-installer
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/djangocms-installer/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-installer?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/djangocms-installer/master.svg?style=flat-square
    :target: https://codecov.io/github/nephila/djangocms-installer
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/djangocms-installer/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-installer
   :alt: Code Climate

Command to easily bootstrap django CMS projects

* Free software: BSD license

Features
--------

``djangocms-installer`` is a console wizard to help bootstrapping a django CMS
project.

Refer to `django CMS Tutorial`_
on how to properly setup your first django CMS project.

.. warning:: Version 0.9 will drop support for Python 2.6, Django <1.8 and django CMS < 3.2.
             More 0.8.x versions may be released after 0.9 is out in case important bugfixes will
             be needed.

Documentation
-------------

For detailed information see http://djangocms-installer.readthedocs.org

Preliminary checks and system libraries
---------------------------------------

While this wizard try to handle most of the things for you, it doesn't check for
all the proper native (non python) libraries to be installed.
Before running this, please check you have the proper header and libraries
installed and available for packages to be installed.

Libraries you would want to check:

* libjpeg (for JPEG support in ``Pillow``)
* zlib (for PNG support in ``Pillow``)
* postgresql (for ``psycopg2``)
* libmysqlclient (for ``Mysql``)
* python-dev (for compilation and linking)

For additional information, check http://djangocms-installer.readthedocs.org/en/latest/libraries.html

Supported versions
------------------

The current supported version matrix is the following:

+----------------+-------------+-------------+---------------+
|                | Django 1.8  | Django 1.9  | Django master |
+----------------+-------------+-------------+---------------+
| django CMS 3.2 | Supported   | Supported   | Unsupported   |
+----------------+-------------+-------------+---------------+
| django CMS dev | Supported   | Supported   | Unsupported   |
+----------------+-------------+-------------+---------------+

Check `version 0.8`_ for older Django / django CMS versions support

Any beta and develop version of Django and django CMS, by its very nature,
it's not supported, while it still may work.

``djangocms-installer`` tries to support beta versions of django CMS when they
are be considered sufficiently stable by the upstream project.

Warning
-------

``djangocms-installer`` assumes that ``django-admin.py`` is installed in the same directory
as python executable, which is the standard virtualenv layout.


Windows support
---------------

The installer is tested on Windows 7 with Python versions 3.4.2 and 2.7.8 installed using
official MSI packages available at http://python.org.

Please check that the ``.py`` extension is associated correctly with Python interpreter::

    c:\> assoc .py
    .py=Python.File

    c:\>ftype Python.File
    Python.File="C:\Windows\py.exe" "%1" %*


.. _version 0.8: https://github.com/nephila/djangocms-installer/tree/release/0.8.x#supported-versions
.. _django CMS Tutorial: http://django-cms.readthedocs.org/en/latest/introduction/index.html
