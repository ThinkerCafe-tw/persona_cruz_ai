"""
Persona CRUZ Memory API - Day 1 MVP
極簡實現，專注核心功能
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

app = FastAPI(
    title="Persona CRUZ Memory API",
    description="極簡記憶系統 - 14天交付計劃 Day 1",
    version="0.1.0-alpha"
)

# 臨時記憶存儲（Day 1 先用內存，Day 2 接入PostgreSQL）
memory_store = {}

class MemoryInput(BaseModel):
    user_id: str
    content: str
    context: Optional[Dict] = {}

class MemoryOutput(BaseModel):
    memory_id: str
    user_id: str
    content: str
    context: Dict
    created_at: datetime

@app.get("/")
async def root():
    return {
        "status": "alive",
        "message": "Memory API is running",
        "timestamp": datetime.now(),
        "day": 1,
        "countdown": "13 days to MVP"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "memory-api", 
        "version": "0.1.0-alpha",
        "uptime": "just started",
        "musk_says": "Stop talking, start shipping"
    }

@app.post("/memory/store", response_model=MemoryOutput)
async def store_memory(memory: MemoryInput):
    """存儲記憶 - Day 1 極簡版本"""
    # 生成簡單的記憶ID
    memory_id = f"{memory.user_id}_{datetime.now().timestamp()}"
    
    # 存儲到內存（明天換PostgreSQL）
    memory_data = {
        "memory_id": memory_id,
        "user_id": memory.user_id,
        "content": memory.content,
        "context": memory.context,
        "created_at": datetime.now()
    }
    
    if memory.user_id not in memory_store:
        memory_store[memory.user_id] = []
    
    memory_store[memory.user_id].append(memory_data)
    
    return memory_data

@app.get("/memory/search")
async def search_memory(user_id: str, query: str, limit: int = 10):
    """搜索記憶 - Day 1 簡單關鍵詞匹配"""
    if user_id not in memory_store:
        return {"results": [], "count": 0}
    
    # 極簡搜索：關鍵詞匹配
    results = []
    for memory in memory_store[user_id]:
        if query.lower() in memory["content"].lower():
            results.append(memory)
    
    # 限制返回數量
    results = results[:limit]
    
    return {
        "user_id": user_id,
        "query": query,
        "results": results,
        "count": len(results),
        "total": len(memory_store.get(user_id, []))
    }

@app.get("/stats")
async def get_stats():
    """系統統計 - 馬斯克喜歡看數據"""
    total_users = len(memory_store)
    total_memories = sum(len(memories) for memories in memory_store.values())
    
    return {
        "total_users": total_users,
        "total_memories": total_memories,
        "status": "Day 1 - On track",
        "next_milestone": "Day 3 - Production ready"
    }

# 啟動提示
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Memory API - Day 1/14")
    print("⚡ First endpoint in 10 minutes - DONE!")
    print("🎯 Goal: Basic memory store/search by end of day")
    uvicorn.run(app, host="0.0.0.0", port=8000)