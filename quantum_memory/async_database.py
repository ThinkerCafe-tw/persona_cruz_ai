"""
異步資料庫連接和會話管理（用於 FastAPI）
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from .models import Base

# 從環境變數取得資料庫 URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:password@localhost:5432/persona_cruz"
)

# 建立異步引擎
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # 避免連接池問題
    echo=False  # 生產環境設為 False
)

# 建立異步會話工廠
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """初始化資料庫表格"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """取得資料庫會話"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()