from flask import Flask, request, abort
import os
import logging
import sys
from startup_test import StartupTest

# 設定基礎日誌（在 import 其他模組前）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# 執行啟動自我檢測
startup_tester = StartupTest()
if not startup_tester.run_all_tests():
    logger.error("啟動測試失敗！服務無法啟動。")
    sys.exit(1)

logger.info("所有啟動測試通過！繼續初始化服務...")

# 環境檢查（生產環境）
if os.getenv('RAILWAY_ENVIRONMENT'):
    logger.info(f"Running in Railway environment")
    logger.info(f"Environment variables loaded: {len(os.environ)}")

from config import Config
from line_bot_handler import LineBotHandler
from linebot.exceptions import InvalidSignatureError

# 日誌已在前面設定，這裡不需要重複設定

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
    # 取得啟動測試狀態
    startup_status = startup_tester.get_status()
    
    # 基本健康狀態
    health_status = {
        "status": "healthy" if startup_status["startup_test_passed"] else "unhealthy",
        "service": "Persona Cruz AI Bot",
        "startup_tests": startup_status,
        "timestamp": startup_status["test_time"]
    }
    
    # 如果有錯誤，返回 503 狀態碼
    if not startup_status["startup_test_passed"]:
        return health_status, 503
    
    return health_status

@app.route("/debug-env", methods=['GET'])
def debug_env():
    """偵錯環境變數（部署後請刪除）"""
    import os
    db_url = os.getenv('DATABASE_URL', 'NOT_SET')
    return {
        'DATABASE_URL_exists': db_url != 'NOT_SET',
        'DATABASE_URL_prefix': db_url[:30] + '...' if db_url != 'NOT_SET' else 'NOT_SET',
        'DATABASE_URL_format': 'postgresql://' if db_url.startswith('postgresql://') else 
                               'postgres://' if db_url.startswith('postgres://') else 
                               'unknown' if db_url != 'NOT_SET' else 'NOT_SET',
        'RAILWAY_ENVIRONMENT': os.getenv('RAILWAY_ENVIRONMENT', 'NOT_SET'),
        'env_vars_count': len([k for k in os.environ.keys() if not k.startswith('_')])
    }

@app.route("/test", methods=['GET', 'POST'])
def test_endpoint():
    """測試端點"""
    logger.info(f"Test endpoint called with method: {request.method}")
    return {"status": "ok", "method": request.method}

if __name__ == "__main__":
    port = Config.PORT
    logger.info(f"Starting Line Bot on port {port}")
    
    # Railway 使用 gunicorn，本機開發才用 Flask 內建伺服器
    if not Config.IS_RAILWAY:
        logger.warning("Running in development mode - not for production use!")
        app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)