"""
測試 CRUZ 人格與記憶 API 整合
"""
import asyncio
import os
from cruz_chatbot import CruzChatbot

async def test_integration():
    """測試整合流程"""
    print("🎯 CRUZ + Memory API Integration Test\n")
    
    # 模擬用戶 token (實際應從登入獲得)
    mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIifQ.test"
    
    # 創建 CRUZ 實例
    cruz = CruzChatbot(
        memory_api_url="http://localhost:8000",
        user_token=mock_token
    )
    
    print("📝 Simulating conversations...")
    
    # 模擬對話
    conversations = [
        "Hey CRUZ, I need to build a new feature quickly",
        "Should I focus on perfection or speed?",
        "I'm feeling stuck with the implementation"
    ]
    
    for i, user_input in enumerate(conversations, 1):
        print(f"\n[{i}] User: {user_input}")
        
        # 顯示當前情緒
        from emotion_engine import cruz_emotion
        emotion_status = cruz_emotion.get_status()
        print(f"    [Emotion: {emotion_status['current_state']} - Intensity: {emotion_status['intensity']}]")
        
        # 模擬回應（不實際調用 Gemini）
        if "quickly" in user_input:
            response = "🎯 Stop planning, start building! Action beats perfection every time!"
        elif "perfection" in user_input:
            response = "Speed! Perfect is the enemy of done. Ship it and iterate!"
        else:
            response = "Push through! Every obstacle is just fuel for success!"
        
        print(f"    CRUZ: {response}")
        
        # 添加到對話歷史
        cruz.conversation_history.append({
            "user": user_input,
            "cruz": response,
            "emotion": emotion_status['current_state']
        })
    
    print("\n📊 Conversation Stats:")
    stats = cruz.get_conversation_stats()
    print(f"  • Total exchanges: {stats['total_exchanges']}")
    print(f"  • Emotional journey: {' → '.join(stats['emotional_journey'])}")
    print(f"  • Current emotion: {stats['current_emotion']['current_state']}")
    
    print("\n✅ Integration test complete!")
    print("💡 Next step: Connect to running Memory API for full integration")

if __name__ == "__main__":
    asyncio.run(test_integration())