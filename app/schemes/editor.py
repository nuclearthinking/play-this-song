from pydantic import BaseModel


class AddSongRequest(BaseModel):
    artist_name: str
    song_title: str
    song_text: str
