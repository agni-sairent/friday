from peewee import *
from models.BaseModel import BaseModel


class Homework(BaseModel):
    header = CharField()
    description = CharField()
    deadline = DateTimeField()
    user_reference = CharField(max_length=36)
