#!/usr/bin/env python3
"""
使用現有資料庫結構的真實記憶測試
不假設，使用實際存在的欄位
"""

import requests
import json
import os
import asyncpg
import asyncio
from datetime import datetime

async def test_real_memory_structure():
    print("🧠 測試真實記憶結構...")
    
    database_url = "postgres://postgres:eZR43clAm~RDR.0MPV_TAIfr8aVMTool@trolley.proxy.rlwy.net:34472/railway"
    
    try:
        conn = await asyncpg.connect(database_url)
        
        # 使用實際存在的欄位
        test_concept = f"測試概念 - {datetime.now().isoformat()}"
        
        # 插入到現有結構
        await conn.execute("""
            INSERT INTO memory_crystals (crystal_id, concept, stability, entropy)
            VALUES ($1, $2, $3, $4)
        """, f"test_{int(datetime.now().timestamp())}", test_concept, 0.8, 0.2)
        
        print(f"✅ 記憶已存入: {test_concept}")
        
        # 讀取記憶
        recent_memories = await conn.fetch("""
            SELECT crystal_id, concept, stability, created_at FROM memory_crystals
            ORDER BY created_at DESC
            LIMIT 3
        """)
        
        print("📖 最近的記憶:")
        for memory in recent_memories:
            print(f"  - {memory['concept']} (穩定度: {memory['stability']})")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 記憶測試失敗: {e}")
        return False

async def test_ollama_with_real_structure():
    print("🔄 測試 Ollama + 真實記憶結構...")
    
    try:
        # 用 Ollama 生成概念
        response = requests.post('http://localhost:11434/api/generate', 
                               json={
                                   "model": "mistral",
                                   "prompt": "用簡短的詞組描述：什麼是真實的記憶？",
                                   "stream": False
                               })
        
        if response.status_code != 200:
            print("❌ Ollama 生成失敗")
            return False
            
        concept = response.json()['response'].strip()[:100]  # 限制長度
        print(f"💡 Ollama 生成概念: {concept}")
        
        # 存入真實的表結構
        database_url = "postgres://postgres:eZR43clAm~RDR.0MPV_TAIfr8aVMTool@trolley.proxy.rlwy.net:34472/railway"
        conn = await asyncpg.connect(database_url)
        
        crystal_id = f"ollama_{int(datetime.now().timestamp())}"
        
        await conn.execute("""
            INSERT INTO memory_crystals (crystal_id, concept, stability, entropy, possibilities)
            VALUES ($1, $2, $3, $4, $5)
        """, crystal_id, concept, 0.9, 0.1, json.dumps({"source": "ollama", "test": True}))
        
        print("✅ Ollama 概念已存入記憶系統")
        
        # 驗證存入
        result = await conn.fetchrow("""
            SELECT * FROM memory_crystals WHERE crystal_id = $1
        """, crystal_id)
        
        if result:
            print(f"🔍 驗證成功: {result['concept']}")
            print(f"   穩定度: {result['stability']}, 熵: {result['entropy']}")
            return True
        else:
            print("❌ 驗證失敗: 找不到剛存入的記憶")
            return False
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Ollama+記憶整合失敗: {e}")
        return False

async def main():
    print("🚀 真實記憶系統測試\n")
    
    # 使用實際的表結構進行測試
    tests = [
        ("真實記憶結構測試", test_real_memory_structure),
        ("Ollama+真實結構整合", test_ollama_with_real_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = await test_func()
        results.append((test_name, result))
        
        if not result:
            print(f"⚠️ {test_name} 失敗")
            # 但繼續其他測試，不中斷
    
    print(f"\n{'='*50}")
    print("📊 真實測試結果:")
    
    passed_count = 0
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {test_name}: {status}")
        if result:
            passed_count += 1
    
    print(f"\n🎯 真實結果: {passed_count}/{len(results)} 測試通過")
    
    if passed_count == len(results):
        print("🎉 基本記憶功能正常！")
        print("💡 學到的教訓: 使用現有結構而不是假設結構")
    else:
        print("💧 部分功能正常，部分需要修復")
        print("🔧 這就是真實的進度 - 承認現狀，逐步改進")

if __name__ == "__main__":
    asyncio.run(main())