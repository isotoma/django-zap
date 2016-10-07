Changelog
=========

0.0.7 (2016-10-07)
------------------

Now only compatible with django 1.8+

- Replaces option_list with add_arguments


0.0.6 (2015-10-29)
------------------

- Adds ``--droptest`` argument, which also drops the test database. This
  feature is aimed at people using --keepdb to speed up their test runs.


0.0.5 (2015-09-16)
------------------

- database argument now passed to backend in support of multiple database
  setups.


0.0.4 (2015-04-01)
------------------

- #3 Adds a new flag ``--dropconnections``, disabled by default, that tells
  postgres to terminate all existing sessions before zapping. This is to work
  around an issue where third party applications open database connections
  upon app registry installation.


0.0.3 (2015-02-12)
------------------

- Adds OSX detection
- Adds port option for postgres backend
- Changes working directory of postgres subprocess command to /tmp


0.0.2 (2014-11-25)
------------------

- Update how args are parsed to allow use from call_command


0.0.1 (2013-09-27)
------------------

- All important fix-the-bladdy-packaging release


0.0.0 (2013-09-27)
------------------

- Initial Release
