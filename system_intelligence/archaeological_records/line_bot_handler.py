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
from quantum_integration import quantum_integration
import json

logger = logging.getLogger(__name__)

class LineBotHandler:
    def __init__(self):
        """初始化 Line Bot 處理器"""
        self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        self.gemini_service = GeminiService()
        
        # 註冊訊息處理器 - 使用裝飾器方式
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            self.handle_text_message(event)
        
        logger.info("LineBotHandler initialized successfully")
    
    def handle_webhook(self, body, signature):
        """處理 webhook 請求"""
        self.handler.handle(body, signature)
    
    def handle_text_message(self, event):
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
            # 量子記憶系統指令
            elif message_text in ['/quantum', '/量子']:
                reply_text = quantum_integration.get_quantum_status()
            elif message_text.startswith('/quantum '):
                # 查看特定角色的量子記憶
                persona = message_text.split(' ', 1)[1]
                reply_text = quantum_integration.get_persona_quantum_report(persona)
            elif message_text in ['/entangle', '/糾纏']:
                reply_text = quantum_integration.get_entanglement_status()
            elif message_text in ['/evolve', '/演化']:
                reply_text = quantum_integration.get_evolution_insights()
            # CRUZ 模式指令
            elif message_text in ['/cruz', '/CRUZ', '切換到CRUZ']:
                self.gemini_service.cruz_mode = True
                self.gemini_service.element_mode = False
                reply_text = "已切換到 CRUZ 模式！我是 CRUZ，很高興能和你聊天。有什麼想討論的嗎？"
            elif message_text in ['/ai', '/AI', '切換到AI']:
                self.gemini_service.cruz_mode = False
                self.gemini_service.element_mode = False
                reply_text = "已切換回 AI 助理模式。"
            else:
                # 一般對話，交給 Gemini 處理
                reply_text = self.gemini_service.get_response(user_id, message_text)
                
                # 將對話同步到量子記憶系統
                try:
                    current_role = self._get_current_role()
                    quantum_integration.process_conversation(
                        user_id=user_id,
                        message=message_text,
                        response=reply_text,
                        current_role=current_role
                    )
                except Exception as e:
                    logger.warning(f"Failed to sync to quantum memory: {e}")
            
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

【CRUZ 模式】
• /cruz - 切換到 CRUZ 本人對話
• /ai - 切換回 AI 助理模式
• 說「創業」「創造」會自動觸發 CRUZ 模式

【五行系統】
• /dashboard - 查看完整系統儀表板
• /status - 查看簡易系統狀態
• /harmony - 查看五行和諧度
• 說「開發」- 切換到火屬性開發專員
• 說「測試」- 切換到水屬性測試專員
• 說「卡住了」- 召喚無極觀察者

【量子記憶】
• /quantum - 查看量子記憶系統狀態
• /quantum <角色> - 查看特定角色量子記憶
• /entangle - 查看量子糾纏關係
• /evolve - 查看演化洞察

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
    
    def _get_current_role(self):
        """獲取當前活躍的角色"""
        if self.gemini_service.cruz_mode:
            return "CRUZ"
        elif self.gemini_service.element_mode and hasattr(self.gemini_service, 'five_elements'):
            current = self.gemini_service.five_elements.get_current_element()
            if current:
                return current.name
        return "AI助理"