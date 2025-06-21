from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from config import Config
from gemini_service import GeminiService
from jokes import get_random_joke
import logging

logger = logging.getLogger(__name__)

class LineBotHandler:
    def __init__(self):
        """初始化 Line Bot 處理器"""
        self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        self.gemini_service = GeminiService()
        
        # 註冊訊息處理器
        self._register_handlers()
    
    def _register_handlers(self):
        """註冊各種訊息類型的處理器"""
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            """處理文字訊息"""
            user_id = event.source.user_id
            user_message = event.message.text
            
            logger.info(f"Received message from {user_id}: {user_message}")
            
            # 特殊指令處理
            if user_message.lower() in ['/clear', '清除對話']:
                self.gemini_service.clear_history(user_id)
                reply_text = "對話記錄已清除！我們可以開始新的對話了。"
            elif user_message.lower() in ['/help', '幫助']:
                reply_text = self._get_help_message()
            elif user_message in ['說個笑話', '講個笑話', '來個笑話']:
                reply_text = get_random_joke()
            elif user_message.lower() == '/test':
                reply_text = self._run_self_test()
            else:
                # 取得 Gemini AI 回應
                reply_text = self.gemini_service.get_response(user_id, user_message)
            
            # 回覆訊息
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
    
    def _get_help_message(self):
        """取得幫助訊息"""
        return """🤖 Persona Cruz AI 助理使用說明：

我是您的 AI 助理，可以回答各種問題並與您對話。

📅 日曆功能：
• 建立行程：「幫我安排明天下午3點開會」
• 查詢行程：「我明天有什麼行程？」
• 管理行程：自然語言描述即可

💬 對話功能：
• /help 或 幫助 - 顯示此說明
• /clear 或 清除對話 - 清除對話記錄
• 說個笑話 - 聽個冷笑話放鬆一下

有任何問題都可以直接問我喔！"""
    
    def _run_self_test(self):
        """執行自我測試"""
        test_results = []
        
        # 測試基本對話
        try:
            response = self.gemini_service.get_response("test_user", "你好")
            test_results.append("✅ 基本對話: 通過" if response else "❌ 基本對話: 失敗")
        except:
            test_results.append("❌ 基本對話: 錯誤")
        
        # 測試笑話功能
        try:
            from jokes import get_random_joke
            joke = get_random_joke()
            test_results.append("✅ 笑話功能: 通過" if joke else "❌ 笑話功能: 失敗")
        except:
            test_results.append("❌ 笑話功能: 錯誤")
        
        # 測試日曆功能
        try:
            if self.gemini_service.calendar_service:
                test_results.append("✅ 日曆服務: 已啟用")
            else:
                test_results.append("⚠️ 日曆服務: 未設定")
        except:
            test_results.append("❌ 日曆服務: 錯誤")
        
        # 建立測試報告
        from datetime import datetime
        report = "🧪 自我測試報告\n" + "="*20 + "\n"
        report += "\n".join(test_results)
        report += "\n" + "="*20 + "\n"
        report += f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return report
    
    def handle_webhook(self, body, signature):
        """處理 webhook 請求"""
        try:
            self.handler.handle(body, signature)
        except InvalidSignatureError as e:
            logger.error(f"Invalid signature error: {str(e)}")
            logger.error(f"Received signature: {signature}")
            logger.error(f"Body: {body[:100]}...")  # 只顯示前100個字符
            raise
        except Exception as e:
            logger.error(f"Error handling webhook: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            raise