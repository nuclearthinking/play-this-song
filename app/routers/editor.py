from fastapi import APIRouter, Depends, Request

from app.dependencies import auth_as_admin
from app.entities.artist import Artist
from app.entities.editor import CreateArtistRequest
from app.repository.database.song_repository import create_artist

router = APIRouter(prefix="/edit", dependencies=[Depends(auth_as_admin)])


@router.get(path="/artist")
async def get_all_artists() -> Request:
    ...


@router.post(path="/artist")
async def add_artist(request: CreateArtistRequest) -> Request:
    create_artist(artist_name=request.name)
