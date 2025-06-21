import os
import sys
import time
import logging
from datetime import datetime
import google.generativeai as genai
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

logger = logging.getLogger(__name__)

class StartupTest:
    """啟動時自我檢測系統"""
    
    def __init__(self):
        self.start_time = time.time()
        self.tests = []
        self.results = {}
        self.critical_failures = []
        self.warnings = []
        
    def run_all_tests(self) -> bool:
        """執行所有啟動測試"""
        print("\n" + "="*50)
        print("🔍 執行啟動自我檢測...")
        print("="*50)
        
        # 執行各項測試
        self._test_environment_variables()
        self._test_gemini_connection()
        self._test_line_bot_credentials()
        self._test_google_calendar()
        self._test_basic_ai_response()
        
        # 計算測試時間
        self.test_duration = time.time() - self.start_time
        
        # 顯示測試報告
        self._print_report()
        
        # 返回是否所有關鍵測試都通過
        return len(self.critical_failures) == 0
    
    def _test_environment_variables(self):
        """測試環境變數"""
        test_name = "環境變數檢查"
        try:
            required_vars = {
                'LINE_CHANNEL_ACCESS_TOKEN': os.getenv('LINE_CHANNEL_ACCESS_TOKEN'),
                'LINE_CHANNEL_SECRET': os.getenv('LINE_CHANNEL_SECRET'),
                'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY')
            }
            
            missing_vars = [var for var, value in required_vars.items() if not value]
            
            if missing_vars:
                self.results[test_name] = "❌ 失敗"
                self.critical_failures.append(f"缺少必要環境變數: {', '.join(missing_vars)}")
            else:
                self.results[test_name] = "✅ 通過"
                
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"環境變數檢查錯誤: {str(e)}")
    
    def _test_gemini_connection(self):
        """測試 Gemini API 連線"""
        test_name = "Gemini API 連線"
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                self.results[test_name] = "⏭️ 跳過"
                self.warnings.append("未設定 Gemini API Key")
                return
                
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # 發送簡單測試
            response = model.generate_content("回應OK即可")
            if response.text:
                self.results[test_name] = "✅ 通過"
            else:
                self.results[test_name] = "❌ 失敗"
                self.critical_failures.append("Gemini API 無回應")
                
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"Gemini 連線錯誤: {str(e)}")
    
    def _test_line_bot_credentials(self):
        """測試 Line Bot 憑證"""
        test_name = "Line Bot 設定"
        try:
            token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
            secret = os.getenv('LINE_CHANNEL_SECRET')
            
            if not token or not secret:
                self.results[test_name] = "❌ 失敗"
                self.critical_failures.append("Line Bot 憑證不完整")
                return
            
            # 驗證 token 格式
            if len(token) < 100 or len(secret) < 20:
                self.results[test_name] = "⚠️ 警告"
                self.warnings.append("Line Bot 憑證格式可能有誤")
            else:
                self.results[test_name] = "✅ 通過"
                
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"Line Bot 設定錯誤: {str(e)}")
    
    def _test_google_calendar(self):
        """測試 Google Calendar 服務"""
        test_name = "Google Calendar"
        try:
            credentials = os.getenv('GOOGLE_CALENDAR_CREDENTIALS')
            
            if not credentials:
                self.results[test_name] = "⏭️ 跳過"
                self.warnings.append("未設定 Google Calendar（選用功能）")
                return
            
            # 嘗試解析 JSON
            import json
            json.loads(credentials)
            self.results[test_name] = "✅ 通過"
            
        except json.JSONDecodeError:
            self.results[test_name] = "⚠️ 警告"
            self.warnings.append("Google Calendar 憑證格式錯誤")
        except Exception as e:
            self.results[test_name] = "⚠️ 警告"
            self.warnings.append(f"Google Calendar 設定問題: {str(e)}")
    
    def _test_basic_ai_response(self):
        """測試基本 AI 功能"""
        test_name = "基本 AI 功能"
        try:
            # 簡單測試 import 是否成功
            from gemini_service import GeminiService
            from line_bot_handler import LineBotHandler
            
            self.results[test_name] = "✅ 通過"
            
        except ImportError as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"模組載入失敗: {str(e)}")
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"基本功能錯誤: {str(e)}")
    
    def _print_report(self):
        """列印測試報告"""
        print("\n" + "="*50)
        print("📊 啟動檢測報告")
        print("="*50)
        
        # 顯示各項測試結果
        for test, result in self.results.items():
            print(f"{result} {test}")
        
        # 顯示警告
        if self.warnings:
            print("\n⚠️  警告訊息:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        # 顯示嚴重錯誤
        if self.critical_failures:
            print("\n❌ 嚴重錯誤:")
            for error in self.critical_failures:
                print(f"   - {error}")
        
        # 總結
        print(f"\n測試時間: {self.test_duration:.2f} 秒")
        print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.critical_failures:
            print("\n狀態: ❌ 啟動失敗")
        else:
            print("\n狀態: ✅ 準備就緒")
        
        print("="*50 + "\n")
    
    def get_status(self) -> dict:
        """取得測試狀態（供健康檢查使用）"""
        return {
            "startup_test_passed": len(self.critical_failures) == 0,
            "test_results": self.results,
            "warnings": self.warnings,
            "errors": self.critical_failures,
            "test_duration": getattr(self, 'test_duration', 0),
            "test_time": datetime.now().isoformat()
        }