import os
import sys
import shutil
import logging
import tempfile
import platform
from contextlib import contextmanager
from subprocess import check_output, CalledProcessError, STDOUT


logger = logging.getLogger(__name__)


def run(cmd, shell=False):
    try:
        check_output(cmd, shell=shell, stderr=STDOUT)
    except CalledProcessError as e:
        cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
        print 'Got error {} while running command {}'.format(e.output, cmd_str)
        raise


def get_distro():
    distro = platform.linux_distribution()[0].lower()
    if distro == '':
        distro = 'arch'
    return distro


def is_root():
    if not os.geteuid() == 0:
        logger.error('Running with unprivileged user. Exiting.')
        sys.exit('Run script as root')


def create_symlink(src, link, backup=True):
    logger.info('Creating link %s' % link)
    try:
        if os.path.exists(link):
            if os.path.islink(link):
                logger.info('symlink %s already exists. Unlinking and creating a new one' % link)
                os.unlink(link)
            else:
                if backup:
                    logger.info('File {} already exists. Moving to {}.bak and creating a new one'.format(link, link))
                    shutil.move(link, link + '.bak')
                else:
                    logger.info('Removing path {}'.format(link))
                    os.remove(link)
        os.symlink(src, link)
    except OSError as e:
        print 'Error {} while creating link {} for src {}'.format(e, link, src)
        raise e


@contextmanager
def tempdir(remove_tempdir=True):
    temp = tempfile.mkdtemp()
    try:
        yield temp
    finally:
        if remove_tempdir:
            shutil.rmtree(temp)


@contextmanager
def cd(path):
    cwd = os.getcwd()
    try:
        yield os.chdir(path)
    finally:
        os.chdir(cwd)
