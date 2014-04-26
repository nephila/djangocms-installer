====================
django CMS Installer
====================

.. image:: https://badge.fury.io/py/djangocms-installer.png
    :target: http://badge.fury.io/py/djangocms-installer
    
.. image:: https://travis-ci.org/nephila/djangocms-installer.png?branch=master
        :target: https://travis-ci.org/nephila/djangocms-installer

.. image:: https://pypip.in/d/djangocms-installer/badge.png
        :target: https://pypi.python.org/pypi/djangocms-installer

.. image:: https://coveralls.io/repos/nephila/djangocms-installer/badge.png?branch=master
        :target: https://coveralls.io/r/nephila/djangocms-installer?branch=master

Command to easily bootstrap django CMS projects

* Free software: BSD license

Features
--------

``djangocms-installer`` is a console wizard to help bootstrapping a django CMS
project.

Refer to `django CMS Tutorial <https://github.com/divio/django-cms-tutorial/>`_ on
how to properly setup your first django CMS project.

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

For additional information, check http://djangocms-installer.readthedocs.org/en/latest/libraries.html


.. image:: https://d2weczhvl823v0.cloudfront.net/nephila/djangocms-installer/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

