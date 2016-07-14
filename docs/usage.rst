Usage
=====

**djangocms installer** creates a complete and fully featured django CMS project.

By default it:

* creates the project
* installs requirements
* creates database
* (optionally) creates a sample database
* (optionally) copy a provided set of templates
* write the requirements file to the project directory

**djangocms installer** works as a batch script and as a command line wizard.


.. _wizard_mode:

Wizard mode
-----------

Wizard mode works by asking relevant questions to the user; it must be called with
the `-p` option (which is the project main directory) and the `project_name`
argument::

    djangocms -p /path/whatever project_name

A wizard will ask for the missing parameters; for most of them sane defaults are
provided, but you're free to adapt to your own needs.
The only required parameters are the database name, in url format, and the
project languages, as a comma separated list.

.. _batch_mode:

Batch mode
----------

By giving the `-q` parameter **djangocms installer** will use the arguments
provided to create and configure the project.
All the paramaters asked by the wizard can be passed as command line arguments.

See :ref:`arguments` for arguments reference


.. _dump_mode:

Dump mode
---------

By using the `-R` arguments, **djangocms-installer** won't create a new
django CMS instance but will print to stdout the list of packages
required to properly setup the virtualenv.
This can be helpful to customize the virtualenv:

#. Dump the list of requirements::

    $ djangocms -p /path/whatever project_name -R > requirements.txt

#. Edit requirements.txt according to your needs
#. Run the installer again providing the customized requirements file::

    $ djangocms -r custom_requirements.txt -p /path/whatever project_name

   or install the requirements manually and execute the installer with `n`
   argument::

    $ pip install -r custom_requirements.txt
    $ djangocms -n -p /path/whatever project_name


See :ref:`arguments` for arguments reference

.. _ini_mode:

Config file mode
----------------

In config file mode, all (or some) options can be provided via an external configuration file.

See a `complete example`_
with all available arguments.

Is it possible to either provide all the values in the config file:

.. code-block:: shell

    djangocms --config-file /path/to/config.ini project_name

Or just some, or overriding by using the command line arguments:

.. code-block:: shell

    djangocms --config-file /path/general-config.ini -p /path/other/proj -s -q project_name

.. note:: If config.ini not contains `no-input = true` and `-q` argument isn't set then one
          act as a placeholder with default values for wizard.


Dump config files
^^^^^^^^^^^^^^^^^

Values passed to the installer can be dumped for later reuse:

.. code-block:: shell

    djangocms --config-dump /path/config.ini -p . project_name

if installation fails dump can be used to fix some arguments and re-run installer with dumped config:

.. code-block:: shell

    djangocms --config-dump /path/config.ini --db postgres://wrong-usr:pwd@host/db -p . project_name
    # fails

    djangocms --config-file /path/config.ini --db postgres://correct-user:pwd@host/db -p . project_name
    # succeed

Custom settings
---------------

If want or need to provide custom settings **before** the initial database sync is run, use `--extra-settings`
parameter.
To use this option, pass the path to a file as argument: its content is going to be appended to the generated
settings file.


HOWTO
-----

#. Create an empty virtualenv::

    virtualenv /virtualenv/path/my_project

#. Install `djangocms-installer`::

    pip install djangocms-installer

   or::

    pip install https://github.com/nephila/djangocms-installer/archive/master.zip

#. Execute the wizard::

    djangocms -p /path/whatever project_name

#. Answer the wizard questions;

#. Change to your project directory::

    cd /path/whatever project_name

#. Modify the provided settings.
   You will want to modify at least the language and the template settings;

#. Execute the project::

    (whatever) $ python manage.py runserver

#. Enjoy!

Use different templates directory
---------------------------------

You can create the base project with a custom templateset by using the ``--templates`` parameter.
Be aware that while **djangocms installer** will copy the files for you, it won't update the ``CMS_TEMPLATES`` settings
parameter, so you'll need to modify that after installation.

.. _complete example: https://github.com/nephila/djangocms-installer/blob/develop/config.ini.sample


Bare install
------------

You can optionally install just Django and django CMS without any additiona plugin by using the
``--no-plugins`` option; this will allow you to further customise your installation.
