"""
量子演化引擎
處理記憶的量子演化過程
"""
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

from .quantum_memory import QuantumMemory, MemoryCrystal, Possibility

logger = logging.getLogger(__name__)


class QuantumEvolutionEngine:
    """量子演化引擎 - 純提示詞驅動的演化"""
    
    def __init__(self):
        self.evolution_prompts = self._load_evolution_prompts()
        self.ripple_patterns = self._load_ripple_patterns()
        
    def _load_evolution_prompts(self) -> Dict[str, List[str]]:
        """載入演化提示詞模板"""
        return {
            "新經驗": [
                "當{persona}遇到{event}時，{concept}的意義開始轉變...",
                "{event}讓{persona}對{concept}有了新的理解...",
                "這個{event}如何影響{persona}對{concept}的看法？"
            ],
            "強化": [
                "{event}證實了{persona}關於{concept}的{possibility}...",
                "又一次經歷證明{possibility}是{concept}的真實面向...",
                "{persona}更加確信{concept}意味著{possibility}..."
            ],
            "衝突": [
                "{event}與{persona}對{concept}的理解產生矛盾...",
                "這個{event}挑戰了{possibility}的可能性...",
                "{persona}開始懷疑{concept}是否真的是{possibility}..."
            ],
            "突破": [
                "{event}帶來關於{concept}的全新視角...",
                "{persona}突然意識到{concept}可能是完全不同的東西...",
                "這個洞察徹底改變了{concept}的意義..."
            ]
        }
    
    def _load_ripple_patterns(self) -> Dict[str, dict]:
        """載入漣漪模式"""
        return {
            "insight": {
                "spread": 0.8,      # 擴散強度
                "depth": 3,         # 影響深度
                "decay": 0.3        # 衰減率
            },
            "breakthrough": {
                "spread": 0.9,
                "depth": 5,
                "decay": 0.2
            },
            "failure": {
                "spread": 0.6,
                "depth": 2,
                "decay": 0.5
            },
            "routine": {
                "spread": 0.3,
                "depth": 1,
                "decay": 0.7
            }
        }
    
    def evolve(self, memory: QuantumMemory, event: dict) -> QuantumMemory:
        """執行量子演化"""
        logger.info(f"Starting quantum evolution for {memory.persona_id}")
        
        # 1. 分析事件類型
        event_type = self._classify_event(event)
        
        # 2. 找出受影響的晶體
        affected_crystals = self._find_affected_crystals(memory, event)
        
        # 3. 執行量子坍縮
        for crystal, resonance in affected_crystals:
            self._collapse_crystal(crystal, event, event_type, resonance)
        
        # 4. 創造漣漪效應
        ripples = self._create_ripples(memory, event, event_type)
        
        # 5. 處理量子糾纏
        self._process_entanglements(memory, event, ripples)
        
        # 6. 可能產生新晶體
        if self._should_create_new_crystal(event, event_type):
            self._create_new_crystal(memory, event)
        
        # 7. 更新記憶狀態
        memory.evolution_count += 1
        memory.add_ripple(event)
        
        # 8. 調整身份場
        self._adjust_identity_field(memory, event_type)
        
        logger.info(f"Quantum evolution completed for {memory.persona_id}")
        return memory
    
    def _classify_event(self, event: dict) -> str:
        """分類事件類型"""
        # 基於事件內容判斷類型
        event_type = event.get("type", "")
        
        if event_type in ["insight", "breakthrough", "failure"]:
            return event_type
        
        # 基於內容分析
        content = str(event.get("content", "")) + str(event.get("message", ""))
        
        insight_keywords = ["發現", "理解", "原來", "洞察", "明白"]
        breakthrough_keywords = ["突破", "革新", "創新", "全新", "徹底"]
        failure_keywords = ["失敗", "錯誤", "問題", "bug", "無法"]
        
        for keyword in breakthrough_keywords:
            if keyword in content:
                return "breakthrough"
        
        for keyword in insight_keywords:
            if keyword in content:
                return "insight"
                
        for keyword in failure_keywords:
            if keyword in content:
                return "failure"
        
        return "routine"
    
    def _find_affected_crystals(self, memory: QuantumMemory, event: dict) -> List[Tuple[MemoryCrystal, float]]:
        """找出受事件影響的晶體"""
        affected = []
        
        # 提取關鍵詞
        keywords = self._extract_keywords_from_event(event)
        
        # 計算每個晶體的共振強度
        for crystal in memory.crystals.values():
            resonance = self._calculate_crystal_resonance(crystal, keywords, event)
            if resonance > 0.1:  # 共振閾值
                affected.append((crystal, resonance))
        
        # 按共振強度排序
        affected.sort(key=lambda x: x[1], reverse=True)
        
        # 限制影響的晶體數量
        return affected[:5]
    
    def _extract_keywords_from_event(self, event: dict) -> List[str]:
        """從事件中提取關鍵詞"""
        keywords = []
        
        # 從各個欄位提取
        for field in ["content", "message", "lesson", "tags"]:
            if field in event:
                if isinstance(event[field], list):
                    keywords.extend(event[field])
                else:
                    # 簡單分詞
                    text = str(event[field])
                    keywords.extend([w for w in text.split() if len(w) > 2])
        
        return list(set(keywords))
    
    def _calculate_crystal_resonance(self, crystal: MemoryCrystal, keywords: List[str], event: dict) -> float:
        """計算晶體共振強度"""
        resonance = 0.0
        
        # 概念匹配
        for keyword in keywords:
            if keyword in crystal.concept:
                resonance += 0.5
        
        # 可能性描述匹配
        for possibility in crystal.possibilities:
            for keyword in keywords:
                if keyword in possibility.description:
                    resonance += 0.3 * possibility.probability
        
        # 考慮晶體的穩定性（不穩定的晶體更容易共振）
        resonance *= (2.0 - crystal.stability)
        
        return min(resonance, 1.0)
    
    def _collapse_crystal(self, crystal: MemoryCrystal, event: dict, event_type: str, resonance: float):
        """執行晶體的量子坍縮"""
        # 根據事件類型選擇坍縮模式
        if event_type == "breakthrough":
            self._breakthrough_collapse(crystal, event, resonance)
        elif event_type == "insight":
            self._insight_collapse(crystal, event, resonance)
        elif event_type == "failure":
            self._failure_collapse(crystal, event, resonance)
        else:
            self._routine_collapse(crystal, event, resonance)
        
        # 記錄坍縮歷史
        crystal.resonance_history.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "resonance": resonance
        })
        
        # 更新最後演化時間
        crystal.last_evolution = datetime.now()
        
        # 調整穩定性
        crystal.stability = self._calculate_new_stability(crystal)
    
    def _breakthrough_collapse(self, crystal: MemoryCrystal, event: dict, resonance: float):
        """突破性坍縮 - 可能創造全新可能性"""
        # 選擇演化提示詞
        prompt_template = random.choice(self.evolution_prompts["突破"])
        
        # 創造新的可能性
        new_possibility_desc = self._generate_possibility_from_prompt(
            prompt_template, crystal, event
        )
        
        # 大幅調整機率分布
        if crystal.possibilities:
            # 降低所有現有可能性
            for p in crystal.possibilities:
                p.weaken(0.3 * resonance)
        
        # 添加新的主導可能性
        crystal.add_possibility(new_possibility_desc, 0.4 * resonance)
        
        logger.info(f"Breakthrough collapse: {crystal.concept} -> {new_possibility_desc}")
    
    def _insight_collapse(self, crystal: MemoryCrystal, event: dict, resonance: float):
        """洞察性坍縮 - 強化或調整現有可能性"""
        if not crystal.possibilities:
            return
        
        # 找出最相關的可能性
        best_match = self._find_best_matching_possibility(crystal, event)
        
        if best_match:
            # 強化這個可能性
            best_match.reinforce(0.2 * resonance)
            
            # 選擇強化提示詞
            prompt_template = random.choice(self.evolution_prompts["強化"])
            log_msg = self._generate_log_from_prompt(prompt_template, crystal, event, best_match)
            logger.info(f"Insight collapse: {log_msg}")
        
        # 正規化機率
        crystal.normalize_probabilities()
    
    def _failure_collapse(self, crystal: MemoryCrystal, event: dict, resonance: float):
        """失敗性坍縮 - 弱化相關可能性"""
        if not crystal.possibilities:
            return
        
        # 找出可能導致失敗的可能性
        problematic = self._find_problematic_possibility(crystal, event)
        
        if problematic:
            # 弱化這個可能性
            problematic.weaken(0.25 * resonance)
            
            # 選擇衝突提示詞
            prompt_template = random.choice(self.evolution_prompts["衝突"])
            log_msg = self._generate_log_from_prompt(prompt_template, crystal, event, problematic)
            logger.info(f"Failure collapse: {log_msg}")
        
        # 可能需要新的理解
        if problematic and problematic.probability < 0.2:
            new_desc = f"避免{problematic.description}的替代方案"
            crystal.add_possibility(new_desc, 0.15)
        
        crystal.normalize_probabilities()
    
    def _routine_collapse(self, crystal: MemoryCrystal, event: dict, resonance: float):
        """常規坍縮 - 小幅調整"""
        if not crystal.possibilities:
            return
        
        # 輕微強化相關可能性
        for possibility in crystal.possibilities:
            if self._is_possibility_relevant(possibility, event):
                possibility.reinforce(0.05 * resonance)
        
        crystal.normalize_probabilities()
    
    def _generate_possibility_from_prompt(self, template: str, crystal: MemoryCrystal, event: dict) -> str:
        """從提示詞生成新可能性描述"""
        # 這裡簡化處理，實際應該調用 AI
        concept = crystal.concept
        event_desc = event.get("content", event.get("message", "新經驗"))
        
        # 基於模板生成描述
        if "創新" in event_desc or "突破" in event_desc:
            return f"{concept}的創新應用方式"
        elif "失敗" in event_desc:
            return f"更謹慎的{concept}處理方法"
        else:
            return f"{concept}的新理解維度"
    
    def _find_best_matching_possibility(self, crystal: MemoryCrystal, event: dict) -> Optional[Possibility]:
        """找出最匹配的可能性"""
        if not crystal.possibilities:
            return None
        
        event_text = str(event.get("content", "")) + str(event.get("message", ""))
        
        best_match = None
        best_score = 0
        
        for possibility in crystal.possibilities:
            score = 0
            # 簡單的文本相似度
            for word in possibility.description.split():
                if word in event_text:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = possibility
        
        return best_match
    
    def _find_problematic_possibility(self, crystal: MemoryCrystal, event: dict) -> Optional[Possibility]:
        """找出可能有問題的可能性"""
        # 簡化實現：返回機率最高的（假設它可能是導致問題的）
        return crystal.get_dominant_possibility()
    
    def _is_possibility_relevant(self, possibility: Possibility, event: dict) -> bool:
        """判斷可能性是否與事件相關"""
        event_text = str(event.get("content", "")) + str(event.get("message", ""))
        
        # 簡單的關鍵詞匹配
        for word in possibility.description.split():
            if len(word) > 2 and word in event_text:
                return True
        return False
    
    def _generate_log_from_prompt(self, template: str, crystal: MemoryCrystal, event: dict, possibility: Possibility) -> str:
        """從提示詞生成日誌訊息"""
        return template.format(
            persona=crystal.id.split("_")[0],
            event=event.get("type", "event"),
            concept=crystal.concept,
            possibility=possibility.description
        )
    
    def _calculate_new_stability(self, crystal: MemoryCrystal) -> float:
        """計算新的穩定性"""
        if not crystal.possibilities:
            return 1.0
        
        # 基於熵計算穩定性
        entropy = crystal.calculate_entropy()
        
        # 低熵 = 高穩定性
        stability = 1.0 - (entropy / 3.0)  # 假設最大熵為3
        
        # 考慮最近的共振歷史
        recent_resonances = list(crystal.resonance_history)[-5:]
        if recent_resonances:
            avg_resonance = sum(r["resonance"] for r in recent_resonances) / len(recent_resonances)
            stability *= (1.0 - avg_resonance * 0.3)
        
        return max(0.1, min(1.0, stability))
    
    def _create_ripples(self, memory: QuantumMemory, event: dict, event_type: str) -> List[dict]:
        """創造漣漪效應"""
        pattern = self.ripple_patterns.get(event_type, self.ripple_patterns["routine"])
        
        ripples = []
        
        # 主漣漪
        main_ripple = {
            "origin": event,
            "strength": pattern["spread"],
            "depth": pattern["depth"],
            "decay": pattern["decay"],
            "affected_concepts": []
        }
        
        # 找出會被漣漪影響的概念
        for crystal in memory.crystals.values():
            # 計算距離（簡化為隨機）
            distance = random.random()
            
            if distance < pattern["spread"]:
                impact = pattern["spread"] * (1.0 - distance) * (1.0 - pattern["decay"])
                if impact > 0.1:
                    main_ripple["affected_concepts"].append({
                        "concept": crystal.concept,
                        "impact": impact
                    })
        
        ripples.append(main_ripple)
        
        # 次級漣漪
        if pattern["depth"] > 1:
            for i in range(1, min(pattern["depth"], 3)):
                secondary_ripple = {
                    "origin": main_ripple,
                    "strength": pattern["spread"] * (pattern["decay"] ** i),
                    "depth": pattern["depth"] - i,
                    "affected_concepts": []
                }
                
                # 影響更少的概念
                num_affected = max(1, len(main_ripple["affected_concepts"]) // (i + 1))
                secondary_ripple["affected_concepts"] = random.sample(
                    main_ripple["affected_concepts"], 
                    min(num_affected, len(main_ripple["affected_concepts"]))
                )
                
                ripples.append(secondary_ripple)
        
        return ripples
    
    def _process_entanglements(self, memory: QuantumMemory, event: dict, ripples: List[dict]):
        """處理量子糾纏效應"""
        # 更新與其他角色的糾纏度
        event_source = event.get("source", "")
        
        if "conversation" in event_source:
            # 對話會增加糾纏
            other_persona = event.get("other_persona", "unknown")
            if other_persona in memory.entanglements:
                memory.entanglements[other_persona] += 0.1
            else:
                memory.entanglements[other_persona] = 0.1
        
        # 基於漣漪調整糾纏
        for ripple in ripples:
            if ripple["strength"] > 0.5:
                # 強漣漪會影響糾纏關係
                for concept_data in ripple["affected_concepts"]:
                    # 這裡簡化處理
                    pass
    
    def _should_create_new_crystal(self, event: dict, event_type: str) -> bool:
        """判斷是否應該創建新晶體"""
        # 突破性事件更可能創造新晶體
        if event_type == "breakthrough":
            return random.random() < 0.7
        elif event_type == "insight":
            return random.random() < 0.3
        else:
            return random.random() < 0.1
    
    def _create_new_crystal(self, memory: QuantumMemory, event: dict):
        """創建新的記憶晶體"""
        # 從事件中提取新概念
        new_concept = self._extract_new_concept(event)
        
        if new_concept and new_concept not in [c.concept for c in memory.crystals.values()]:
            # 創建初始可能性
            initial_possibilities = [
                {
                    "description": f"{new_concept}的初始理解",
                    "probability": 0.6
                },
                {
                    "description": f"{new_concept}的潛在意義",
                    "probability": 0.4
                }
            ]
            
            memory.add_crystal(new_concept, initial_possibilities)
            logger.info(f"Created new crystal: {new_concept}")
    
    def _extract_new_concept(self, event: dict) -> Optional[str]:
        """從事件中提取新概念"""
        # 優先從標籤中提取
        if "tags" in event and event["tags"]:
            return event["tags"][0]
        
        # 從內容中提取關鍵詞
        content = str(event.get("content", "")) + str(event.get("message", ""))
        
        # 簡單提取：找最長的詞
        words = content.split()
        if words:
            longest = max(words, key=len)
            if len(longest) > 3:
                return longest
        
        return None
    
    def _adjust_identity_field(self, memory: QuantumMemory, event_type: str):
        """調整身份場參數"""
        # 根據事件類型調整
        if event_type == "breakthrough":
            # 突破會增加振幅
            memory.identity.amplitude = min(1.0, memory.identity.amplitude * 1.1)
            # 相位快速變化
            memory.identity.phase = (memory.identity.phase + 0.2) % 1.0
        
        elif event_type == "insight":
            # 洞察會提高一致性
            memory.identity.coherence = min(1.0, memory.identity.coherence * 1.05)
            # 相位緩慢推進
            memory.identity.phase = (memory.identity.phase + 0.05) % 1.0
        
        elif event_type == "failure":
            # 失敗會降低一致性
            memory.identity.coherence = max(0.3, memory.identity.coherence * 0.95)
            # 頻率可能降低
            memory.identity.frequency = max(0.1, memory.identity.frequency * 0.98)
        
        # 常規化調整
        memory.identity.frequency = max(0.1, min(1.0, memory.identity.frequency))
        memory.identity.amplitude = max(0.1, min(1.0, memory.identity.amplitude))
        memory.identity.coherence = max(0.1, min(1.0, memory.identity.coherence))