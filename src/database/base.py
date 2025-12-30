"""Database base configuration and engine setup.

This module provides the SQLAlchemy declarative base and engine configuration
for the application's database connections.
"""

from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import get_settings
from src.core.constants import DB_NAMING_CONVENTION


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class.

    All ORM models should inherit from this base class.
    Includes metadata with naming conventions for constraints.
    """

    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary.

        Returns:
            Dictionary representation of the model.
        """
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """Get or create the async database engine.

    Returns:
        AsyncEngine instance for database operations.
    """
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            pool_pre_ping=True,
        )
    return _engine


async def dispose_engine() -> None:
    """Dispose the database engine and close all connections."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
