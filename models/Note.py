from enum import Enum

from peewee import *
from models.BaseModel import BaseModel
from models.enum_field import EnumField


class Note(BaseModel):
    class NotePriority(Enum):
        NONE = '0'
        LOW = '1'
        MEDIUM = '2'
        HIGH = '3'
        EXTREME = '4'

    name = CharField(max_length=64)
    content = TextField()
    created = DateTimeField()
    priority = EnumField(choices=NotePriority)
    notify = DateTimeField(null=True)
    user_reference = CharField(max_length=36)

