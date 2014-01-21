import os
import sys
import logging
import argparse

package = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, package)

from provision.base import Provisioner
from provision.tools import is_root


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='install.py',
        usage='%(prog)s [options]'
    )
    parser.add_argument(
        '--actions',
        help='Determine which actions to run, default=all. Comma separated.'
    )
    args = parser.parse_args()

    provisioner_kwargs = {}
    if args.actions:
        provisioner_kwargs.update({'actions': args.actions.split(',')})

    try:
        log_filename = os.path.join('/', 'var', 'log', 'newinstall-script.log')
        logging.basicConfig(filename=log_filename, level=logging.DEBUG)
        is_root()
        provisioner = Provisioner(**provisioner_kwargs)
        logging.info(
            'Starting script for distro {}'.format(provisioner.distro).center(30, '=')
        )
        provisioner.install()
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        raise
    finally:
        logging.info("Finishing script".center(30, '='))
