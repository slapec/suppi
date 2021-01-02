# coding: utf-8

import asyncio
import logging
from typing import TYPE_CHECKING, Optional

from suppi import manager, models
from suppi.cli.parser import subparsers

if TYPE_CHECKING:
    import argparse

log = logging.getLogger(__name__)


async def main(settings: models.Settings):
    async with settings.DATABASE as db, manager.SourceManager(settings.SOURCES) as sources:
        for source in sources.sources:
            for sensor_id in source.protocol.sensor_id_translations.values():
                await db.register_sensor_id(sensor_id)

        async for protocol_event in sources:  # type: models.ProtocolEvent
            measurement = protocol_event.measurement
            if measurement is not None:
                await db.save_measurement(measurement)

            else:
                await db.save_event(protocol_event.source_event)

        log.info('No more measurements are left, exiting.')


def command(settings: models.Settings, args: 'argparse.Namespace') -> Optional[int]:
    return_code = asyncio.run(main(settings))

    return return_code


parser = subparsers.add_parser(
    'listen',
    help='Listen and persist events into database'
)

parser.set_defaults(func=command)
