"""
PostgreSQL + pgvector 資料庫層
Day 2 - 真正的持久化存儲
"""
from sqlalchemy import create_engine, Column, String, DateTime, JSON, Text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    # Railway 可能需要時間安裝 pgvector
    from sqlalchemy import Column as Vector
import os
from datetime import datetime

# 資料庫連接
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/memory_db"
)

# 異步引擎
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 基礎模型
Base = declarative_base()

class Memory(Base):
    """記憶模型 - 極簡但完整"""
    __tablename__ = "memories"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))  # OpenAI embeddings dimension
    context = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "memory_id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "context": self.context,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

async def init_db():
    """初始化資料庫"""
    async with engine.begin() as conn:
        # 創建 pgvector 擴展
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        # 創建表格
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    """獲取資料庫會話"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()