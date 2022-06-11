from pydantic import BaseModel

from app.schemes.artist import ArtistScheme


class SongBase(BaseModel):
    title: str
    text: str


class SongCreate(SongBase):
    pass


class SongScheme(SongBase):
    id: int
    artist_id: int
    artist: ArtistScheme

    class Config:
        orm_mode = True
