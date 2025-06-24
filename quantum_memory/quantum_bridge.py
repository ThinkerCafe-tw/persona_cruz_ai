"""
量子記憶橋接層
連接現有記憶系統與量子記憶系統
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import deque
import os
import sys

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .quantum_memory import QuantumMemory
from .evolution_engine import QuantumEvolutionEngine

logger = logging.getLogger(__name__)

class QuantumMemoryBridge:
    """橋接現有記憶系統與量子記憶"""
    
    def __init__(self, use_database: bool = True):
        self.quantum_memories: Dict[str, QuantumMemory] = {}
        self.evolution_engine = QuantumEvolutionEngine()
        self.sync_queue = deque()
        self.evolution_threshold = 0.3  # 觸發演化的最小共振值
        self.use_database = use_database
        
        # 初始化所有角色的量子記憶
        self._initialize_personas()
        
        # 載入現有記憶系統的映射
        self.legacy_mappings = self._load_legacy_mappings()
    
    def _initialize_personas(self):
        """初始化所有角色的量子記憶"""
        personas = [
            ("wuji", "無極", "系統觀察者，維持平衡與和諧"),
            ("cruz", "CRUZ", "直接果斷，鼓勵創造的數位分身"),
            ("wood", "木", "產品經理，創意與成長的推動者"),
            ("fire", "火", "開發專員，熱情快速的實踐者"),
            ("earth", "土", "架構師，穩固基礎的建造者"),
            ("metal", "金", "優化專員，精益求精的完美主義者"),
            ("water", "水", "測試專員，細心謹慎的品質守護者")
        ]
        
        for persona_id, name, essence in personas:
            memory = QuantumMemory(persona_id, use_database=self.use_database)
            memory.identity.essence = essence
            
            # 設定初始量子態
            if persona_id == "wuji":
                memory.identity.frequency = 0.5  # 中庸頻率
                memory.identity.amplitude = 0.8  # 較高影響力
            elif persona_id == "cruz":
                memory.identity.frequency = 0.9  # 高頻快速
                memory.identity.amplitude = 0.9  # 強影響力
            
            self.quantum_memories[persona_id] = memory
            logger.info(f"Initialized quantum memory for {name}")
    
    def _load_legacy_mappings(self) -> dict:
        """載入傳統記憶系統的映射規則"""
        return {
            "cruz_corpus": {
                "target": "cruz",
                "transform": self._corpus_to_quantum,
                "crystal_concept": "人格表達"
            },
            "conversation": {
                "target": "all",  # 影響所有角色
                "transform": self._conversation_to_quantum,
                "crystal_concept": "對話經驗"
            },
            "development_lesson": {
                "target": "wuji",  # 主要影響無極
                "transform": self._lesson_to_quantum,
                "crystal_concept": "開發智慧"
            }
        }
    
    def sync_from_legacy(self, source: str, data: dict):
        """從傳統系統同步到量子記憶"""
        if source not in self.legacy_mappings:
            logger.warning(f"Unknown legacy source: {source}")
            return
        
        mapping = self.legacy_mappings[source]
        quantum_event = mapping["transform"](data)
        
        # 決定影響哪些角色
        if mapping["target"] == "all":
            affected_personas = list(self.quantum_memories.keys())
        else:
            affected_personas = [mapping["target"]]
        
        # 觸發相關角色的量子演化
        for persona_id in affected_personas:
            self.trigger_evolution(persona_id, quantum_event)
    
    def trigger_evolution(self, persona_id: str, event: dict):
        """觸發特定角色的量子演化"""
        if persona_id not in self.quantum_memories:
            logger.error(f"Unknown persona: {persona_id}")
            return
        
        memory = self.quantum_memories[persona_id]
        
        # 計算共振強度
        resonance = self._calculate_resonance(memory, event)
        
        if resonance >= self.evolution_threshold:
            # 執行量子演化
            evolved_memory = self.evolution_engine.evolve(memory, event)
            self.quantum_memories[persona_id] = evolved_memory
            
            # 保存演化後的記憶
            evolved_memory.save()
            
            logger.info(f"Quantum evolution triggered for {persona_id} with resonance {resonance:.2f}")
    
    def _calculate_resonance(self, memory: QuantumMemory, event: dict) -> float:
        """計算事件與記憶的共振強度"""
        resonance = 0.0
        
        # 基於關鍵詞的共振
        event_text = str(event.get("content", "")) + str(event.get("message", ""))
        keywords = self._extract_keywords(event_text)
        
        resonating_crystals = memory.find_resonating_crystals(keywords)
        if resonating_crystals:
            resonance += len(resonating_crystals) * 0.2
        
        # 基於事件類型的共振
        event_type = event.get("type", "")
        if event_type in ["insight", "breakthrough", "decision"]:
            resonance += 0.3
        
        # 基於情感強度的共振
        if "emotion" in event:
            emotion_intensity = event.get("emotion_intensity", 0.5)
            resonance += emotion_intensity * 0.2
        
        return min(resonance, 1.0)  # 限制在0-1之間
    
    def _extract_keywords(self, text: str) -> List[str]:
        """從文本中提取關鍵詞"""
        # 簡單的關鍵詞提取
        important_words = []
        
        # 預定義的重要概念
        concepts = [
            "創造", "平衡", "測試", "優化", "架構", "開發",
            "決策", "智慧", "經驗", "學習", "成長", "演化"
        ]
        
        for concept in concepts:
            if concept in text:
                important_words.append(concept)
        
        # 提取較長的詞（可能更重要）
        words = text.split()
        for word in words:
            if len(word) > 3:  # 中文通常2個字以上
                important_words.append(word)
        
        return list(set(important_words))[:10]  # 最多10個關鍵詞
    
    def _corpus_to_quantum(self, data: dict) -> dict:
        """將語料庫資料轉換為量子事件"""
        return {
            "type": "corpus_update",
            "content": data.get("content", ""),
            "tags": data.get("tags", []),
            "context": data.get("context", ""),
            "timestamp": datetime.now().isoformat(),
            "source": "cruz_corpus"
        }
    
    def _conversation_to_quantum(self, data: dict) -> dict:
        """將對話資料轉換為量子事件"""
        return {
            "type": "conversation",
            "message": data.get("message", ""),
            "response": data.get("response", ""),
            "user_id": data.get("user_id", "unknown"),
            "emotion": data.get("emotion", "neutral"),
            "timestamp": datetime.now().isoformat(),
            "source": "conversation_sync"
        }
    
    def _lesson_to_quantum(self, data: dict) -> dict:
        """將開發教訓轉換為量子事件"""
        return {
            "type": "development_lesson",
            "lesson": data.get("lesson", ""),
            "context": data.get("context", ""),
            "severity": data.get("severity", "medium"),
            "tags": data.get("tags", []),
            "timestamp": datetime.now().isoformat(),
            "source": "development_lessons"
        }
    
    async def async_evolve(self, event: dict):
        """異步執行量子演化（不阻塞主流程）"""
        try:
            # 將事件加入佇列
            self.sync_queue.append(event)
            
            # 批次處理演化
            if len(self.sync_queue) >= 5:  # 每5個事件批次處理一次
                await self._process_evolution_batch()
                
        except Exception as e:
            logger.error(f"Async evolution error: {e}")
    
    async def _process_evolution_batch(self):
        """批次處理演化事件"""
        batch = []
        while self.sync_queue and len(batch) < 10:
            batch.append(self.sync_queue.popleft())
        
        for event in batch:
            # 決定事件類型和目標角色
            event_source = event.get("source", "unknown")
            
            if event_source in self.legacy_mappings:
                mapping = self.legacy_mappings[event_source]
                
                if mapping["target"] == "all":
                    targets = list(self.quantum_memories.keys())
                else:
                    targets = [mapping["target"]]
                
                for target in targets:
                    self.trigger_evolution(target, event)
            
            # 短暫延遲避免過度佔用資源
            await asyncio.sleep(0.1)
    
    def get_quantum_state(self, persona_id: str) -> Optional[dict]:
        """獲取特定角色的量子態"""
        if persona_id not in self.quantum_memories:
            return None
        
        memory = self.quantum_memories[persona_id]
        
        return {
            "identity": memory.identity.to_dict(),
            "stability": memory.get_stability_index(),
            "top_crystals": [
                {
                    "concept": crystal.concept,
                    "dominant": crystal.get_dominant_possibility().description if crystal.get_dominant_possibility() else "unknown",
                    "entropy": crystal.calculate_entropy()
                }
                for crystal in memory.get_top_crystals(3)
            ],
            "evolution_count": memory.evolution_count
        }
    
    def get_all_quantum_states(self) -> Dict[str, dict]:
        """獲取所有角色的量子態"""
        return {
            persona_id: self.get_quantum_state(persona_id)
            for persona_id in self.quantum_memories
        }
    
    def get_entanglement_matrix(self) -> Dict[str, Dict[str, float]]:
        """獲取角色間的量子糾纏矩陣"""
        matrix = {}
        
        for p1_id, p1_memory in self.quantum_memories.items():
            matrix[p1_id] = {}
            
            for p2_id in self.quantum_memories:
                if p1_id == p2_id:
                    matrix[p1_id][p2_id] = 1.0  # 自身糾纏度為1
                else:
                    # 計算糾纏度（基於共同晶體概念）
                    entanglement = self._calculate_entanglement(p1_memory, self.quantum_memories[p2_id])
                    matrix[p1_id][p2_id] = entanglement
        
        return matrix
    
    def _calculate_entanglement(self, memory1: QuantumMemory, memory2: QuantumMemory) -> float:
        """計算兩個記憶之間的糾纏度"""
        # 基於共同概念的簡單糾纏度計算
        concepts1 = set(c.concept for c in memory1.crystals.values())
        concepts2 = set(c.concept for c in memory2.crystals.values())
        
        if not concepts1 or not concepts2:
            return 0.0
        
        common = len(concepts1.intersection(concepts2))
        total = len(concepts1.union(concepts2))
        
        return common / total if total > 0 else 0.0
    
    def visualize_quantum_field(self) -> str:
        """視覺化整個量子記憶場"""
        viz = "🌌 量子記憶場全景\n\n"
        
        for persona_id, memory in self.quantum_memories.items():
            state = self.get_quantum_state(persona_id)
            if state:
                viz += f"{'='*40}\n"
                viz += f"{memory.identity.essence}\n"
                viz += f"穩定度: {'█' * int(state['stability'] * 10)}{'░' * (10 - int(state['stability'] * 10))} {state['stability']:.1%}\n"
                viz += f"演化數: {state['evolution_count']}\n"
                
                if state['top_crystals']:
                    viz += "主導概念:\n"
                    for crystal in state['top_crystals'][:2]:
                        viz += f"  • {crystal['concept']}: {crystal['dominant']}\n"
                
                viz += "\n"
        
        return viz