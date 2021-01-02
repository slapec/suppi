# coding: utf-8

import copy
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from suppi import models


class BaseProtocol:
    def __init__(self, sensor_id_translations: Dict[str, str]):
        self._sensor_id_translations = copy.deepcopy(sensor_id_translations)

    @property
    def sensor_id_translations(self):
        return MappingProxyType(self._sensor_id_translations)

    async def on_event(self, source_event: 'models.SourceEvent') -> 'models.Measurement':
        raise NotImplementedError
