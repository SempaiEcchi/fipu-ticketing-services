from pony.orm import *
from datetime import datetime
import env
import os

DB = Database()


class CloseEvent(DB.Entity):
    _table_ = "close_event"
    instance_id = PrimaryKey(str)
    close_timestamp = Required(datetime, precision=6)


def setup_db():
    if not os.path.isdir("database"):
        os.mkdir("database")
    if env.DB["provider"] == "postgres":
        DB.bind(**env.DB)
    else:
        DB.bind(provider="sqlite", filename="database/database.sqlite", create_db=True)
    DB.generate_mapping(create_tables=True)


@db_session
def add_event(
        instance_id, close_timestamp
):
    CloseEvent(
        instance_id=instance_id,
        close_timestamp=close_timestamp,
    )
