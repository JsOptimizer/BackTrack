import sqlite3

from datetime import datetime

import click
from flask import current_app ,g

def get_db():
    if "db" not in g:
       g.db=sqlite3.connect(
        current_app.config["DATABASE"],
        detect_type=sqlite3.PARSE_DECLTYPES
       )
       g.db.row_factory=sqlite3.Row
       pass
    return g.db
def close_db(e:None):
    db=g.pop("db",None)
    if db is not None:
        db.close()