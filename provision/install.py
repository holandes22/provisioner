import os
import sys
import logging
import importlib

from tools import get_distro

log_filename = os.path.join('/', 'var', 'log', 'newinstall-script.log')
logging.basicConfig(filename=log_filename, level=logging.DEBUG)


if __name__ == "__main__":
    distro = get_distro()
    module = importlib.import_module('.', distro, 'provisioner')
    cls = getattr(module, '{}Provisioner'.format(distro.capitalize()))

    try:
        logging.info("Starting script".center(30, '='))
        provisioner = cls()
        provisioner.install()
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        raise
    finally:
        logging.info("Finishing script".center(30, '='))
