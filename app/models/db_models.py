import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base


class Artist(Base):
    __tablename__ = "artist"

    id: int = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name: str = sa.Column(sa.String(255), nullable=False, unique=True)
    songs = relationship("Song", back_populates="artist")


class Song(Base):
    __tablename__ = "songs"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text: str = sa.Column(sa.Text, nullable=False)
    title: str = sa.Column(sa.String(255), nullable=False)
    artist_id: int = sa.Column(sa.Integer, sa.ForeignKey("artist.id"), nullable=False)
    artist = relationship("Artist", back_populates="songs")
