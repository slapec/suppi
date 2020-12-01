# coding: utf-8

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from suppi.db import Database
    from suppi.sources import BaseSource


class SourceManager:
    def __init__(self, *sources: 'BaseSource'):
        self._sources = tuple(sources)

    def __aiter__(self):
        return self

    async def __anext__(self):
        pass
