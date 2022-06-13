import sqlalchemy as sa

from app.database import scoped_async_session as async_db_session
from app.models.db_models import Artist, Song


async def create_song(song: Song, artist: Artist) -> Song:
    async with async_db_session() as session:
        song.artist = artist
        session.add(song)
        await session.commit()
        await session.refresh(song)
        await session.refresh(artist)
        return song


async def create_artist(artist_name: str) -> Artist:
    artist = Artist(
        name=artist_name,
    )
    async_db_session.add(artist)
    await async_db_session.commit()
    await async_db_session.refresh(artist)
    return artist


async def get_all_artist() -> list[Artist]:
    query = sa.select(Artist)
    result = await async_db_session.execute(query)
    return result.scalars().all()


async def get_artist(artist_name: str) -> Artist | None:
    query = sa.select(Artist).where(Artist.name == artist_name)
    result = await async_db_session.execute(query)
    artists = result.scalar_one_or_none()
    if not artists:
        return None
    return artists
