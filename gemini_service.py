import google.generativeai as genai
from config import Config
import logging
import json
from datetime import datetime, timedelta
from calendar_service import CalendarService

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        """初始化 Gemini 服務"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # 定義 Function Calling 工具
        tools = self._get_calendar_tools()
        
        # 使用支援 Function Calling 的模型
        try:
            self.model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                tools=tools
            )
            logger.info("Gemini model initialized with function calling")
        except Exception as e:
            logger.warning(f"Failed to initialize with function calling: {str(e)}")
            # 降級到基本模型
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Fallback to gemini-pro without function calling")
        
        self.conversation_history = {}
        
        # 初始化 Calendar Service（如果有憑證的話）
        try:
            self.calendar_service = CalendarService()
        except Exception as e:
            logger.warning(f"Calendar service initialization failed: {str(e)}")
            self.calendar_service = None
        
    def _get_calendar_tools(self):
        """定義日曆相關的工具函數"""
        return [{
            "function_declarations": [
                {
                    "name": "create_calendar_event",
                    "description": "在 Google Calendar 建立新的行程或事件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": "事件標題或名稱"
                            },
                            "date": {
                                "type": "string",
                                "description": "日期，格式：YYYY-MM-DD"
                            },
                            "time": {
                                "type": "string",
                                "description": "時間，格式：HH:MM"
                            },
                            "duration_hours": {
                                "type": "number",
                                "description": "活動持續時間（小時）"
                            },
                            "description": {
                                "type": "string",
                                "description": "事件描述或備註"
                            },
                            "location": {
                                "type": "string",
                                "description": "地點"
                            }
                        },
                        "required": ["summary", "date", "time"]
                    }
                },
                {
                    "name": "list_calendar_events",
                    "description": "查詢 Google Calendar 的行程",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "要查詢的日期，格式：YYYY-MM-DD，如果是今天可以用 'today'，明天用 'tomorrow'"
                            },
                            "days_ahead": {
                                "type": "integer",
                                "description": "查詢未來幾天的行程"
                            }
                        }
                    }
                },
                {
                    "name": "delete_calendar_event",
                    "description": "刪除 Google Calendar 的行程",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "event_id": {
                                "type": "string",
                                "description": "要刪除的事件 ID"
                            }
                        },
                        "required": ["event_id"]
                    }
                }
            ]
        }]
        
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
            # 如果是簡單的日曆請求且 calendar_service 不可用，直接回應
            if self.calendar_service is None and any(keyword in message for keyword in ['行程', '安排', '會議', '約會']):
                return "抱歉，日曆功能目前無法使用。請確認日曆服務已正確設定。"
            # 初始化使用者對話歷史
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # 建立對話上下文
            context = self._build_context(user_id, message)
            
            # 呼叫 Gemini API with Function Calling
            response = self.model.generate_content(context)
            
            # 檢查是否有 function call
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts') and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            logger.info(f"Function call detected: {part.function_call.name}")
                            # 處理 function call
                            function_response = self._handle_function_call(part.function_call)
                            
                            # 建立包含 function response 的新訊息
                            messages = [
                                {"role": "user", "parts": [{"text": message}]},
                                {"role": "model", "parts": [{"function_call": {"name": part.function_call.name, "args": dict(part.function_call.args)}}]},
                                {"role": "function", "parts": [{"function_response": {
                                    "name": part.function_call.name,
                                    "response": {"result": function_response}
                                }}]}
                            ]
                            
                            # 如果 function 回傳了訊息，直接使用
                            if function_response.get('message'):
                                final_response = function_response['message']
                                logger.info(f"Using function response message directly: {final_response[:100]}...")
                            else:
                                # 將 function 結果回傳給模型產生回應
                                response = self.model.generate_content(messages)
                                
                                # 取得最終回應
                                if hasattr(response, 'text'):
                                    final_response = response.text
                                else:
                                    # 嘗試從 candidates 取得文字
                                    try:
                                        if response.candidates and response.candidates[0].content.parts:
                                            final_response = response.candidates[0].content.parts[0].text
                                        else:
                                            final_response = "抱歉，我無法處理這個請求。"
                                    except:
                                        final_response = "抱歉，我遇到了一些問題。"
            
            # 儲存對話歷史
            self._save_conversation(user_id, message, final_response)
            
            return final_response
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # 如果是日曆相關錯誤，提供更具體的訊息
            if "calendar" in str(e).lower():
                return "抱歉，我在處理日曆功能時遇到問題。請確認您已經分享日曆給我。"
            else:
                return "抱歉，我現在無法回應您的訊息。請稍後再試。"
    
    def _handle_function_call(self, function_call):
        """處理 function call"""
        function_name = function_call.name
        args = dict(function_call.args)
        
        logger.info(f"Handling function call: {function_name} with args: {args}")
        
        if function_name == "create_calendar_event":
            return self._create_event_handler(args)
        elif function_name == "list_calendar_events":
            return self._list_events_handler(args)
        elif function_name == "delete_calendar_event":
            return self._delete_event_handler(args)
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    def _create_event_handler(self, args):
        """處理建立事件的請求"""
        try:
            # 解析日期和時間
            date_str = args.get('date')
            time_str = args.get('time', '09:00')
            duration = args.get('duration_hours', 1)
            
            # 建立 datetime 物件
            datetime_str = f"{date_str}T{time_str}:00"
            start_time = datetime.fromisoformat(datetime_str)
            end_time = start_time + timedelta(hours=duration)
            
            # 呼叫 Calendar Service
            result = self.calendar_service.create_event(
                summary=args.get('summary'),
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                description=args.get('description'),
                location=args.get('location')
            )
            
            if result.get('success'):
                message = f"✅ 已成功建立行程「{args.get('summary')}」\n"
                message += f"📅 時間：{date_str} {time_str}\n"
                message += f"⏱️ 長度：{duration} 小時\n"
                if args.get('location'):
                    message += f"📍 地點：{args.get('location')}\n"
                if result.get('link'):
                    message += f"🔗 連結：{result.get('link')}"
                
                logger.info(f"Calendar event created: {result}")
                
                return {
                    "success": True,
                    "message": message,
                    "event_id": result.get('event_id'),
                    "link": result.get('link')
                }
            else:
                error_msg = result.get('error', '未知錯誤')
                logger.error(f"Failed to create calendar event: {error_msg}")
                
                return {
                    "success": False,
                    "message": f"❌ 建立行程失敗：{error_msg}",
                    "error": error_msg
                }
                
        except Exception as e:
            logger.error(f"Error creating event: {str(e)}")
            return {
                "success": False,
                "message": "建立行程時發生錯誤",
                "error": str(e)
            }
    
    def _list_events_handler(self, args):
        """處理查詢事件的請求"""
        try:
            # 解析查詢參數
            date_str = args.get('date', 'today')
            days_ahead = args.get('days_ahead', 1)
            
            # 計算時間範圍
            if date_str == 'today':
                start_date = datetime.now()
            elif date_str == 'tomorrow':
                start_date = datetime.now() + timedelta(days=1)
            else:
                start_date = datetime.fromisoformat(date_str)
            
            # 設定為當天開始
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # 查詢行程
            result = self.calendar_service.list_events(
                max_results=10,
                time_min=start_date.isoformat() + 'Z'
            )
            
            if result.get('success'):
                events = result.get('events', [])
                if not events:
                    return {
                        "success": True,
                        "message": "沒有找到任何行程",
                        "events": []
                    }
                
                # 格式化事件列表
                formatted_events = []
                for event in events:
                    formatted_events.append(
                        self.calendar_service.format_event_for_display(event)
                    )
                
                return {
                    "success": True,
                    "message": f"找到 {len(events)} 個行程",
                    "events": formatted_events
                }
            else:
                return {
                    "success": False,
                    "message": "查詢行程失敗",
                    "error": result.get('error')
                }
                
        except Exception as e:
            logger.error(f"Error listing events: {str(e)}")
            return {
                "success": False,
                "message": "查詢行程時發生錯誤",
                "error": str(e)
            }
    
    def _delete_event_handler(self, args):
        """處理刪除事件的請求"""
        try:
            event_id = args.get('event_id')
            result = self.calendar_service.delete_event(event_id)
            
            if result.get('success'):
                return {
                    "success": True,
                    "message": "已成功刪除行程"
                }
            else:
                return {
                    "success": False,
                    "message": "刪除行程失敗",
                    "error": result.get('error')
                }
                
        except Exception as e:
            logger.error(f"Error deleting event: {str(e)}")
            return {
                "success": False,
                "message": "刪除行程時發生錯誤",
                "error": str(e)
            }
    
    def _build_context(self, user_id: str, message: str) -> str:
        """建立包含對話歷史的上下文"""
        # 系統提示詞
        system_prompt = """你是一個友善的 AI 助理，請用繁體中文回答。
請保持回答簡潔清楚，並且親切有禮。
如果使用者詢問你的身份，請告訴他們你是 Persona Cruz AI 助理。

你可以幫助使用者管理 Google Calendar：
- 建立新的行程（例如：幫我安排明天下午3點開會）
- 查詢行程（例如：我明天有什麼行程？）
- 刪除行程（需要提供事件ID）

當使用者要求日曆相關操作時，請使用提供的函數來完成。"""
        
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