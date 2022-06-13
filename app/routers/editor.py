from fastapi import APIRouter, Depends

from app.dependencies import auth_as_admin
from app.models.db_models import Artist, Song
from app.repository.database.song_repository import create_artist, create_song, get_artist
from app.schemes.editor import AddSongRequest
from app.schemes.song import SongScheme

router = APIRouter(prefix="/edit", dependencies=[Depends(auth_as_admin)])


@router.post(path="/song", response_model=SongScheme)
async def add_song(request: AddSongRequest):
    artist: Artist = await get_artist(request.artist_name)
    if not artist:
        artist = await create_artist(request.artist_name)
    song = await create_song(
        song=Song(
            title=request.song_title,
            text=request.song_text,
        ),
        artist=artist,
    )
    return song
