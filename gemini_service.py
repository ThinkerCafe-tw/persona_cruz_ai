import google.generativeai as genai
from config import Config
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        """初始化 Gemini 服務"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.conversation_history = {}
        
    def get_response(self, user_id: str, message: str) -> str:
        """
        處理使用者訊息並回傳 AI 回應
        
        Args:
            user_id: Line 使用者 ID
            message: 使用者訊息
            
        Returns:
            AI 回應文字
        """
        try:
            # 初始化使用者對話歷史
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # 建立對話上下文
            context = self._build_context(user_id, message)
            
            # 呼叫 Gemini API
            response = self.model.generate_content(context)
            
            # 儲存對話歷史
            self._save_conversation(user_id, message, response.text)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return "抱歉，我現在無法回應您的訊息。請稍後再試。"
    
    def _build_context(self, user_id: str, message: str) -> str:
        """建立包含對話歷史的上下文"""
        # 系統提示詞
        system_prompt = """你是一個友善的 AI 助理，請用繁體中文回答。
請保持回答簡潔清楚，並且親切有禮。
如果使用者詢問你的身份，請告訴他們你是 Persona Cruz AI 助理。"""
        
        # 組合對話歷史
        history = self.conversation_history.get(user_id, [])
        context = system_prompt + "\n\n"
        
        # 只保留最近 10 則對話
        recent_history = history[-10:] if len(history) > 10 else history
        
        for conv in recent_history:
            context += f"使用者：{conv['user']}\n"
            context += f"助理：{conv['assistant']}\n"
        
        context += f"使用者：{message}\n助理："
        
        return context
    
    def _save_conversation(self, user_id: str, user_message: str, ai_response: str):
        """儲存對話歷史"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'user': user_message,
            'assistant': ai_response
        })
        
        # 限制每個使用者最多保存 50 則對話
        if len(self.conversation_history[user_id]) > 50:
            self.conversation_history[user_id] = self.conversation_history[user_id][-50:]
    
    def clear_history(self, user_id: str):
        """清除特定使用者的對話歷史"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]