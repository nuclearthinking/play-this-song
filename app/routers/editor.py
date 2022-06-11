from fastapi import APIRouter, Depends

from app.dependencies import auth_as_admin
from app.models.db_models import Song, Artist
from app.schemes.editor import AddSongRequest
from app.repository.database.song_repository import create_artist, create_song, get_artist
from app.schemes.song import SongScheme

router = APIRouter(prefix="/edit", dependencies=[Depends(auth_as_admin)])


@router.post(path="/song", response_model=SongScheme)
async def add_song(request: AddSongRequest):
    artist: Artist = get_artist(request.artist_name)
    if not artist:
        artist = create_artist(request.artist_name)
    song = create_song(
        song=Song(
            title=request.song_title,
            text=request.song_text,
        ),
        artist=artist,
    )
    return song
