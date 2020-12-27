# coding: utf-8

import argparse
import os

from suppi import consts


parser = argparse.ArgumentParser(
    prog=consts.__project__,
    description="%(prog)s - What's up Pi?",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '-v', '--version',
    action='version',
    version=f'%(prog)s {consts.__version__}'
)

parser.add_argument(
    '-s', '--settings',
    default=os.getenv(consts.ENVVAR_NAME, 'settings'),
    help=f"Import Suppi settings from this Python module. If not specified the {consts.ENVVAR_NAME} environment"
         f" variable will be used which defaults to 'settings' string."
)

subparsers = parser.add_subparsers(
    title='Commands',
    dest='command',
    required=True
)
