import os
import pwd
import grp
import logging
import importlib
from subprocess import call

import yaml

from provision.tools import get_distro


logger = logging.getLogger(__name__)


class BaseProvisioner(object):

    def __init__(self):
        with open(self.get_config_path()) as f:
            self.config = yaml.load(f)

    def install(self):
        self.mkdirs_in_home_folder()
        self.install_distro_packages()
        self.install_user_packages()
        self.install_python_packages()
        self.install_ruby_gems()
        self.install_node_packages()
        self.run_scripts()

    def get_config_path(self):
        base = os.path.dirname(__file__)
        print os.path.join(base, get_distro(), 'config.yml')
        return os.path.join(base, get_distro(), 'config.yml')

    def mkdirs_in_home_folder(self):
        home_folder = self.config.get('home')
        directories = self.config.get('home_folders')

        for directory in directories:
            path = os.path.join(home_folder, directory)
            try:
                os.mkdir(path)
            except OSError:
                logger.info('{} already exists. Skipping.'.format(directory))
            finally:
                uid = pwd.getpwnam(self.config.get('user')).pw_uid
                gid = grp.getgrnam(self.config.get('group')).gr_gid
                os.chown(path, uid, gid)

    def install_distro_packages(self):
        raise NotImplementedError()

    def install_user_packages(self):
        raise NotImplementedError()

    def install_python_packages(self):
        logger.info('Installing pip and virtualenv')
        # requires to be run after distro packages
        call(['pip', 'install', '--upgrade', 'pip'])
        call(['pip', 'install', '--upgrade', 'virtualenv'])
        packages = self.config.get('python_packages')
        logger.info('Installing python packages: {}'.format(packages))
        call(['pip', 'install'] + packages)

    def install_ruby_gems(self):
        gems = self.config.get('ruby_gems')
        logger.info('Installing gems {}'.format(gems))
        for gem in gems:
            call(['gem', 'install', gem])

    def install_node_packages(self):
        packages = self.config.get('node_packages')
        logger.info('Installing node packages {}'.format(packages))
        for package in packages:
            call(['npm', 'install', '-g', package])

    def run_scripts(self):
        module = importlib.import_module('provision.{}.scripts'.format(distro))
        scripts = self.config.get('scripts')
        for script in scripts:
            logger.info('Running script {}'.format(script))
            func = getattr(module, script)
            func()

