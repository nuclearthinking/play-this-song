from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import declarative_base, registry, sessionmaker

from app.config import DATABASE_URL

mapper_registry = registry()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
scoped_async_session = async_scoped_session(async_session_factory, scopefunc=current_task)

Base = declarative_base()
