from pydantic import BaseModel


class UserValidator(BaseModel):
    username: str
    password: str
