"""
Memory API with SQLite (Day 5 Testing)
簡化版本，使用 SQLite 進行本地測試
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
import sqlite3
import json
import numpy as np
from contextlib import contextmanager

# 設定
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI 應用
app = FastAPI(title="Memory API (SQLite)", version="1.0.0")

# 密碼加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# 資料模型
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class MemoryInput(BaseModel):
    content: str
    category: Optional[str] = "general"
    tags: Optional[List[str]] = []
    context: Optional[Dict[str, Any]] = {}

class MemoryOutput(BaseModel):
    id: str
    content: str
    embedding: Optional[List[float]] = None
    category: str
    tags: List[str]
    context: Dict[str, Any]
    created_at: datetime
    user_id: str

# SQLite 連接
@contextmanager
def get_db():
    conn = sqlite3.connect("memory.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# 初始化資料庫
def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                embedding TEXT,
                category TEXT DEFAULT 'general',
                tags TEXT DEFAULT '[]',
                context TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()

# 啟動時初始化
init_db()

# 輔助函數
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "user_id": payload.get("user_id")}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 簡單的嵌入生成（模擬）
def create_embedding(text: str) -> List[float]:
    """生成簡單的文本嵌入（用於測試）"""
    # 簡單的 hash-based embedding
    np.random.seed(hash(text) % 2**32)
    return np.random.randn(768).tolist()

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """計算餘弦相似度"""
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# API 端點
@app.get("/")
async def root():
    return {"message": "Memory API (SQLite) - Day 5 Testing"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# 認證端點
@app.post("/auth/register")
async def register(user: UserCreate):
    with get_db() as conn:
        # 檢查用戶是否存在
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?",
            (user.username, user.email)
        ).fetchone()
        
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # 創建用戶
        cursor = conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (user.username, user.email, get_password_hash(user.password))
        )
        conn.commit()
        
        return {"message": "User created successfully", "user_id": cursor.lastrowid}

@app.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db() as conn:
        user = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (form_data.username,)
        ).fetchone()
        
        if not user or not verify_password(form_data.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(
            data={"sub": user["username"], "user_id": user["id"]}
        )
        
        return {"access_token": access_token, "token_type": "bearer"}

# 記憶端點
@app.post("/memory/store", response_model=MemoryOutput)
async def store_memory(
    memory: MemoryInput,
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        # 生成嵌入
        embedding = create_embedding(memory.content)
        
        # 存儲記憶
        cursor = conn.execute(
            """INSERT INTO memories 
               (user_id, content, embedding, category, tags, context) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                current_user["user_id"],
                memory.content,
                json.dumps(embedding),
                memory.category,
                json.dumps(memory.tags),
                json.dumps(memory.context)
            )
        )
        conn.commit()
        
        # 返回結果
        return MemoryOutput(
            id=str(cursor.lastrowid),
            content=memory.content,
            embedding=embedding,
            category=memory.category,
            tags=memory.tags,
            context=memory.context,
            created_at=datetime.now(),
            user_id=str(current_user["user_id"])
        )

@app.get("/memory/search")
async def search_memories(
    query: str,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        # 生成查詢嵌入
        query_embedding = create_embedding(query)
        
        # 獲取用戶的所有記憶
        memories = conn.execute(
            """SELECT id, content, embedding, category, tags, context, created_at 
               FROM memories WHERE user_id = ?""",
            (current_user["user_id"],)
        ).fetchall()
        
        # 計算相似度並排序
        results = []
        for memory in memories:
            memory_embedding = json.loads(memory["embedding"])
            similarity = cosine_similarity(query_embedding, memory_embedding)
            
            results.append({
                "id": str(memory["id"]),
                "content": memory["content"],
                "category": memory["category"],
                "tags": json.loads(memory["tags"]),
                "context": json.loads(memory["context"]),
                "created_at": memory["created_at"],
                "similarity": similarity
            })
        
        # 按相似度排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        return {"results": results[:limit]}

@app.get("/memory/list")
async def list_memories(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        memories = conn.execute(
            """SELECT id, content, category, tags, context, created_at 
               FROM memories WHERE user_id = ? 
               ORDER BY created_at DESC LIMIT ? OFFSET ?""",
            (current_user["user_id"], limit, skip)
        ).fetchall()
        
        return {
            "memories": [
                {
                    "id": str(m["id"]),
                    "content": m["content"],
                    "category": m["category"],
                    "tags": json.loads(m["tags"]),
                    "context": json.loads(m["context"]),
                    "created_at": m["created_at"]
                }
                for m in memories
            ]
        }

@app.get("/memory/category/{category}")
async def get_memories_by_category(
    category: str,
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        memories = conn.execute(
            """SELECT id, content, tags, context, created_at 
               FROM memories WHERE user_id = ? AND category = ?
               ORDER BY created_at DESC""",
            (current_user["user_id"], category)
        ).fetchall()
        
        return {
            "memories": [
                {
                    "id": str(m["id"]),
                    "content": m["content"],
                    "tags": json.loads(m["tags"]),
                    "context": json.loads(m["context"]),
                    "created_at": m["created_at"]
                }
                for m in memories
            ]
        }

@app.delete("/memory/{memory_id}")
async def delete_memory(
    memory_id: int,
    current_user: dict = Depends(get_current_user)
):
    with get_db() as conn:
        # 檢查記憶是否屬於當前用戶
        memory = conn.execute(
            "SELECT id FROM memories WHERE id = ? AND user_id = ?",
            (memory_id, current_user["user_id"])
        ).fetchone()
        
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        # 刪除記憶
        conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        conn.commit()
        
        return {"message": "Memory deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Memory API (SQLite) on http://localhost:8000")
    print("📊 API docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)