#!/usr/bin/env python3
"""
量子記憶系統遷移腳本
將現有的 JSON 檔案記憶遷移到 pgvector 資料庫
"""
import os
import sys
import json
import logging
from datetime import datetime
from quantum_memory import QuantumDatabase, QuantumVectorizer, QuantumMemory

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def migrate_memories():
    """執行記憶遷移"""
    print("🚀 開始遷移量子記憶到 pgvector...")
    print("=" * 60)
    
    # 檢查環境變數
    if not os.getenv('DATABASE_URL'):
        print("❌ 錯誤：未設定 DATABASE_URL 環境變數")
        print("請確保 Railway pgvector 服務已啟動並正確連接")
        return False
    
    # 初始化資料庫和向量化器
    db = QuantumDatabase()
    vectorizer = QuantumVectorizer()
    
    if not db.pool:
        print("❌ 無法連接到資料庫")
        return False
    
    # 掃描記憶檔案
    memories_dir = "quantum_memory/memories"
    if not os.path.exists(memories_dir):
        print(f"❌ 找不到記憶目錄：{memories_dir}")
        return False
    
    memory_files = [f for f in os.listdir(memories_dir) if f.endswith('.json')]
    print(f"\n📁 找到 {len(memory_files)} 個記憶檔案")
    
    success_count = 0
    
    for memory_file in memory_files:
        persona_id = memory_file.replace('.json', '')
        print(f"\n🔄 遷移 {persona_id} 的記憶...")
        
        try:
            # 讀取 JSON 檔案
            file_path = os.path.join(memories_dir, memory_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 保存主記憶
            identity_data = data.get('identity', {})
            identity_vector = vectorizer.vectorize_identity(identity_data)
            
            memory_id = db.save_quantum_memory(
                persona_id,
                identity_data,
                identity_vector
            )
            
            if not memory_id:
                print(f"  ❌ 無法保存 {persona_id} 的主記憶")
                continue
            
            print(f"  ✅ 主記憶已保存 (ID: {memory_id})")
            
            # 保存記憶晶體
            crystals = data.get('crystals', {})
            crystal_count = 0
            
            for crystal_id, crystal_data in crystals.items():
                concept_vector = vectorizer.vectorize_concept(
                    crystal_data['concept'],
                    crystal_data.get('possibilities', [])
                )
                
                db.save_memory_crystal(memory_id, crystal_data, concept_vector)
                crystal_count += 1
            
            print(f"  ✅ {crystal_count} 個記憶晶體已保存")
            
            # 保存漣漪（最近的20個）
            ripples = data.get('ripples', [])
            ripple_count = 0
            
            for ripple in ripples[-20:]:  # 只保存最近的20個
                event_vector = vectorizer.vectorize_event(ripple['event'])
                db.save_ripple(memory_id, ripple, event_vector)
                ripple_count += 1
            
            print(f"  ✅ {ripple_count} 個量子漣漪已保存")
            
            # 統計資訊
            print(f"  📊 統計：")
            print(f"     • 演化次數：{data.get('evolution_count', 0)}")
            print(f"     • 創建時間：{data.get('created_at', 'N/A')}")
            print(f"     • 最後保存：{data.get('last_save', 'N/A')}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ 遷移失敗：{e}")
            logger.error(f"Failed to migrate {persona_id}: {e}", exc_info=True)
    
    print("\n" + "=" * 60)
    print(f"✅ 遷移完成！成功遷移 {success_count}/{len(memory_files)} 個記憶")
    
    # 驗證遷移結果
    print("\n📋 驗證遷移結果...")
    verify_migration(db)
    
    db.close()
    return success_count == len(memory_files)


def verify_migration(db: QuantumDatabase):
    """驗證遷移結果"""
    with db.get_connection() as conn:
        if not conn:
            return
        
        with conn.cursor() as cur:
            # 統計各表的記錄數
            tables = ['quantum_memories', 'memory_crystals', 'quantum_ripples']
            
            for table in tables:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"  • {table}: {count} 筆記錄")
            
            # 列出所有角色
            cur.execute("SELECT persona_id FROM quantum_memories ORDER BY persona_id")
            personas = [row[0] for row in cur.fetchall()]
            print(f"\n  已遷移的角色：{', '.join(personas)}")


def test_vector_search(db: QuantumDatabase, vectorizer: QuantumVectorizer):
    """測試向量搜尋功能"""
    print("\n🔍 測試向量搜尋...")
    
    # 測試搜尋相似記憶
    test_text = "量子記憶系統的突破性發展"
    test_vector = vectorizer.vectorize_text(test_text)
    
    if test_vector:
        results = db.search_similar_memories(test_vector, limit=5)
        
        print(f"\n搜尋 '{test_text}' 的相似記憶：")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['concept']} (距離: {result['distance']:.4f})")


if __name__ == "__main__":
    # 檢查命令列參數
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("🧪 測試模式：測試向量搜尋功能")
        db = QuantumDatabase()
        vectorizer = QuantumVectorizer()
        test_vector_search(db, vectorizer)
        db.close()
    else:
        # 執行遷移
        success = migrate_memories()
        sys.exit(0 if success else 1)