import logging
import tarfile
from subprocess import call

from provision.base import BaseProvisioner
from provision.tools import tempdir


logger = logging.getLogger(__name__)


class ArchProvisioner(BaseProvisioner):

    def pre_steps(self):
        self.install_yaourt()

    def install_yaourt(self):
        with open('/etc/pacman.conf', 'a') as f:
            f.write('''\n[archlinuxfr]\nSigLevel = Never\nServer = http://repo.archlinux.fr/$arch''')
        # Sync and install
        call(['pacman', '-Sy', '--noconfirm', 'yaourt'])

    def install_distro_packages(self):
        logger.info('Installing Arch Packages')
        packages = self.config.get('distro_packages')
        call(['pacman', '-Sy', '--noconfirm'])
        cmd = ['pacman', '--noconfirm', '-S'] + packages
        retcode = call(cmd)
        if retcode != 0:
            raise OSError('Error installing packages')

    def install_user_packages(self):
        logger.info('Installing AURs')
        packages = self.config.get('user_packages')
        call(['pacman', '-Sy', '--noconfirm'])
        call(['yaour', '--noconfirm', '-S'] + packages.keys())
