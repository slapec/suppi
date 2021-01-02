# coding: utf-8

import pathlib

from suppi import db, sources, protocols
from suppi.sources.decorators import lag, repeat

APP_DIR = pathlib.Path(__file__).parent

DATABASE = db.Sqlite(APP_DIR / 'appdata/suppi.sqlite3')

SOURCES = [
    sources.FileSource(
        protocol=protocols.Rtl433({
            '65': 'living_room',
            '69': 'outdoor'
        }),
        file_path=APP_DIR / 'temp.json'
    )
]
