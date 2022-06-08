from pydantic import BaseModel

from app.entities.song import Song


class Artist(BaseModel):
    id: int | None = None
    name: str
    songs: list[Song] = []

    class Config:
        orm_mode = True
