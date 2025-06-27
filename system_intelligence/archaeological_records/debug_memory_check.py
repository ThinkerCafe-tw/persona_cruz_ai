#!/usr/bin/env python3
"""
調試量子記憶系統 - 檢查實際儲存的內容
"""
import os
import psycopg2
from pgvector.psycopg2 import register_vector

# Railway PostgreSQL URL
DATABASE_URL = "postgresql://postgres:eZR43clAm~RDR.0MPV_TAIfr8aVMTool@trolley.proxy.rlwy.net:34472/railway"

def check_memory_content():
    """檢查資料庫中的記憶內容"""
    try:
        print("🔍 連接到 Railway PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # 註冊 vector 類型
        register_vector(conn)
        
        print("\n📊 檢查量子記憶表...")
        
        # 檢查表格
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND (table_name LIKE '%quantum%' OR table_name LIKE '%memory%')
        """)
        
        tables = cur.fetchall()
        print(f"找到 {len(tables)} 個相關表格:")
        for table in tables:
            print(f"  - {table[0]}")
            
            # 檢查每個表的記錄數
            cur.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cur.fetchone()[0]
            print(f"    記錄數: {count}")
            
            # 如果有記錄，顯示前5筆
            if count > 0:
                cur.execute(f"SELECT * FROM {table[0]} LIMIT 5")
                columns = [desc[0] for desc in cur.description]
                print(f"    欄位: {columns}")
                
                records = cur.fetchall()
                for i, record in enumerate(records):
                    print(f"    記錄 {i+1}:")
                    for j, col in enumerate(columns):
                        if col == 'embedding':
                            print(f"      {col}: [向量資料...]")
                        else:
                            print(f"      {col}: {record[j]}")
        
        # 特別檢查是否有任何包含 "名字" 或 "你好" 的記憶
        print("\n🔍 搜尋特定記憶內容...")
        for keyword in ["名字", "你好", "新用戶", "記得"]:
            cur.execute("""
                SELECT COUNT(*) FROM quantum_memories 
                WHERE content LIKE %s OR metadata::text LIKE %s
            """, (f'%{keyword}%', f'%{keyword}%'))
            
            count = cur.fetchone()[0] if cur.rowcount > 0 else 0
            print(f"  包含 '{keyword}' 的記錄: {count} 筆")
        
        cur.close()
        conn.close()
        
        print("\n✅ 檢查完成！")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    print("🧠 量子記憶系統調試工具")
    print("=" * 50)
    check_memory_content()