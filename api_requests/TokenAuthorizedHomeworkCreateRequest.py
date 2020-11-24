from datetime import datetime
from pydantic import BaseModel


class TokenAuthorizedHomeworkCreateRequest(BaseModel):
    token: str
    header: str
    description: str
    deadline: datetime
