"""Database session management.

This module provides async session factories and dependency injection
functions for database access in the application.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database.base import get_engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Create an async session factory.

    Returns:
        Async session factory configured with the database engine.
    """
    return async_sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


AsyncSessionLocal = get_session_factory()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session for dependency injection.

    Yields:
        AsyncSession instance for database operations.

    Note:
        The session is automatically closed when the context exits.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
