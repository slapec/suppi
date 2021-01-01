# coding: utf-8

import asyncio
import itertools
from typing import TYPE_CHECKING, Union

from suppi.utils import switch

if TYPE_CHECKING:
    from suppi.sources.base import BaseSource


class _BaseDecorator:
    def __init__(self, source: Union['BaseSource', '_BaseDecorator']):
        self._source = source

    @property
    def protocol(self):
        return self._source.protocol

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        return

    def __aiter__(self):
        return self

    async def __anext__(self):
        raise NotImplementedError


class repeat(_BaseDecorator):  # noqa
    async def __aiter__(self):
        measurements = []
        async with self._source as source:
            async for measurement in source:
                measurements.append(measurement)
                yield measurement
                await switch()

        cycle = itertools.cycle(measurements)
        for measurement in cycle:
            yield measurement
            await switch()


class lag(_BaseDecorator):  # noqa
    def __init__(self, source: Union['BaseSource', '_BaseDecorator'], delay: float):
        super().__init__(source)
        self._delay = delay

    async def __aiter__(self):
        async with self._source as source:
            async for measurement in source:
                yield measurement
                await asyncio.sleep(self._delay)
