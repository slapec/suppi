# coding: utf-8

import asyncio
import logging
from typing import TYPE_CHECKING, Iterable, Optional

from suppi import utils

if TYPE_CHECKING:
    from suppi.sources.base import BaseSource

log = logging.getLogger(__name__)


class SourceManager:
    def __init__(self, sources: Iterable['BaseSource']):
        self._sources = tuple(sources)
        self._contexts = []
        self._consumer_tasks = []

        self._queue_from_tasks: Optional[asyncio.Queue] = None

    def __aiter__(self):
        return self

    async def __aenter__(self):
        assert self._queue_from_tasks is None
        self._queue_from_tasks = asyncio.Queue()

        log.debug('Setting up sources: %s', self._sources)
        for source in self._sources:
            log.debug('Setting up %s', source)
            await source.__aenter__()

            task = asyncio.create_task(utils.consume_source(source, self._queue_from_tasks))
            self._consumer_tasks.append(task)
            self._contexts.append(source)
            log.debug('%s is up', source)

        return self

    async def __anext__(self):
        assert self._queue_from_tasks is not None
        return await self._queue_from_tasks.get()

    async def __aexit__(self, *args, **kwargs):
        log.debug('Shutting down resources: %s', self._sources)
        for source in self._contexts:
            log.debug('Shutting down %s', source)
            await source.__aexit__(*args, **kwargs)
            log.debug('%s is down', source)

        self._queue_from_tasks = None
