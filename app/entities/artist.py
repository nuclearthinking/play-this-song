from pydantic import BaseModel


class ArtistScheme(BaseModel):
    id: int | None = None
    name: str

    class Config:
        orm_mode = True
