import os
import argparse
import logging
from subprocess import call, CalledProcessError

from ..tools import tempdir, create_symlink, cd, run


logger = logging.getLogger(__name__)


def install_heroku_toolbelt():
    run('wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh', shell=True)


def install_vim(tag=None):
    config_path = '/usr/lib/python2.7/config-x86_64-linux-gnu'
    with tempdir(False) as build_dir:
        vim_src_dir = os.path.join(build_dir, 'vim_src')
        logger.info('Cloning Vim repo')
        run(['hg', 'clone', 'https://vim.googlecode.com/hg/', vim_src_dir])
        with cd(vim_src_dir):
            if tag:
                run(['hg', 'update', tag]) #-rv7-3-1034, -rv7-4b-022
            run(['./configure', '--enable-multibyte', '--with-tlib=ncurses', '--enable-pythoninterp=yes',
                '--enable-rubyinterp=yes', '--with-features=huge', '--with-python-config-dir={}'.format(config_path)])
            run(['make', vim_src_dir, '-j', '3'])
            run(['make', vim_src_dir, 'install'])
        logger.info('Vim compiled and installed. Linking to /usr/bin/vim')
        create_symlink('/usr/local/bin/vim', '/usr/bin/vim', backup=False)


def install_chrome():
    filename = os.path.join('/', 'tmp', 'google-chrome-stable_current_amd64.deb')
    url = 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
    run(['wget', '-O', filename, url])
    try:
        run(['dpkg', '-i', filename])
    except CalledProcessError:
        run(['apt-get', 'install', '-f'])


def install_virtualbox():
    with open('/etc/apt/sources.list.d/virtualbox.list', 'w') as f:
        f.write('deb http://download.virtualbox.org/virtualbox/debian wheezy contrib')
    call('wget -q http://download.virtualbox.org/virtualbox/debian/oracle_vbox.asc -O- | sudo apt-key add -', shell=True)
    call(['apt-get', 'update'])
    call(['apt-get', 'install', 'virtualbox-4.3'])


def set_locale():
    lines = []
    filepath = '/etc/default/locale'
    with open(filepath, 'r') as locale_file:
        lines = locale_file.readlines()
    with open(filepath, 'w') as locale_file:
        for line in lines:
            locale_file.write(line.replace('he_IL', 'en_US'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='scripts',
        usage='%(prog)s [options]',
    )
    parser.add_argument('-r', '--run', help='Run script by func name.')
    args = parser.parse_args()
    locals()['{}'.format(args.run)]()
