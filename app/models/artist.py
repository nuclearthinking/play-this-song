import sqlalchemy as sa

from app.database import Base


class Artist(Base):
    __tablename__ = "artist"
    id: int = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name: str = sa.Column(sa.String(255), nullable=False, unique=True)
