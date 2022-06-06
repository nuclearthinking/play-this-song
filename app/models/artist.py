from typing import TYPE_CHECKING

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.orm import relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.song import Song, SongOrm


class ArtistOrm(Base):
    __tablename__ = "artists"

    id: int = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name: str = sa.Column(sa.String(255), nullable=False)
    songs: list["SongOrm"] = relationship("SongOrm", back_populates="songs")


class Artist(BaseModel):
    id: int
    name: str
    songs: list["Song"]

    class Config:
        orm_mode = True
