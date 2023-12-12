import peewee
from database.common.models import *


def database_initialize():
    try:
        db.connect()
        db.create_tables([History])
    except peewee.InternalError as px:
        print(px.__repr__())
