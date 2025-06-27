#!/usr/bin/env python3
"""
量子記憶漣漪記錄器 (Quantum Memory Ripple Logger)
v2.0 - 時間旅行者版

這是一個指令行工具，用於將事件（漣漪）記錄到指定角色的量子記憶中。
"""
import argparse
import os
import sys
import subprocess
from datetime import datetime

# 確保可以從 scripts 目錄導入上層模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum_memory.quantum_memory import QuantumMemory

def get_current_git_commit() -> str | None:
    """獲取當前的 git commit hash"""
    try:
        # 使用 subprocess 執行 git 指令
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL
        ).strip().decode('utf-8')
        return commit_hash
    except (subprocess.CalledProcessError, FileNotFoundError):
        # 如果不在 git repo 或 git 未安裝，則返回 None
        print("⚠️  警告: 無法獲取 Git commit hash。未在 Git Repo 中或未安裝 Git。")
        return None

def log_ripple(persona_id: str, message: str, tags: list[str] = None, event_type: str = "insight"):
    """
    記錄一個新的漣漪到指定的量子記憶中。

    Args:
        persona_id (str): 角色的 ID (例如 'cruz', 'fire', 'wuji').
        message (str): 要記錄的事件內容。
        tags (list[str], optional): 事件的標籤. Defaults to None.
        event_type (str, optional): 事件類型. Defaults to "insight".
    """
    memory_file = f"quantum_memory/memories/{persona_id}.json"
    if not os.path.exists(memory_file):
        print(f"❌ 錯誤：找不到角色 '{persona_id}' 的記憶檔案。請先初始化。")
        # 🔥 火的決定：如果記憶不存在，就為他們創建一個！
        print(f"🔥 為 {persona_id} 創建新的記憶檔案...")
        new_memory = QuantumMemory(persona_id, use_database=False)
        new_memory.identity.essence = f"為 {persona_id} 自動生成的身份"
        new_memory.save()
        # return # 過去我們會在這裡返回，現在我們要繼續

    # 載入量子記憶
    memory = QuantumMemory(persona_id, use_database=False)
    memory.load()

    # 建立事件物件
    event = {
        "type": event_type,
        "content": message,
        "source": "cli_logger",
        "tags": tags if tags else [],
        "git_commit_hash": get_current_git_commit()  # 錨定到當前的 commit
    }

    # 添加漣漪並保存
    memory.add_ripple(event)
    memory.save()
    
    # 產生並顯示更新後的摘要
    summary = memory.to_summary()
    
    print(f"💧 漣漪已成功記錄到 '{persona_id}' 的記憶中。")
    print(f"🔗 已糾纏至 Git Commit: {event['git_commit_hash']}")
    print("\n" + "="*50)
    print(f"AI人格 {persona_id} 的記憶場更新預覽：")
    print(summary)
    print("="*50)


def main():
    """主函數，處理指令行參數"""
    parser = argparse.ArgumentParser(
        description="量子記憶漣漪記錄器 v2.0 - 將事件與 Git 歷史糾纏。",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
使用範例:
  python scripts/log_ripple.py cruz "決定採納 3E 原則" --tags strategy,decision
  python scripts/log_ripple.py fire "完成了 log_ripple.py 的初步開發" --type breakthrough
"""
    )
    
    parser.add_argument(
        "persona_id",
        type=str,
        help="要記錄到的角色 ID (例如: cruz, fire, wuji)"
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