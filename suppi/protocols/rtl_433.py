# coding: utf-8

import json
from datetime import datetime

from suppi import models
from suppi.protocols import exceptions as exc
from suppi.protocols.base import BaseProtocol


class Rtl433(BaseProtocol):
    async def on_event(self, source_event: 'models.SourceEvent') -> 'models.Measurement':
        try:
            model_dict = json.loads(source_event.payload)
            sensor_id = str(model_dict['id'])

            try:
                sensor_id = self.sensor_id_translations[sensor_id]
            except KeyError:
                raise exc.UnknownSensorId(source_event, sensor_id)

            model = models.Measurement(
                source_event=source_event,
                sensor_id=sensor_id,
                temperature=float(model_dict['temperature_C']),
                humidity=float(model_dict['humidity']),
                created_at=datetime.strptime(model_dict['time'], '%Y-%m-%d %H:%M:%S')
            )

        except exc.UnknownSensorId:
            raise

        except Exception as e:
            raise exc.ProtocolError(source_event)

        else:
            return model

    def __repr__(self):
        return '<Rtl433>'
