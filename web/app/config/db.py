"""
Database Infrastructure Configuration.

Initializes the SQLAlchemy AsyncEngine and provides tools for 
schema integrity verification and dependency-injected sessions.
"""
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext

from app.models.base import Base
from app.config.settings import settings

# Global Database Connection Pool
# 
# Uses 'async_sessionmaker' with 'expire_on_commit=False' to allow 
# access to model attributes after a transaction commit.
engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def verify_schema():
    """
    Validates that the physical database schema matches the SQLAlchemy models.

    This function uses Alembic's 'MigrationContext' to perform a 
    live comparison (diff) between the 'Base.metadata' and the 
    actual DB tables on startup.

    Raises:
        RuntimeError: If there is any discrepancy (missing tables, 
                      mismatched columns) between code and database.
    
    Note: 
        This is a safety guard to prevent the app from running 
        with an outdated or unmigrated schema.
    """
    async with engine.begin() as conn:
        def _sync_verify(sync_conn):
            ctx = MigrationContext.configure(sync_conn)
            diff = compare_metadata(ctx, Base.metadata)
            if diff:
                for d in diff:
                    print(d)
                raise RuntimeError("DB schema verification failed")
        
        await conn.run_sync(_sync_verify)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency for providing a scoped database session.

    Yields a session from the global maker and automatically 
    closes it after the request lifecycle is complete.

    Yields:
        AsyncSession: An active, non-expired SQLAlchemy session.
    """
    async with async_session_maker() as session:
        yield session
