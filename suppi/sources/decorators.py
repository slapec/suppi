# coding: utf-8

import asyncio
import itertools
from typing import TYPE_CHECKING, Union

from suppi.utils import switch

if TYPE_CHECKING:
    from suppi.sources.base import BaseSource


class _BaseSourceDecorator:
    def __init__(self, source: Union['BaseSource', '_BaseSourceDecorator']):
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


class repeat(_BaseSourceDecorator):  # noqa
    async def __aiter__(self):
        protocol_events = []
        async with self._source as source:
            async for protocol_event in source:
                protocol_events.append(protocol_event)
                yield protocol_event
                await switch()

        cycle = itertools.cycle(protocol_events)
        for protocol_event in cycle:
            yield protocol_event
            await switch()

    def __repr__(self):
        return f'<repeat({self._source})>'


class lag(_BaseSourceDecorator):  # noqa
    def __init__(self, source: Union['BaseSource', '_BaseSourceDecorator'], delay: float):
        super().__init__(source)
        self._delay = delay

    async def __aiter__(self):
        async with self._source as source:
            async for protocol_event in source:
                yield protocol_event
                await asyncio.sleep(self._delay)

    def __repr__(self):
        return '<lag({source}, delay={delay:.2f})>'.format(
            source=self._source,
            delay=self._delay
        )
