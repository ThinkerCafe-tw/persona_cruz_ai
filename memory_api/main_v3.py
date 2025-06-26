"""
Persona CRUZ Memory API - Day 3 生產版
完整的認證、分類和標籤系統
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from database import get_session, init_db, Memory
from embeddings import embedding_service
from auth import (
    authenticate_user, create_access_token, get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(
    title="Persona CRUZ Memory API",
    description="Day 3 - Production Ready with Auth",
    version="0.3.0-beta"
)

# 請求/響應模型
class MemoryInput(BaseModel):
    content: str
    context: Optional[Dict] = {}
    category: Optional[str] = "general"
    tags: Optional[List[str]] = []

class MemoryOutput(BaseModel):
    memory_id: str
    user_id: str
    content: str
    context: Dict
    category: str
    tags: List[str]
    created_at: datetime
    similarity: Optional[float] = None

class Token(BaseModel):
    access_token: str
    token_type: str

@app.on_event("startup")
async def startup_event():
    """啟動時初始化資料庫"""
    await init_db()
    print("🚀 Day 3: Production Ready Memory API!")

@app.get("/")
async def root():
    return {
        "status": "alive",
        "message": "Memory API v3 - Production Ready",
        "timestamp": datetime.now(),
        "day": 3,
        "countdown": "11 days to MVP",
        "features": ["Authentication", "Categories", "Tags", "Production Deploy"]
    }

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """登入獲取 token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["user_id"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """獲取當前用戶資訊"""
    return current_user

@app.post("/memory/store", response_model=MemoryOutput)
async def store_memory(
    memory: MemoryInput,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """存儲記憶 - 需要認證"""
    user_id = current_user["user_id"]
    memory_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
    
    # 創建嵌入向量
    embedding = await embedding_service.create_embedding(memory.content)
    
    # 擴展資料庫模型以支援分類和標籤
    memory_data = {
        "id": memory_id,
        "user_id": user_id,
        "content": memory.content,
        "embedding": embedding,
        "context": {
            **memory.context,
            "category": memory.category,
            "tags": memory.tags
        }
    }
    
    db_memory = Memory(**memory_data)
    db.add(db_memory)
    await db.commit()
    await db.refresh(db_memory)
    
    result = db_memory.to_dict()
    result["category"] = memory.category
    result["tags"] = memory.tags
    
    return MemoryOutput(**result)

@app.get("/memory/search")
async def search_memory(
    query: str,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 10,
    threshold: float = 0.7,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """搜索記憶 - 支援分類和標籤過濾"""
    user_id = current_user["user_id"]
    query_embedding = await embedding_service.create_query_embedding(query)
    
    # 構建查詢
    sql_parts = ["""
        SELECT 
            id, user_id, content, context, created_at,
            1 - (embedding <=> :query_embedding::vector) as similarity
        FROM memories
        WHERE user_id = :user_id
            AND 1 - (embedding <=> :query_embedding::vector) > :threshold
    """]
    
    params = {
        "query_embedding": query_embedding,
        "user_id": user_id,
        "threshold": threshold,
        "limit": limit
    }
    
    # 分類過濾
    if category:
        sql_parts.append("AND context->>'category' = :category")
        params["category"] = category
    
    # 標籤過濾（簡化版）
    if tags:
        sql_parts.append("AND context->'tags' ?| ARRAY[:tags]")
        params["tags"] = tags
    
    sql_parts.append("ORDER BY similarity DESC LIMIT :limit")
    sql = text(" ".join(sql_parts))
    
    result = await db.execute(sql, params)
    
    memories = []
    for row in result:
        context = row.context or {}
        memory_dict = {
            "memory_id": row.id,
            "user_id": row.user_id,
            "content": row.content,
            "context": context,
            "category": context.get("category", "general"),
            "tags": context.get("tags", []),
            "created_at": row.created_at.isoformat(),
            "similarity": round(row.similarity, 4)
        }
        memories.append(memory_dict)
    
    return {
        "user_id": user_id,
        "query": query,
        "filters": {"category": category, "tags": tags},
        "results": memories,
        "count": len(memories)
    }

@app.get("/memory/categories")
async def get_categories(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """獲取用戶的所有分類"""
    user_id = current_user["user_id"]
    
    sql = text("""
        SELECT DISTINCT context->>'category' as category
        FROM memories
        WHERE user_id = :user_id
            AND context->>'category' IS NOT NULL
    """)
    
    result = await db.execute(sql, {"user_id": user_id})
    categories = [row.category for row in result if row.category]
    
    return {
        "user_id": user_id,
        "categories": categories,
        "count": len(categories)
    }

@app.get("/memory/tags")
async def get_tags(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """獲取用戶的所有標籤"""
    user_id = current_user["user_id"]
    
    # 簡化版本 - 實際應該解析 JSON 陣列
    sql = text("""
        SELECT context->'tags' as tags
        FROM memories
        WHERE user_id = :user_id
            AND context->'tags' IS NOT NULL
    """)
    
    result = await db.execute(sql, {"user_id": user_id})
    all_tags = set()
    for row in result:
        if row.tags:
            tags_list = row.tags if isinstance(row.tags, list) else []
            all_tags.update(tags_list)
    
    return {
        "user_id": user_id,
        "tags": list(all_tags),
        "count": len(all_tags)
    }

@app.get("/stats")
async def get_stats(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """用戶統計 - 個人化"""
    user_id = current_user["user_id"]
    
    # 統計該用戶的記憶
    memory_result = await db.execute(
        select(Memory).where(Memory.user_id == user_id)
    )
    user_memories = memory_result.all()
    
    return {
        "user_id": user_id,
        "total_memories": len(user_memories),
        "status": "Day 3 - Production Ready",
        "features": ["Auth", "Categories", "Tags"],
        "next_milestone": "Day 7 - LibreChat Integration"
    }

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_session)):
    """健康檢查 - 無需認證"""
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "version": "0.3.0-beta",
            "day": 3,
            "musk_says": "Authentication done. Ship to production."
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Railway 專用端點
@app.get("/railway/deploy-check")
async def railway_deploy_check():
    """Railway 部署檢查"""
    return {
        "deploy_ready": True,
        "requirements": {
            "PostgreSQL": "Add DATABASE_URL",
            "Environment": "Add GEMINI_API_KEY and SECRET_KEY",
            "Port": "Railway auto-assigns"
        },
        "estimated_time": "5 minutes"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Memory API v3 - Day 3/14")
    print("🔐 Authentication enabled")
    print("🏷️ Categories and tags supported")
    print("☁️ Ready for Railway deployment")
    uvicorn.run(app, host="0.0.0.0", port=8000)