import sqlalchemy as sa

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    twitch_id: int = sa.Column(sa.Integer, unique=True, nullable=False)
    login: str = sa.Column(sa.String(255), unique=True, nullable=False)
    email: str = sa.Column(sa.String(255), unique=True, nullable=False)
