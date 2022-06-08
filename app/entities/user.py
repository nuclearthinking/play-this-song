from pydantic import BaseModel


class User(BaseModel):
    id: int
    twitch_id: int
    login: str
    email: str

    class Config:
        orm_mode = True
