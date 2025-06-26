#!/usr/bin/env python3
"""
進度檢查工具 - 快速查看 14 天 MVP 進度
"""
import json
import os
from datetime import datetime
from pathlib import Path

def load_progress():
    """載入進度資料"""
    status_file = Path("memory_api/api_status.json")
    if status_file.exists():
        with open(status_file) as f:
            return json.load(f)
    return None

def print_progress_bar(progress, width=50):
    """打印進度條"""
    filled = int(width * progress / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {progress:.1f}%"

def main():
    """主程式"""
    print("\n🚀 Persona CRUZ AI - 14 Day MVP Progress Tracker\n")
    
    data = load_progress()
    if not data:
        print("❌ 無法載入進度資料")
        return
    
    # 總體進度
    print(f"📅 Day {data['current_day']}/14")
    print(f"📊 總體進度: {print_progress_bar(data['progress_percentage'])}")
    print()
    
    # 里程碑狀態
    print("🏆 里程碑狀態:")
    for milestone_id, milestone in data['milestones'].items():
        status_emoji = "✅" if milestone['status'] == "completed" else "⏳" if milestone['status'] == "in_progress" else "🔒"
        print(f"  {status_emoji} {milestone_id}: Day {milestone['target_day']} - {milestone['completion']}%")
        if milestone['status'] == "in_progress":
            print(f"     功能: {', '.join(milestone['features'])}")
    print()
    
    # 關鍵指標
    print("📈 關鍵指標:")
    metrics = data['metrics']
    print(f"  • 代碼行數: {metrics['code_lines']} 行")
    print(f"  • API 端點: {metrics['api_endpoints']} 個")
    print(f"  • 測試覆蓋: {metrics['test_coverage']}%")
    print(f"  • 響應時間: {metrics['response_time_ms']}ms")
    print(f"  • 搜索準確率: {metrics['search_accuracy']}%")
    print()
    
    # 團隊速度
    velocity = data['team_velocity']
    print("⚡ 團隊速度:")
    print(f"  • 預期: {velocity['expected_features_per_day']} 功能/天")
    print(f"  • 實際: {velocity['actual_features_per_day']} 功能/天")
    print(f"  • 加速倍數: {velocity['velocity_multiplier']}x")
    print()
    
    # 今日目標
    print("🎯 接下來 24 小時目標:")
    for i, goal in enumerate(data['next_24h_goals'], 1):
        print(f"  {i}. {goal}")
    print()
    
    # API 健康狀態
    health = data['api_health']
    print(f"💚 API 狀態: {health['status'].upper()} | 運行時間: {health['uptime']}")
    print()
    
    # 馬斯克語錄
    musk_quotes = [
        "If you're not failing, you're not innovating enough.",
        "The best part is no part.",
        "Move fast and break things... then fix them faster."
    ]
    import random
    print(f"🚀 馬斯克說: \"{random.choice(musk_quotes)}\"")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()