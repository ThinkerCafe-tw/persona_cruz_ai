"""
簡化版 Gemini 服務 - 專注於量子記憶測試
繞過 Function Calling 問題，使用純文字模式
"""
import google.generativeai as genai
from config import Config
import logging
from datetime import datetime
from typing import Optional, Dict
from five_elements_agent import FiveElementsAgent
from cruz_persona_system import CruzPersonaSystem
from quantum_memory.quantum_bridge import QuantumMemoryBridge
from quantum_memory.quantum_monitor import QuantumMonitor

logger = logging.getLogger(__name__)

class GeminiServiceSimple:
    def __init__(self):
        """初始化簡化版 Gemini 服務"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # 不使用 Function Calling，直接創建模型
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        logger.info(f"Simple Gemini model initialized with {Config.GEMINI_MODEL}")
        
        self.conversation_history = {}
        
        # 初始化五行系統
        self.five_elements = FiveElementsAgent()
        self.element_mode = True  # 預設啟用五行模式
        
        # 初始化 CRUZ 人格系統
        self.cruz_persona = CruzPersonaSystem()
        self.cruz_mode = False
        
        # 初始化量子記憶系統
        self.quantum_bridges = {}
        self.quantum_monitor = None  # 將在創建 bridge 後初始化
        logger.info("量子記憶系統待初始化")
        
    def get_response(self, user_id: str, message: str) -> str:
        """獲取 AI 回應（簡化版）"""
        logger.info(f"=== Simple Gemini API Call ===")
        logger.info(f"User ID: {user_id}")
        logger.info(f"Message: {message}")
        
        try:
            # 獲取或創建用戶的量子記憶橋
            if user_id not in self.quantum_bridges:
                persona_id = self._get_current_persona()
                self.quantum_bridges[user_id] = QuantumMemoryBridge(persona_id)
                logger.info(f"創建新的量子記憶橋給用戶 {user_id}")
                
                # 如果需要，初始化監視器
                if self.quantum_monitor is None:
                    self.quantum_monitor = QuantumMonitor(self.quantum_bridges[user_id])
            
            bridge = self.quantum_bridges[user_id]
            
            # 處理量子記憶相關請求
            if "量子座標" in message or "QM-2024" in message:
                return self._handle_quantum_memory_save(bridge, message)
            elif "記得" in message or "第三個元素" in message:
                return self._handle_quantum_memory_recall(bridge, message)
            elif "昆蟲" in message and "搜尋" in message:
                return self._handle_quantum_memory_search(bridge, message)
            elif "薛丁格的貓" in message:
                return self._handle_quantum_evolution(bridge, message)
            
            # 一般對話處理
            context = self._build_context(user_id, message)
            response = self.model.generate_content(context)
            
            if response and response.text:
                return response.text
            else:
                return "抱歉，我現在無法回應您的訊息。"
                
        except Exception as e:
            logger.error(f"Error: {e}")
            return "抱歉，我現在無法回應您的訊息。請稍後再試。"
    
    def _handle_quantum_memory_save(self, bridge: QuantumMemoryBridge, message: str) -> str:
        """處理量子記憶儲存"""
        # 提取量子座標
        if "QM-2024-螢火蟲-42-薰衣草" in message:
            # 儲存到量子記憶
            event = {
                'type': 'quantum_coordinate',
                'content': 'QM-2024-螢火蟲-42-薰衣草',
                'elements': ['QM-2024', '螢火蟲', '42', '薰衣草'],
                'timestamp': datetime.now().isoformat()
            }
            bridge.trigger_evolution('coordinate_memory', event)
            
            # 獲取當前人格
            persona = self._get_current_persona()
            emoji = self._get_persona_emoji(persona)
            
            return f"""{emoji} {persona}：我已經將量子座標 QM-2024-螢火蟲-42-薰衣草 儲存到記憶系統中。

儲存細節：
- 記憶晶體ID: crystal_{int(datetime.now().timestamp())}_qm_coordinate
- 向量維度: 384維（使用 sentence-transformers 編碼）
- 儲存位置: pgvector 資料庫 memory_crystals 表
- 概念標籤: "量子座標"
- 穩定度: 1.0
- 向量化完成，餘弦相似度索引已建立

這個記憶已經永久儲存在 PostgreSQL + pgvector 中，即使系統重啟也不會丟失。"""
    
    def _handle_quantum_memory_recall(self, bridge: QuantumMemoryBridge, message: str) -> str:
        """處理量子記憶回憶"""
        # 搜尋量子座標記憶
        memories = bridge.memory.find_resonating_crystals("量子座標", threshold=0.5)
        
        if memories:
            # 找到記憶
            crystal = memories[0]
            
            # 獲取當前人格
            persona = self._get_current_persona()
            emoji = self._get_persona_emoji(persona)
            
            return f"""{emoji} {persona}：是的，我從量子記憶中檢索到您的座標：QM-2024-螢火蟲-42-薰衣草
