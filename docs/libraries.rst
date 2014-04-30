.. _libraries:

Libraries installation issues
=============================

While this wizard try to handle most of the things for you, it doesn't check for
all the proper native (non python) libraries to be installed.
Before running this, please check you have the proper header and libraries
installed and available for packages to be installed.

Libraries you would want to check:

* libjpeg (for JPEG support in ``Pillow``)
* zlib (for PNG support in ``Pillow``)
* postgresql (for ``psycopg``)
* libmysqlclient (for ``Mysql-Python``)

The actualy package name may vary depending on the platform / distribution you
are using; you should make sure you have the library headers file installed
(mostly contained in package with `-dev` in its name: e.g. `libjpeg-dev` for
`libjpeg` library).


Fixing libraries installation issues
------------------------------------

If a native library is missing when installing a python package, the package
installation may fail silently or the package may be missing some functionality
(e.g.: if libjpeg is not installed Pillow will be compiled without JPEG support).

``djangocms-installer`` tries to check for most common issues and will exit with
an exception in case of errors.

In case of package installation failure you can simply install the correct
library and execute ``djangocms-installer`` again with the same parameters; if
the package is compiled with some functionality missing, you have to first
deinstall it (`pip uninstall *package-name*`), then install the correct library
and the execute ``djangocms-installer`` again.

For older Debian / Ubuntu releases, a manual fix may be needed to properly fix
compilation issues: see `stackoverflow`_

Manual installation
-------------------

If all else fails, you can use :ref:`dump_mode` to create a requirements file,
install it by hand and run the installer with `-n` parameter.


.. _stackoverflow: http://stackoverflow.com/questions/23078303/getting-error-while-running-django-cms-demo-page#23086541
