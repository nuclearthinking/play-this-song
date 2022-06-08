from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, registry, scoped_session, sessionmaker

from app.config import DATABASE_URL

mapper_registry = registry()

engine = create_engine(DATABASE_URL, echo=True)

db_session = scoped_session(sessionmaker(autoflush=False, autocommit=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
