# coding: utf-8

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from suppi.protocols.base import BaseProtocol


class BaseSource:
    def __init__(self, protocol: 'BaseProtocol'):
        self._protocol = protocol

    @property
    def protocol(self):
        return self._protocol

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, *args, **kwargs):
        raise NotImplementedError

    def __aiter__(self):
        raise NotImplementedError
