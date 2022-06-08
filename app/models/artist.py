from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.song import SongOrm


class ArtistOrm(Base):
    __tablename__ = "artists"

    id: int = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name: str = sa.Column(sa.String(255), nullable=False, unique=True)
    repertoire: list["SongOrm"] = relationship("SongOrm", backref="songs")
