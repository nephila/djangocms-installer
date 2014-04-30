djangocms-installer FAQ
=======================

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



.. _project: https://github.com/nephila/djangocms-installer/issues