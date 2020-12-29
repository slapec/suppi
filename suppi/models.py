# coding: utf-8

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Iterable, NamedTuple, Optional

if TYPE_CHECKING:
    from suppi.db.base import BaseDatabase
    from suppi.sources.base import BaseSource


class Event(NamedTuple):
    payload: bytes
    received_at: datetime

    @classmethod
    def with_defaults(cls, payload: bytes):
        return cls(
            payload=payload,
            received_at=datetime.now()
        )


class Measurement(NamedTuple):
    event: Event
    device_id: str
    temperature: float
    humidity: Optional[float]
    created_at: datetime


class Settings:
    DATABASE: 'BaseDatabase'
    SOURCES: Iterable['BaseSource']
    LOGGING: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            'suppi': {
                'level': 'DEBUG',
                'handlers': ['console_verbose']
            }
        },
        'handlers': {
            'console_verbose': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(asctime)s | %(levelname)-7s | %(message)s'
            }
        }
    }

    def __init__(self, settings_module):
        self._module = settings_module

    def __getattr__(self, item):
        return getattr(self._module, item)
