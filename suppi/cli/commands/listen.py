# coding: utf-8

import asyncio
import logging
from typing import TYPE_CHECKING, Optional

from suppi import manager, models
from suppi.cli.parser import subparsers
from suppi.db import exceptions as db_exc

if TYPE_CHECKING:
    import argparse

log = logging.getLogger(__name__)


async def main(settings: models.Settings):
    async with settings.DATABASE as db, manager.SourceManager(settings.SOURCES) as sources:
        async for measurement in sources:  # type: models.Measurement
            try:
                await db.save_measurement(measurement)

            except db_exc.UnknownDeviceId as e:
                log.warning(e)
                await db.save_event(measurement.event)

        log.info('No more measurements are left, exiting.')


def command(settings: models.Settings, args: 'argparse.Namespace') -> Optional[int]:
    return_code = asyncio.run(main(settings))

    return return_code


parser = subparsers.add_parser(
    'listen',
    help='Listen and persist events into database'
)

parser.set_defaults(func=command)
