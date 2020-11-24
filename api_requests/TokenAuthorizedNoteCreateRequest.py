from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class TokenAuthorizedNoteCreateRequest(BaseModel):
    class NotePriority(Enum):
        NONE = '0'
        LOW = '1'
        MEDIUM = '2'
        HIGH = '3'
        EXTREME = '4'

    token: str
    name: str
    content: str
    created: datetime
    priority: NotePriority
    notify: datetime
