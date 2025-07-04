import os
from dotenv import load_dotenv

# Railway 環境不需要 .env 檔案
if not os.getenv('RAILWAY_ENVIRONMENT'):
    load_dotenv()

class Config:
    # Line Bot 設定
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
    
    # Gemini API 設定
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Flask 設定
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # 判斷是否在 Railway 環境
    IS_RAILWAY = os.getenv('RAILWAY_ENVIRONMENT') is not None
    
    # Gemini 模型設定
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    # 資料庫設定 (pgvector)
    DATABASE_URL = os.getenv('DATABASE_URL')
    # Railway 使用 postgres:// 需要轉換為 postgresql://
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    USE_QUANTUM_DATABASE = bool(DATABASE_URL)  # 自動偵測是否使用資料庫
    
    @classmethod
    def validate(cls):
        """驗證必要的環境變數是否存在"""
        required_vars = [
            ('LINE_CHANNEL_ACCESS_TOKEN', cls.LINE_CHANNEL_ACCESS_TOKEN),
            ('LINE_CHANNEL_SECRET', cls.LINE_CHANNEL_SECRET),
            ('GEMINI_API_KEY', cls.GEMINI_API_KEY)
        ]
        
        missing_vars = [var[0] for var in required_vars if not var[1]]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True