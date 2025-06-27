#!/usr/bin/env python3
"""
量子記憶漣漪記錄器 (Quantum Memory Ripple Logger)

這是一個指令行工具，用於將事件（漣漪）記錄到指定角色的量子記憶中。
"""
import argparse
import os
import sys
from datetime import datetime

# 確保可以從 scripts 目錄導入上層模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum_memory.quantum_memory import QuantumMemory

def log_ripple(persona_id: str, message: str, tags: list[str] = None, event_type: str = "insight"):
    """
    記錄一個新的漣漪到指定的量子記憶中。

    Args:
        persona_id (str): 角色的 ID (例如 'cruz', 'fire', 'wuji').
        message (str): 要記錄的事件內容。
        tags (list[str], optional): 事件的標籤. Defaults to None.
        event_type (str, optional): 事件類型. Defaults to "insight".
    """
    # 確保記憶檔案存在
    memory_file = f"quantum_memory/memories/{persona_id}.json"
    if not os.path.exists(memory_file):
        print(f"❌ 錯誤：找不到角色 '{persona_id}' 的記憶檔案。請先初始化。")
        return

    # 載入量子記憶 (這裡我們先禁用資料庫，專注於檔案操作)
    memory = QuantumMemory(persona_id, use_database=False)
    memory.load()

    # 建立事件物件
    event = {
        "type": event_type,
        "content": message,
        "source": "cli_logger",
        "tags": tags if tags else []
    }

    # 添加漣漪並保存
    memory.add_ripple(event)
    memory.save()
    
    # 產生並顯示更新後的摘要
    summary = memory.to_summary()
    
    print(f"💧 漣漪已成功記錄到 '{persona_id}' 的記憶中。")
    print("\n" + "="*50)
    print(f"AI人格 {persona_id} 的記憶場更新預覽：")
    print(summary)
    print("="*50)


def main():
    """主函數，處理指令行參數"""
    parser = argparse.ArgumentParser(
        description="量子記憶漣漪記錄器 - 將事件記錄到 AI 人格的記憶中。",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
使用範例:
  python scripts/log_ripple.py cruz "決定採納 3E 原則" --tags strategy,decision
  python scripts/log_ripple.py fire "完成了 log_ripple.py 的初步開發" --type breakthrough
  python scripts/log_ripple.py wood "思考如何讓摘要體驗更好" --tags ux,design
"""
    )
    
    parser.add_argument(
        "persona_id",
        type=str,
        help="要記錄到的角色 ID (例如: cruz, fire, wuji, wood, earth, metal, water)"
    )
    
    parser.add_argument(
        "message",
        type=str,
        help="要記錄的事件內容或訊息"
    )
    
    parser.add_argument(
        "--tags",
        nargs='*',
        default=[],
        help="為事件加上標籤 (可選，多個標籤用空格分開)"
    )

    parser.add_argument(
        "--type",
        type=str,
        default="insight",
        help="事件類型 (例如: insight, breakthrough, failure, decision), 預設為 'insight'"
    )
    
    args = parser.parse_args()
    
    log_ripple(args.persona_id, args.message, args.tags, args.type)

if __name__ == "__main__":
    main() 