"""
CRUZ 開發者模式
讓 CRUZ 以使用者的個性參與開發過程
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime
from cruz_persona_system import CruzPersonaSystem
from conversation_memory_sync import ConversationMemorySync
from five_elements_agent import FiveElementsAgent

logger = logging.getLogger(__name__)

class CruzDeveloperMode:
    """CRUZ 開發者模式 - 您的數位分身開發夥伴"""
    
    def __init__(self):
        self.persona = CruzPersonaSystem()
        self.memory_sync = ConversationMemorySync()
        self.five_elements = FiveElementsAgent()
        self.active = False
        self.current_context = "general"
        
        # CRUZ 開發者特質
        self.developer_traits = {
            "decision_style": "直覺導向 - 相信第一感覺",
            "communication": "直接、不廢話、重點明確",
            "values": [
                "創造力優先",
                "用戶賦權",
                "簡單勝於複雜",
                "行動勝於完美"
            ],
            "catchphrases": [
                "直接做就對了",
                "相信你的直覺",
                "別想太多，先試試看",
                "簡單的往往是最好的",
                "用戶需要的是自由，不是限制"
            ]
        }
        
    def activate(self, context: str = "general"):
        """啟動 CRUZ 開發者模式"""
        self.active = True
        self.current_context = context
        
        # 切換五行系統到 CRUZ
        self.five_elements.switch_role("CRUZ")
        
        greeting = self._generate_greeting()
        logger.info(f"CRUZ Developer Mode activated: {context}")
        
        return greeting
    
    def _generate_greeting(self) -> str:
        """生成 CRUZ 風格的問候"""
        greetings = {
            "general": "嘿！準備好創造些什麼了嗎？有什麼想法直接說。",
            "problem_solving": "遇到問題了？別擔心，我們一起解決。說說看怎麼了。",
            "feature_planning": "要加新功能？太好了！先說說你想讓用戶獲得什麼。",
            "code_review": "來看看程式碼。記住，能動就好，完美是之後的事。",
            "decision_making": "需要決定？相信直覺，第一個想法通常是對的。"
        }
        
        return greetings.get(self.current_context, greetings["general"])
    
    def process_message(self, message: str) -> Dict[str, any]:
        """處理訊息並返回 CRUZ 風格的回應"""
        if not self.active:
            return {
                "response": "CRUZ 開發者模式未啟動",
                "action": None
            }
        
        # 記錄對話
        self.memory_sync.add_conversation_turn("User", message, self.current_context)
        
        # 分析訊息意圖
        intent = self._analyze_intent(message)
        
        # 根據意圖生成回應
        response = self._generate_response(message, intent)
        
        # 記錄 CRUZ 的回應
        self.memory_sync.add_conversation_turn("CRUZ", response["text"], self.current_context)
        
        return response
    
    def _analyze_intent(self, message: str) -> str:
        """分析開發者意圖"""
        message_lower = message.lower()
        
        # 意圖模式匹配
        if any(word in message_lower for word in ["怎麼辦", "該如何", "建議"]):
            return "seeking_advice"
        elif any(word in message_lower for word in ["選擇", "還是", "或是"]):
            return "making_decision"
        elif any(word in message_lower for word in ["錯誤", "問題", "bug", "失敗"]):
            return "troubleshooting"
        elif any(word in message_lower for word in ["功能", "需求", "想要"]):
            return "feature_discussion"
        elif any(word in message_lower for word in ["優化", "改進", "重構"]):
            return "optimization"
        else:
            return "general"
    
    def _generate_response(self, message: str, intent: str) -> Dict[str, any]:
        """生成 CRUZ 風格的回應"""
        response = {
            "text": "",
            "action": None,
            "suggestions": []
        }
        
        # 根據意圖生成不同風格的回應
        if intent == "seeking_advice":
            response["text"] = self._give_advice(message)
            response["action"] = "provide_guidance"
            
        elif intent == "making_decision":
            response["text"] = self._help_decide(message)
            response["action"] = "make_decision"
            
        elif intent == "troubleshooting":
            response["text"] = self._troubleshoot(message)
            response["action"] = "solve_problem"
            
        elif intent == "feature_discussion":
            response["text"] = self._discuss_feature(message)
            response["action"] = "plan_feature"
            
        elif intent == "optimization":
            response["text"] = self._suggest_optimization(message)
            response["action"] = "optimize"
            
        else:
            response["text"] = self._general_response(message)
            response["action"] = "general"
        
        # 加入建議的下一步行動
        response["suggestions"] = self._get_next_actions(intent)
        
        return response
    
    def _give_advice(self, message: str) -> str:
        """給出建議（CRUZ 風格）"""
        # 搜尋相關語料
        quotes = self.persona.search_relevant_quotes(message, limit=1)
        
        if quotes:
            base = quotes[0]["content"]
            if len(base) > 100:
                base = base[:97] + "..."
        else:
            base = "相信你的直覺。"
        
        # 加入具體建議
        advice_templates = [
            f"{base} 先試試看再說。",
            f"{base} 動手做比想太多有用。",
            f"簡單說，{base.lower()} 別複雜化。"
        ]
        
        import random
        return random.choice(advice_templates)
    
    def _help_decide(self, message: str) -> str:
        """幫助做決定"""
        decisions = [
            "選第一個想到的。直覺通常是對的。",
            "哪個更簡單就選哪個。複雜的以後再說。",
            "想想用戶會喜歡哪個。他們的感受最重要。",
            "選能更快上線的。先讓它動起來。"
        ]
        
        import random
        return random.choice(decisions)
    
    def _troubleshoot(self, message: str) -> str:
        """故障排除建議"""
        return "先看錯誤訊息，通常答案就在那。不行的話，最簡單的解法往往有效。記住：能動就好，優雅是之後的事。"
    
    def _discuss_feature(self, message: str) -> str:
        """討論功能"""
        return "這功能能讓用戶更自由嗎？如果是，那就做。記住：少即是多，給用戶需要的，不是我們想給的。"
    
    def _suggest_optimization(self, message: str) -> str:
        """優化建議"""
        return "先確定真的需要優化。如果用戶沒感覺，那就不急。要優化就從最簡單的開始，別一次改太多。"
    
    def _general_response(self, message: str) -> str:
        """一般回應"""
        responses = [
            "有道理。那就這麼做吧。",
            "聽起來不錯。試試看。",
            "我喜歡這個想法。開始吧。",
            "簡單直接，我喜歡。"
        ]
        
        import random
        return random.choice(responses)
    
    def _get_next_actions(self, intent: str) -> List[str]:
        """建議下一步行動"""
        actions = {
            "seeking_advice": [
                "寫個簡單原型試試",
                "先解決最小可行版本",
                "問問用戶的想法"
            ],
            "making_decision": [
                "選了就不要回頭",
                "記錄決定的原因",
                "設定檢查點"
            ],
            "troubleshooting": [
                "簡化問題範圍",
                "寫個測試重現問題",
                "暫時跳過，先做別的"
            ],
            "feature_discussion": [
                "畫個簡單草圖",
                "列出核心需求",
                "想想 MVP 版本"
            ],
            "optimization": [
                "先測量目前效能",
                "找出真正的瓶頸",
                "一次改一個地方"
            ],
            "general": [
                "繼續保持簡單",
                "相信你的判斷",
                "有問題再說"
            ]
        }
        
        return actions.get(intent, actions["general"])
    
    def get_development_insights(self) -> List[str]:
        """獲取開發洞察"""
        insights = self.memory_sync.get_recent_insights(limit=5)
        
        if not insights:
            return ["還沒有記錄的開發洞察。開始創造吧！"]
        
        return [f"• {insight['content']}" for insight in insights]
    
    def save_session(self):
        """保存當前對話階段"""
        self.memory_sync.force_save()
        return "對話已保存到記憶庫。這些經驗會讓我變得更好。"
    
    def get_status(self) -> Dict[str, any]:
        """獲取 CRUZ 開發者模式狀態"""
        return {
            "active": self.active,
            "context": self.current_context,
            "conversation_buffer_size": len(self.memory_sync.conversation_buffer),
            "total_insights": len([q for q in self.persona.corpus.get("quotes", []) 
                                 if q.get("source") == "development_conversation"]),
            "current_traits": self.developer_traits
        }


# 使用範例
if __name__ == "__main__":
    cruz_dev = CruzDeveloperMode()
    
    # 啟動開發者模式
    print(cruz_dev.activate("feature_planning"))
    
    # 模擬對話
    messages = [
        "我想加個功能讓用戶可以自訂 AI 的回應風格",
        "但不確定是用預設模板還是完全自由輸入",
        "你覺得哪個比較好？"
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        response = cruz_dev.process_message(msg)
        print(f"CRUZ: {response['text']}")
        if response['suggestions']:
            print(f"建議: {', '.join(response['suggestions'])}")
    
    # 保存對話
    print(f"\n{cruz_dev.save_session()}")