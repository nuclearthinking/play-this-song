from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:

    from app.entities.artist import Artist


class Song(BaseModel):
    id: int
    text: str
    artist: "Artist"

    class Config:
        orm_mode = True
