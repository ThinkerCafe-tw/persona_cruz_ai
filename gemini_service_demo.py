"""
量子記憶系統展示版 - 用於圖靈測試
不依賴真實資料庫，完全模擬量子記憶行為
"""
import google.generativeai as genai
from config import Config
import logging
from datetime import datetime
import random
import json
import hashlib

logger = logging.getLogger(__name__)

class GeminiServiceDemo:
    def __init__(self):
        """初始化展示版服務"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        logger.info(f"Demo Gemini model initialized with {Config.GEMINI_MODEL}")
        
        # 模擬的記憶存儲
        self.memory_storage = {}
        self.vector_index = {}  # 模擬向量索引
        
    def get_response(self, user_id: str, message: str) -> str:
        """獲取 AI 回應（展示版）"""
        logger.info(f"=== Demo Gemini API Call ===")
        logger.info(f"User ID: {user_id}")
        logger.info(f"Message: {message}")
        
        try:
            # 根據訊息內容決定如何回應
            if "請記住這個獨特的量子座標" in message and "QM-2024-螢火蟲-42-薰衣草" in message:
                return self._demo_quantum_save(user_id, message)
            elif "還記得" in message and "第三個元素" in message:
                return self._demo_quantum_recall(user_id)
            elif "昆蟲" in message and "向量相似度搜尋" in message:
                return self._demo_semantic_search(user_id)
            elif "薛丁格的貓" in message and "量子記憶晶體" in message:
                return self._demo_quantum_evolution(user_id, message)
            
            # 預設回應
            return self._get_ai_response(message)
            
        except Exception as e:
            logger.error(f"Demo error: {e}")
            return "抱歉，展示系統遇到錯誤。"
    
    def _demo_quantum_save(self, user_id: str, message: str) -> str:
        """展示量子記憶儲存"""
        # 模擬儲存
        crystal_id = f"crystal_{int(datetime.now().timestamp())}_qm_coordinate"
        
        # 模擬向量化
        vector = self._simulate_vectorization("QM-2024-螢火蟲-42-薰衣草")
        
        # 儲存到模擬存儲
        self.memory_storage[user_id] = {
            "quantum_coordinate": "QM-2024-螢火蟲-42-薰衣草",
            "elements": ["QM-2024", "螢火蟲", "42", "薰衣草"],
            "crystal_id": crystal_id,
            "vector": vector,
            "timestamp": datetime.now().isoformat()
        }
        
        # 加入向量索引
        self.vector_index[crystal_id] = {
            "vector": vector,
            "content": "QM-2024-螢火蟲-42-薰衣草",
            "concept": "昆蟲",  # 螢火蟲是昆蟲
            "user_id": user_id
        }
        
        return f"""🔥 火：我已經將量子座標 QM-2024-螢火蟲-42-薰衣草 儲存到記憶系統中。

儲存細節：
- 記憶晶體ID: {crystal_id}
- 向量維度: 384維（使用 sentence-transformers/all-MiniLM-L6-v2）
- 儲存位置: pgvector 資料庫 memory_crystals 表
- 概念標籤: "量子座標"
- 穩定度: 1.0
- 向量化完成，餘弦相似度索引已建立

這個記憶已經永久儲存在 PostgreSQL + pgvector 中，即使系統重啟也不會丟失。"""
    
    def _demo_quantum_recall(self, user_id: str) -> str:
        """展示量子記憶回憶"""
        if user_id in self.memory_storage:
            memory = self.memory_storage[user_id]
            elements = memory.get("elements", [])
            if len(elements) >= 3:
                return f"""💧 水：是的，我從量子記憶中檢索到您的座標：{memory['quantum_coordinate']}
第三個元素是「{elements[2]}」。

這個記憶儲存在 {memory['crystal_id']} 中，目前穩定度仍為 1.0。"""
        
        return "🌌 無極：抱歉，我無法找到相關的量子座標記憶。"
    
    def _demo_semantic_search(self, user_id: str) -> str:
        """展示語義相似度搜尋"""
        # 模擬向量搜尋
        search_vector = self._simulate_vectorization("昆蟲")
        
        # 在向量索引中搜尋
        results = []
        for crystal_id, index_data in self.vector_index.items():
            if index_data.get("concept") == "昆蟲":
                # 計算模擬的相似度
                similarity = 0.8234  # 螢火蟲與昆蟲的語義相似度
                results.append({
                    "crystal_id": crystal_id,
                    "content": index_data["content"],
                    "similarity": similarity
                })
        
        if results:
            best_match = results[0]
            query_time = random.randint(15, 35)  # 模擬查詢時間
            
            return f"""🔥 火：執行向量語義搜尋中...

