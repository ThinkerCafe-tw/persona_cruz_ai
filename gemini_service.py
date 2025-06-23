import google.generativeai as genai
from config import Config
import logging
import json
from datetime import datetime, timedelta
from typing import Optional
from calendar_service import CalendarService
from five_elements_agent import FiveElementsAgent

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
        
        # 初始化五行系統
        self.five_elements = FiveElementsAgent()
        self.element_mode = False  # 是否啟用五行模式
        
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
            # 初始化 final_response
            final_response = None
            
            # 檢查是否是五行系統指令
            if message.strip() in ["/dashboard", "/狀態", "/儀表板"]:
                return self.five_elements.get_dashboard()
            elif message.strip() in ["/status", "/mini", "/簡報"]:
                return self.five_elements.get_mini_dashboard()
            elif message.strip() in ["/harmony", "/和諧度"]:
                return self.five_elements.get_harmony_status()
            
            # 如果是簡單的日曆請求且 calendar_service 不可用，直接回應
            if self.calendar_service is None and any(keyword in message for keyword in ['行程', '安排', '會議', '約會']):
                return "抱歉，日曆功能目前無法使用。請確認日曆服務已正確設定。"
            # 初始化使用者對話歷史
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # 建立對話上下文
            context = self._build_context(user_id, message)
            
            # 記錄開始時間
            start_time = datetime.now()
            
            # 判斷當前使用的元素（如果有的話）
            current_element = self.five_elements.current_role.element if self.five_elements.current_role else "火"
            
            # 呼叫 Gemini API with Function Calling
            logger.info(f"=== Calling Gemini API ===")
            logger.info(f"User ID: {user_id}")
            logger.info(f"Message: {message}")
            logger.info(f"Context length: {len(context)} chars")
            logger.info(f"Current Element: {current_element}")
            
            response = self.model.generate_content(context)
            logger.info(f"✅ Gemini API response received")
            logger.info(f"Response type: {type(response)}")
            logger.info(f"Has candidates: {hasattr(response, 'candidates')}")
            
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
                                logger.info(f"✅ Using function response message directly")
                                logger.info(f"Message length: {len(final_response)}")
                                logger.info(f"Message preview: {final_response[:200]}...")
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
                            
                            # 找到 function call 後就跳出迴圈
                            break
            
            # 如果不是 function call，取得一般回應
            if final_response is None:
                if hasattr(response, 'text'):
                    final_response = response.text
                else:
                    final_response = "抱歉，我無法理解您的訊息。"
            
            # 確保 final_response 不是 None
            if final_response is None:
                final_response = "抱歉，我無法處理您的請求。"
                logger.warning("final_response was None, using default message")
            
            # 儲存對話歷史
            self._save_conversation(user_id, message, final_response)
            
            # 計算響應時間並更新指標
            response_time = (datetime.now() - start_time).total_seconds()
            self.five_elements.update_metrics(current_element, success=True, response_time=response_time)
            
            # 如果有角色切換，記錄流程
            if self.five_elements.current_role:
                self.five_elements.record_flow("用戶", current_element, "對話")
            
            logger.info(f"=== Returning final response ===")
            logger.info(f"Response length: {len(final_response)}")
            logger.info(f"Response preview: {final_response[:200]}...")
            logger.info(f"Response time: {response_time:.2f}s")
            
            return final_response
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # 更新錯誤指標
            if hasattr(self, 'five_elements'):
                current_element = self.five_elements.current_role.element if self.five_elements.current_role else "火"
                response_time = (datetime.now() - start_time).total_seconds() if 'start_time' in locals() else 0
                self.five_elements.update_metrics(current_element, success=False, response_time=response_time)
            
            # 如果是日曆相關錯誤，提供更具體的訊息
            if "calendar" in str(e).lower():
                return "抱歉，我在處理日曆功能時遇到問題。請確認您已經分享日曆給我。"
            else:
                return "抱歉，我現在無法回應您的訊息。請稍後再試。"
    
    def _handle_function_call(self, function_call):
        """處理 function call"""
        function_name = function_call.name
        args = dict(function_call.args)
        
        logger.info(f"=== Handling function call ===")
        logger.info(f"Function name: {function_name}")
        logger.info(f"Arguments: {args}")
        
        result = None
        if function_name == "create_calendar_event":
            result = self._create_event_handler(args)
        elif function_name == "list_calendar_events":
            result = self._list_events_handler(args)
        elif function_name == "delete_calendar_event":
            result = self._delete_event_handler(args)
        else:
            result = {"error": f"Unknown function: {function_name}"}
            
        logger.info(f"Function call result: {result}")
        return result
    
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
                
                logger.info(f"✅ Calendar event created successfully")
                logger.info(f"CalendarService result: {result}")
                logger.info(f"Generated message: {message}")
                
                return_value = {
                    "success": True,
                    "message": message,
                    "event_id": result.get('event_id'),
                    "link": result.get('link')
                }
                logger.info(f"Returning: {return_value}")
                return return_value
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
        
        # 檢查是否需要切換角色或使用五行系統
        element_context = self._check_element_trigger(message)
        
        # 根據是否啟用五行模式選擇不同的系統提示詞
        if element_context:
            system_prompt = element_context
        else:
            # 原本的系統提示詞
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
    
    def _check_element_trigger(self, message: str) -> Optional[str]:
        """檢查是否需要啟動五行系統"""
        message_lower = message.lower()
        
        # 特定觸發詞
        element_triggers = {
            "五行": "分析",
            "卡住": "無極",
            "debug": "分析",
            "測試": "水",
            "開發": "火",
            "架構": "土",
            "優化": "金",
            "需求": "木"
        }
        
        # 檢查是否有觸發詞
        for trigger, suggested_element in element_triggers.items():
            if trigger in message_lower:
                if suggested_element == "分析":
                    # 讓無極分析適合的角色
                    analysis = self.five_elements.analyze_situation(message)
                    suggested_element = analysis["suggested_element"]
                
                # 切換角色並返回角色提示詞
                self.five_elements.switch_role(suggested_element)
                return self.five_elements.get_role_prompt(suggested_element)
        
        # 檢查是否明確要求某個角色
        role_requests = {
            "火": ["開發專員", "快速實作", "寫程式"],
            "水": ["測試專員", "找bug", "檢查"],
            "木": ["產品經理", "規劃", "功能設計"],
            "土": ["架構師", "系統設計", "穩定性"],
            "金": ["優化專員", "重構", "效能"],
            "無極": ["觀察", "分析情況", "系統狀態"]
        }
        
        for element, keywords in role_requests.items():
            for keyword in keywords:
                if keyword in message_lower:
                    self.five_elements.switch_role(element)
                    return self.five_elements.get_role_prompt(element)
        
        return None