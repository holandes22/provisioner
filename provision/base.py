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
        with open(self.get_base_config_path()) as f:
            self.config = yaml.load(f)

        # Include distro specific
        with open(self.get_config_path()) as f:
            self.config.update(yaml.load(f))

    def pre_steps(self):
        pass

    def post_steps(self):
        pass

    def install(self):
        try:
            self.pre_steps()
            self.mkdirs_in_home_folder()
            self.install_distro_packages()
            self.install_user_packages()
            self.install_python_packages()
            self.install_ruby_gems()
            self.install_node_packages()
            self.run_scripts()
        finally:
            self.post_steps()

    def get_base_config_path(self):
        base = os.path.dirname(__file__)
        return os.path.join(base, 'base_config.yml')

    def get_config_path(self):
        base = os.path.dirname(__file__)
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
        pip = 'pip' if get_distro() == 'ubuntu' else 'pip2.7'
        logger.info('Using pip: {}'.format(pip))
        call([pip, 'install', '--upgrade', 'pip'])
        call([pip, 'install', '--upgrade', 'virtualenv'])
        packages = self.config.get('python_packages')
        if packages:
            logger.info('Installing python packages: {}'.format(packages))
            call([pip, 'install'] + packages)

    def install_ruby_gems(self):
        gems = self.config.get('ruby_gems', [])
        logger.info('Installing gems {}'.format(gems))
        for gem in gems:
            call(['gem', 'install', '--no-user-install', gem])

    def install_node_packages(self):
        packages = self.config.get('node_packages', [])
        logger.info('Installing node packages {}'.format(packages))
        for package in packages:
            call(['npm', 'install', '-g', package])

    def run_scripts(self):
        module = importlib.import_module('provision.{}.scripts'.format(get_distro()))
        scripts = self.config.get('scripts', [])
        for script in scripts:
            logger.info('Running script {}'.format(script))
            func = getattr(module, script)
            func()

