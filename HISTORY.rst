.. :changelog:

History
-------

1.1.1 (unreleased)
++++++++++++++++++

* Added support for pipenv

1.1.0 (2019-03-05)
++++++++++++++++++

* Added support for django CMS 3.6
* Added detection of incompatible DJANGO_SETTINGS_MODULE environment variable
* Added detection of mismatched Django version between currently installed and declared one

1.0.2 (2018-11-21)
++++++++++++++++++

* Bumped html5lib / djangocms-text-ckeditor version

1.0.1 (2018-06-03)
++++++++++++++++++

* Pinned django-polymorphic version to fix issues with django < 1.11
* Pinned djangocms core plugins versions

1.0.0 (2018-02-01)
++++++++++++++++++

* Dropped cmsplugin-filer in favor of core plugins which now use filer
* Added django CMS 3.5

0.9.8 (2018-01-10)
++++++++++++++++++

* Raised more informative messages on command failures
* Fixed tests for django CMS develop

0.9.7 (2017-07-15)
++++++++++++++++++

* Improved django-admin invocation to support more python environments layouts

0.9.6 (2017-03-12)
++++++++++++++++++

* Added more Django 1.10 fixes / cleanups
* Added python 3.6 compatibility

0.9.5 (2017-02-16)
++++++++++++++++++

* Added more Django 1.10 fixes / cleanups

0.9.4 (2017-01-03)
++++++++++++++++++

