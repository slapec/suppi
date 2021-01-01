# coding: utf-8

import copy
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from suppi import models


class BaseProtocol:
    def __init__(self, device_source_map: Dict[str, str]):
        self._device_source_map = copy.deepcopy(device_source_map)

    @property
    def device_source_map(self):
        return MappingProxyType(self._device_source_map)

    async def on_event(self, event: 'models.Event') -> 'models.Measurement':
        raise NotImplementedError
