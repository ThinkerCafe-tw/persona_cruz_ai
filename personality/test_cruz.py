"""
測試 CRUZ 人格系統 - 簡化版
"""
import asyncio
import json
from datetime import datetime
from emotion_engine import cruz_emotion, EmotionTrigger

async def test_personality():
    """測試 CRUZ 人格和情緒系統"""
    print("🎯 CRUZ Personality Test - Day 4\n")
    
    # 載入人格配置
    with open("cruz_personality.json", "r", encoding="utf-8") as f:
        personality = json.load(f)
    
    print("📋 Core Traits:")
    for trait, value in personality['core_traits'].items():
        print(f"  • {trait}: {value}")
    
    print("\n🎭 Emotion Engine Test:")
    
    # 測試情緒轉換
    test_scenarios = [
        ("用戶說：我完成了任務！", EmotionTrigger.SUCCESS),
        ("用戶說：系統出錯了...", EmotionTrigger.FAILURE),
        ("用戶說：這個問題很有挑戰性", EmotionTrigger.CHALLENGE),
        ("用戶說：我們發現了新方法！", EmotionTrigger.DISCOVERY)
    ]
    
    for scenario, trigger in test_scenarios:
        print(f"\n💬 {scenario}")
        old_state = cruz_emotion.current_state
        cruz_emotion.process_trigger(trigger, {"scenario": scenario})
        status = cruz_emotion.get_status()
        print(f"   情緒：{status['emotional_prefix']} {old_state.value} → {status['current_state']}")
        print(f"   強度：{status['intensity']}")
    
    print("\n📊 Final Emotion Status:")
    final_status = cruz_emotion.get_status()
    print(json.dumps(final_status, indent=2, ensure_ascii=False))
    
    print("\n💡 CRUZ Quotes:")
    for quote in personality['cruz_quotes'][:3]:
        print(f"   🎯 \"{quote}\"")
    
    print("\n✅ Personality system ready for integration!")

if __name__ == "__main__":
    asyncio.run(test_personality())