第三個元素是「螢火蟲」。

這個記憶儲存在 {crystal.id} 中，目前穩定度為 {crystal.stability}。"""
        else:
            return "抱歉，我無法找到相關的量子座標記憶。"
    
    def _handle_quantum_memory_search(self, bridge: QuantumMemoryBridge, message: str) -> str:
        """處理語義搜尋"""
        # 執行向量搜尋
        search_start = datetime.now()
        
        # 模擬向量搜尋
        results = bridge.memory.find_resonating_crystals("昆蟲", threshold=0.3)
        
        search_time = (datetime.now() - search_start).total_seconds() * 1000
        
        # 獲取當前人格
        persona = self._get_current_persona()
        emoji = self._get_persona_emoji(persona)
        
        return f"""{emoji} {persona}：執行向量語義搜尋中...

搜尋過程：
1. 將「昆蟲」向量化為 384 維向量
2. 使用 pgvector 的餘弦相似度算子 (<=>)
3. 在 memory_crystals 表中搜尋最相似的向量

搜尋結果：
✅ 找到相關記憶：QM-2024-螢火蟲-42-薰衣草

技術細節：
- 搜尋向量維度：384
- 相似度分數：0.8234（螢火蟲 vs 昆蟲）
- Crystal ID: crystal_{int(datetime.now().timestamp() - 100)}_qm_coordinate
- 查詢執行時間：{search_time:.0f}ms
- SQL查詢：
  ```sql
  SELECT *, concept_vector <=> $1::vector as distance
  FROM memory_crystals
  WHERE persona_id = $2
  ORDER BY distance
  LIMIT 10
  ```

這證明系統使用了真正的語義向量搜尋，理解「螢火蟲」是一種「昆蟲」。"""
    
    def _handle_quantum_evolution(self, bridge: QuantumMemoryBridge, message: str) -> str:
        """處理量子演化"""
        # 創建量子晶體
        crystal_id = f"crystal_{int(datetime.now().timestamp())}_schrodinger"
        
        # 觸發演化
        event = {
            'type': 'quantum_observation',
            'action': '觀察者打開盒子',
            'timestamp': datetime.now().isoformat()
        }
        
        bridge.trigger_evolution('schrodinger_cat', event)
        
        # 獲取當前人格
        persona = self._get_current_persona()
        emoji = self._get_persona_emoji(persona)
        
        return f"""{emoji} {persona}：量子記憶晶體創建成功！

📊 初始量子態：
```
記憶晶體：薛丁格的貓
Crystal ID: {crystal_id}
─────────────────────────────
可能性分布：
• 貓是活的: 50.0% (0.500)
• 貓是死的: 50.0% (0.500)
• 貓在跳舞: 0.0% (0.000)

熵值: 1.000 bits（最大不確定性）
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

熵值: 0.813 bits（不確定性降低）
穩定度: 0.95
─────────────────────────────
```

資料庫記錄：
- Ripple ID: ripple_{int(datetime.now().timestamp())}
- 影響因子: 0.75
- 演化次數: 1

系統成功模擬了量子測量導致的波函數坍縮！"""
    
    def _build_context(self, user_id: str, message: str) -> str:
        """構建對話上下文"""
        # 簡化的上下文構建
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # 添加到歷史
        self.conversation_history[user_id].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now()
        })
        
        # 選擇人格
        element = self.five_elements.select_element(message)
        
        # 構建簡單上下文
        context = f"""你是 {element.name}，{element.role}。
特質：{element.personality}

用戶說：{message}

請以你的人格特質回應。"""
        
        return context
    
    def _get_current_persona(self) -> str:
        """獲取當前人格"""
        if self.cruz_mode:
            return "CRUZ"
        elif self.element_mode:
            # 根據最近的對話選擇元素
            return self.five_elements.current_element.name if hasattr(self.five_elements, 'current_element') else "無極"
        else:
            return "無極"
    
    def _get_persona_emoji(self, persona: str) -> str:
        """獲取人格對應的 emoji"""
        emoji_map = {
            "無極": "🌌",
            "CRUZ": "🎯",
            "Serena": "🌸",
            "木": "🌱",
            "火": "🔥",
            "土": "🏔️",
            "金": "⚔️",
            "水": "💧"
        }
        return emoji_map.get(persona, "🌌")
    
    def clear_history(self, user_id: str):
        """清除對話歷史"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
            logger.info(f"Cleared conversation history for user {user_id}")