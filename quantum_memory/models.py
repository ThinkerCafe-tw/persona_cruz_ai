"""
量子記憶系統的資料庫模型
"""

from sqlalchemy import Column, String, Float, DateTime, JSON, Integer, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from typing import List, Optional
import uuid

Base = declarative_base()

class Agent(Base):
    """代理人（AI 人格）模型"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    emoji = Column(String, nullable=False)
    element = Column(String)  # 五行元素：wood, fire, earth, metal, water, wuji
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True))
    
    # 關聯
    memories = relationship("Memory", back_populates="agent", cascade="all, delete-orphan")
    quantum_states = relationship("QuantumState", back_populates="agent", cascade="all, delete-orphan")
    
    @classmethod
    async def get_all(cls, db: AsyncSession) -> List["Agent"]:
        """取得所有代理人"""
        result = await db.execute(select(cls))
        return result.scalars().all()
    
    @classmethod
    async def get_by_id(cls, db: AsyncSession, agent_id: str) -> Optional["Agent"]:
        """根據 ID 取得代理人"""
        result = await db.execute(select(cls).where(cls.id == agent_id))
        return result.scalar_one_or_none()
    
    @classmethod
    async def get_by_name(cls, db: AsyncSession, name: str) -> Optional["Agent"]:
        """根據名稱取得代理人"""
        result = await db.execute(select(cls).where(cls.name == name))
        return result.scalar_one_or_none()
    
    @classmethod
    async def count_total(cls, db: AsyncSession) -> int:
        """計算總代理人數"""
        result = await db.execute(select(func.count(cls.id)))
        return result.scalar()

class Memory(Base):
    """記憶模型"""
    __tablename__ = "memories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(JSON)  # 向量嵌入
    emotion = Column(String)
    context = Column(JSON)
    importance = Column(Float, default=0.5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    accessed_at = Column(DateTime(timezone=True))
    access_count = Column(Integer, default=0)
    
    # 關聯
    agent = relationship("Agent", back_populates="memories")
    
    # 用於搜尋結果的臨時屬性
    similarity_score: float = 0.0
    
    @classmethod
    async def count_by_agent(cls, db: AsyncSession, agent_id: str) -> int:
        """計算特定代理人的記憶數量"""
        result = await db.execute(
            select(func.count(cls.id)).where(cls.agent_id == agent_id)
        )
        return result.scalar()
    
    @classmethod
    async def count_total(cls, db: AsyncSession) -> int:
        """計算總記憶數量"""
        result = await db.execute(select(func.count(cls.id)))
        return result.scalar()
    
    @classmethod
    async def get_recent(cls, db: AsyncSession, agent_id: str, limit: int = 10) -> List["Memory"]:
        """取得最近的記憶"""
        result = await db.execute(
            select(cls)
            .where(cls.agent_id == agent_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

class QuantumState(Base):
    """量子態記錄"""
    __tablename__ = "quantum_states"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    phase = Column(Float, default=0.0)
    frequency = Column(Float, default=1.0)
    amplitude = Column(Float, default=1.0)
    coherence = Column(Float, default=1.0)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 關聯
    agent = relationship("Agent", back_populates="quantum_states")
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            "phase": self.phase,
            "frequency": self.frequency,
            "amplitude": self.amplitude,
            "coherence": self.coherence,
            "metadata": self.metadata or {},
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Interaction(Base):
    """代理人之間的互動記錄"""
    __tablename__ = "interactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    from_agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    to_agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    interaction_type = Column(String)  # 互動類型：support, challenge, collaborate, etc.
    content = Column(Text)
    energy_exchange = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 關聯
    from_agent = relationship("Agent", foreign_keys=[from_agent_id])
    to_agent = relationship("Agent", foreign_keys=[to_agent_id])