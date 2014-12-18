import logging
from subprocess import call

from provision.base import Provisioner


logger = logging.getLogger(__name__)


class FedoraProvisioner(Provisioner):

    upgrade_pip = False

    def pre_steps(self):
        self.configure_rpm_fusion()

    def install_distro_packages(self):
        logger.info('Installing Fedora Packages')
        packages = self.config.get('distro_packages')
        cmd = ['yum', 'install', '-y'] + packages
        retcode = call(cmd)
        if retcode != 0:
            raise OSError('Error installing packages')

    def install_user_packages(self):
        pass

    def configure_rpm_fusion(self):
        cmd = r'''su -c 'yum localinstall --nogpgcheck
        http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E \%fedora).noarch.rpm
        http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E \%fedora).noarch.rpm'''
        call(cmd)
