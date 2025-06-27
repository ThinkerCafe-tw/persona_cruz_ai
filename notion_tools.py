import os
import logging
from dotenv import load_dotenv
from notion_client import Client, APIResponseError

# --- 設定日誌 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 載入環境變數 ---
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_INTERNAL_INTEGRATION_TOKEN")

def get_notion_client():
    """
    初始化並回傳一個 Notion 客戶端實例。
    如果沒有找到 Token，會回傳 None。
    """
    if not NOTION_TOKEN:
        logging.error("錯誤：找不到 NOTION_INTERNAL_INTEGRATION_TOKEN。請檢查您的 .env 檔案。")
        return None
    
    return Client(auth=NOTION_TOKEN)

# ------------------------------------------------------------------------------
#  未來將在這裡擴充更多與 Notion 互動的函式
# ------------------------------------------------------------------------------

def query_database(client: Client, database_id: str, filter_params: dict = None) -> list:
    """
    查詢一個 Notion 資料庫。

    :param client: 已初始化的 Notion 客戶端。
    :param database_id: 要查詢的資料庫 ID。
    :param filter_params: Notion API 的過濾器物件 (可選)。
    :return: 一個包含查詢結果頁面物件的列表。
    """
    if not client:
        logging.error("Notion 客戶端未初始化。")
        return []
        
    try:
        query_args = {
            "database_id": database_id
        }
        if filter_params:
            query_args["filter"] = filter_params

        logging.info(f"正在查詢資料庫 ID: {database_id}...")
        response = client.databases.query(**query_args)
        logging.info("查詢成功！")
        return response.get("results", [])
    except APIResponseError as e:
        logging.error(f"查詢資料庫時發生 API 錯誤: {e}")
        return []

# --- 測試區塊 ---
if __name__ == '__main__':
    # 這段程式碼只在直接執行此檔案時才會運行
    
    notion_client = get_notion_client()
    
    if notion_client:
        # 替換成您想要測試的資料庫 ID
        # 例如 'Thinker Engine Board' 的 ID
        # TEST_DATABASE_ID = "YOUR_DATABASE_ID_HERE" 
        
        # logging.info(f"--- 正在執行一個測試查詢 ---")
        # logging.info(f"如果想測試查詢功能，請在此腳本的 'if __name__ == '__main__':' 區塊中，")
        # logging.info(f"填入一個您的 Bot 有權限訪問的資料庫 ID 到 TEST_DATABASE_ID 變數。")
        
        # 範例：
        # pages = query_database(notion_client, TEST_DATABASE_ID)
        # if pages:
        #     logging.info(f"成功從資料庫 '{TEST_DATABASE_ID}' 中獲取了 {len(pages)} 個頁面。")
        #     # 在這裡可以加入更多處理頁面內容的程式碼
        # else:
        #     logging.info("查詢完成，但沒有回傳任何頁面。")
        pass
    else:
        logging.error("無法創建 Notion 客戶端，測試終止。")

