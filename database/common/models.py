from datetime import datetime
from peewee import *

db = SqliteDatabase('logs.db')


class BaseModel(Model):
    class Meta:
        database = db


# class User(BaseModel):
#     id = IntegerField(unique=True)


class History(BaseModel):
    # user = ForeignKeyField(User, backref='requests_history')
    user_id = IntegerField()
    request = TextField(null=False)
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        order_by = "created_at"
