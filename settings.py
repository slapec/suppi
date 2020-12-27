# coding: utf-8

import pathlib

from suppi import db, sources

APP_DIR = pathlib.Path(__file__).parent

DATABASE = db.Database(APP_DIR / 'appdata/suppi.sqlite3')

SOURCES = [
    sources.DummyFileSource(
        file_path=APP_DIR / '/temp.json',
        # protocol=protocols.Rtl433
    )
]
