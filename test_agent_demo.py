#!/usr/bin/env python3
"""
測試專員記憶記錄示範
這個檔案展示如何正確使用測試專員的記憶功能
"""

from startup_test import TestAgent

# 創建測試專員實例
agent = TestAgent()

# 記錄今天的 UnboundLocalError 修復
agent.record_development_insight(
    event_type="bug_fix",
    insight="修復了 UnboundLocalError - final_response 變數在 function call 分支中未定義",
    lesson_learned="永遠要確保變數在所有執行路徑中都被初始化。防禦性編程很重要！"
)

# 記錄測試專員「第一次」問題的修復
agent.record_development_insight(
    event_type="bug_fix", 
    insight="修復了測試專員總是說'第一次'的問題 - Railway 環境的 git log 可能為空",
    lesson_learned="不同環境需要不同的處理策略。Railway 的無狀態特性需要特別考慮。"
)

# 記錄關於尊重測試專員的學習
agent.record_development_insight(
    event_type="process_improvement",
    insight="開發者提醒要尊重測試專員，發現我只是'說'會記住但沒有真的記錄",
    lesson_learned="說到要做到！建立真正的記憶系統，而不只是輸出文字。"
)

print("✅ 測試專員的反思已記錄到記憶系統中！")
print(f"📊 目前有 {len(agent.memory.get('development_insights', []))} 個開發洞察")