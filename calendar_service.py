import os
import json
import logging
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class CalendarService:
    """Google Calendar 服務整合"""
    
    def __init__(self):
        """初始化 Google Calendar 服務"""
        self.service = None
        self.calendar_id = 'primary'
        self._initialize_service()
    
    def _initialize_service(self):
        """初始化 Google Calendar API 服務"""
        try:
            # 使用服務帳戶憑證（適合後端應用）
            credentials_json = os.getenv('GOOGLE_CALENDAR_CREDENTIALS')
            if credentials_json:
                credentials_info = json.loads(credentials_json)
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
            else:
                # 如果沒有設定服務帳戶，使用簡化模式（需要後續設定）
                logger.warning("Google Calendar credentials not found. Calendar features will be limited.")
                return
            
            self.service = build('calendar', 'v3', credentials=credentials)
            logger.info("Google Calendar service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Calendar service: {str(e)}")
    
    def list_events(self, max_results=10, time_min=None):
        """列出即將到來的行程"""
        if not self.service:
            return {"error": "Calendar service not initialized"}
        
        try:
            if not time_min:
                time_min = datetime.utcnow().isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return {"success": True, "events": events}
            
        except HttpError as error:
            logger.error(f'An error occurred: {error}')
            return {"error": str(error)}
    
    def create_event(self, summary, start_time, end_time=None, description=None, location=None):
        """建立新的行程"""
        if not self.service:
            return {"error": "Calendar service not initialized"}
        
        try:
            # 如果沒有指定結束時間，預設為開始時間後1小時
            if not end_time:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                end_dt = start_dt + timedelta(hours=1)
                end_time = end_dt.isoformat()
            
            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'Asia/Taipei',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'Asia/Taipei',
                }
            }
            
            if description:
                event['description'] = description
            if location:
                event['location'] = location
            
            event = self.service.events().insert(
                calendarId=self.calendar_id, 
                body=event
            ).execute()
            
            return {
                "success": True, 
                "event_id": event.get('id'),
                "link": event.get('htmlLink')
            }
            
        except HttpError as error:
            logger.error(f'An error occurred: {error}')
            return {"error": str(error)}
    
    def delete_event(self, event_id):
        """刪除行程"""
        if not self.service:
            return {"error": "Calendar service not initialized"}
        
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            return {"success": True, "message": "Event deleted successfully"}
            
        except HttpError as error:
            logger.error(f'An error occurred: {error}')
            return {"error": str(error)}
    
    def update_event(self, event_id, updates):
        """更新行程"""
        if not self.service:
            return {"error": "Calendar service not initialized"}
        
        try:
            # 先獲取現有事件
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            # 更新欄位
            for key, value in updates.items():
                if key in ['summary', 'description', 'location']:
                    event[key] = value
                elif key == 'start_time':
                    event['start'] = {
                        'dateTime': value,
                        'timeZone': 'Asia/Taipei',
                    }
                elif key == 'end_time':
                    event['end'] = {
                        'dateTime': value,
                        'timeZone': 'Asia/Taipei',
                    }
            
            updated_event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            return {
                "success": True,
                "event_id": updated_event.get('id'),
                "link": updated_event.get('htmlLink')
            }
            
        except HttpError as error:
            logger.error(f'An error occurred: {error}')
            return {"error": str(error)}
    
    def format_event_for_display(self, event):
        """格式化事件以便顯示"""
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        
        # 轉換為台北時間
        formatted_time = start_dt.strftime('%m/%d %H:%M')
        
        summary = event.get('summary', '無標題')
        location = event.get('location', '')
        
        display_text = f"📅 {formatted_time} - {summary}"
        if location:
            display_text += f"\n📍 {location}"
        
        return display_text