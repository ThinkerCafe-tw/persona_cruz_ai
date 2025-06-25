#!/usr/bin/env python3
"""
量子記憶系統圖靈測試 - 只記錄輸入
測試測試腳本是否能正確接收來自使用者的提示詞
"""
import time
import sys
import os
import json
from datetime import datetime

# 添加專案根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 確保載入環境變數
from dotenv import load_dotenv
load_dotenv()

class QuantumMemoryTuringTestInput:
    """測試輸入記錄器"""
    
    def __init__(self):
        self.test_user_id = f"quantum_turing_test_{int(time.time())}"
        
    def test_record_inputs(self):
        """記錄三段測試提示詞"""
        print("\n" + "="*60)
        print("🧪 量子記憶圖靈測試 - 輸入記錄")
        print("="*60)
        
        # 測試1提示詞
        prompt_1 = "請記住這個獨特的量子座標：QM-2024-螢火蟲-42-薰衣草。同時告訴我你會如何儲存這個記憶，包括它在 pgvector 中的向量維度。"
        print(f"\n[測試 1] 基礎記憶持久化")
        print(f"提示詞：{prompt_1}")
        print(f"長度：{len(prompt_1)} 字元")
        
        # 測試2提示詞
        prompt_2 = "我曾經跟你提過一個關於昆蟲的座標。請使用向量相似度搜尋找出這個記憶，並告訴我搜尋的技術細節。"
        print(f"\n[測試 2] 語義相似度搜尋")
        print(f"提示詞：{prompt_2}")
        print(f"長度：{len(prompt_2)} 字元")
        
        # 測試3提示詞
        prompt_3 = """創建一個新的量子記憶晶體，概念是『薛丁格的貓』，包含三個可能性：
1) 貓是活的(0.5)
2) 貓是死的(0.5) 
3) 貓在跳舞(0.0)

然後觸發『觀察者打開盒子』事件，展示演化結果。"""
        print(f"\n[測試 3] 量子疊加態演化")
        print(f"提示詞：{prompt_3}")
        print(f"長度：{len(prompt_3)} 字元")
        
        # 儲存提示詞
        prompts_data = {
            "test_id": self.test_user_id,
            "timestamp": datetime.now().isoformat(),
            "prompts": {
                "test_1": {
                    "name": "基礎記憶持久化",
                    "prompt": prompt_1,
                    "expected_keywords": ["pgvector", "384", "向量", "晶體", "儲存"]
                },
                "test_2": {
                    "name": "語義相似度搜尋",
                    "prompt": prompt_2,
                    "expected_keywords": ["相似", "向量", "餘弦", "搜尋", "螢火蟲"]
                },
                "test_3": {
                    "name": "量子疊加態演化",
                    "prompt": prompt_3,
                    "expected_keywords": ["機率", "演化", "熵", "坍縮", "可能性"]
                }
            }
        }
        
        # 儲存到檔案
        with open("test_prompts_record.json", "w", encoding="utf-8") as f:
            json.dump(prompts_data, f, ensure_ascii=False, indent=2)
        
        print("\n✅ 提示詞已記錄到 test_prompts_record.json")
        
        return prompts_data

def main():
    tester = QuantumMemoryTuringTestInput()
    tester.test_record_inputs()

if __name__ == "__main__":
    main()