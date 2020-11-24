from pydantic import BaseModel
from datetime import time, date


class TokenAuthorizedWorkCreateRequest(BaseModel):
    token: str
    topic: str
    workday: date
    since: time
    until: time
