from pydantic import BaseModel

from app.database import Base

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.artist import Artist, ArtistOrm


class SongOrm(Base):
    __tablename__ = "songs"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text: str = sa.Column(sa.Text, nullable=False)
    artist_id: int = sa.Column(sa.Integer, sa.ForeignKey("artists.id"), nullable=False)
    artist: "ArtistOrm" = relationship("ArtistOrm", back_populates="artists")


class Song(BaseModel):
    id: int
    text: str
    artist: "Artist"

    class Config:
        orm_mode = True
