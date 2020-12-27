# coding: utf-8

import logging
import logging.config
import os
import pathlib
import traceback
from typing import Optional

from suppi import consts, utils, exceptions as exc
from suppi.cli.commands import listen
from suppi.cli.parser import parser

log = logging.getLogger(__name__)


def main() -> Optional[int]:
    args = parser.parse_args()

    return_code = 0
    try:
        settings = utils.import_settings(args.settings)
        logging.config.dictConfig(settings.LOGGING)

        log.info('%s %s', consts.__project__, consts.__version__)
        log.debug('Arguments: %s', args)
        log.debug('Environment: %s', os.environ)
        log.debug('Working directory: %s', pathlib.Path.cwd())

        command = args.func
        log.debug('Executing %s', command.__module__)

        return_code = command(settings, args)

    except exc.SuppiError as e:
        return_code = e.RETURN_CODE

        if isinstance(e, exc.SettingsModuleError):
            log.error(traceback.format_exc())

        else:
            log.error(e)

    except Exception as e:
        log.error(traceback.format_exc())
        log.error('Suppi has crashed due to an unexpected error.')
        return_code = 1

    finally:
        log.debug('Main returns with %s', return_code)

        return return_code
