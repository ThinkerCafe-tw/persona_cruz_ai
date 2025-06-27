import os
import psycopg2
from dotenv import load_dotenv
import logging

# --- 設定日誌 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 載入環境變數 ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# --- 要執行的 SQL 指令 ---
# 使用多行字串來保持 SQL 的可讀性
SQL_COMMANDS = """
-- 1. 創建事件表
CREATE TABLE IF NOT EXISTS dashboard_events (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_data JSONB NOT NULL
);

-- 2. 創建用於發送 NOTIFY 的函式
CREATE OR REPLACE FUNCTION notify_dashboard_event()
RETURNS TRIGGER AS $$
BEGIN
    -- 將新插入的行的 event_data 欄位作為 payload 發送到 'dashboard_events' 頻道
    PERFORM pg_notify(
        'dashboard_events',
        NEW.event_data::text
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 3. 創建觸發器，在每次 INSERT 後呼叫上述函式
-- 首先刪除可能已存在的舊觸發器，以確保冪等性
DROP TRIGGER IF EXISTS on_new_dashboard_event ON dashboard_events;
CREATE TRIGGER on_new_dashboard_event
AFTER INSERT ON dashboard_events
FOR EACH ROW
EXECUTE FUNCTION notify_dashboard_event();
"""

def initialize_database():
    """
    連接到 PostgreSQL 資料庫並執行初始化 SQL 指令。
    """
    if not DATABASE_URL:
        logging.error("錯誤：找不到 DATABASE_URL。請檢查您的 .env 檔案。")
        return

    conn = None
    try:
        # 連接到資料庫
        logging.info("正在連接到您的 Railway PostgreSQL 資料庫...")
        conn = psycopg2.connect(DATABASE_URL)
        logging.info("連接成功！")
        
        # 創建一個 cursor 物件
        cur = conn.cursor()
        
        # 執行 SQL 指令
        logging.info("正在執行資料庫初始化腳本...")
        cur.execute(SQL_COMMANDS)
        
        # 提交交易
        conn.commit()
        logging.info("資料庫初始化成功！'dashboard_events' 表、函式和觸發器均已設定完畢。")
        
        # 關閉 cursor 和連線
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"資料庫操作出錯：{error}")
    finally:
        if conn is not None:
            conn.close()
            logging.info("資料庫連線已關閉。")

if __name__ == "__main__":
    initialize_database()
