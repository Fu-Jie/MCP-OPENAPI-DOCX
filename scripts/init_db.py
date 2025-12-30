#!/usr/bin/env python3
"""Database initialization script.

This script initializes the database with the initial schema
and optionally seeds initial data.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import get_settings
from src.database.base import Base
from src.models.database import (
    User,
    Document,
    DocumentVersion,
    Comment,
    Revision,
    Template,
    AuditLog,
)


async def init_database(create_tables: bool = True, seed_data: bool = False) -> None:
    """Initialize the database.

    Args:
        create_tables: Whether to create tables.
        seed_data: Whether to seed initial data.
    """
    settings = get_settings()
    print(f"Initializing database: {settings.database_url}")

    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
    )

    if create_tables:
        print("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")

    if seed_data:
        print("Seeding initial data...")
        await seed_initial_data(engine)
        print("Data seeded successfully!")

    await engine.dispose()
    print("Database initialization complete!")


async def seed_initial_data(engine) -> None:
    """Seed the database with initial data.

    Args:
        engine: Database engine.
    """
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime
    import uuid

    from src.utils.security_utils import SecurityUtils

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Create admin user
        admin_user = User(
            id=str(uuid.uuid4()),
            email="admin@example.com",
            username="admin",
            hashed_password=SecurityUtils.hash_password("admin123"),
            full_name="System Administrator",
            is_active=True,
            is_superuser=True,
            created_at=datetime.utcnow(),
        )
        session.add(admin_user)

        # Create sample templates
        templates = [
            Template(
                id=str(uuid.uuid4()),
                name="Blank Document",
                file_path="templates/blank.docx",
                description="A blank document template",
                category="General",
                tags=["blank", "default"],
                created_at=datetime.utcnow(),
            ),
            Template(
                id=str(uuid.uuid4()),
                name="Business Report",
                file_path="templates/business_report.docx",
                description="Professional business report template",
                category="Business",
                tags=["report", "business", "professional"],
                created_at=datetime.utcnow(),
            ),
            Template(
                id=str(uuid.uuid4()),
                name="Meeting Notes",
                file_path="templates/meeting_notes.docx",
                description="Template for meeting notes and minutes",
                category="Business",
                tags=["meeting", "notes", "minutes"],
                created_at=datetime.utcnow(),
            ),
        ]

        for template in templates:
            session.add(template)

        await session.commit()
        print(f"Created admin user: admin@example.com")
        print(f"Created {len(templates)} templates")


async def drop_tables() -> None:
    """Drop all database tables."""
    settings = get_settings()
    print(f"Dropping all tables from: {settings.database_url}")

    engine = create_async_engine(settings.database_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
    print("All tables dropped!")


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Database initialization script")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables before creating",
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed initial data",
    )
    parser.add_argument(
        "--drop-only",
        action="store_true",
        help="Only drop tables, don't recreate",
    )

    args = parser.parse_args()

    if args.drop_only:
        asyncio.run(drop_tables())
    else:
        if args.drop:
            asyncio.run(drop_tables())
        asyncio.run(init_database(create_tables=True, seed_data=args.seed))


if __name__ == "__main__":
    main()
