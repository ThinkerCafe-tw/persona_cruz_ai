"""
量子記憶系統與 LINE Bot 整合
"""
import logging
from typing import Optional, Dict, Any
from quantum_memory import QuantumMemoryBridge, QuantumMonitor
from five_elements_agent import FiveElementsAgent

logger = logging.getLogger(__name__)


class QuantumIntegration:
    """整合量子記憶到現有系統"""
    
    def __init__(self):
        # 強制使用資料庫模式
        self.bridge = QuantumMemoryBridge(use_database=True)
        self.monitor = QuantumMonitor(self.bridge)
        self.five_elements = None  # 將在需要時初始化
        
    def initialize_with_five_elements(self, five_elements: FiveElementsAgent):
        """與五行系統整合"""
        self.five_elements = five_elements
        logger.info("Quantum memory integrated with Five Elements system")
        
    def process_conversation(self, user_id: str, message: str, response: str, 
                           current_role: str = "unknown", emotion: str = "neutral"):
        """處理對話並更新量子記憶"""
        # 創建對話事件
        conversation_event = {
            "type": "conversation",
            "message": message,
            "response": response,
            "user_id": user_id,
            "emotion": emotion,
            "role": current_role,
            "other_persona": current_role if current_role != "unknown" else None
        }
        
        # 同步到量子記憶
        self.bridge.sync_from_legacy("conversation", conversation_event)
        
        # 如果是特殊內容，可能觸發額外演化
        self._check_special_content(message, response, current_role)
        
    def _check_special_content(self, message: str, response: str, role: str):
        """檢查是否有特殊內容需要額外處理"""
        content = message + " " + response
        
        # 檢查是否包含洞察性內容
        insight_keywords = ["原來", "發現", "理解", "明白", "洞察", "學到"]
        if any(keyword in content for keyword in insight_keywords):
            insight_event = {
                "type": "insight",
                "content": content,
                "source": f"conversation_{role}",
                "tags": [role, "對話洞察"]
            }
            
            # 主要影響當前角色
            role_mapping = {
                "木": "wood",
                "火": "fire",
                "土": "earth",
                "金": "metal",
                "水": "water",
                "無極": "wuji",
                "CRUZ": "cruz"
            }
            
            persona_id = role_mapping.get(role, "wuji")
            self.bridge.trigger_evolution(persona_id, insight_event)
        
    def get_quantum_status(self) -> str:
        """獲取量子記憶狀態（用於 /quantum 指令）"""
        return self.monitor.get_system_overview()
        
    def get_persona_quantum_report(self, persona_name: str) -> str:
        """獲取特定角色的量子報告"""
        # 角色名稱映射
        name_to_id = {
            "木": "wood",
            "火": "fire", 
            "土": "earth",
            "金": "metal",
            "水": "water",
            "無極": "wuji",
            "CRUZ": "cruz",
            "wood": "wood",
            "fire": "fire",
            "earth": "earth",
            "metal": "metal",
            "water": "water",
            "wuji": "wuji",
            "cruz": "cruz"
        }
        
        persona_id = name_to_id.get(persona_name.lower(), persona_name.lower())
        return self.monitor.get_detailed_persona_report(persona_id)
        
    def sync_development_lesson(self, lesson: str, context: str, severity: str = "medium"):
        """同步開發教訓到量子記憶"""
        lesson_event = {
            "type": "development_lesson",
            "lesson": lesson,
            "context": context,
            "severity": severity,
            "tags": ["開發經驗", severity]
        }
        
        self.bridge.sync_from_legacy("development_lesson", lesson_event)
        
    def sync_cruz_corpus(self, content: str, tags: list, context: str = ""):
        """同步CRUZ語料到量子記憶"""
        corpus_event = {
            "type": "corpus_update",
            "content": content,
            "tags": tags,
            "context": context
        }
        
        self.bridge.sync_from_legacy("cruz_corpus", corpus_event)
        
    def get_quantum_suggestions(self, current_context: str) -> list:
        """基於量子記憶獲取建議"""
        suggestions = []
        
        # 分析當前上下文
        keywords = current_context.split()[:5]  # 簡單取前5個詞
        
        # 查找各角色的共振晶體
        for persona_id, memory in self.bridge.quantum_memories.items():
            resonating_crystals = memory.find_resonating_crystals(keywords, threshold=0.2)
            
            for crystal in resonating_crystals[:2]:  # 每個角色最多2個建議
                dominant = crystal.get_dominant_possibility()
                if dominant:
                    suggestions.append({
                        "source": memory.identity.essence,
                        "concept": crystal.concept,
                        "suggestion": dominant.description,
                        "confidence": dominant.probability
                    })
        
        # 按信心度排序
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        
        return suggestions[:5]  # 返回前5個建議
        
    def trigger_breakthrough(self, description: str, impact: str = "high"):
        """觸發突破性事件"""
        breakthrough_event = {
            "type": "breakthrough",
            "content": description,
            "impact": impact,
            "tags": ["突破", "創新"]
        }
        
        # 突破事件影響所有角色
        for persona_id in self.bridge.quantum_memories:
            self.bridge.trigger_evolution(persona_id, breakthrough_event)
            
    def save_all_memories(self):
        """保存所有量子記憶"""
        for memory in self.bridge.quantum_memories.values():
            memory.save()
        logger.info("All quantum memories saved")
        
    def get_entanglement_status(self) -> str:
        """獲取量子糾纏狀態"""
        matrix = self.bridge.get_entanglement_matrix()
        
        status = "🔗 量子糾纏狀態\n"
        status += "─" * 30 + "\n"
        
        # 找出最強的糾纏關係
        strong_entanglements = []
        
        for p1, connections in matrix.items():
            for p2, strength in connections.items():
                if p1 != p2 and strength > 0.5:
                    # 避免重複（A-B 和 B-A）
                    pair = tuple(sorted([p1, p2]))
                    strong_entanglements.append((pair, strength))
        
        # 去重並排序
        unique_entanglements = {}
        for pair, strength in strong_entanglements:
            if pair not in unique_entanglements or strength > unique_entanglements[pair]:
                unique_entanglements[pair] = strength
        
        sorted_entanglements = sorted(unique_entanglements.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_entanglements:
            for (p1, p2), strength in sorted_entanglements[:5]:
                name1 = self.bridge.quantum_memories[p1].identity.essence
                name2 = self.bridge.quantum_memories[p2].identity.essence
                status += f"{name1} ←→ {name2}: {strength:.1%}\n"
        else:
            status += "（尚無強糾纏關係）\n"
            
        return status
        
    def get_evolution_insights(self) -> str:
        """獲取演化洞察"""
        insights = "💡 量子演化洞察\n"
        insights += "─" * 30 + "\n"
        
        # 收集最近的重要演化
        important_evolutions = []
        
        for persona_id, memory in self.bridge.quantum_memories.items():
            # 檢查最近的漣漪
            recent_ripples = list(memory.ripples)[-5:]
            for ripple in recent_ripples:
                if ripple["impact"] > 0.7:
                    important_evolutions.append({
                        "persona": memory.identity.essence,
                        "event": ripple["event"],
                        "impact": ripple["impact"],
                        "timestamp": ripple["timestamp"]
                    })
        
        # 按影響力排序
        important_evolutions.sort(key=lambda x: x["impact"], reverse=True)
        
        if important_evolutions:
            for evo in important_evolutions[:5]:
                event_type = evo["event"].get("type", "unknown")
                insights += f"• {evo['persona']}: {event_type} (影響力 {evo['impact']:.1f})\n"
        else:
            insights += "（暫無重要演化事件）\n"
            
        return insights


# 全局實例
quantum_integration = QuantumIntegration()