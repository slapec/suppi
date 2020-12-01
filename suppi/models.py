# coding: utf-8

import dataclasses
from datetime import datetime
from typing import NamedTuple, Optional


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
