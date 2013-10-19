===============================
Aldryn Installer
===============================

.. image:: https://badge.fury.io/py/aldryn-installer.png
    :target: http://badge.fury.io/py/aldryn-installer
    
.. image:: https://travis-ci.org/nephila/aldryn-installer.png?branch=master
        :target: https://travis-ci.org/nephila/aldryn-installer

.. image:: https://pypip.in/d/aldryn-installer/badge.png
        :target: https://crate.io/packages/aldryn-installer?version=latest

.. image:: https://coveralls.io/repos/nephila/aldryn-installer/badge.png?branch=master
        :target: https://coveralls.io/r/nephila/aldryn-installer?branch=master

Command to easily bootstrap django CMS projects

* Free software: BSD license

Features
--------

``aldryn-installer`` is a console wizard to help bootstrapping a django CMS
project.

Refer to `django CMS Tutorial <http://slid.es/chive/djangocms/fullscreen>`_ on
how to properly setup your first django CMS project.

Installation
------------

#. Create an empty virtualenv::

    virtualenv /virtualenv/path/my_project

#. Install `aldryn-installer`::

    pip install aldryn-installer

   or::

    pip install -e git+https://github.com/nephila/aldryn-installer#egg=aldryn-installer

Documentation
-------------

See http://aldryn-installer.readthedocs.org

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
