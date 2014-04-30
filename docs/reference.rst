.. _arguments:

djangocms-installer arguments
==========================

Required arguments
------------------

You must always provide the following arguments when invoking **djangocms installer**:

* ``project_name``: Name of the project to be created
* ``--parent-dir``, ``-p``: Optional project parent directory;


Wizard arguments
----------------

The following arguments can be overridden in :ref:`wizard_mode`

* ``--db``, ``-d``: Database configuration (in URL format); default: ``sqlite://localhost/project.db``
* ``--i18n``, ``-i``: Activate Django I18N / L10N setting; choices: ``yes|no``, default: ``yes``
* ``--use-tz``, ``-z``: Activate Django timezone support;  choices: ``yes|no``, default: ``yes``
* ``--timezone``, ``-t``: Optional default time zone, default: ``America/Chicago``
* ``--reversion``, ``-e``: Install and configure reversion support, choices: ``yes|no``, default: ``yes``
* ``--permissions``: Activate CMS permission management; choices: ``yes|no``, default: ``yes``
* ``--languages``, ``-l``: Languages to enable. Option can be provided multiple times, or as a comma separated list
* ``--django-version``: Django version;  choices: ``1.4|1.5|1.6|stable``, default: ``stable``
* ``--cms-version``, ``-v``: django CMS version, choices: ``2.4|3.0|stable|develop``. default: ``stable``
* ``--bootstrap``, ``-v``: Use Twitter Bootstrap as theme, choices: ``yes|no``, default: ``no``
* ``--starting-page``, ``-v``: Load a starting page with examples after installation, choices: ``yes|no``, default: ``no``

.. note:: the ``stable`` keyword is expanded to the following Django version::

   * if django CMS version is 3.0 or develop: **stable** is expanded to Django==1.6;
   * if django CMS version is 2.4: **stable** is expanded to Django==1.5;

.. note:: the ``stable`` keyword is expanded to the latest django CMS stable version (3.0)


Advanced options
----------------

The following options are not managed by the config wizard and are meant for
advanced usage:

* ``--no-input``, ``-q``: If given **djangocms installer** run in :ref:`batch_mode`;
* ``--filer``, ``-f``: Install and configure django-filer plugins;
* ``--dump-requirements``, ``-R``: Dumps the generated requirements to stdout
  and exits; see :ref:`dump_mode`;
* ``--requirements``, ``-r``: You can use a custom requirements files instead of the
  requirements provided by **djangocms installer**;
* ``--no-deps``, ``-n``: Don't install package dependencies;
* ``--no-db-driver``: Don't install database package;
* ``--no-sync``, ``-m``: Don't run syncdb / migrate after bootstrapping the project;
* ``--no-user``, ``-u``: Don't create the admin user;
* ``--list-plugins``, ``-P``: List plugins that's going to be installed and
  configured for the project; this will not alter the virtualenv or create the
  project;
