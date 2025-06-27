import os
import logging
from dotenv import load_dotenv
from notion_client import Client, APIResponseError

# --- 設定日誌 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 載入環境變數 ---
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_INTERNAL_INTEGRATION_TOKEN")

def test_notion_connection():
    """
    初始化 Notion 客戶端，並嘗試搜尋有權限訪問的內容，以驗證連線。
    """
    if not NOTION_TOKEN:
        logging.error("錯誤：找不到 NOTION_INTERNAL_INTEGRATION_TOKEN。請檢查您的 .env 檔案。")
        return

    logging.info("正在初始化 Notion 客戶端...")
    notion = Client(auth=NOTION_TOKEN)

    try:
        logging.info("正在嘗試搜尋 Bot 有權限訪問的頁面和資料庫...")
        
        # search() 方法會回傳該 Bot 被授權的所有內容
        response = notion.search()
        
        results = response.get("results")
        
        if not results:
            logging.warning("連線成功，但此 Bot 目前沒有被授權訪問任何頁面或資料庫。")
            logging.warning("請在 Notion 中，點擊您想要分享的頁面或資料庫右���角的 '...' -> 'Add connections'，然後選擇 'MCP' 這個整合。")
            return

        logging.info(f"連線成功！找到了 {len(results)} 個 Bot 有權限訪問的項目：")
        
        for item in results:
            item_type = item.get("object")
            item_id = item.get("id")
            
            if item_type == "database":
                title_list = item.get("title", [])
                if title_list:
                    title = title_list[0].get("plain_text", "無標題的資料庫")
                else:
                    title = "無標題的資料庫"
                logging.info(f"  - [資料庫] {title} (ID: {item_id})")
            elif item_type == "page":
                properties = item.get("properties", {})
                title_property = next((prop for prop_name, prop in properties.items() if prop.get("type") == "title"), None)
                if title_property:
                    title_list = title_property.get("title", [])
                    if title_list:
                        title = title_list[0].get("plain_text", "無標題的頁面")
                    else:
                        title = "無標題的頁��"
                else:
                    title = "無標題的頁面"
                logging.info(f"  - [頁面] {title} (ID: {item_id})")
            else:
                logging.info(f"  - [其他類型: {item_type}] (ID: {item_id})")

    except APIResponseError as e:
        logging.error(f"Notion API 錯誤：{e}")
        logging.error("請檢查您的 NOTION_INTERNAL_INTEGRATION_TOKEN 是否正確，以及 Bot 是否有被正確設定。")

if __name__ == "__main__":
    test_notion_connection()
