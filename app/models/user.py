from pydantic import BaseModel

from app.database import Base
import sqlalchemy as sa


class UserOrm(Base):
    __tablename__ = "users"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    twitch_id: int = sa.Column(sa.Integer, unique=True, nullable=False)
    login: str = sa.Column(sa.String(255), unique=True, nullable=False)
    email: str = sa.Column(sa.String(255), unique=True, nullable=False)


class User(BaseModel):
    id: int
    twitch_id: int
    login: str
    email: str

    class Config:
        orm_mode = True
