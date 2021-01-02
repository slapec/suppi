# coding: utf-8

from typing import TYPE_CHECKING

from suppi.exceptions import SuppiError

if TYPE_CHECKING:
    from suppi import models


class ProtocolError(SuppiError):
    RETURN_CODE = 6

    def __init__(self, event: 'models.SourceEvent'):
        self.event = event


class UnknownSensorId(ProtocolError):
    def __init__(self, event: 'models.SourceEvent', sensor_id: str):
        super().__init__(event)
        self.sensor_id = sensor_id

    def __str__(self):
        return f'Unknown sensor id {self.sensor_id!r}'
