#!/usr/bin/env python3
import asyncpg
import asyncio
import os

async def check_database():
    database_url = "postgres://postgres:eZR43clAm~RDR.0MPV_TAIfr8aVMTool@trolley.proxy.rlwy.net:34472/railway"
    
    conn = await asyncpg.connect(database_url)
    
    # 檢查所有表
    tables = await conn.fetch("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    
    print("📋 現有表格:")
    for table in tables:
        print(f"  - {table['table_name']}")
    
    # 檢查 memory_crystals 表結構
    if any(table['table_name'] == 'memory_crystals' for table in tables):
        print(f"\n🔍 memory_crystals 表結構:")
        columns = await conn.fetch("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'memory_crystals'
            ORDER BY ordinal_position
        """)
        
        for col in columns:
            print(f"  - {col['column_name']}: {col['data_type']} (nullable: {col['is_nullable']})")
        
        # 檢查資料
        count = await conn.fetchval("SELECT COUNT(*) FROM memory_crystals")
        print(f"\n📊 記錄數量: {count}")
        
        if count > 0:
            sample = await conn.fetch("SELECT * FROM memory_crystals LIMIT 3")
            print(f"\n📄 樣本資料:")
            for row in sample:
                print(f"  {dict(row)}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_database())