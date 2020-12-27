# coding: utf-8

import atexit
import contextlib
import logging
import pathlib
import sqlite3
from typing import TYPE_CHECKING, Optional, Dict

from suppi import exceptions as exc
from suppi.utils import switch

if TYPE_CHECKING:
    from suppi import models

log = logging.getLogger(__name__)

DeviceToSourceType = Dict[str, str]


class Database:
    def __init__(self, path: pathlib.Path):
        self._path = path
        self._db: Optional[sqlite3.Connection] = None

        self._device_id_to_source_id: Optional[DeviceToSourceType] = None

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

        async with self.cursor() as c:
            await execute('''
                CREATE TABLE IF NOT EXISTS sources(
                    id TEXT NOT NULL PRIMARY KEY,
                    runtime_device_id TEXT NOT NULL
                )
            ''')

            await execute('''
                CREATE TABLE IF NOT EXISTS measurements(
                    source_id TEXT NOT NULL REFERENCES sources(id),
                    temperature REAL NOT NULL,
                    humidity REAL NULL,
                    created_at TEXT NOT NULL,
                    received_at TEXT NOT NULL 
                );
            ''')

            await execute('''
                CREATE TABLE IF NOT EXISTS failures(
                    received_at TEXT NOT NULL,
                    payload BLOB NOT NULL
                )
            ''')

        log.debug('All tables have been created')
        log.info('DB is up')

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        log.debug('Leaving the DB context')
        self._close()

    @contextlib.asynccontextmanager
    async def cursor(self):
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

    async def add_measurement(self, measurement: 'models.Measurement'):
        log.debug('Persisting %s', measurement)
        try:
            source_id = self._device_id_to_source_id[measurement.device_id]

        except KeyError:
            log.warning('Received unknown device id: %s', measurement)
            await self.add_event(measurement.event)

            raise exc.UnknownDeviceId(measurement)

        else:
            async with self.cursor() as c:
                c.execute('''
                INSERT INTO measurements(source_id, temperature, humidity, created_at, received_at)
                VALUES (?, ?, ?, ?, ?) 
                ''', (
                    source_id,
                    measurement.temperature,
                    measurement.humidity,
                    measurement.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    measurement.event.received_at.strftime('%Y-%m-%d %H:%M:%S')
                ))

            log.debug('Measurement has been added successfully')

    async def add_event(self, event: 'models.Event'):
        log.debug('Persisting %s', event)
        async with self.cursor() as c:
            c.execute('''
            INSERT INTO failures(received_at, payload)
            VALUES (?, ?)
            ''', (
                event.received_at.strftime('%Y-%m-%d %H:%M:%S'),
                event.payload
            ))

        log.debug('Failure has been added successfully')

    async def bind_device_to_source(self, device_id: str, source_id: str):
        log.info('Device id %r is now bound to source id %r', device_id, source_id)
        async with self.cursor() as c:
            c.execute('''
            INSERT INTO sources(runtime_device_id, id) 
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE
            SET runtime_device_id = ?''', (device_id, source_id, device_id))

    async def bind_devices_to_sources(self, device_id_to_source_id: DeviceToSourceType):
        self._device_id_to_source_id = {**device_id_to_source_id}
        for device_id, source_id in device_id_to_source_id.items():
            await self.bind_device_to_source(device_id, source_id)
            await switch()
