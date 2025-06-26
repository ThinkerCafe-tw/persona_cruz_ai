-- 初始化 pgvector 擴展
CREATE EXTENSION IF NOT EXISTS vector;

-- 創建索引以加速向量搜索
CREATE INDEX IF NOT EXISTS idx_memories_embedding 
ON memories 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 創建用戶索引
CREATE INDEX IF NOT EXISTS idx_memories_user_id 
ON memories(user_id);