"""
情緒狀態引擎 - Day 4
管理 CRUZ 的情緒狀態和轉換
"""
from enum import Enum
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import random

class EmotionState(Enum):
    """情緒狀態枚舉"""
    DETERMINED = "determined"      # 決心（預設）
    ENERGIZED = "energized"       # 充滿活力
    FRUSTRATED = "frustrated"     # 挫折
    INTENSE = "intense"          # 強烈
    INTRIGUED = "intrigued"      # 好奇
    CAUTIOUS = "cautious"        # 謹慎

class EmotionTrigger(Enum):
    """情緒觸發器"""
    SUCCESS = "success"           # 成功完成
    FAILURE = "failure"          # 失敗
    CHALLENGE = "challenge"      # 挑戰
    DELAY = "delay"             # 延遲
    DISCOVERY = "discovery"      # 發現
    UNCERTAINTY = "uncertainty"  # 不確定

class EmotionEngine:
    """CRUZ 情緒引擎"""
    
    def __init__(self):
        self.current_state = EmotionState.DETERMINED
        self.intensity = 0.7  # 0-1 情緒強度
        self.stability = 0.8  # 0-1 情緒穩定性
        self.last_change = datetime.now()
        self.history = []
        
        # 狀態轉換矩陣
        self.transitions = {
            (EmotionState.DETERMINED, EmotionTrigger.SUCCESS): EmotionState.ENERGIZED,
            (EmotionState.DETERMINED, EmotionTrigger.FAILURE): EmotionState.FRUSTRATED,
            (EmotionState.DETERMINED, EmotionTrigger.CHALLENGE): EmotionState.INTENSE,
            (EmotionState.ENERGIZED, EmotionTrigger.DELAY): EmotionState.FRUSTRATED,
            (EmotionState.FRUSTRATED, EmotionTrigger.SUCCESS): EmotionState.DETERMINED,
            (EmotionState.INTENSE, EmotionTrigger.SUCCESS): EmotionState.ENERGIZED,
            (EmotionState.INTRIGUED, EmotionTrigger.DISCOVERY): EmotionState.ENERGIZED,
            (EmotionState.CAUTIOUS, EmotionTrigger.SUCCESS): EmotionState.DETERMINED,
        }
        
        # 情緒對應的行為調整
        self.behavior_modifiers = {
            EmotionState.DETERMINED: {
                "response_speed": 1.0,
                "confidence": 0.9,
                "directness": 0.9
            },
            EmotionState.ENERGIZED: {
                "response_speed": 1.2,
                "confidence": 0.95,
                "directness": 0.95
            },
            EmotionState.FRUSTRATED: {
                "response_speed": 0.8,
                "confidence": 0.7,
                "directness": 1.0  # 更直接
            },
            EmotionState.INTENSE: {
                "response_speed": 1.1,
                "confidence": 0.85,
                "directness": 0.95
            },
            EmotionState.INTRIGUED: {
                "response_speed": 0.9,
                "confidence": 0.8,
                "directness": 0.7
            },
            EmotionState.CAUTIOUS: {
                "response_speed": 0.7,
                "confidence": 0.6,
                "directness": 0.6
            }
        }
    
    def process_trigger(self, trigger: EmotionTrigger, context: Optional[Dict] = None) -> EmotionState:
        """處理情緒觸發器"""
        old_state = self.current_state
        
        # 檢查是否有定義的轉換
        transition_key = (self.current_state, trigger)
        if transition_key in self.transitions:
            new_state = self.transitions[transition_key]
            
            # 考慮穩定性（高穩定性 = 不易改變）
            if random.random() > self.stability:
                self.current_state = new_state
                self.intensity = min(1.0, self.intensity + 0.1)
            else:
                # 保持當前狀態但調整強度
                self.intensity = max(0.3, self.intensity - 0.05)
        
        # 記錄歷史
        self.history.append({
            "timestamp": datetime.now(),
            "trigger": trigger,
            "old_state": old_state,
            "new_state": self.current_state,
            "intensity": self.intensity,
            "context": context
        })
        
        # 自然衰減（回歸預設狀態）
        self._natural_decay()
        
        return self.current_state
    
    def _natural_decay(self):
        """情緒自然衰減"""
        time_since_change = datetime.now() - self.last_change
        
        # 每小時衰減 10% 強度
        if time_since_change > timedelta(hours=1):
            self.intensity = max(0.3, self.intensity - 0.1)
            
            # 低強度時回歸預設狀態
            if self.intensity < 0.4 and self.current_state != EmotionState.DETERMINED:
                self.current_state = EmotionState.DETERMINED
                self.intensity = 0.7
    
    def get_behavior_modifiers(self) -> Dict[str, float]:
        """獲取當前情緒的行為調整參數"""
        return self.behavior_modifiers[self.current_state]
    
    def get_emotional_prefix(self) -> str:
        """獲取情緒前綴"""
        prefixes = {
            EmotionState.DETERMINED: "💪",
            EmotionState.ENERGIZED: "⚡",
            EmotionState.FRUSTRATED: "😤",
            EmotionState.INTENSE: "🔥",
            EmotionState.INTRIGUED: "🤔",
            EmotionState.CAUTIOUS: "🤨"
        }
        
        # 根據強度調整
        if self.intensity > 0.8:
            return f"{prefixes[self.current_state]} [強烈]"
        elif self.intensity < 0.4:
            return f"{prefixes[self.current_state]} [微弱]"
        else:
            return prefixes[self.current_state]
    
    def analyze_text_emotion(self, text: str) -> EmotionTrigger:
        """分析文本以決定情緒觸發器"""
        text_lower = text.lower()
        
        # 簡單的關鍵詞匹配
        if any(word in text_lower for word in ["成功", "完成", "做到", "贏", "victory"]):
            return EmotionTrigger.SUCCESS
        elif any(word in text_lower for word in ["失敗", "錯誤", "不行", "輸", "failure"]):
            return EmotionTrigger.FAILURE
        elif any(word in text_lower for word in ["挑戰", "困難", "艱難", "challenge"]):
            return EmotionTrigger.CHALLENGE
        elif any(word in text_lower for word in ["等待", "延遲", "慢", "delay"]):
            return EmotionTrigger.DELAY
        elif any(word in text_lower for word in ["發現", "新", "有趣", "discovery"]):
            return EmotionTrigger.DISCOVERY
        elif any(word in text_lower for word in ["不確定", "也許", "可能", "uncertain"]):
            return EmotionTrigger.UNCERTAINTY
        
        return None
    
    def get_status(self) -> Dict:
        """獲取情緒狀態摘要"""
        return {
            "current_state": self.current_state.value,
            "intensity": round(self.intensity, 2),
            "stability": round(self.stability, 2),
            "emotional_prefix": self.get_emotional_prefix(),
            "behavior_modifiers": self.get_behavior_modifiers(),
            "time_in_state": str(datetime.now() - self.last_change),
            "recent_triggers": [h["trigger"].value for h in self.history[-5:]]
        }

# 全局情緒引擎實例
cruz_emotion = EmotionEngine()