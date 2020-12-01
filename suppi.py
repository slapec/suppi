# coding: utf-8

import asyncio
import logging.config
import pathlib

import suppi.db
from suppi import exceptions as exc
from suppi import models
from suppi.manager import SourceManager
from suppi.sources import DummyFileSource


DEVICES_TO_SOURCES = {
    '65': 'living_room',
    '69': 'outdoor',
    'cpu': 'cpu'
}

APP_DIR = pathlib.Path(__file__).parent

log = logging.getLogger(__name__)


async def main(db_path: pathlib.Path):
    async with suppi.db.Database(db_path) as db:
        await db.bind_devices_to_sources(DEVICES_TO_SOURCES)

        fs = DummyFileSource('./temp.json')
        async with SourceManager(fs) as manager:
            async for measurement in manager:  # type: models.Measurement
                try:
                    await db.add_measurement(measurement)

                except exc.UnknownDeviceId as e:
                    log.warning(e)
                    await db.add_event(e.measurement.event)


if __name__ == '__main__':
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            'suppi': {
                'level': 'DEBUG',
                'handlers': ['console_verbose']
            }
        },
        'handlers': {
            'console_verbose': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(asctime)s | %(levelname)-7s | %(message)s'
            }
        }
    })

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(APP_DIR / 'appdata/suppi.sqlite3'))
