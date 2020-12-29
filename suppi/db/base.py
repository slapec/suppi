# coding: utf-8

import logging
from typing import TYPE_CHECKING, Optional, Dict

from suppi.db import exceptions as exc

if TYPE_CHECKING:
    from suppi import models

log = logging.getLogger(__name__)


class BaseDatabase:
    def __init__(self):
        self._device_id_to_source_id: Optional[Dict[str, str]] = {}

    def resolve_source_id_of_measurement(self, measurement: 'models.Measurement') -> str:
        try:
            return self._device_id_to_source_id[measurement.device_id]

        except KeyError:
            raise exc.UnknownDeviceId(measurement)

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, *args, **kwargs):
        raise NotImplementedError

    async def save_measurement(self, measurement: 'models.Measurement'):
        raise NotImplementedError

    async def save_event(self, event: 'models.Event'):
        raise NotImplementedError

    async def _bind_device_to_source(self, device_id: str, source_id: str):
        raise NotImplementedError

    async def bind_device_to_source(self, device_id: str, source_id: str):
        if device_id in self._device_id_to_source_id:
            raise exc.DeviceIdConflict(device_id, self._device_id_to_source_id[device_id], source_id)

        log.debug('Binding id %r to source id %r', device_id, source_id)
        await self._bind_device_to_source(device_id, source_id)
        log.info('Device id %r is now bound to source id %r', device_id, source_id)
