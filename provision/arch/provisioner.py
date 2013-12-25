import logging
from subprocess import call

from provision.tools import setuid
from provision.base import BaseProvisioner


logger = logging.getLogger(__name__)


class ArchProvisioner(BaseProvisioner):

    def pre_steps(self):
        self.install_yaourt()

    def post_steps(self):
        call(['systemctl', 'enable', 'sshd.service'])

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
        call(['yaourt', '--noconfirm', '-S'] + packages.keys())

    def install_ruby_gems(self):
        gems = self.config.get('ruby_gems')
        logger.info('Installing gems {}'.format(gems))
        with setuid(self.config.get('user')):
            for gem in gems:
                call(['gem', 'install', gem])
