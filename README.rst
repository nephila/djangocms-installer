===============================
Aldryn Installer
===============================

.. image:: https://badge.fury.io/py/aldryn-installer.png
    :target: http://badge.fury.io/py/aldryn-installer
    
.. image:: https://travis-ci.org/nephila/aldryn-installer.png?branch=master
        :target: https://travis-ci.org/nephila/aldryn-installer

.. image:: https://pypip.in/d/aldryn-installer/badge.png
        :target: https://crate.io/packages/aldryn-installer?version=latest

Command to easily bootstrap django CMS projects

* Free software: BSD license

Features
--------

``aldryn-installer`` is a console wizard to help bootstrapping a django CMS
project.

Usage
-----
Call it with a project name and a directory path to install the project into::

    aldryn -p /path/whatever project_name

HOWTO
-----

#. Create an empty virtualenv::

    virtualenv /virtualenv/path/my_project

#. Install `aldryn-installer`::

    pip install aldryn-installer

   or::

    pip install https://github.com/nephila/aldryn-installer/archive/master.zip

#. Execute the wizard::

    aldryn -p /path/whatever project_name

#. Answer the questions; most of them already provide sane default, but you're
   free to adapt to your own needs.
   The only required parameter is the database name, provided in url format.

#. Change to your project directory::

    cd /path/whatever project_name

#. Modify the provided settings.
   You will want to modify at least the language and the template settings;

#. Execute the project::

    (whatever) $ python manage.py runserver

#. Enjoy!
