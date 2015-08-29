FAQ
===

#. I need to use version **foo** of package *blargh*, while the installer
   want to use version **baz**, how can I solve this?

   Use :ref:`dump_mode` to dump the requirements used by the installer, customize
   them and pass them again to the installer for the installation run


#. After installing the virtualenv, the installer exit with "*Pillow is not
   compiled with ... support*" / "*Pillow is not installed*" errors, what can
   I do?

   Pillow can be a bit tricky in some environments, so please check the
   ":ref:`libraries`" section for more detailed help.

#. I followed the advices above, but I keep having the same messages!

   Checking for correct Pillow installation can be a bit tricky: installer
   try to be smart but it may sometimes fail and report Pillow errors while
   errors lie somewhere else. In this case, please open an issue on github
   `project`_, or ask in the #django-cms IRC channel.

#. How can I configure the database to use?

   **djangocms-installer** uses `dj-database-url`_ to get database
   configuration parameters; refer to this package for more details.

#. The installer dies with an error like
   ``ImportError: Could not import settings 'foo.bar.settings' (Is it on sys.path? Is there an import error in the settings file?): No module named foo.bar.settings``,
   what's happening?

   Chances are you have ``DJANGO_SETTINGS_MODULE`` set in you environment,
   either by default or using postactivate virtualenv hooks or other tools;
   please check you environment right after the error happening (for example
   using the ``env`` command on *nix systems) and remove any customisation: the
   installer requires that ``DJANGO_SETTINGS_MODULE`` is not set on the first
   run. You can customise it later.


.. _dj-database-url: https://github.com/kennethreitz/dj-database-url
.. _project: https://github.com/nephila/djangocms-installer/issues