* Added support for Django 1.10
* Added 'lts' keyword (it's now the default instead of 'stable')

0.9.3 (2016-11-16)
++++++++++++++++++

* Fixed issue with create_user command

0.9.2 (2016-11-12)
++++++++++++++++++

* Fixed search 'django-admin.py'
* Improved error reporting during package installation

0.9.1 (2016-10-02)
++++++++++++++++++

* Fixed issue with -p parameter

0.9.0 (2016-09-15)
++++++++++++++++++

* Drop support for Python 2.6
* Drop support for Django < 1.8
* Drop support for django CMS < 3.2
* Improve inline documentation
* If -s option is used, original directory is not removed
* Set django CMS 3.3 as stable
* Add support for 'rc' releases
* Only "core" plugins are now supported
* Drop support for django-reversion in django CMS 3.4 (due to upstream drop)
* Make project-path option optional
* Batch mode is now the default one
* Add support for conda package manager
* Admin user is now created in batch mode by default. Use --no-user option to skip user creation
* In batch mode directory is not removed in case of cleanup unless --delete-project-dir is given
* Disable permission by default

0.8.12 (2016-08-27)
+++++++++++++++++++

* Pin plugins versions

0.8.11 (2016-07-15)
+++++++++++++++++++

* Better plugins version pinning
* Move sitemaps to non-language prefix url
* Fallback to UTC when timezone cannot be detected
* Pin html5lib version

0.8.10 (2016-05-28)
+++++++++++++++++++

* Add support for django CMS 3.3 final

0.8.9 (2016-05-19)
++++++++++++++++++

* Add support for django CMS 3.3rc

0.8.8 (2016-05-06)
++++++++++++++++++

* Force language codes to lowercase
* Force i18n if multiple languages is provided
* Fix some errors in selecting dependencies
* Fix error in Django 1.9 regexp

0.8.7 (2016-02-23)
++++++++++++++++++

* Add clearer cleanup message

0.8.6 (2016-02-05)
++++++++++++++++++

* Add support for Django 1.9
* Fix formatting CONN_MAX_AGE
* Improve error handling in case of fatal error

0.8.5 (2015-12-24)
++++++++++++++++++

* Fix createsuperuser command

0.8.4 (2015-12-21)
++++++++++++++++++

* Remove flash plugin from installed plugins
* Add ``--verbose`` option to improve debug
* Fix unicode errors
* Improve documentation

0.8.3 (2015-11-25)
++++++++++++++++++

* Improve text editor plugin version selection
* Improve admin style version selection

0.8.2 (2015-11-24)
++++++++++++++++++

* Add support for django CMS 3.2
* Add support for apphook reload middleware
* Add viewport meta tag for mobile devices support

0.8.1 (2015-10-11)
++++++++++++++++++

* Add option to not install plugins
* Add Python 3.5 to build matrix
* Add argument to pass options to pip
* Fix support for custom user models
* Dump requirements file in the created project
* Improve documentation

0.8.0 (2015-08-30)
++++++++++++++++++

* Options can now be provided via an ini file for easy scripting
* Better migration modules discovery strategy
* Minor fixes

0.7.9 (2015-07-21)
++++++++++++++++++

* Better Django 1.8 support
* Fix error with newer Pillow versions

0.7.8 (2015-06-27)
++++++++++++++++++

* Add Django 1.8 support
* Fix template styles

0.7.7 (2015-06-05)
++++++++++++++++++

* Switch to cloudflare CDN for bootstrap template
* Fix support for django-filer 0.9.10

0.7.6 (2015-05-01)
++++++++++++++++++

* Switch to django CMS 3.1 as stable django CMS release
* Rework the Django supported matrix
* Always use djangocms-link instead of cmsplugin-filer-link

0.7.5 (2015-04-21)
++++++++++++++++++

* Add support for django CMS 3.1
* Switch to Django 1.7 as stable django release

0.7.4 (2015-04-14)
++++++++++++++++++

* Add automatic timezone detection
* Pin django-reversion versions
* Make installer more compatible with windows environment

0.7.3 (2015-04-08)
++++++++++++++++++

* Fix issues with django CMS requirements
* Fix minor issues in shipped templates

0.7.2 (2015-02-08)
++++++++++++++++++

* Fixed Windows compatibility issues
* Fixed python 3 compatibility issues
* Add a flag to skip the project directory emptiness check

0.7.1 (2015-01-15)
++++++++++++++++++

* Ask for permission before cleanup
* Clarify the `-p` parameter
* Check if the project directory is empty before proceeding

0.7.0 (2015-01-10)
++++++++++++++++++

* Improved support for Django 1.7 and django CMS develop (3.1)
* Totally new test strategy
* Reverted -I parameter to install packages
* Improved support for cleanup after failure

0.6.0 (2014-11-30)
++++++++++++++++++

* Add support for installing aldryn-boilerplate
* Force installing all packages (-I) when creating the project virtualenv
* Fix multiplatform support bugs
* Update supported Django / django CMS versions
* Add preliminary support for django CMS develop (3.1)

0.5.4 (2014-08-14)
++++++++++++++++++

* Fix reversion version selection for older Django versions
* Better project name validation

0.5.3 (2014-07-23)
++++++++++++++++++

* Add support for easy_thumbnails 2.0 migrations
* Fix asking for creating user even when --no-input flag is used
* Unpin reversion as django CMS 3.0.3 solves the issue
* Versioned dependency for django-filer when installing django CMS 2.4
* Switch to official django-filer and cmsplugin-filer releases for CMS 3.0

0.5.2 (2014-05-30)
++++++++++++++++++

* Pin reversion to 1.8 waiting for a proper fix in django CMS

0.5.1 (2014-05-22)
++++++++++++++++++

* Fix error in bootstrap template handling
* Add clarification about custom template set and starting page

0.5.0 (2014-05-21)
++++++++++++++++++

* Add dump-requirements argument
* Add user provided extra setting
* Add FAQ section
* Add templates argument
* Documentation update

0.4.2 (2014-04-26)
++++++++++++++++++

* Use current cms.context_processors.cms_settings instead of deprecated one
* Document some fixes for library issues
* Fix Python 3 issue
* Switch default Django version to stable instead of 1.5

0.4.1 (2014-04-09)
++++++++++++++++++

* Fix some newlines issues in the settings file

0.4.0 (2014-04-09)
++++++++++++++++++

* Update for django CMS 3.0 stable!
* Fixes for settings parameter

0.3.5 (2014-04-03)
++++++++++++++++++

* Update for django CMS 3.0c2

0.3.4 (2014-03-29)
++++++++++++++++++

* Fix issues with django CMS 2.4

0.3.3 (2014-03-20)
++++++++++++++++++

* Better handling of differenct CMS version configuration

0.3.2 (2014-03-18)
++++++++++++++++++

* Fix some versioned dependency resolve error

0.3.1 (2014-03-16)
++++++++++++++++++

* Fix error in loading resource files
* Fix error with non-standard python executable paths
* Fix error with Django 1.6
* Fix error installing django-filer

0.3.0 (2014-03-15)
++++++++++++++++++

* Sync with django CMS RC1 changes
* Use external django CMS plugins instead of removed core ones

0.2.0 (2014-02-06)
++++++++++++++++++

* Project renamed to djangocms-installer
* Bugfixes
* Better default templates
* Python 3 compatibility
* Django 1.6 compatibility
* django CMS 3 beta3 and dev snapshot support
* Support for django-admin project templates
* Ships Twitter bootstrap templates
* Can now creates a dummy starting page

0.1.1 (2013-10-20)
++++++++++++++++++

* Improved documentation on how to fix installation in case of missing libraries.

0.1.0 (2013-10-19)
++++++++++++++++++

* First public release.
