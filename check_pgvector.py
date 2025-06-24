#!/usr/bin/env python3
"""
快速檢查 pgvector 連接狀態
用於驗證 Railway pgvector 設定是否正確
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def check_pgvector():
    """檢查 pgvector 連接和設定"""
    print("🔍 檢查 pgvector 設定...")
    print("=" * 60)
    
    # 1. 檢查環境變數
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ 錯誤：未設定 DATABASE_URL")
        print("\n請在 Railway Dashboard 中：")
        print("1. 進入你的應用程式服務")
        print("2. 點擊 Variables 標籤")
        print("3. 新增 DATABASE_URL 變數")
        print("4. 選擇 Add Reference → PostgreSQL → DATABASE_URL")
        return False
    
    print("✅ DATABASE_URL 已設定")
    
    # 2. 嘗試連接
    try:
        # Railway 提供的 URL 可能需要調整
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://')
        
        print("\n📡 連接到資料庫...")
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # 3. 檢查 PostgreSQL 版本
        cur.execute("SELECT version()")
        version = cur.fetchone()[0]
        print(f"✅ PostgreSQL 連接成功")
        print(f"   版本：{version.split(',')[0]}")
        
        # 4. 檢查 pgvector
        cur.execute("""
            SELECT extname, extversion 
            FROM pg_extension 
            WHERE extname = 'vector'
        """)
        result = cur.fetchone()
        
        if result:
            print(f"✅ pgvector 已安裝：v{result[1]}")
        else:
            print("⚠️  pgvector 未安裝")
            print("\n嘗試安裝 pgvector...")
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                print("✅ pgvector 安裝成功！")
            except Exception as e:
                print(f"❌ 無法安裝 pgvector: {e}")
                print("\n請使用 Railway CLI 或資料庫客戶端執行：")
                print("CREATE EXTENSION vector;")
                return False
        
        # 5. 檢查量子記憶表
        print("\n📊 檢查量子記憶表...")
        tables = ['quantum_memories', 'memory_crystals', 'quantum_ripples', 'quantum_entanglements']
        existing_tables = []
        
        for table in tables:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                )
            """, (table,))
            exists = cur.fetchone()[0]
            if exists:
                existing_tables.append(table)
        
        if existing_tables:
            print(f"✅ 已建立 {len(existing_tables)}/{len(tables)} 個表：")
            for table in existing_tables:
                print(f"   • {table}")
        else:
            print("ℹ️  量子記憶表尚未建立（將在第一次使用時自動建立）")
        
        # 6. 測試向量操作
        print("\n🧪 測試向量操作...")
        try:
            # 建立測試表
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vector_test (
                    id serial PRIMARY KEY,
                    embedding vector(3)
                )
            """)
            
            # 插入測試向量
            cur.execute("""
                INSERT INTO vector_test (embedding) 
                VALUES ('[1,2,3]'::vector)
                RETURNING id
            """)
            test_id = cur.fetchone()[0]
            
            # 查詢測試
            cur.execute("""
                SELECT embedding FROM vector_test 
                WHERE id = %s
            """, (test_id,))
            result = cur.fetchone()
            
            # 清理
            cur.execute("DROP TABLE vector_test")
            
            print("✅ 向量操作測試成功")
            
        except Exception as e:
            print(f"❌ 向量操作測試失敗: {e}")
            return False
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("🎉 所有檢查通過！pgvector 已就緒")
        print("\n下一步：")
        print("1. 推送程式碼到 GitHub")
        print("2. Railway 將自動部署")
        print("3. 量子記憶系統將使用 pgvector 儲存")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ 無法連接到資料庫：{e}")
        print("\n可能的原因：")
        print("1. DATABASE_URL 設定錯誤")
        print("2. PostgreSQL 服務未啟動")
        print("3. 網路連接問題")
        
        if "does not exist" in str(e):
            print("\n💡 提示：資料庫可能尚未建立")
            print("請在 Railway 中檢查 PostgreSQL 服務狀態")
            
        return False
        
    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
        return False


if __name__ == "__main__":
    # 支援從命令列傳入 DATABASE_URL
    if len(sys.argv) > 1:
        os.environ['DATABASE_URL'] = sys.argv[1]
        print(f"使用提供的 DATABASE_URL")
    
    success = check_pgvector()
    sys.exit(0 if success else 1)