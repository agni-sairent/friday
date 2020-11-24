from peewee import *
from models.BaseModel import BaseModel


class Work(BaseModel):
    topic = CharField()
    workday = DateField()
    since = TimeField()
    until = TimeField()
    user_reference = CharField(max_length=36)

