import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
)

engine = create_async_engine(DATABASE_URL, echo=False)

# Async session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def init_db() -> None:
    """Create database tables (if they don't exist)."""
    async with engine.begin() as conn:
        # Use SQLAlchemy's run_sync to call the synchronous create_all
        await conn.run_sync(Base.metadata.create_all)
