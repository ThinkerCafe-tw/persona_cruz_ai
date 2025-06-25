"""
量子記憶系統 FastAPI 服務
提供 RESTful API 給 LibreChat 整合使用
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import os
import json
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from .quantum_state_manager import QuantumStateManager
from .quantum_memory_persistence import QuantumMemoryPersistence
from .database import get_db, init_db
from .models import Memory, Agent

app = FastAPI(
    title="Persona CRUZ Quantum Memory API",
    description="量子記憶系統 API，支援 CRUZ 人格系統的記憶管理",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應該限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化量子狀態管理器
quantum_manager = QuantumStateManager()
memory_persistence = None

# API 模型定義
class MemoryCreateRequest(BaseModel):
    """建立記憶請求"""
    agent_id: str = Field(..., description="代理人 ID")
    content: str = Field(..., description="記憶內容")
    emotion: Optional[str] = Field(None, description="情緒狀態")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="上下文資訊")
    importance: float = Field(0.5, ge=0, le=1, description="重要性分數")

class MemorySearchRequest(BaseModel):
    """搜尋記憶請求"""
    agent_id: str = Field(..., description="代理人 ID")
    query: str = Field(..., description="搜尋查詢")
    limit: int = Field(10, ge=1, le=100, description="返回結果數量")
    similarity_threshold: float = Field(0.7, ge=0, le=1, description="相似度閾值")

class AgentStateResponse(BaseModel):
    """代理人狀態回應"""
    agent_id: str
    name: str
    emoji: str
    quantum_state: Dict[str, Any]
    memory_count: int
    last_active: Optional[datetime]

class QuantumEvolutionRequest(BaseModel):
    """量子演化請求"""
    agent_id: str
    interaction_type: str = Field(..., description="互動類型：創造、實踐、穩定、精煉、流動")
    energy_level: float = Field(0.5, ge=0, le=1, description="能量等級")

# 啟動事件
@app.on_event("startup")
async def startup_event():
    """啟動時初始化資料庫和量子系統"""
    global memory_persistence
    
    # 初始化資料庫
    await init_db()
    
    # 初始化記憶持久化
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/persona_cruz")
    memory_persistence = QuantumMemoryPersistence(database_url)
    
    # 載入現有的量子態
    await quantum_manager.load_states_from_db(memory_persistence)
    
    print("🌌 量子記憶系統 API 啟動完成")

# 健康檢查
@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "service": "Quantum Memory API",
        "version": "1.0.0",
        "quantum_state": "coherent"
    }

# 代理人管理
@app.get("/agents", response_model=List[AgentStateResponse])
async def list_agents(db: AsyncSession = Depends(get_db)):
    """列出所有代理人及其狀態"""
    agents = await Agent.get_all(db)
    
    responses = []
    for agent in agents:
        quantum_state = quantum_manager.get_agent_state(agent.id)
        memory_count = await Memory.count_by_agent(db, agent.id)
        
        responses.append(AgentStateResponse(
            agent_id=agent.id,
            name=agent.name,
            emoji=agent.emoji,
            quantum_state=quantum_state.to_dict() if quantum_state else {},
            memory_count=memory_count,
            last_active=agent.last_active
        ))
    
    return responses

@app.get("/agents/{agent_id}", response_model=AgentStateResponse)
async def get_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    """取得特定代理人狀態"""
    agent = await Agent.get_by_id(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    quantum_state = quantum_manager.get_agent_state(agent_id)
    memory_count = await Memory.count_by_agent(db, agent_id)
    
    return AgentStateResponse(
        agent_id=agent.id,
        name=agent.name,
        emoji=agent.emoji,
        quantum_state=quantum_state.to_dict() if quantum_state else {},
        memory_count=memory_count,
        last_active=agent.last_active
    )

# 記憶管理
@app.post("/memories")
async def create_memory(
    request: MemoryCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """建立新記憶"""
    # 確保代理人存在
    agent = await Agent.get_by_id(db, request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {request.agent_id} not found")
    
    # 建立記憶
    memory = await memory_persistence.store_memory(
        agent_id=request.agent_id,
        content=request.content,
        emotion=request.emotion,
        context=request.context,
        importance=request.importance
    )
    
    # 更新量子態
    quantum_manager.update_agent_state(request.agent_id, {
        "last_memory": request.content,
        "emotion": request.emotion,
        "timestamp": datetime.now()
    })
    
    # 更新代理人最後活動時間
    agent.last_active = datetime.now()
    await db.commit()
    
    return {
        "success": True,
        "memory_id": memory.id,
        "message": f"記憶已儲存到 {agent.emoji} {agent.name} 的量子記憶庫"
    }

@app.post("/memories/search")
async def search_memories(
    request: MemorySearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """搜尋記憶"""
    # 確保代理人存在
    agent = await Agent.get_by_id(db, request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {request.agent_id} not found")
    
    # 搜尋記憶
    memories = await memory_persistence.search_memories(
        agent_id=request.agent_id,
        query=request.query,
        limit=request.limit,
        similarity_threshold=request.similarity_threshold
    )
    
    return {
        "agent": f"{agent.emoji} {agent.name}",
        "query": request.query,
        "results": [
            {
                "id": str(mem.id),
                "content": mem.content,
                "emotion": mem.emotion,
                "similarity": mem.similarity_score,
                "created_at": mem.created_at.isoformat(),
                "context": mem.context
            }
            for mem in memories
        ],
        "count": len(memories)
    }

# 量子態管理
@app.post("/quantum/evolve")
async def evolve_quantum_state(
    request: QuantumEvolutionRequest,
    db: AsyncSession = Depends(get_db)
):
    """演化代理人的量子態"""
    agent = await Agent.get_by_id(db, request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {request.agent_id} not found")
    
    # 執行量子演化
    old_state = quantum_manager.get_agent_state(request.agent_id)
    
    quantum_manager.evolve_state(
        agent_id=request.agent_id,
        interaction_type=request.interaction_type,
        energy_level=request.energy_level
    )
    
    new_state = quantum_manager.get_agent_state(request.agent_id)
    
    # 儲存演化記錄
    evolution_memory = await memory_persistence.store_memory(
        agent_id=request.agent_id,
        content=f"量子態演化：{request.interaction_type}",
        emotion="focused",
        context={
            "evolution_type": request.interaction_type,
            "energy_level": request.energy_level,
            "old_coherence": old_state.coherence if old_state else 0,
            "new_coherence": new_state.coherence if new_state else 0
        },
        importance=0.8
    )
    
    return {
        "success": True,
        "agent": f"{agent.emoji} {agent.name}",
        "evolution_type": request.interaction_type,
        "new_state": new_state.to_dict() if new_state else {},
        "evolution_id": str(evolution_memory.id)
    }

@app.get("/quantum/coherence/{agent_id}")
async def get_quantum_coherence(agent_id: str, db: AsyncSession = Depends(get_db)):
    """取得代理人的量子相干性"""
    agent = await Agent.get_by_id(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    state = quantum_manager.get_agent_state(agent_id)
    if not state:
        return {
            "agent": f"{agent.emoji} {agent.name}",
            "coherence": 0,
            "status": "uninitialized"
        }
    
    return {
        "agent": f"{agent.emoji} {agent.name}",
        "coherence": state.coherence,
        "phase": state.phase,
        "frequency": state.frequency,
        "amplitude": state.amplitude,
        "status": "active" if state.coherence > 0.7 else "degraded"
    }

# 系統狀態
@app.get("/system/stats")
async def get_system_stats(db: AsyncSession = Depends(get_db)):
    """取得系統統計資訊"""
    total_memories = await Memory.count_total(db)
    total_agents = await Agent.count_total(db)
    
    active_states = quantum_manager.get_all_states()
    avg_coherence = np.mean([s.coherence for s in active_states.values()]) if active_states else 0
    
    return {
        "total_memories": total_memories,
        "total_agents": total_agents,
        "active_quantum_states": len(active_states),
        "average_coherence": float(avg_coherence),
        "system_status": "optimal" if avg_coherence > 0.8 else "normal"
    }

@app.post("/system/sync")
async def sync_quantum_states():
    """同步所有量子態到資料庫"""
    await quantum_manager.sync_to_db(memory_persistence)
    return {
        "success": True,
        "message": "量子態已同步到資料庫"
    }

# WebSocket 端點（用於實時更新）
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket 連接用於實時量子態更新"""
    await websocket.accept()
    
    try:
        while True:
            # 發送當前量子態
            state = quantum_manager.get_agent_state(agent_id)
            if state:
                await websocket.send_json({
                    "type": "quantum_state",
                    "agent_id": agent_id,
                    "state": state.to_dict(),
                    "timestamp": datetime.now().isoformat()
                })
            
            # 等待下次更新
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for agent {agent_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)