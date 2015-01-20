.. _arguments:

Arguments reference
===================

Required arguments
------------------

You must always provide the following arguments when invoking **djangocms installer**:

* ``project_name``: Name of the project to be created
* ``--parent-dir``, ``-p``: Optional project directory;

.. warning:: project directory dir is the main project directory (the one where ``manage.py``
             will be created); by default the installer check if it's empty (minus hidden files)
             to ensure that you're running in a clean environment. If you want to use a
             non-empty directory use the ``-s`` flag;



Wizard arguments
----------------

The following arguments can be overridden in :ref:`wizard_mode`

* ``--db``, ``-d``: Database configuration (in URL format); use `dj-database-url`_
  syntax;  default: ``sqlite://localhost/project.db``
* ``--i18n``, ``-i``: Activate Django I18N / L10N setting; choices: ``yes|no``, default: ``yes``
* ``--use-tz``, ``-z``: Activate Django timezone support;  choices: ``yes|no``, default: ``yes``
* ``--timezone``, ``-t``: Optional default time zone, default: ``America/Chicago``
* ``--reversion``, ``-e``: Install and configure reversion support, choices: ``yes|no``, default: ``yes``
* ``--permissions``: Activate CMS permission management; choices: ``yes|no``, default: ``yes``
* ``--languages``, ``-l``: Languages available for the project. Option can be provided multiple times, or as a
  comma separated list.
  Only language codes supported by Django can be used here. Refer to `django source`_ for a list of supported codes.
* ``--django-version``: Django version;  choices: ``1.4|1.5|1.6|stable``, default: ``stable``
* ``--cms-version``, ``-v``: django CMS version, choices: ``2.4|3.0|stable|develop``. default: ``stable``
* ``--bootstrap``: Use Twitter Bootstrap as theme, choices: ``yes|no``, default: ``no``
* ``--starting-page``: Load a starting page with examples after installation, choices: ``yes|no``, default: ``no``
* ``--templates``: Use a custom directory as template source; is checked to be a valid path, otherwise the
  shipped templates are used

.. note:: for Django the ``stable`` keyword is expanded to the following Django version:

   * if django CMS version is 3.0 or develop: **stable** is expanded to Django==1.6;
   * if django CMS version is 2.4: **stable** is expanded to Django==1.5;

.. note:: the django CMS ``stable`` keyword is expanded to the latest django CMS stable version (3.0)


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
* ``--extra-settings``: Path to a file with extra variables to append to generated settings file. It doesn't need to be
  a Python file, its content is blindly copied in the project settings.
*``--aldryn``, ``-a``: Use `aldryn-boilerplate`_; this downloads **aldryn-boilerplate** and copies it
  into the project, adapting the project layout according to boilerplate specifications; the use
  of aldryn-boilerplate requires manual actions, look at `aldryn-boilerplate documentation`_ for
  further informations.
*``--skip-empty-check``, ``-s``: Skip the check if the project dir contains files or directory;
  in case of error when setting up the project, ``djangocms-installer`` may ask you to remove
  the directory, be careful if using this option as you may remove files not related to the
  project set up by the installer.


.. _dj-database-url: https://github.com/kennethreitz/dj-database-url
.. _django source: https://github.com/django/django/blob/master/django/conf/global_settings.py#L50
.. _aldryn-boilerplate: https://github.com/aldryn/aldryn-boilerplate
.. _aldryn-boilerplate documentation: http://aldryn-boilerplate.readthedocs.org/en/latest/general/requirements.html