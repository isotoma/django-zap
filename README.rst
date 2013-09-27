==========
Django-Zap
==========

What?
-----

Automates the destruction and recreation of django databases.

Why?
----

In the early stages of development when your models are heavily in flux, you
want to be frequently dropping and recreating the database before re-running
django's ``syncdb`` command. This tool uses the database settings in your
settings file to prevent you having to duplicate them in some separate database
drop/create script.

How?
----

Just add ``zap`` to your installed apps.

Backends
--------

At the moment the only backend is for linux machines running a local postgresql
instance, and authentication is done using the ident rule in the ``pg_hba.conf``,
then calling psql as the ``postgres`` user.

Feel free to provide more backends or extend the one we have, perhaps to include
mac support, or support for other django database engines.
