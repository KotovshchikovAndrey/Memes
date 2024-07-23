from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from config.settings import settings
from database.models.base import Base


class DatabaseConnection:
    _engine: AsyncEngine
    _session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, url: str, echo: bool = False) -> None:
        self._engine = create_async_engine(url=url)

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self):
        session = self._get_scoped_session()
        yield session
        await session.remove()

    async def close(self) -> None:
        await self._engine.dispose()

    async def create_tables(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    def _get_scoped_session(self) -> async_scoped_session[AsyncSession]:
        scoped_session = async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=current_task,
        )

        return scoped_session


database = DatabaseConnection(
    url=f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}",
    echo=settings.is_debug,
)
