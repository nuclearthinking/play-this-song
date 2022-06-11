import sqlalchemy as sa

from app.database import db_session
from app.models.db_models import Artist, Song


def create_song(song: Song, artist: Artist) -> Song:
    song.artist = artist
    db_session.add(song)
    db_session.commit()
    db_session.refresh(song)
    db_session.refresh(artist)
    return song


def create_artist(artist_name: str) -> Artist:
    artist = Artist(
        name=artist_name,
    )
    db_session.add(artist)
    db_session.commit()
    db_session.refresh(artist)
    return artist


def get_all_artist() -> list[Artist]:
    query = sa.select(Artist)
    return db_session.execute(query).scalars().all()


def get_artist(artist_name: str) -> Artist | None:
    query = sa.select(Artist).where(Artist.name == artist_name)
    result = db_session.execute(query).scalar_one_or_none()
    if not result:
        return None
    return result
