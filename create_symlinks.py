import os
import sys
import logging
import argparse
from provision.tools import create_symlink

HOME_FOLDER = os.getenv('HOME')
DOTFILES_ROOT = os.path.join(HOME_FOLDER, 'provisioner', 'dotfiles')

CREATE_FOLDERS = ['.pip']

DOTFILE_LINKS_AND_NAMES = {
    '.gitignore_global': '.gitignore_global',
    '.gitconfig': '.gitconfig.personal',
    '.vimrc': '.vimrc',
    '.bashrc': '.bashrc',
    '.bash_profile': '.bash_profile',
    '.pip/pip.conf': '.pip/pip.conf',
    '.tmux.conf': '.tmux.conf',
    '.tmuxinator': 'tmuxinator',
    '.fonts.conf': '.fonts.conf',
    '.pylintrc': '.pylintrc',
}

logging.basicConfig(
    filename=os.path.join(HOME_FOLDER, 'create_symlinks.log'),
    level=logging.DEBUG,
)


def create_folders():
    for folder in CREATE_FOLDERS:
        try:
            os.mkdir(os.path.join(HOME_FOLDER, folder))
        except OSError:
            logging.info('Skipping already existing folder: {}'.format(folder))


def set_symlinks():
    for link_name in DOTFILE_LINKS_AND_NAMES.keys():
        logging.info('Creating link %s' % link_name)
        src = os.path.join(DOTFILES_ROOT, DOTFILE_LINKS_AND_NAMES[link_name])
        link = os.path.join(HOME_FOLDER, link_name)
        print 'Setting link source {0}, link name {1}'.format(src, link)
        create_symlink(src, link)


def main():
    logging.info("Starting script".center(35, '='))
    try:
        create_folders()
        set_symlinks()
    except Exception as e:
        logging.error('An error occured in main {}'.format(e))
        raise
    finally:
        logging.info("Finishing script".center(35, '='))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='create_symlinks.py',
        usage='%(prog)s [options]',
    )
    parser.add_argument(
        '-w',
        '--work',
        action='store_true',
        help='Dev location: work or personal',
    )
    args = parser.parse_args()
    if args.work:
        DOTFILE_LINKS_AND_NAMES['.gitconfig'] = '.gitconfig.work'
    main()
    sys.exit(0)
