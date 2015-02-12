import os
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management import call_command

from zap.backends import get_backend
from zap.exceptions import NoBackendError


class Command(BaseCommand):

    help = 'This management script drops the database and database user ' \
           '(if they exist) then recreates them.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--database',
            default='default',
            help='Which database in your django settings to zap and create',
        ),
        make_option(
            '--nozap',
            default=False,
            action='store_true',
            help='Do not zap the database and user, only try to create them',
        ),
        make_option(
            '--noinput',
            default=False,
            action='store_true',
            help='Do not require any input from the user - note that any ' \
                 'calls to sudo made by the backends may still require input',
        ),
        make_option(
            '--syncdb',
            default=False,
            action='store_true',
            help='Run syncdb after a successfull zap and creation',
        ),
        make_option(
            '--migrate',
            default=False,
            action='store_true',
            help='Run migrate after a successful zap and creation',
        )
    )

    def handle(self, *args, **kwargs):
        try:
            self.backend = get_backend()
        except NoBackendError:
            self.stderr.write('Cannot zap and create - no appropriate backend')
            raise SystemExit(1)

        if os.geteuid() == 0:
            self.stderr.write('Warning: running this script as root could ' \
                              'generate troublesome pyc files owned by root!')

        if not kwargs['nozap']:
            self.zap()

        created = self.create()

        if created and kwargs['syncdb']:
            call_command('syncdb', interactive=(not kwargs['noinput']))

        if created and kwargs['migrate']:
            call_command('migrate', interactive=(not kwargs['noinput']))

    def zap(self):
        self.stdout.write('Attempting to DROP database')
        if not self.backend.zap_db():
            self.stderr.write('Could not DROP database... perhaps it does not exist yet')

        self.stdout.write('Attempting to DROP ROLE')
        if not self.backend.zap_user():
            self.stderr.write('Could not DROP ROLE... perhaps the user does not exist yet')

    def create(self):
        ok = True

        self.stdout.write('Creating user')
        if not self.backend.create_user():
            self.stderr.write('Could not create user')
            ok = False

        if not self.backend.create_db():
            self.stderr.write('Could not create database')
            ok = False

        return ok
