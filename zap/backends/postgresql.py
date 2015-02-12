import sys
import pwd
import subprocess

from .base import ZapBase


class LocalPostgresZap(ZapBase):
    """ zap and create a local running postgresql instance """

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

    def _psql(self, *command):
        ''' Run a command via psql as the postgres user '''
        if self.debug:
            sys.stderr.write('psql -c "' + ' '.join(command) + '"\n')
        base_command = ['sudo', '-u', 'postgres', 'psql']
        if self.port:
            port_string = '{port}'.format(port=self.port)
            base_command += ['-p', port_string]
        base_command.append('-c')
        base_command += command
        p = subprocess.Popen(
            base_command,
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
