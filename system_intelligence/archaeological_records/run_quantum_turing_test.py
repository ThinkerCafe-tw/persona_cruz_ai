#!/usr/bin/env python3
"""
快速執行量子記憶圖靈測試
"""
import subprocess
import sys
import os

def run_test():
    """執行測試並顯示結果"""
    print("🚀 啟動量子記憶圖靈測試...")
    print("=" * 60)
    
    # 執行測試腳本
    test_script = os.path.join("tests", "test_quantum_memory_turing.py")
    
    try:
        result = subprocess.run(
            [sys.executable, test_script],
            capture_output=False,  # 直接顯示輸出
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ 測試執行成功！系統通過所有測試。")
        elif result.returncode == 1:
            print("\n⚠️ 測試完成，但有部分測試未通過。")
        else:
            print("\n❌ 測試執行過程中發生錯誤。")
            
        return result.returncode
        
    except Exception as e:
        print(f"\n❌ 無法執行測試：{e}")
        return 2

if __name__ == "__main__":
    sys.exit(run_test())