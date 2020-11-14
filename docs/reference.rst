.. _arguments:

Arguments reference
===================

Required arguments
------------------

You must always provide the following argument when invoking **djangocms installer**:

* ``project_name``: Name of the project to be created

Optionally you can provide a project directory, otherwise a directory named after the project name
will be created in the current directory.

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
* ``--timezone``, ``-t``: Optional default time zone, default: *local timezone*
* ``--reversion``, ``-e``: Install and configure reversion support, choices: ``yes|no``,
  default: ``yes``; this will ignored for 3.4 and higher versions of django CMS as support has
  been dropped upstream;
* ``--permissions``: Activate CMS permission management; choices: ``yes|no``, default: ``no``
* ``--languages``, ``-l``: Languages available for the project. Option can be provided multiple
  times, or as a comma separated list.
  Only language codes supported by Django can be used here;
  refer to `django source`_ for a list of supported codes.
* ``--django-version``: Django version;  choices: ``1.11|2.0|2.1|2.2|stable|lts``, default: ``stable```
* ``--cms-version``, ``-v``: django CMS version, choices: ``3.6|3.7|stable|lts|rc|develop``.
  default: ``stable``
* ``--bootstrap``: Use Bootstrap 4 theme, choices: ``yes|no``, default: ``no``
* ``--starting-page``: Load a starting page with examples (available for english language only)
  after installation, choices: ``yes|no``, default: ``no``
* ``--templates``: Use a custom directory as template source; is checked to be a valid path,
  otherwise the shipped templates are used

.. note:: Django ``stable`` keyword is expanded to latest released Django version supported by django CMS
.. note:: Django ``lts`` keyword is expanded to latest released Django LTS supported by django CMS
.. note:: django-cms ``stable`` keyword is expanded to latest released django-cms version
.. note:: django-cms ``lts`` keyword is expanded to latest released django-cms LTS version, or latest stable if LTS is not supported
.. warning:: if an unsupported combination of Django and django CMS version is selected, the
             wizard exits reporting the error.

Advanced options
----------------

The following options are not managed by the config wizard and are meant for
advanced usage:

* ``--no-input``, ``-q``: If given **djangocms installer** run in :ref:`batch_mode` (default behavior);
* ``--wizard``, ``-w``: If given **djangocms installer** run in :ref:`wizard_mode`;
* ``--parent-dir``, ``-p``: Optional project directory;
* ``--verbose``, : Provides output of the commands used to setup the project, namely ``pip`` and
  ``django-admin``;
* ``--filer``, ``-f``: Install and configure django-filer plugins; since 0.9 this is enabled by default
  and can't be disabled;
* ``--config-file``: Provides the configuration options via a ini file; see :ref:`ini_mode`;
* ``--config-dump``: Dumps the configuration in a format suitable for ``-config-file``
  option; see :ref:`ini_mode`;
* ``--dump-requirements``, ``-R``: Dumps the generated requirements to stdout
  and exits; see :ref:`dump_mode`;
* ``--requirements``, ``-r``: You can use a custom requirements files instead of the
  requirements provided by **djangocms installer**;
* ``--no-deps``, ``-n``: Don't install package dependencies;
* ``--no-plugins``: Don't install plugins;
* ``--no-db-driver``: Don't install database package;
* ``--no-sync``, ``-m``: Don't run syncdb / migrate after bootstrapping the project;
* ``--no-user``, ``-u``: Don't create the admin user;
* ``--utc``, : Use UTC as default timezone;
* ``--list-plugins``, ``-P``: List plugins that's going to be installed and
  configured for the project; this will not alter the virtualenv or create the
  project;
* ``--extra-settings``: Path to a file with extra variables to append to generated settings file.
  It doesn't need to be a Python file, its content is blindly copied in the project settings.
* ``--skip-empty-check``, ``-s``: Skip the check if the project dir contains files or directory;
  in case of error when setting up the project the existing directory will be preserved.
* ``--delete-project-dir``', ``-c``: Delete project directory on creation failure in :ref:`batch_mode`.



.. _dj-database-url: https://github.com/kennethreitz/dj-database-url
.. _django source: https://github.com/django/django/blob/master/django/conf/global_settings.py#L50
