import logging
from subprocess import call

from provision.base import BaseProvisioner


logger = logging.getLogger(__name__)


class UbuntuProvisioner(BaseProvisioner):

    def install_distro_packages(self):
        logger.info('Installing Ubuntu Packages')
        packages = self.config.get('distro_packages')
        call(['apt-get', 'update'])
        cmd = ['apt-get', 'install', '--yes'] + packages
        retcode = call(cmd)
        if retcode != 0:
            raise OSError('Error installing packages')

    def install_user_packages(self):
        logger.info('Installing Ubuntu PPAs')
        packages = self.config.get('user_packages')
        for ppa in packages.values():
            call(['add-apt-repository', '--yes', ppa])
        call(['apt-get', 'update'])
        for package in packages:
            call(['apt-get', 'install', '--yes', package])
