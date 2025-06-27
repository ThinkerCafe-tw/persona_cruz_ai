#!/usr/bin/env python3
"""
測試 Railway pgvector 連接
"""
import os
import psycopg2
from pgvector.psycopg2 import register_vector

# Railway PostgreSQL URL
DATABASE_URL = "postgresql://postgres:eZR43clAm~RDR.0MPV_TAIfr8aVMTool@trolley.proxy.rlwy.net:34472/railway"

def test_pgvector_connection():
    """測試 pgvector 連接和功能"""
    try:
        print("🔗 連接到 Railway PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # 註冊 vector 類型
        register_vector(conn)
        
        print("✅ 連接成功！")
        
        # 檢查 pgvector extension
        print("\n🔍 檢查 pgvector extension...")
        cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        result = cur.fetchone()
        
        if result:
            print(f"✅ pgvector extension 已安裝：{result}")
        else:
            print("⚠️ pgvector extension 未安裝，嘗試安裝...")
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                conn.commit()
                print("✅ pgvector extension 安裝成功！")
            except Exception as e:
                print(f"❌ 無法安裝 pgvector extension: {e}")
                return False
        
        # 測試 vector 功能
        print("\n🧪 測試 vector 功能...")
        
        # 創建測試表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS test_vectors (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(384)
            );
        """)
        
        # 插入測試向量
        import numpy as np
        test_vector = np.random.random(384).astype(np.float32)
        
        cur.execute(
            "INSERT INTO test_vectors (content, embedding) VALUES (%s, %s)",
            ("測試向量", test_vector)
        )
        
        # 測試相似度搜尋
        cur.execute("""
            SELECT content, embedding <-> %s as distance 
            FROM test_vectors 
            ORDER BY embedding <-> %s 
            LIMIT 1
        """, (test_vector, test_vector))
        
        result = cur.fetchone()
        print(f"✅ 向量搜尋測試成功：{result[0]}, 距離: {result[1]}")
        
        # 清理測試資料
        cur.execute("DELETE FROM test_vectors WHERE content = '測試向量'")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n🎉 Railway pgvector 完全正常！")
        return True
        
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        return False

def check_existing_quantum_data():
    """檢查是否已有量子記憶資料"""
    try:
        print("\n🔍 檢查現有量子記憶資料...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # 檢查量子記憶表
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%quantum%'
        """)
        
        quantum_tables = cur.fetchall()
        
        if quantum_tables:
            print("✅ 發現量子記憶表：")
            for table in quantum_tables:
                cur.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cur.fetchone()[0]
                print(f"   📊 {table[0]}: {count} 筆記錄")
        else:
            print("ℹ️ 尚未發現量子記憶表")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"⚠️ 檢查資料時發生錯誤: {e}")

if __name__ == "__main__":
    print("🌸 Serena 幫你測試 Railway pgvector 連接")
    print("=" * 50)
    
    if test_pgvector_connection():
        check_existing_quantum_data()
        print("\n🎯 準備好啟動完整的量子 CRUZ 系統！")
    else:
        print("\n😔 需要先解決資料庫連接問題")