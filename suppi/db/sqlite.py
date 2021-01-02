# coding: utf-8

import atexit
import contextlib
import logging
import pathlib
import sqlite3
from typing import TYPE_CHECKING, Optional

from suppi.db.base import BaseDatabase
from suppi.utils import switch

if TYPE_CHECKING:
    from suppi import models

log = logging.getLogger(__name__)


class Sqlite(BaseDatabase):
    def __init__(self, path: pathlib.Path):
        super().__init__()

        self._path = path
        self._db: Optional[sqlite3.Connection] = None

        log.info('DB path is: %s', self._path)

    @classmethod
    def _dict_factory(cls, cursor_, row):
        d = {}
        for idx, col in enumerate(cursor_.description):
            d[col[0]] = row[idx]
        return d

    def _close(self):
        if self._db:
            log.info('Closing DB')
            self._db.close()
            self._db = None
            log.info('DB is down')

    async def __aenter__(self):
        assert self._db is None

        async def execute(query):
            log.debug(query)
            c.execute(query)
            await switch()

        log.info('Opening DB')
        self._db = db = sqlite3.connect(str(self._path))
        atexit.register(self._close)
        db.row_factory = self._dict_factory
        log.debug('DB: %s', db)
        await switch()

        async with self._cursor() as c:
            await execute('''
                CREATE TABLE IF NOT EXISTS sensors(
                    id TEXT NOT NULL PRIMARY KEY
                )
            ''')

            await execute('''
                CREATE TABLE IF NOT EXISTS measurements(
                    sensor_id TEXT NOT NULL REFERENCES sensors(id),
                    created_at TEXT NOT NULL,
                    received_at TEXT NOT NULL,
                    
                    -- TODO: Might switch to json one day
                    temperature REAL NOT NULL,
                    humidity REAL NULL
                );
            ''')

            await execute('''
                CREATE TABLE IF NOT EXISTS events(
                    received_at TEXT NOT NULL,
                    payload BLOB NOT NULL
                )
            ''')

        log.debug('All tables have been created')
        log.info('DB is up')

        return self

    async def __aexit__(self, *args, **kwargs):
        log.debug('Leaving the DB context')
        self._close()

    @contextlib.asynccontextmanager
    async def _cursor(self):
        assert self._db

        db = self._db
        c = db.cursor()
        await switch()

        try:
            yield c
            await switch()
            db.commit()

        except Exception as e:
            await switch()
            db.rollback()
            await switch()
            raise

    async def register_sensor_id(self, sensor_id: str):
        log.debug('Registering sensor_id %r', sensor_id)
        async with self._cursor() as c:
            c.execute('''
            INSERT INTO sensors(id) 
            VALUES (?)
            ON CONFLICT DO NOTHING 
            ''', (sensor_id,))
        log.debug('Sensor has been registered')

    async def save_measurement(self, measurement: 'models.Measurement'):
        log.debug('Saving %s', measurement)

        async with self._cursor() as c:
            c.execute('''
            INSERT INTO measurements(sensor_id, created_at, received_at, temperature, humidity)
            VALUES (?, ?, ?, ?, ?) 
            ''', (
                measurement.sensor_id,
                measurement.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                measurement.source_event.received_at.strftime('%Y-%m-%d %H:%M:%S'),
                measurement.temperature,
                measurement.humidity
            ))

        log.debug('Saved measurement successfully')

    async def save_event(self, event: 'models.SourceEvent'):
        log.debug('Saving %s', event)

        async with self._cursor() as c:
            c.execute('''
            INSERT INTO events(received_at, payload)
            VALUES (?, ?)
            ''', (
                event.received_at.strftime('%Y-%m-%d %H:%M:%S'),
                event.payload
            ))

        log.debug('Saved event successfully')
