# coding: utf-8

import asyncio
import importlib
import logging

from suppi import models, exceptions as exc

log = logging.getLogger(__name__)


async def iter_stream(stream):
    while True:
        line = await stream.readline()
        if not line:
            break

        yield line


async def switch():
    # Let the loop roll
    return await asyncio.sleep(0)


def import_settings(settings_module_name: str) -> models.Settings:
    try:
        settings_module = importlib.import_module(settings_module_name)

        return models.Settings(settings_module)

    except Exception as e:
        raise exc.SettingsModuleError(
            f'Failed to import settings from the {settings_module_name!r} Python module.'
            f' See the traceback for more information.'
        )
