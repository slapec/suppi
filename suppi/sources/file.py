# coding: utf-8

import logging
import pathlib
from typing import TYPE_CHECKING
from typing import Union

from suppi import models
from suppi.protocols import exceptions as exc
from suppi.sources import base

if TYPE_CHECKING:
    from suppi.protocols.base import BaseProtocol

log = logging.getLogger(__name__)


class FileSource(base.BaseSource):
    def __init__(self, protocol: 'BaseProtocol', file_path: Union[str, pathlib.Path]):
        super().__init__(protocol)

        self._file_path = pathlib.Path(file_path)

        self._file = None
        self._line_it = None

    async def __aenter__(self):
        assert self._file is None
        file = self._file = self._file_path.open('rb')
        file.__enter__()
        self._line_it = iter(file)

        return self

    async def __aexit__(self, *args, **kwargs):
        file = self._file
        self._file, self._line_it = None, None
        return file.__exit__(*args, **kwargs)

    def __aiter__(self):
        return self

    async def __anext__(self) -> models.Measurement:
        assert self._file is not None

        try:
            line = next(self._line_it)
            event = models.Event.with_defaults(line)

        except StopIteration:
            raise StopAsyncIteration

        try:
            measurement = await self._protocol.on_event(event)

        except exc.ProtocolError:
            log.exception('Failed to parse %s', event.payload)

        else:
            return measurement
