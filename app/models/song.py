from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.artist import Artist


class Song(Base):
    __tablename__ = "songs"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text: str = sa.Column(sa.Text, nullable=False)
    title: str = sa.Column(sa.String(255), nullable=False)
    artist_id: int = sa.Column(sa.Integer, sa.ForeignKey("artist.id"), nullable=False)
    artist: "Artist" = relationship("Artist", uselist=False, backref="artist")
