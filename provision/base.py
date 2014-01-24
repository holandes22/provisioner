import os
import pwd
import grp
import logging
import importlib
from subprocess import call

import yaml

from provision.tools import get_distro


logger = logging.getLogger(__name__)


class Provisioner(object):

    pip = 'pip'

    def __new__(cls, actions='all'):
        distro = get_distro()
        module = importlib.import_module(
            'provision.{}.provisioner'.format(distro)
        )
        cls_type = getattr(module, '{}Provisioner'.format(distro.capitalize()))
        instance = super(Provisioner, cls).__new__(cls_type)
        instance.distro = distro
        return instance

    def __init__(self, actions='all'):
        with open(self.get_base_config_path()) as f:
            self.config = yaml.load(f)

        # Include distro specific
        with open(self.get_config_path()) as f:
            self.config.update(yaml.load(f))

        if actions == 'all':
            self.actions = [
                'pre_steps',
                'mkdirs_in_home_folder',
                'install_distro_packages',
                'install_user_packages',
                'install_python_packages',
                'install_ruby_gems',
                'install_node_packages',
                'run_scripts',
                'post_steps',
            ]
        else:
            self.actions = actions

    def pre_steps(self):
        pass

    def post_steps(self):
        pass

    def install(self):
        for action in self.actions:
            getattr(self, action)()

    def get_base_config_path(self):
        base = os.path.dirname(__file__)
        return os.path.join(base, 'base_config.yml')

    def get_config_path(self, distro=None):
        base = os.path.dirname(__file__)
        return os.path.join(base, self.distro, 'config.yml')

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
        logger.info('Using pip: {}'.format(self.pip))
        call([self.pip, 'install', '--upgrade', 'pip'])
        call([self.pip, 'install', '--upgrade', 'virtualenv'])
        packages = self.config.get('python_packages')
        if packages:
            logger.info('Installing python packages: {}'.format(packages))
            call([self.pip, 'install'] + packages)

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
        try:
            module = importlib.import_module(
                'provision.{}.scripts'.format(self.distro)
            )
        except ImportError:
            logger.warning('scripts module is not importable. Skipping step.')
            return

        scripts = self.config.get('scripts', [])
        for script in scripts:
            logger.info('Running script {}'.format(script))
            func = getattr(module, script)
            func()
