from flask import Flask, request, abort
import os
import logging
import sys

# 環境檢查（除錯用）
print("=== Environment Check ===")
print(f"RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT')}")
print(f"PORT: {os.getenv('PORT')}")
print(f"LINE_CHANNEL_ACCESS_TOKEN exists: {bool(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))}")
print(f"LINE_CHANNEL_SECRET exists: {bool(os.getenv('LINE_CHANNEL_SECRET'))}")
print(f"GEMINI_API_KEY exists: {bool(os.getenv('GEMINI_API_KEY'))}")
print(f"Total environment variables: {len(os.environ)}")
print("========================")

from config import Config
from line_bot_handler import LineBotHandler
from linebot.exceptions import InvalidSignatureError

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# 驗證環境變數
try:
    Config.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    sys.exit(1)

# 初始化 Flask 應用
app = Flask(__name__)
line_bot_handler = LineBotHandler()

@app.route("/", methods=['GET'])
def index():
    """首頁路由"""
    return "Persona Cruz AI Line Bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    """Line Bot Webhook 端點"""
    # 記錄所有請求頭
    logger.info("=== Webhook Request ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"URL: {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    # 取得請求的簽名
    signature = request.headers.get('X-Line-Signature', '')
    logger.info(f"Signature present: {'Yes' if signature else 'No'}")
    
    # 取得請求的內容
    body = request.get_data(as_text=True)
    logger.info(f"Body length: {len(body)}")
    logger.info(f"Body preview: {body[:200]}..." if body else "Empty body")
    
    # 如果沒有簽名且 body 是空的或特定格式，可能是驗證請求
    if not signature and (not body or body == '{}'):
        logger.info("Possible verification request - returning 200")
        return 'OK', 200
    
    # 如果沒有簽名，這是無效的請求
    if not signature:
        logger.warning("No signature provided")
        abort(400)
    
    # 處理 webhook
    try:
        line_bot_handler.handle_webhook(body, signature)
        logger.info("Webhook handled successfully")
    except InvalidSignatureError as e:
        logger.error(f"Invalid signature: {str(e)}")
        abort(400)
    except Exception as e:
        logger.error(f"Error in callback: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        abort(400)
    
    return 'OK', 200

@app.route("/health", methods=['GET'])
def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "service": "Persona Cruz AI Bot"}

@app.route("/test", methods=['GET', 'POST'])
def test_endpoint():
    """測試端點"""
    logger.info(f"Test endpoint called with method: {request.method}")
    return {"status": "ok", "method": request.method}

if __name__ == "__main__":
    port = Config.PORT
    logger.info(f"Starting Line Bot on port {port}")
    
    # 在 Railway 環境下，由 gunicorn 處理，不直接運行
    if not Config.IS_RAILWAY:
        app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)