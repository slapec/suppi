# coding: utf-8

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from suppi import models


class SuppiError(Exception):
    pass


class UnknownDeviceId(SuppiError):
    def __init__(self, measurement: 'models.Measurement'):
        self.measurement = measurement

    def __str__(self):
        return f'Unknown device id {self.measurement.device_id!r}'
