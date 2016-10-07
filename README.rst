==========
Django-Zap
==========

Compatible with Django 1.8+

For 1.7 compatibility use ``django-zap==0.0.6``

What?
-----

Automates the destruction and recreation of django databases.

Currently only supports local postgres databases. Feel free to add more
backends.

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

A new django management command will appear: ``zap_and_create_db``.

Help is at ``python manage.py zap_and_create_db --help`` but the TL;DR is that
you can run it without arguments and it'll drop the user and database, then
recreate them. Run it with ``--migrate`` and it'll also run
``manage.py migrate``.

Backends
--------

At the moment the only backend is for linux machines running a local postgresql
instance, and authentication is done using the ident rule in the ``pg_hba.conf``,
then calling psql as the ``postgres`` user.

Feel free to provide more backends or extend the one we have, perhaps to include
mac support, or support for other django database engines.
