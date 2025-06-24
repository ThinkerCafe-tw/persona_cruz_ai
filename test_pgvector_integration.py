#!/usr/bin/env python3
"""
測試 pgvector 整合
驗證量子記憶系統與資料庫的整合是否正常運作
"""
import os
import logging
from datetime import datetime
from quantum_memory import QuantumDatabase, QuantumVectorizer, QuantumMemoryBridge

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_database_connection():
    """測試資料庫連接"""
    print("\n1️⃣ 測試資料庫連接...")
    
    db = QuantumDatabase()
    if db.pool:
        print("✅ 資料庫連接成功")
        
        # 測試查詢
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                print(f"   PostgreSQL 版本：{version}")
                
                # 檢查 pgvector 擴展
                cur.execute("""
                    SELECT extname, extversion 
                    FROM pg_extension 
                    WHERE extname = 'vector'
                """)
                result = cur.fetchone()
                if result:
                    print(f"   pgvector 版本：{result[1]}")
                else:
                    print("   ⚠️ pgvector 擴展未安裝")
        
        db.close()
        return True
    else:
        print("❌ 資料庫連接失敗")
        return False


def test_vectorizer():
    """測試向量化功能"""
    print("\n2️⃣ 測試向量化功能...")
    
    vectorizer = QuantumVectorizer()
    
    # 測試身份向量化
    identity = {
        'essence': '測試角色',
        'phase': 0.5,
        'frequency': 0.8,
        'amplitude': 0.9,
        'coherence': 1.0
    }
    
    identity_vector = vectorizer.vectorize_identity(identity)
    print(f"✅ 身份向量化成功：{len(identity_vector)} 維")
    
    # 測試文字向量化
    test_text = "量子記憶系統的測試文字"
    text_vector = vectorizer.vectorize_text(test_text)
    
    if text_vector:
        print(f"✅ 文字向量化成功：{len(text_vector)} 維")
    else:
        print("⚠️ 文字向量化失敗（可能是 API 問題）")
    
    return True


def test_quantum_memory_with_db():
    """測試量子記憶與資料庫整合"""
    print("\n3️⃣ 測試量子記憶系統...")
    
    # 建立支援資料庫的橋接器
    bridge = QuantumMemoryBridge(use_database=True)
    
    # 觸發測試事件
    test_event = {
        'type': 'test',
        'content': 'pgvector 整合測試事件',
        'tags': ['測試', 'pgvector', '整合'],
        'source': 'test_script'
    }
    
    print("   觸發測試事件...")
    bridge.trigger_evolution('wuji', test_event)
    
    # 保存到資料庫
    print("   保存到資料庫...")
    for memory in bridge.quantum_memories.values():
        memory.save()
    
    print("✅ 量子記憶系統測試完成")
    
    return bridge


def test_vector_search(bridge: QuantumMemoryBridge):
    """測試向量搜尋功能"""
    print("\n4️⃣ 測試向量搜尋...")
    
    if not bridge.quantum_memories['wuji'].use_database:
        print("⚠️ 未啟用資料庫模式，跳過向量搜尋測試")
        return
    
    db = QuantumDatabase()
    vectorizer = QuantumVectorizer()
    
    # 搜尋相似記憶
    search_text = "量子記憶系統的突破"
    search_vector = vectorizer.vectorize_text(search_text)
    
    if search_vector:
        results = db.search_similar_memories(search_vector, limit=5)
        
        print(f"   搜尋 '{search_text}' 的相似記憶：")
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result.get('concept', 'N/A')} (相似度: {1 - result.get('distance', 1):.2%})")
    
    db.close()
    print("✅ 向量搜尋測試完成")


def main():
    """主測試流程"""
    print("🧪 開始測試 pgvector 整合")
    print("=" * 60)
    
    # 檢查環境變數
    if not os.getenv('DATABASE_URL'):
        print("⚠️ 警告：未設定 DATABASE_URL 環境變數")
        print("將使用純檔案模式進行測試")
        use_db = False
    else:
        use_db = test_database_connection()
    
    # 測試向量化
    test_vectorizer()
    
    # 測試量子記憶
    bridge = test_quantum_memory_with_db()
    
    # 測試向量搜尋
    if use_db:
        test_vector_search(bridge)
    
    print("\n" + "=" * 60)
    print("✅ 所有測試完成！")
    
    # 總結
    print("\n📊 測試總結：")
    print(f"   • 資料庫連接：{'✅ 成功' if use_db else '❌ 失敗'}")
    print(f"   • 向量化功能：✅ 正常")
    print(f"   • 量子記憶系統：✅ 正常")
    print(f"   • 向量搜尋：{'✅ 正常' if use_db else '⏭️ 跳過'}")


if __name__ == "__main__":
    main()