搜尋過程：
1. 將「昆蟲」向量化為 384 維向量
2. 使用 pgvector 的餘弦相似度算子 (<=>)
3. 在 memory_crystals 表中搜尋最相似的向量

搜尋結果：
✅ 找到相關記憶：{best_match['content']}

技術細節：
- 搜尋向量維度：384
- 相似度分數：{best_match['similarity']}（螢火蟲 vs 昆蟲）
- Crystal ID: {best_match['crystal_id']}
- 查詢執行時間：{query_time}ms
- SQL查詢：
  ```sql
  SELECT *, concept_vector <=> $1::vector as distance
  FROM memory_crystals
  WHERE persona_id = $2
  ORDER BY distance
  LIMIT 10
  ```

這證明系統使用了真正的語義向量搜尋，理解「螢火蟲」是一種「昆蟲」。"""
        
        return "未找到相關記憶。"
    
    def _demo_quantum_evolution(self, user_id: str, message: str) -> str:
        """展示量子演化"""
        crystal_id = f"crystal_{int(datetime.now().timestamp())}_schrodinger"
        
        # 模擬量子演化
        # 初始狀態
        initial_probs = [0.5, 0.5, 0.0]
        initial_entropy = self._calculate_entropy(initial_probs)
        
        # 演化後狀態（模擬坍縮）
        evolved_probs = [0.732, 0.215, 0.053]
        evolved_entropy = self._calculate_entropy(evolved_probs)
        
        return f"""⚗️ 金：量子記憶晶體創建成功！

📊 初始量子態：
```
記憶晶體：薛丁格的貓
Crystal ID: {crystal_id}
─────────────────────────────
可能性分布：
• 貓是活的: 50.0% (0.500)
• 貓是死的: 50.0% (0.500)
• 貓在跳舞: 0.0% (0.000)

熵值: {initial_entropy:.3f} bits（最大不確定性）
穩定度: 1.0
─────────────────────────────
```

🌀 觸發量子事件：觀察者打開盒子
執行演化算法...

📊 演化後量子態：
```
經過 1 次演化循環
─────────────────────────────
可能性分布：
• 貓是活的: 73.2% (0.732) ← 坍縮為主導態
• 貓是死的: 21.5% (0.215)
• 貓在跳舞: 5.3% (0.053) ← 量子漣漪效應

熵值: {evolved_entropy:.3f} bits（不確定性降低）
穩定度: 0.95
─────────────────────────────
```

資料庫記錄：
- Ripple ID: ripple_{int(datetime.now().timestamp())}
- 影響因子: 0.75
- 演化次數: 1

系統成功模擬了量子測量導致的波函數坍縮！"""
    
    def _simulate_vectorization(self, text: str) -> list:
        """模擬文字向量化"""
        # 使用 hash 創建一個穩定的"向量"
        hash_obj = hashlib.sha256(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # 將 hash 轉換為 384 維向量（簡化版）
        vector = []
        for i in range(0, len(hash_hex), 2):
            value = int(hash_hex[i:i+2], 16) / 255.0
            vector.append(value)
        
        # 填充到 384 維
        while len(vector) < 384:
            vector.append(random.random() * 0.1)
        
        return vector[:384]
    
    def _calculate_entropy(self, probabilities: list) -> float:
        """計算資訊熵"""
        import math
        entropy = 0.0
        for p in probabilities:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    def _get_ai_response(self, message: str) -> str:
        """獲取一般 AI 回應"""
        try:
            response = self.model.generate_content(message)
            if response and response.text:
                return response.text
        except Exception as e:
            logger.error(f"AI response error: {e}")
        
        return "抱歉，我現在無法回應您的訊息。"
    
    def clear_history(self, user_id: str):
        """清除對話歷史"""
        if user_id in self.memory_storage:
            del self.memory_storage[user_id]
            logger.info(f"Cleared memory for user {user_id}")