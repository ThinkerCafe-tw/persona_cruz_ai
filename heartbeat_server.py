import asyncio
import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import asyncpg
import logging

# --- 設定日誌 ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 載入環境變數 ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# --- FastAPI 應用程式實例 ---
app = FastAPI()

# --- 資料庫監聽與事件廣播 ---
async def event_stream_generator():
    """
    這個非同步產生器會連接到 PostgreSQL，監聽 'dashboard_events' 頻道，
    並在收到通知時，將其 payload 作為 Server-Sent Event (SSE) 產出。
    """
    conn = None
    while True:
        try:
            # 建立連接
            conn = await asyncpg.connect(DATABASE_URL)
            logger.info("成功連接到 PostgreSQL，開始監聽 'dashboard_events' 頻道...")
            
            # 定義一個佇列，用來在連線和通知處理之間傳遞訊息
            queue = asyncio.Queue()

            async def listener(connection, pid, channel, payload):
                logger.info(f"從頻道 '{channel}' 收到新事件: {payload}")
                await queue.put(payload)

            await conn.add_listener('dashboard_events', listener)
            
            # 保持連線開啟，並從佇列中發送事件
            while True:
                payload = await queue.get()
                # SSE 格式: "data: <json_string>\n\n"
                yield f"data: {payload}\n\n"

        except (asyncpg.PostgresError, OSError) as e:
            logger.error(f"資料庫連接或監聽出錯: {e}")
            if conn:
                # 關閉舊的、可能已損壞的連線
                await conn.close()
                logger.info("連線已關閉。")
            logger.info("5 秒後嘗試重新連接...")
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            logger.info("任務被取消，正在關閉連線...")
            if conn:
                await conn.close()
            logger.info("連線已關閉。")
            break


@app.get("/events")
async def event_stream(request: Request):
    """
    SSE 端點，客戶端 (我們的儀表板) 會連接到這裡來接收即時事件。
    """
    return StreamingResponse(event_stream_generator(), media_type="text/event-stream")

@app.get("/")
def read_root():
    return {"message": "Cruz AI Heartbeat Server is running. Connect to /events to get live updates."}

# --- Gemini 思考與寫入資料庫的邏輯 (未來將取代 heartbeat.sh) ---
# 這裡我們先留一個預留位置，之後會把 Gemini CLI 的呼叫邏輯整合進來。
# 目前，我們需要手動向資料庫插入事件來進行測試。

if __name__ == "__main__":
    import uvicorn
    # 建議從終端機執行 uvicorn heartbeat_server:app --reload
    # 但這裡也提供一個直接執行的選項
    uvicorn.run(app, host="0.0.0.0", port=8000)
