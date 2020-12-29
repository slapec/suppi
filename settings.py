# coding: utf-8

import pathlib

from suppi import db, sources, protocols


APP_DIR = pathlib.Path(__file__).parent

DATABASE = db.Sqlite(APP_DIR / 'appdata/suppi.sqlite3')

SOURCES = [
    sources.FileSource(protocols.Rtl433(), APP_DIR / 'temp.json')
]
