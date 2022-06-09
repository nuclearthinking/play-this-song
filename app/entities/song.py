from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.entities.artist import ArtistScheme


class SongScheme(BaseModel):
    id: int | None = None
    title: str
    text: str
    artist: Optional["ArtistScheme"] = None

    class Config:
        orm_mode = True
