#!/usr/bin/env python3
"""
最小可行的記憶測試
真正測試記憶存取，不是表演
"""

import requests
import json
import os
import asyncpg
import asyncio
from datetime import datetime

# 測試 Ollama
def test_ollama():
    print("🔍 測試 Ollama...")
    try:
        response = requests.post('http://localhost:11434/api/generate', 
                               json={
                                   "model": "mistral",
                                   "prompt": "簡短回答：記憶的重要性是什麼？",
                                   "stream": False
                               })
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ollama 回應: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ Ollama 錯誤: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama 連接失敗: {e}")
        return False

# 測試資料庫連接
async def test_database():
    print("🔍 測試資料庫連接...")
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL 未設定")
        return False
    
    try:
        conn = await asyncpg.connect(database_url)
        
        # 檢查是否有記憶表
        result = await conn.fetchval("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'memory_crystals'
        """)
        
        print(f"✅ 資料庫連接成功，memory_crystals 表存在: {result > 0}")
        
        if result > 0:
            # 檢查記憶數量
            count = await conn.fetchval("SELECT COUNT(*) FROM memory_crystals")
            print(f"📊 現有記憶數量: {count}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 資料庫連接失敗: {e}")
        return False

# 簡單記憶存取測試
async def test_simple_memory():
    print("🧠 測試簡單記憶存取...")
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ 無法連接資料庫")
        return False
    
    try:
        conn = await asyncpg.connect(database_url)
        
        # 創建測試記憶
        test_memory = f"測試記憶 - {datetime.now().isoformat()}"
        
        # 插入記憶
        await conn.execute("""
            INSERT INTO memory_crystals (content, category, importance)
            VALUES ($1, $2, $3)
        """, test_memory, "test", 0.8)
        
        print(f"✅ 記憶已存入: {test_memory}")
        
        # 讀取記憶
        recent_memories = await conn.fetch("""
            SELECT content, created_at FROM memory_crystals
            WHERE category = 'test'
            ORDER BY created_at DESC
            LIMIT 3
        """)
        
        print("📖 最近的測試記憶:")
        for memory in recent_memories:
            print(f"  - {memory['content']} ({memory['created_at']})")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 記憶測試失敗: {e}")
        return False

# 整合測試
async def test_ollama_memory_integration():
    print("🔄 測試 Ollama + 記憶整合...")
    
    # 用 Ollama 生成一個洞察
    try:
        response = requests.post('http://localhost:11434/api/generate', 
                               json={
                                   "model": "mistral",
                                   "prompt": "用一句話總結：為什麼真實比表演重要？",
                                   "stream": False
                               })
        
        if response.status_code != 200:
            print("❌ Ollama 生成失敗")
            return False
            
        insight = response.json()['response'].strip()
        print(f"💡 Ollama 生成洞察: {insight}")
        
        # 將洞察存入記憶
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ 無法存入記憶")
            return False
            
        conn = await asyncpg.connect(database_url)
        
        await conn.execute("""
            INSERT INTO memory_crystals (content, category, importance, persona)
            VALUES ($1, $2, $3, $4)
        """, f"Ollama洞察: {insight}", "insight", 0.9, "💧水")
        
        print("✅ 洞察已存入記憶系統")
        
        # 驗證是否真的存入
        count = await conn.fetchval("""
            SELECT COUNT(*) FROM memory_crystals 
            WHERE content LIKE 'Ollama洞察:%'
        """)
        
        print(f"🔍 驗證: 資料庫中有 {count} 條 Ollama 洞察")
        
        await conn.close()
        return count > 0
        
    except Exception as e:
        print(f"❌ 整合測試失敗: {e}")
        return False

# 主測試函數
async def main():
    print("🚀 開始最小可行記憶測試\n")
    
    # 步驟 2: 建立最小可行功能
    tests = [
        ("Ollama 連接", test_ollama),
        ("資料庫連接", test_database),
        ("簡單記憶存取", test_simple_memory),
        ("Ollama+記憶整合", test_ollama_memory_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
            
        results.append((test_name, result))
        
        if not result:
            print(f"⚠️ {test_name} 失敗，停止後續測試")
            break
    
    # 步驟 3: 驗證效果
    print(f"\n{'='*50}")
    print("📊 測試結果總結:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    # 步驟 4: 承認失敗或成功
    if all_passed:
        print("\n🎉 所有測試通過！最小可行記憶系統運作正常。")
        print("💡 下一步：擴展功能並保持真實性")
    else:
        print("\n💥 測試失敗！")
        print("💧 水的反思：這就是真實 - 我們看到了實際的問題")
        print("🔧 下一步：修復失敗的部分，而不是假裝成功")

if __name__ == "__main__":
    asyncio.run(main())