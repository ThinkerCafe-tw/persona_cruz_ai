"""
向量嵌入服務
Day 2 - 使用 Gemini 進行嵌入（免費且快速）
"""
import os
import numpy as np
from typing import List
import google.generativeai as genai

# 配置 Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class EmbeddingService:
    """極簡嵌入服務"""
    
    def __init__(self):
        self.model = "models/embedding-001"
        self.dimension = 768  # Gemini embedding dimension
    
    async def create_embedding(self, text: str) -> List[float]:
        """創建文本嵌入向量"""
        try:
            # 使用 Gemini 嵌入
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding error: {e}")
            # 降級方案：返回隨機向量
            return np.random.rand(self.dimension).tolist()
    
    async def create_query_embedding(self, query: str) -> List[float]:
        """創建查詢嵌入向量"""
        try:
            result = genai.embed_content(
                model=self.model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Query embedding error: {e}")
            return np.random.rand(self.dimension).tolist()

# 全局實例
embedding_service = EmbeddingService()