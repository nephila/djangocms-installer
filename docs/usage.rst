Usage
=====
**aldryn installer** can be executed both as a batch script and as a command line
wizard.

.. _wizard_mode:

Wizard mode
-----------

Call it with a project name and a directory path to install the project into::

    aldryn -p /path/whatever project_name

A wizard will ask for the missing parameters; for most of them sane defaults are
provided, but you're free to adapt to your own needs.
The only required parameters are the database name, in url format, and the
project languages, as a comma separated list.

.. _batch_mode:

Batch mode
----------

By giving the `-q` parameter **aldryn installer** will use the arguments
provided to create and configure the project.
All the paramaters asked by the wizard can be passed as command line arguments.

See :ref:`arguments` for arguments reference

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

#. Answer the wizard questions;

#. Change to your project directory::

    cd /path/whatever project_name

#. Modify the provided settings.
   You will want to modify at least the language and the template settings;

#. Execute the project::

    (whatever) $ python manage.py runserver

#. Enjoy!
