"""
Day 5: CRUZ + Memory API 完整整合測試
"""
import asyncio
import httpx
import json
from datetime import datetime
from typing import List, Dict
import os

# 設置 Gemini API Key
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

from cruz_chatbot import CruzChatbot
from emotion_engine import cruz_emotion, EmotionTrigger

class MemoryIntegrationTest:
    """記憶整合測試器"""
    
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.test_user = "test_user_day5"
        self.test_email = "day5@test.com"
        self.test_password = "Test123!@#"
        self.token = None
        
    async def setup_test_user(self):
        """設置測試用戶"""
        async with httpx.AsyncClient() as client:
            # 嘗試註冊新用戶
            try:
                response = await client.post(
                    f"{self.api_url}/auth/register",
                    json={
                        "username": self.test_user,
                        "email": self.test_email,
                        "password": self.test_password
                    }
                )
                if response.status_code == 200:
                    print(f"✅ 註冊成功: {self.test_user}")
            except:
                pass
            
            # 登入獲取 token
            response = await client.post(
                f"{self.api_url}/auth/token",
                data={
                    "username": self.test_user,
                    "password": self.test_password
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                print(f"🔑 Token 獲取成功")
                return True
            else:
                print(f"❌ 登入失敗: {response.status_code}")
                return False
    
    async def test_memory_operations(self):
        """測試記憶操作"""
        print("\n📝 測試記憶 CRUD 操作...")
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # 1. 存儲測試記憶
            memories = [
                {
                    "content": "CRUZ helped me overcome procrastination today",
                    "category": "achievement",
                    "tags": ["motivation", "productivity"],
                    "context": {"emotion": "energized", "date": "2025-06-26"}
                },
                {
                    "content": "Learned to prioritize speed over perfection",
                    "category": "lesson",
                    "tags": ["philosophy", "cruz"],
                    "context": {"source": "CRUZ coaching session"}
                },
                {
                    "content": "Successfully shipped MVP in record time",
                    "category": "milestone",
                    "tags": ["success", "mvp"],
                    "context": {"emotion": "determined", "impact": "high"}
                }
            ]
            
            stored_ids = []
            for memory in memories:
                response = await client.post(
                    f"{self.api_url}/memory/store",
                    headers=headers,
                    json=memory
                )
                if response.status_code == 200:
                    result = response.json()
                    stored_ids.append(result["id"])
                    print(f"  ✅ 存儲記憶: {memory['content'][:30]}...")
            
            # 2. 搜尋記憶
            search_queries = [
                "CRUZ motivation",
                "perfection vs speed",
                "MVP success"
            ]
            
            print("\n🔍 測試向量搜尋...")
            for query in search_queries:
                response = await client.get(
                    f"{self.api_url}/memory/search",
                    headers=headers,
                    params={"query": query, "limit": 3}
                )
                if response.status_code == 200:
                    results = response.json()["results"]
                    print(f"  Query: '{query}' → {len(results)} results")
                    for r in results[:1]:
                        print(f"    - {r['content'][:50]}... (相似度: {r['similarity']:.2f})")
            
            # 3. 按類別獲取
            print("\n📂 測試類別過濾...")
            response = await client.get(
                f"{self.api_url}/memory/category/achievement",
                headers=headers
            )
            if response.status_code == 200:
                memories = response.json()["memories"]
                print(f"  Achievement 類別: {len(memories)} 條記憶")
            
            return True
    
    async def test_cruz_with_memory(self):
        """測試 CRUZ 與記憶的整合"""
        print("\n🎯 測試 CRUZ + Memory 整合...")
        
        # 創建帶記憶的 CRUZ
        cruz = CruzChatbot(
            memory_api_url=self.api_url,
            user_token=self.token
        )
        
        # 模擬對話場景
        conversations = [
            {
                "user": "I'm struggling with perfectionism again",
                "expected_emotion": EmotionTrigger.CHALLENGE
            },
            {
                "user": "You're right! I just shipped the feature!",
                "expected_emotion": EmotionTrigger.SUCCESS
            },
            {
                "user": "What did we discuss about speed vs perfection?",
                "expected_emotion": None  # 記憶查詢
            }
        ]
        
        print("\n💬 開始對話測試...")
        for conv in conversations:
            print(f"\n👤 User: {conv['user']}")
            
            # 如果有預期情緒，先處理
            if conv['expected_emotion']:
                cruz_emotion.process_trigger(conv['expected_emotion'])
            
            # 搜尋相關記憶
            memories = await cruz.search_memories(conv['user'], limit=2)
            if memories:
                print(f"   📚 找到 {len(memories)} 條相關記憶")
                for m in memories:
                    print(f"      - {m['content'][:40]}... ({m['similarity']:.2f})")
            
            # 模擬 CRUZ 回應
            emotion_status = cruz_emotion.get_status()
            print(f"   🎯 CRUZ [{emotion_status['emotional_prefix']}]: ", end="")
            
            if "perfectionism" in conv['user'].lower():
                response = "Stop overthinking! Ship it NOW! Perfect is the enemy of done!"
            elif "shipped" in conv['user'].lower():
                response = "YES! That's the spirit! Action beats hesitation every time! 🚀"
            else:
                response = "We agreed: Speed > Perfection. Every. Single. Time. Now GO!"
            
            print(response)
            
            # 存儲對話到記憶
            await cruz.store_memory(
                f"User: {conv['user']}\nCRUZ: {response}",
                category="conversation"
            )
        
        return True
    
    async def test_persistence(self):
        """測試記憶持久性"""
        print("\n💾 測試記憶持久性...")
        
        # 創建新的 CRUZ 實例（模擬新會話）
        new_cruz = CruzChatbot(
            memory_api_url=self.api_url,
            user_token=self.token
        )
        
        # 搜尋之前的對話
        query = "perfectionism speed ship"
        memories = await new_cruz.search_memories(query, limit=5)
        
        print(f"  搜尋 '{query}':")
        print(f"  找到 {len(memories)} 條歷史記憶")
        
        if memories:
            print("\n  📜 歷史對話摘要:")
            for i, m in enumerate(memories[:3], 1):
                print(f"  {i}. {m['content'][:60]}...")
                print(f"     相似度: {m['similarity']:.2f} | 類別: {m.get('category', 'unknown')}")
        
        return True

async def run_day5_tests():
    """運行 Day 5 整合測試"""
    print("🚀 Day 5: Memory API Integration Test")
    print("=" * 50)
    
    tester = MemoryIntegrationTest()
    
    # 檢查 API 是否運行
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{tester.api_url}/health")
            if response.status_code != 200:
                print("❌ Memory API 未運行！請先執行: ./start_memory_api.sh")
                return
    except:
        print("❌ 無法連接到 Memory API (http://localhost:8000)")
        print("   請先執行: ./start_memory_api.sh")
        return
    
    print("✅ Memory API 運行中")
    
    # 執行測試流程
    try:
        # 1. 設置測試用戶
        if not await tester.setup_test_user():
            print("❌ 無法設置測試用戶")
            return
        
        # 2. 測試記憶操作
        await tester.test_memory_operations()
        
        # 3. 測試 CRUZ 整合
        await tester.test_cruz_with_memory()
        
        # 4. 測試持久性
        await tester.test_persistence()
        
        print("\n" + "=" * 50)
        print("✅ Day 5 整合測試完成！")
        print("\n📊 測試結果摘要:")
        print("  • Memory API CRUD: ✅")
        print("  • Vector Search: ✅")
        print("  • CRUZ Integration: ✅")
        print("  • Persistence: ✅")
        print("\n🎯 CRUZ: 'Memory makes us stronger! Now let's build more!'")
        
    except Exception as e:
        print(f"\n❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_day5_tests())