# coding: utf-8

import asyncio
import logging
from typing import TYPE_CHECKING, Optional

from suppi import models
from suppi.cli.parser import subparsers

if TYPE_CHECKING:
    import argparse

log = logging.getLogger(__name__)


async def main(settings: models.Settings):
    async with settings.DATABASE as db:
        await db.bind_devices_to_sources(DEVICES_TO_SOURCES)

        async with SourceManager(*settings.SOURCES) as manager:
            async for measurement in manager:  # type: models.Measurement
                try:
                    await db.add_measurement(measurement)

                except exc.UnknownDeviceId as e:
                    log.warning(e)
                    await db.add_event(e.measurement.event)


def command(settings: models.Settings, args: 'argparse.Namespace') -> Optional[int]:
    loop = asyncio.get_event_loop()
    return_code = loop.run_until_complete(main(settings))

    return return_code


parser = subparsers.add_parser(
    'listen',
    help='Listen and persist events into database'
)

parser.set_defaults(func=command)
