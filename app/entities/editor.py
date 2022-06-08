from pydantic import BaseModel


class CreateArtistRequest(BaseModel):
    name: str
