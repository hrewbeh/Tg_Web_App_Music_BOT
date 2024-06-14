from pydantic import BaseModel


class UserCreate(BaseModel):
    tg_id: int
    username: str
    password: str
    email: str
