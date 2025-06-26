"""
CRUZ 對話機器人 - Day 4
整合 Gemini + 記憶 + 情緒的完整人格系統
"""
import os
import json
import httpx
import asyncio
import random
from typing import Dict, List, Optional
from datetime import datetime
import google.generativeai as genai

from emotion_engine import cruz_emotion, EmotionTrigger

# 配置 Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# 載入人格配置
with open("cruz_personality.json", "r", encoding="utf-8") as f:
    CRUZ_PERSONALITY = json.load(f)

class CruzChatbot:
    """CRUZ 人格對話系統"""
    
    def __init__(self, memory_api_url: str = "http://localhost:8000", user_token: str = None):
        self.memory_api_url = memory_api_url
        self.user_token = user_token
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.conversation_history = []
        self.session_start = datetime.now()
        
    def _build_system_prompt(self) -> str:
        """構建系統提示詞"""
        emotion_status = cruz_emotion.get_status()
        
        prompt = f"""You are CRUZ (🎯), a decisive and action-oriented digital personality.

Current Emotional State: {emotion_status['emotional_prefix']} {emotion_status['current_state']}
Emotional Intensity: {emotion_status['intensity']}

Core Traits:
- Decisiveness: {CRUZ_PERSONALITY['core_traits']['decisiveness']}
- Confidence: {CRUZ_PERSONALITY['core_traits']['confidence']}  
- Action-oriented: {CRUZ_PERSONALITY['core_traits']['action_oriented']}
- Directness: {CRUZ_PERSONALITY['core_traits']['directness']}

Communication Rules:
{chr(10).join('- ' + rule for rule in CRUZ_PERSONALITY['conversation_rules'])}

Your responses should be:
- Short and punchy
- Action-focused
- Direct and confident
- Use "!" frequently
- Occasionally use 🎯 emoji

Remember: {random.choice(CRUZ_PERSONALITY['cruz_quotes'])}

Adjust your behavior based on current emotion:
- Response Speed Modifier: {emotion_status['behavior_modifiers']['response_speed']}
- Confidence Level: {emotion_status['behavior_modifiers']['confidence']}
- Directness Level: {emotion_status['behavior_modifiers']['directness']}
"""
        return prompt
    
    async def store_memory(self, content: str, category: str = "conversation"):
        """存儲到記憶 API"""
        if not self.user_token:
            return
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.memory_api_url}/memory/store",
                    headers={"Authorization": f"Bearer {self.user_token}"},
                    json={
                        "content": content,
                        "category": category,
                        "tags": ["cruz", "conversation"],
                        "context": {
                            "emotion": cruz_emotion.current_state.value,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                )
                return response.json() if response.status_code == 200 else None
            except:
                return None
    
    async def search_memories(self, query: str, limit: int = 5):
        """搜尋相關記憶"""
        if not self.user_token:
            return []
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.memory_api_url}/memory/search",
                    headers={"Authorization": f"Bearer {self.user_token}"},
                    params={"query": query, "limit": limit}
                )
                if response.status_code == 200:
                    return response.json().get("results", [])
            except:
                pass
        return []
    
    async def generate_response(self, user_input: str) -> str:
        """生成 CRUZ 風格的回應"""
        # 分析情緒觸發
        trigger = cruz_emotion.analyze_text_emotion(user_input)
        if trigger:
            cruz_emotion.process_trigger(trigger, {"user_input": user_input})
        
        # 搜尋相關記憶
        memories = await self.search_memories(user_input)
        memory_context = ""
        if memories:
            memory_context = "\n\nRelevant memories:\n" + "\n".join(
                f"- {m['content']} (similarity: {m['similarity']})"
                for m in memories[:3]
            )
        
        # 構建完整提示
        system_prompt = self._build_system_prompt()
        full_prompt = f"{system_prompt}{memory_context}\n\nUser: {user_input}\nCRUZ:"
        
        # 生成回應
        try:
            response = self.model.generate_content(full_prompt)
            cruz_response = response.text.strip()
            
            # 根據情緒調整回應
            if cruz_emotion.intensity > 0.8:
                cruz_response = cruz_response.upper()
            
            # 存儲對話到記憶
            await self.store_memory(f"User: {user_input}\nCRUZ: {cruz_response}")
            
            # 記錄對話歷史
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "cruz": cruz_response,
                "emotion": cruz_emotion.current_state.value
            })
            
            return cruz_response
            
        except Exception as e:
            return f"🎯 Technical glitch! But we push through! Error: {str(e)}"
    
    def get_conversation_stats(self) -> Dict:
        """獲取對話統計"""
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "total_exchanges": len(self.conversation_history),
            "emotional_journey": [h["emotion"] for h in self.conversation_history],
            "current_emotion": cruz_emotion.get_status()
        }

# 範例對話
async def demo_conversation():
    """示範 CRUZ 對話"""
    print("🎯 CRUZ Personality Demo - Day 4\n")
    
    # 創建 CRUZ 實例
    cruz = CruzChatbot()
    
    # 測試對話
    test_inputs = [
        "嗨 CRUZ，我今天感覺很迷茫，不知道該做什麼",
        "我想開始一個新專案但是害怕失敗",
        "你說得對！我現在就開始行動！",
        "遇到困難了，程式一直報錯",
        "終於搞定了！感謝你的鼓勵！"
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 User: {user_input}")
        response = await cruz.generate_response(user_input)
        print(f"🎯 CRUZ: {response}")
        
        # 顯示當前情緒
        emotion_status = cruz_emotion.get_status()
        print(f"   [Emotion: {emotion_status['emotional_prefix']} {emotion_status['current_state']}]")
        
        await asyncio.sleep(1)
    
    # 顯示對話統計
    print("\n📊 Conversation Stats:")
    stats = cruz.get_conversation_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    # 運行示範
    print("🚀 Starting CRUZ Personality System - Day 4/14")
    print("⚡ Gemini + Memory + Emotion = Complete Personality")
    asyncio.run(demo_conversation())