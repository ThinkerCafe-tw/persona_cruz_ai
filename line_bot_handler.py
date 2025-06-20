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

特殊指令：
• /help 或 幫助 - 顯示此說明
• /clear 或 清除對話 - 清除對話記錄
• 說個笑話 - 聽個冷笑話放鬆一下

有任何問題都可以直接問我喔！"""
    
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