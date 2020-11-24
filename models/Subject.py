from enum import Enum
from peewee import *

from models.BaseModel import BaseModel
from models.enum_field import EnumField


class Subject(BaseModel):
    class RepeatInterval(Enum):
        NORMAL = 'NL'
        ONLY_ODD = 'ODD'
        ONLY_EVEN = 'EVN'

    class SubjectType(Enum):
        LECTURE = 'LR'
        EXERCISE = 'EX'

    short = CharField()
    name = CharField()
    room = CharField()
    weekday = IntegerField()
    repeat_interval = EnumField(null=False, choices=RepeatInterval)
    time_start = TimeField()
    time_end = TimeField()
    type = EnumField(null=False, choices=SubjectType)
    user_reference = CharField(max_length=36)

