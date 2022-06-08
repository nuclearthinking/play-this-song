from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.artist import ArtistOrm


class SongOrm(Base):
    __tablename__ = "songs"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text: str = sa.Column(sa.Text, nullable=False)
    artist_id: int = sa.Column(sa.Integer, sa.ForeignKey("artists.id"), nullable=False)
    artist: "ArtistOrm" = relationship("ArtistOrm", backref="artists")
