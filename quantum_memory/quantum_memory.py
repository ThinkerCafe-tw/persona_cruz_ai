"""
量子記憶核心資料結構
定義記憶的量子態表示
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import deque
from dataclasses import dataclass, field
import logging
from .database import QuantumDatabase
from .vectorizer import QuantumVectorizer

logger = logging.getLogger(__name__)

@dataclass
class Possibility:
    """可能性 - 量子疊加態的一種可能"""
    description: str
    probability: float
    evidence_count: int = 0
    last_reinforced: Optional[datetime] = None
    
    def reinforce(self, strength: float = 0.1):
        """強化這個可能性"""
        self.probability = min(1.0, self.probability * (1 + strength))
        self.evidence_count += 1
        self.last_reinforced = datetime.now()
    
    def weaken(self, strength: float = 0.05):
        """弱化這個可能性"""
        self.probability = max(0.001, self.probability * (1 - strength))
    
    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "probability": self.probability,
            "evidence_count": self.evidence_count,
            "last_reinforced": self.last_reinforced.isoformat() if self.last_reinforced else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Possibility':
        return cls(
            description=data["description"],
            probability=data["probability"],
            evidence_count=data.get("evidence_count", 0),
            last_reinforced=datetime.fromisoformat(data["last_reinforced"]) if data.get("last_reinforced") else None
        )


@dataclass
class MemoryCrystal:
    """記憶晶體 - 可坍縮的概念"""
    id: str
    concept: str
    possibilities: List[Possibility] = field(default_factory=list)
    resonance_history: deque = field(default_factory=lambda: deque(maxlen=50))
    stability: float = 1.0
    creation_time: datetime = field(default_factory=datetime.now)
    last_evolution: Optional[datetime] = None
    
    def add_possibility(self, description: str, initial_probability: float = 0.1):
        """添加新的可能性"""
        # 確保總機率不超過1
        current_total = sum(p.probability for p in self.possibilities)
        if current_total + initial_probability > 1.0:
            # 正規化現有機率
            factor = (1.0 - initial_probability) / current_total if current_total > 0 else 1.0
            for p in self.possibilities:
                p.probability *= factor
        
        self.possibilities.append(Possibility(description, initial_probability))
        self.normalize_probabilities()
    
    def normalize_probabilities(self):
        """正規化機率分布"""
        total = sum(p.probability for p in self.possibilities)
        if total > 0:
            for p in self.possibilities:
                p.probability /= total
    
    def get_dominant_possibility(self) -> Optional[Possibility]:
        """獲取最可能的狀態"""
        if not self.possibilities:
            return None
        return max(self.possibilities, key=lambda p: p.probability)
    
    def calculate_entropy(self) -> float:
        """計算資訊熵（不確定性）"""
        import math
        entropy = 0.0
        for p in self.possibilities:
            if p.probability > 0:
                entropy -= p.probability * math.log2(p.probability)
        return entropy
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "concept": self.concept,
            "possibilities": [p.to_dict() for p in self.possibilities],
            "stability": self.stability,
            "creation_time": self.creation_time.isoformat(),
            "last_evolution": self.last_evolution.isoformat() if self.last_evolution else None,
            "entropy": self.calculate_entropy()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MemoryCrystal':
        crystal = cls(
            id=data["id"],
            concept=data["concept"],
            stability=data.get("stability", 1.0),
            creation_time=datetime.fromisoformat(data["creation_time"]),
            last_evolution=datetime.fromisoformat(data["last_evolution"]) if data.get("last_evolution") else None
        )
        crystal.possibilities = [Possibility.from_dict(p) for p in data.get("possibilities", [])]
        return crystal


@dataclass
class QuantumIdentity:
    """量子身份場 - 角色的核心量子態"""
    essence: str = ""  # 核心本質
    phase: float = 0.0  # 當前相位（0-1）
    frequency: float = 1.0  # 振動頻率
    amplitude: float = 1.0  # 影響強度
    coherence: float = 1.0  # 一致性
    
    def to_dict(self) -> dict:
        return {
            "essence": self.essence,
            "phase": self.phase,
            "frequency": self.frequency,
            "amplitude": self.amplitude,
            "coherence": self.coherence
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'QuantumIdentity':
        return cls(**data)


class QuantumMemory:
    """單一角色的量子記憶"""
    
    def __init__(self, persona_id: str, use_database: bool = True):
        self.persona_id = persona_id
        self.identity = QuantumIdentity()
        self.use_database = use_database
        
        # 初始化資料庫和向量化器
        if self.use_database:
            self.db = QuantumDatabase()
            self.vectorizer = QuantumVectorizer()
            self._memory_id = None  # 資料庫中的記憶 ID
        self.crystals: Dict[str, MemoryCrystal] = {}
        self.ripples: deque = deque(maxlen=100)  # 最近100個漣漪
        self.entanglements: Dict[str, float] = {}  # 與其他角色的量子糾纏
        self.evolution_count = 0
        self.created_at = datetime.now()
        self.last_save = None
        
        # 嘗試載入現有記憶
        self.load()
    
    def add_crystal(self, concept: str, initial_possibilities: List[Dict[str, Any]]) -> MemoryCrystal:
        """添加新的記憶晶體"""
        crystal_id = f"{self.persona_id}_{concept}_{datetime.now().timestamp()}"
        crystal = MemoryCrystal(id=crystal_id, concept=concept)
        
        for poss in initial_possibilities:
            crystal.add_possibility(
                poss["description"],
                poss.get("probability", 0.1)
            )
        
        self.crystals[crystal_id] = crystal
        logger.info(f"Added new crystal: {concept} for {self.persona_id}")
        return crystal
    
    def find_resonating_crystals(self, keywords: List[str], threshold: float = 0.3) -> List[MemoryCrystal]:
        """找出與關鍵詞共振的晶體"""
        resonating = []
        
        for crystal in self.crystals.values():
            # 計算共振強度
            resonance = 0.0
            concept_lower = crystal.concept.lower()
            
            for keyword in keywords:
                if keyword.lower() in concept_lower:
                    resonance += 0.5
                
                # 檢查可能性描述
                for possibility in crystal.possibilities:
                    if keyword.lower() in possibility.description.lower():
                        resonance += 0.3 * possibility.probability
            
            if resonance >= threshold:
                resonating.append((crystal, resonance))
        
        # 按共振強度排序
        resonating.sort(key=lambda x: x[1], reverse=True)
        return [crystal for crystal, _ in resonating]
    
    def add_ripple(self, event: dict):
        """添加新的漣漪（事件）"""
        ripple = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "impact": self._calculate_impact(event)
        }
        self.ripples.append(ripple)
        
        # 即時保存到資料庫
        if self.use_database and self.db and self.db.pool and self._memory_id:
            try:
                event_vector = self.vectorizer.vectorize_event(event)
                self.db.save_ripple(self._memory_id, ripple, event_vector)
            except Exception as e:
                logger.error(f"Failed to save ripple to database: {e}")
    
    def _calculate_impact(self, event: dict) -> float:
        """計算事件的影響力"""
        # 簡單的影響力計算
        base_impact = 0.5
        
        # 根據事件類型調整
        if event.get("type") == "breakthrough":
            base_impact = 0.9
        elif event.get("type") == "failure":
            base_impact = 0.7
        elif event.get("type") == "insight":
            base_impact = 0.8
        
        return base_impact
    
    def get_stability_index(self) -> float:
        """計算整體穩定度"""
        if not self.crystals:
            return 1.0
        
        total_stability = sum(c.stability for c in self.crystals.values())
        return total_stability / len(self.crystals)
    
    def get_top_crystals(self, n: int = 5) -> List[MemoryCrystal]:
        """獲取最重要的記憶晶體"""
        # 根據穩定度和熵的組合排序
        crystals_with_score = []
        
        for crystal in self.crystals.values():
            # 高穩定度、低熵的晶體更重要
            score = crystal.stability * (1 - crystal.calculate_entropy() * 0.5)
            crystals_with_score.append((crystal, score))
        
        crystals_with_score.sort(key=lambda x: x[1], reverse=True)
        return [crystal for crystal, _ in crystals_with_score[:n]]
    
    def save(self):
        """保存量子記憶到檔案和資料庫"""
        # 總是保存到檔案作為備份
        memory_path = f"quantum_memory/memories/{self.persona_id}.json"
        
        data = {
            "persona_id": self.persona_id,
            "identity": self.identity.to_dict(),
            "crystals": {
                cid: crystal.to_dict() 
                for cid, crystal in self.crystals.items()
            },
            "ripples": list(self.ripples),
            "entanglements": self.entanglements,
            "evolution_count": self.evolution_count,
            "created_at": self.created_at.isoformat(),
            "last_save": datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        
        with open(memory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 同時保存到資料庫
        if self.use_database and self.db and self.db.pool:
            try:
                # 保存主記憶
                identity_vector = self.vectorizer.vectorize_identity(self.identity.to_dict())
                self._memory_id = self.db.save_quantum_memory(
                    self.persona_id,
                    self.identity.to_dict(),
                    identity_vector
                )
                
                if self._memory_id:
                    # 保存記憶晶體
                    for crystal in self.crystals.values():
                        concept_vector = self.vectorizer.vectorize_concept(
                            crystal.concept,
                            [p.to_dict() for p in crystal.possibilities]
                        )
                        self.db.save_memory_crystal(
                            self._memory_id,
                            crystal.to_dict(),
                            concept_vector
                        )
                    
                    # 保存漣漪（只保存最近的）
                    for ripple in list(self.ripples)[-10:]:
                        event_vector = self.vectorizer.vectorize_event(ripple['event'])
                        self.db.save_ripple(self._memory_id, ripple, event_vector)
                
                logger.info(f"Saved quantum memory to database for {self.persona_id}")
            except Exception as e:
                logger.error(f"Failed to save to database: {e}")
        
        self.last_save = datetime.now()
        logger.info(f"Saved quantum memory for {self.persona_id}")
    
    def load(self):
        """從資料庫或檔案載入量子記憶"""
        loaded_from_db = False
        
        # 優先從資料庫載入
        if self.use_database and self.db and self.db.pool:
            try:
                memory_data = self.db.get_quantum_memory(self.persona_id)
                if memory_data:
                    self._memory_id = memory_data['id']
                    self.identity = QuantumIdentity.from_dict(memory_data['identity_data'])
                    self.created_at = memory_data['created_at']
                    
                    # 載入記憶晶體
                    crystals_data = self.db.get_memory_crystals(self._memory_id)
                    self.crystals = {}
                    for crystal_data in crystals_data:
                        crystal = MemoryCrystal.from_dict({
                            'id': crystal_data['crystal_id'],
                            'concept': crystal_data['concept'],
                            'possibilities': crystal_data['possibilities'],
                            'stability': crystal_data['stability'],
                            'creation_time': crystal_data['created_at'].isoformat(),
                            'last_evolution': crystal_data['updated_at'].isoformat()
                        })
                        self.crystals[crystal.id] = crystal
                    
                    # 載入漣漪
                    ripples_data = self.db.get_ripples(self._memory_id)
                    self.ripples = deque(maxlen=100)
                    for ripple_data in ripples_data:
                        self.ripples.append({
                            'timestamp': ripple_data['timestamp'].isoformat(),
                            'event': ripple_data['event_data'],
                            'impact': ripple_data['impact']
                        })
                    
                    loaded_from_db = True
                    logger.info(f"Loaded quantum memory from database for {self.persona_id}")
            except Exception as e:
                logger.error(f"Failed to load from database: {e}")
        
        # 如果資料庫載入失敗，從檔案載入
        if not loaded_from_db:
            memory_path = f"quantum_memory/memories/{self.persona_id}.json"
            
            if not os.path.exists(memory_path):
                logger.info(f"No existing memory found for {self.persona_id}")
                return
            
            try:
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.identity = QuantumIdentity.from_dict(data["identity"])
                
                self.crystals = {}
                for cid, crystal_data in data.get("crystals", {}).items():
                    self.crystals[cid] = MemoryCrystal.from_dict(crystal_data)
                
                self.ripples = deque(data.get("ripples", []), maxlen=100)
                self.entanglements = data.get("entanglements", {})
                self.evolution_count = data.get("evolution_count", 0)
                self.created_at = datetime.fromisoformat(data["created_at"])
                
                logger.info(f"Loaded quantum memory from file for {self.persona_id}")
                
            except Exception as e:
                logger.error(f"Failed to load quantum memory: {e}")
    
    def to_summary(self) -> str:
        """生成記憶摘要"""
        summary = f"""
🌌 {self.persona_id} 的量子記憶場
        
身份本質: {self.identity.essence}
相位: {self.identity.phase:.2f} | 頻率: {self.identity.frequency:.2f}
穩定指數: {self.get_stability_index():.2%}
記憶晶體數: {len(self.crystals)}
演化次數: {self.evolution_count}

主要記憶晶體:
"""
        
        for crystal in self.get_top_crystals(3):
            dominant = crystal.get_dominant_possibility()
            if dominant:
                summary += f"\n💎 {crystal.concept}"
                summary += f"\n   → {dominant.description} ({dominant.probability:.1%})"
                summary += f"\n   熵值: {crystal.calculate_entropy():.2f}"
        
        return summary