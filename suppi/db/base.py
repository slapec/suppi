# coding: utf-8

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from suppi import models

log = logging.getLogger(__name__)


class BaseDatabase:
    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, *args, **kwargs):
        raise NotImplementedError

    async def register_sensor_id(self, sensor_id: str):
        raise NotImplementedError

    async def save_measurement(self, measurement: 'models.Measurement'):
        raise NotImplementedError

    async def save_event(self, event: 'models.SourceEvent'):
        raise NotImplementedError
