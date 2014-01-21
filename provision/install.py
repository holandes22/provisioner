import os
import sys
import logging
import argparse
import importlib

package = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, package)

from provision.tools import get_distro, is_root



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='install.py',
        usage='%(prog)s [options]'
    )
    parser.add_argument(
        '--actions',
        default='all',
        help='Determine which actions to run, default=all. Comma separated.'
    )
    parser.add_argument(
        '-d',
        '--distro',
        default=None,
        help='Specify distro (by default it tries alone to do so).'
    )
    args = parser.parse_args()

    if not args.distro:
        distro = get_distro()
    else:
        distro = args.distro

    module = importlib.import_module('provision.{}.provisioner'.format(distro))
    cls = getattr(module, '{}Provisioner'.format(distro.capitalize()))

    provisioner_kwargs = {'distro': distro, 'actions': args.actions}

    try:
        log_filename = os.path.join('/', 'var', 'log', 'newinstall-script.log')
        logging.basicConfig(filename=log_filename, level=logging.DEBUG)
        logging.info("Starting script".center(30, '='))
        is_root()
        provisioner = cls(**provisioner_kwargs)
        provisioner.install()
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        raise
    finally:
        logging.info("Finishing script".center(30, '='))
