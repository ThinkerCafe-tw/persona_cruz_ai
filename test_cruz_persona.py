#!/usr/bin/env python3
"""
測試 CRUZ 人格系統
"""
from cruz_persona_system import CruzPersonaSystem

def test_search_and_prompt():
    """測試語料搜尋和提示詞生成"""
    print("=== 測試 CRUZ 人格系統 ===\n")
    
    persona = CruzPersonaSystem()
    
    # 測試不同類型的查詢
    test_queries = [
        "我工作壓力很大，不知道該怎麼辦",
        "AI 會取代人類嗎？",
        "如何保持創造力？",
        "冥想真的有用嗎？",
        "創業好難，想放棄了"
    ]
    
    for query in test_queries:
        print(f"用戶問題：{query}")
        print("-" * 50)
        
        # 搜尋相關語料
        relevant_quotes = persona.search_relevant_quotes(query, limit=2)
        if relevant_quotes:
            print("相關語料：")
            for i, quote in enumerate(relevant_quotes, 1):
                print(f"{i}. {quote['content'][:60]}...")
                print(f"   相關度分數：{quote['relevance_score']}")
        
        # 生成 CRUZ 提示詞
        prompt = persona.generate_cruz_prompt(query)
        print("\n生成的系統提示詞（前300字）：")
        print(prompt[:300] + "...")
        print("\n" + "="*70 + "\n")

def test_statistics():
    """測試統計功能"""
    print("\n=== 語料庫統計 ===")
    
    persona = CruzPersonaSystem()
    stats = persona.get_statistics()
    
    print(f"總語料數：{stats['total_quotes']}")
    print(f"涵蓋主題：{', '.join(stats['topics'])}")
    
    if stats['most_used_quotes']:
        print("\n最常使用的語料：")
        for i, quote in enumerate(stats['most_used_quotes'][:3], 1):
            print(f"{i}. {quote['content'][:50]}... (使用 {quote['usage_count']} 次)")

if __name__ == "__main__":
    test_search_and_prompt()
    test_statistics()