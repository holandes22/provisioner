import os
import sys
import logging
import argparse
from subprocess import call, CalledProcessError

here = lambda * x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
package = here('..', '..')
sys.path.insert(0, package)

from provision.tools import tempdir, create_symlink, cd, run


logger = logging.getLogger(__name__)


def install_vim(tag=None):
    config_path = '/usr/lib/python2.7/config'
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='scripts',
        usage='%(prog)s [options]',
    )
    parser.add_argument('-r', '--run', help='Run script by func name.')
    args = parser.parse_args()
    locals()['{}'.format(args.run)]()
