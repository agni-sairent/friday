from pydantic import BaseModel
from datetime import time
from enum import Enum


class TokenAuthorizedSubjectCreateRequest(BaseModel):
    class RepeatInterval(Enum):
        NORMAL = 'NL'
        ONLY_ODD = 'ODD'
        ONLY_EVEN = 'EVN'

    class SubjectType(Enum):
        LECTURE = 'LR'
        EXERCISE = 'EX'

    token: str
    short: str
    name: str
    room: str
    weekday: int
    repeat_interval: RepeatInterval
    time_start: time = None
    time_end: time = None
    type: SubjectType
