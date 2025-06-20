import os
from dotenv import load_dotenv

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
    
    # Gemini 模型設定
    GEMINI_MODEL = 'gemini-pro'
    
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