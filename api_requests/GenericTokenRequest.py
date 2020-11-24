from pydantic import BaseModel


class GenericTokenRequest(BaseModel):
    token: str
