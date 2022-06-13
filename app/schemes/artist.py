from pydantic import BaseModel


class ArtistBase(BaseModel):
    name: str


class ArtistCreate(ArtistBase):
    pass


class ArtistScheme(ArtistBase):
    id: int

    class Config:
        orm_mode = True
