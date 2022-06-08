from app.database import db_session
from app.entities.artist import Artist
from app.entities.song import Song
from app.models.artist import ArtistOrm
from app.models.song import SongOrm


def create_song(song: Song, artist: Artist) -> Song:
    song_orm = SongOrm(**song.dict(), artist_id=artist.id)
    db_session.add(song_orm)
    db_session.commit()
    db_session.refresh(song_orm)
    return Song.from_orm(song_orm)


def create_artist(artist_name: str) -> Artist:
    artist_orm = ArtistOrm(
        name=artist_name,
    )
    db_session.add(artist_orm)
    db_session.commit()
    db_session.refresh(artist_orm)
    return Artist.from_orm(artist_orm)


async def get_all_artist() -> list[Artist]:
    ...
