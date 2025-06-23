"""
Line Bot 訊息處理器
"""
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction
)
from config import Config
from gemini_service import GeminiService
from jokes import get_random_joke
import json

logger = logging.getLogger(__name__)

class LineBotHandler:
    def __init__(self):
        """初始化 Line Bot 處理器"""
        self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        self.gemini_service = GeminiService()
        
        # 註冊訊息處理器
        self.handler.add(MessageEvent, message=TextMessage)(self.handle_text_message)
        
        logger.info("LineBotHandler initialized successfully")
    
    def handle_webhook(self, body, signature):
        """處理 webhook 請求"""
        self.handler.handle(body, signature)
    
    def handle_text_message(self, event, destination=None):
        """處理文字訊息"""
        user_id = event.source.user_id
        message_text = event.message.text.strip()
        
        logger.info(f"Received message from {user_id}: {message_text}")
        
        try:
            # 處理特殊命令
            if message_text in ['/help', '幫助']:
                reply_text = self._get_help_message()
            elif message_text in ['/clear', '清除對話']:
                self.gemini_service.clear_history(user_id)
                reply_text = "已清除對話記錄！讓我們重新開始吧。"
            elif message_text == '/test':
                reply_text = self._run_self_test()
            elif message_text in ['說個笑話', '講個笑話', '來個笑話']:
                reply_text = get_random_joke()
            # 五行系統指令
            elif message_text in ['/dashboard', '/狀態', '/儀表板']:
                reply_text = self.gemini_service.get_response(user_id, message_text)
            elif message_text in ['/status', '/mini', '/簡報']:
                reply_text = self.gemini_service.get_response(user_id, message_text)
            elif message_text in ['/harmony', '/和諧度']:
                reply_text = self.gemini_service.get_response(user_id, message_text)
            else:
                # 一般對話，交給 Gemini 處理
                reply_text = self.gemini_service.get_response(user_id, message_text)
            
            # 發送回覆
            self._send_reply(event.reply_token, reply_text)
            
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            error_message = "抱歉，處理您的訊息時發生錯誤。請稍後再試。"
            self._send_reply(event.reply_token, error_message)
    
    def _send_reply(self, reply_token, message_text):
        """發送回覆訊息"""
        try:
            # 檢查訊息長度
            if len(message_text) > 5000:
                message_text = message_text[:4997] + "..."
            
            self.line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=message_text)
            )
        except LineBotApiError as e:
            logger.error(f"Failed to send reply: {e}")
    
    def _get_help_message(self):
        """取得說明訊息"""
        return """🤖 Persona Cruz AI 助理使用說明

【基本功能】
• 智能對話：直接輸入訊息即可對話
• 日曆管理：「幫我安排明天下午3點開會」
• 查詢行程：「我明天有什麼行程？」
• 說個笑話：輕鬆一下！

【五行系統】
• /dashboard - 查看完整系統儀表板
• /status - 查看簡易系統狀態
• /harmony - 查看五行和諧度
• 說「開發」- 切換到火屬性開發專員
• 說「測試」- 切換到水屬性測試專員
• 說「卡住了」- 召喚無極觀察者

【系統指令】
• /help 或 幫助 - 顯示此說明
• /clear 或 清除對話 - 清除對話記錄
• /test - 執行系統自我測試

有任何問題都可以直接問我！"""
    
    def _run_self_test(self):
        """執行自我測試"""
        results = []
        
        # 測試 1: Line Bot API
        try:
            self.line_bot_api.get_bot_info()
            results.append("✅ Line Bot API 連線正常")
        except:
            results.append("❌ Line Bot API 連線失敗")
        
        # 測試 2: Gemini Service
        try:
            test_response = self.gemini_service.get_response("test_user", "測試訊息")
            if test_response:
                results.append("✅ Gemini AI 服務正常")
            else:
                results.append("⚠️ Gemini AI 回應為空")
        except:
            results.append("❌ Gemini AI 服務異常")
        
        # 測試 3: 五行系統
        try:
            dashboard = self.gemini_service.five_elements.get_mini_dashboard()
            if dashboard:
                results.append("✅ 五行系統運作正常")
                results.append(f"   {dashboard}")
            else:
                results.append("⚠️ 五行系統無回應")
        except:
            results.append("❌ 五行系統異常")
        
        return "🔧 系統自我測試結果：\n\n" + "\n".join(results)