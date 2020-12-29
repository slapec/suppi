# coding: utf-8

import asyncio
import itertools
import json
import logging
import pathlib
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Union

from suppi import models
from suppi.sources import base

if TYPE_CHECKING:
    from suppi.protocols.base import BaseProtocol

log = logging.getLogger(__name__)


class FileSource(base.BaseSource):
    def __init__(self, protocol: 'BaseProtocol', file_path: Union[str, pathlib.Path], delay: float = 0.3,
                 infinite: bool = False):
        super().__init__(protocol)

        self._file_path = pathlib.Path(file_path)
        self._delay = delay
        self._infinite = infinite

        self._file = None
        self._file_it = None

    async def __aenter__(self):
        assert self._file is None
        file = self._file = self._file_path.open('rb')
        file.__enter__()
        if self._infinite:
            self._file_it = itertools.cycle(file)
        else:
            self._file_it = iter(file)

        return self

    async def __aexit__(self, *args, **kwargs):
        file = self._file
        self._file, self._file_it = None, None
        return file.__exit__(*args, **kwargs)

    def __aiter__(self):
        return self

    async def __anext__(self) -> models.Measurement:
        assert self._file is not None

        try:
            line = next(self._file_it)
            event = models.Event.with_defaults(line)

        except StopIteration:
            raise StopAsyncIteration

        measurement = self._protocol # TODO: Continue here

        try:
            model_dict = json.loads(line)
            model = models.Measurement(
                event=event,
                device_id=str(model_dict['id']),
                temperature=float(model_dict['temperature_C']),
                humidity=float(model_dict['humidity']),
                created_at=datetime.strptime(model_dict['time'], '%Y-%m-%d %H:%M:%S')
            )

        except KeyError:
            log.error('Failed to parse %s', line)
            # continue

        await asyncio.sleep(self._delay)
        return model
