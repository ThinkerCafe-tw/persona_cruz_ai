#!/usr/bin/env python3
"""
測試日曆創建流程的診斷腳本
用於追蹤訊息處理的每個步驟
"""

import os
import logging
import sys

# 設定詳細日誌
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def test_calendar_creation():
    """測試日曆創建的完整流程"""
    logger.info("=== 開始測試日曆創建流程 ===")
    
    # 1. 檢查環境變數
    logger.info("\n1. 檢查環境變數")
    required_vars = ['GEMINI_API_KEY', 'GOOGLE_CALENDAR_CREDENTIALS', 'GOOGLE_CALENDAR_ID']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}: 已設定 (長度: {len(value)})")
        else:
            logger.warning(f"❌ {var}: 未設定")
    
    # 2. 測試 GeminiService 初始化
    logger.info("\n2. 測試 GeminiService 初始化")
    try:
        from gemini_service import GeminiService
        service = GeminiService()
        logger.info("✅ GeminiService 初始化成功")
        
        # 檢查 calendar_service
        if service.calendar_service:
            logger.info("✅ CalendarService 已初始化")
        else:
            logger.warning("❌ CalendarService 未初始化")
    except Exception as e:
        logger.error(f"❌ GeminiService 初始化失敗: {str(e)}")
        return
    
    # 3. 測試訊息處理
    logger.info("\n3. 測試訊息處理")
    test_message = "請幫我在明天下午3點安排一個會議"
    logger.info(f"測試訊息: {test_message}")
    
    try:
        response = service.get_response("test_user", test_message)
        logger.info(f"✅ 收到回應: {response[:100]}...")
        logger.info(f"回應長度: {len(response)}")
        
        # 檢查回應內容
        if "成功" in response:
            logger.info("✅ 回應中包含'成功'關鍵字")
        elif "失敗" in response or "錯誤" in response:
            logger.warning("⚠️ 回應中包含錯誤訊息")
        else:
            logger.info("ℹ️ 回應內容未明確表示成功或失敗")
            
    except Exception as e:
        logger.error(f"❌ 訊息處理失敗: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    # 4. 測試 Line Bot Handler
    logger.info("\n4. 測試 Line Bot Handler")
    try:
        from line_bot_handler import LineBotHandler
        handler = LineBotHandler()
        logger.info("✅ LineBotHandler 初始化成功")
        
        # 檢查 Line API 設定
        if handler.line_bot_api:
            logger.info("✅ Line Bot API 已設定")
        else:
            logger.warning("❌ Line Bot API 未設定")
            
    except Exception as e:
        logger.error(f"❌ LineBotHandler 初始化失敗: {str(e)}")
    
    logger.info("\n=== 測試完成 ===")

if __name__ == "__main__":
    test_calendar_creation()