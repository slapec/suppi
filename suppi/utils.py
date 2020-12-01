# coding: utf-8

import asyncio


async def iter_stream(stream):
    while True:
        line = await stream.readline()
        if not line:
            break

        yield line


async def switch():
    # Let the loop roll
    return await asyncio.sleep(0)
