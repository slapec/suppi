# coding: utf-8

from typing import TYPE_CHECKING

from suppi.exceptions import SuppiError

if TYPE_CHECKING:
    from suppi import models


class DbError(SuppiError):
    ERROR_CODE = 5


class UnknownDeviceId(DbError):
    def __init__(self, measurement: 'models.Measurement'):
        self.measurement = measurement

    def __str__(self):
        return f'Unknown device id {self.measurement.device_id!r}'


class DeviceIdConflict(DbError):
    def __init__(self, device_id: str, existing_source_id: str, new_source_id: str):
        self.device_id = device_id
        self.existing_source_id = existing_source_id
        self.new_source_id = new_source_id

    def __str__(self):
        return f'Tried to bind device id {self.device_id!r} to source {self.new_source_id!r}, however it is already' \
               f' bound to {self.existing_source_id!r}'
