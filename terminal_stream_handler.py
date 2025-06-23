"""
終端串流處理器
捕捉終端對話並轉發到 AI 系統
"""
import sys
import threading
import queue
import time
import logging
from typing import Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)

class TerminalStreamHandler:
    """終端串流處理器"""
    
    def __init__(self, process_callback: Optional[Callable] = None):
        self.process_callback = process_callback
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.running = False
        self.conversation_log = []
        
    def start(self):
        """開始監聽終端輸入輸出"""
        self.running = True
        
        # 啟動輸入監聽執行緒
        input_thread = threading.Thread(target=self._monitor_input, daemon=True)
        input_thread.start()
        
        # 啟動處理執行緒
        process_thread = threading.Thread(target=self._process_stream, daemon=True)
        process_thread.start()
        
        logger.info("Terminal stream handler started")
        
    def stop(self):
        """停止監聽"""
        self.running = False
        logger.info("Terminal stream handler stopped")
        
    def _monitor_input(self):
        """監聽終端輸入"""
        while self.running:
            try:
                # 這是簡化版本，實際實作需要更複雜的輸入捕捉
                user_input = input()
                if user_input:
                    self.input_queue.put({
                        "type": "user_input",
                        "content": user_input,
                        "timestamp": datetime.now().isoformat()
                    })
            except Exception as e:
                logger.error(f"Input monitoring error: {e}")
                
    def _process_stream(self):
        """處理串流數據"""
        while self.running:
            try:
                # 處理輸入佇列
                if not self.input_queue.empty():
                    data = self.input_queue.get()
                    self._handle_stream_data(data)
                    
                # 小延遲避免 CPU 過載
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Stream processing error: {e}")
                
    def _handle_stream_data(self, data: dict):
        """處理串流數據"""
        # 記錄到對話日誌
        self.conversation_log.append(data)
        
        # 如果有回調函數，調用它
        if self.process_callback:
            try:
                result = self.process_callback(data)
                if result:
                    self.output_queue.put(result)
            except Exception as e:
                logger.error(f"Callback processing error: {e}")
                
    def get_recent_conversation(self, limit: int = 10) -> list:
        """獲取最近的對話記錄"""
        return self.conversation_log[-limit:]
    
    def clear_log(self):
        """清除對話記錄"""
        self.conversation_log.clear()
        

class StreamToAI:
    """串流到 AI 的橋接器"""
    
    def __init__(self, ai_endpoint: Optional[str] = None):
        self.ai_endpoint = ai_endpoint
        self.stream_handler = TerminalStreamHandler(self.process_for_ai)
        self.ai_context = []
        
    def process_for_ai(self, data: dict) -> Optional[dict]:
        """處理數據並發送到 AI"""
        # 這裡簡化處理，實際需要連接到 Claude/GPT API
        if data["type"] == "user_input":
            # 構建 AI 請求
            ai_request = {
                "role": "user",
                "content": data["content"],
                "timestamp": data["timestamp"]
            }
            
            # 加入上下文
            self.ai_context.append(ai_request)
            
            # 這裡應該調用實際的 AI API
            # response = self.call_ai_api(self.ai_context)
            
            # 模擬 AI 回應
            ai_response = {
                "role": "assistant",
                "content": f"CRUZ: 收到你說的 '{data['content']}'",
                "timestamp": datetime.now().isoformat()
            }
            
            self.ai_context.append(ai_response)
            
            return ai_response
            
        return None
    
    def start_streaming(self):
        """開始串流"""
        self.stream_handler.start()
        print("🎯 CRUZ 終端串流已啟動...")
        print("（這是原型版本，完整功能需要整合 API）")
        
    def stop_streaming(self):
        """停止串流"""
        self.stream_handler.stop()
        

# 簡單的示範程式
if __name__ == "__main__":
    print("=== 終端串流處理器示範 ===")
    print("這是一個概念驗證，展示如何捕捉終端對話")
    print("實際實作需要：")
    print("1. 整合實際的 Claude/GPT API")
    print("2. 實作語音轉換（TTS/STT）")
    print("3. 更複雜的輸入輸出捕捉機制")
    print("\n輸入 'quit' 結束程式\n")
    
    # 創建串流處理器
    stream_to_ai = StreamToAI()
    
    # 自訂處理函數
    def custom_processor(data):
        if data["type"] == "user_input":
            content = data["content"]
            if content.lower() == "quit":
                stream_to_ai.stop_streaming()
                print("再見！")
                sys.exit(0)
            else:
                # 這裡可以加入 CRUZ 開發者模式的整合
                print(f"[處理中] {content}")
                return {
                    "type": "ai_response",
                    "content": f"我理解了：{content}",
                    "timestamp": datetime.now().isoformat()
                }
    
    # 設置自訂處理器
    stream_to_ai.stream_handler.process_callback = custom_processor
    
    # 開始串流
    try:
        stream_to_ai.start_streaming()
        
        # 保持程式運行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n程式中斷")
        stream_to_ai.stop_streaming()