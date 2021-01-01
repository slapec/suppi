# coding: utf-8

import json
from datetime import datetime

from suppi import models
from suppi.protocols import exceptions as exc
from suppi.protocols.base import BaseProtocol


class Rtl433(BaseProtocol):
    async def on_event(self, event: 'models.Event') -> 'models.Measurement':
        try:
            model_dict = json.loads(event.payload)
            model = models.Measurement(
                event=event,
                device_id=str(model_dict['id']),
                temperature=float(model_dict['temperature_C']),
                humidity=float(model_dict['humidity']),
                created_at=datetime.strptime(model_dict['time'], '%Y-%m-%d %H:%M:%S')
            )

        except Exception as e:
            raise exc.ProtocolError()

        else:
            return model
