import os
import sys
import pwd
import subprocess

from .base import ZapBase


class BasePostgresMixin(object):

    base_command = ['psql']

    def can_zap(self):
        return False

    def _psql(self, *command):
        ''' Run a command via psql as the postgres user '''
        base = self.base_command[:]
        if self.debug:
            sys.stderr.write('psql -c "' + ' '.join(command) + '"\n')
        if self.port:
            port_string = '{port}'.format(port=self.port)
            base += ['-p', port_string]
        base.append('-c')
        p = subprocess.Popen(
            base + list(command),
            cwd='/tmp',
            stdout=sys.stdout,
            stderr=sys.stderr,
            stdin=sys.stdin,
        )
        p.wait()
        return p.returncode == 0

    def zap_user(self):
        return self._psql('DROP ROLE {0}'.format(self.user))

    def zap_db(self):
        if self.dropconnections:
            self._psql("SELECT pg_terminate_backend(pg_stat_activity.pid) \
            FROM pg_stat_activity WHERE pg_stat_activity.datname = '{}' \
            AND pid <> pg_backend_pid();".format(self.name))
        return self._psql('DROP DATABASE {0}'.format(self.name))

    def create_user(self):
        # allow the user createdb permissions for running tests if DEBUG=True
        db_perms = 'CREATEDB' if self.debug else 'NOCREATEDB'
        return self._psql(
            "CREATE ROLE {user} PASSWORD '{password}' " \
            "NOSUPERUSER {db_perms} NOCREATEROLE INHERIT LOGIN".format(
                user=self.user,
                password=self.password,
                db_perms=db_perms,
            )
        )

    def create_db(self):
        return self._psql(
            "CREATE DATABASE {name} WITH OWNER = {owner} " \
            "TEMPLATE = template0 ENCODING = 'UTF8'".format(
                name=self.name, owner=self.user,
            )
        )


class PostgresAppZap(BasePostgresMixin, ZapBase):

    bin_path = '/Applications/Postgres.app/Contents/Versions/latest/bin'
    base_command = [bin_path + '/psql']

    """ zap and create a postgres.app instance """
    def can_zap(self):
        return os.path.exists(self.bin_path) and 'postgresql' in self.engine


class LocalPostgresZap(BasePostgresMixin, ZapBase):
    """ zap and create a local running postgresql instance """

    base_command = ['sudo', '-u', 'postgres', 'psql']

    def can_zap(self):
        if not 'linux' and not 'darwin' in sys.platform:
            return False

        if not 'postgres' in [p[0] for p in pwd.getpwall()]:
            return False

        if not (
            self.host == '' or \
            self.host == 'localhost' or \
            self.host.startswith('127.')
            ):                                  # flake8: noqa
            return False

        if 'postgresql' in self.engine:
            return True
