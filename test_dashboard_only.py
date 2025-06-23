#!/usr/bin/env python3
"""
純粹測試 Dashboard 功能（不需要 API）
"""
from five_elements_agent import FiveElementsAgent

def test_dashboard_features():
    """測試 Dashboard 的各種功能"""
    print("=== 測試 Dashboard 功能 ===\n")
    
    agent = FiveElementsAgent()
    
    # 1. 初始狀態
    print("1. 初始狀態")
    print(agent.get_mini_dashboard())
    print()
    
    # 2. 模擬正常工作流程
    print("2. 模擬正常工作流程")
    # 木 → 火（需求到開發）
    agent.switch_role("木")
    agent.record_flow("木", "火", "需求傳遞")
    agent.update_metrics("木", True, 1.2)
    
    # 火 → 水（開發到測試）
    agent.switch_role("火")
    agent.record_flow("火", "水", "提交測試")
    agent.update_metrics("火", True, 2.5)
    
    # 水發現問題
    agent.switch_role("水")
    agent.record_flow("水", "火", "bug回報")
    agent.update_metrics("水", True, 0.8)
    
    # 火修復
    agent.switch_role("火")
    agent.record_flow("火", "水", "修復提交")
    agent.update_metrics("火", False, 3.5)  # 修復失敗
    
    print(agent.get_mini_dashboard())
    print()
    
    # 3. 無極介入
    print("3. 無極介入情況")
    # 檢測到問題，無極分析
    agent.switch_role("無極")
    intervention = agent._generate_intervention()
    print("無極觀察:", intervention)
    print()
    
    # 4. 顯示完整 Dashboard
    print("4. 完整 Dashboard")
    print(agent.get_dashboard())
    
    # 5. 測試極端情況
    print("\n5. 測試極端情況 - 火元素過載")
    for i in range(10):
        agent.update_metrics("火", False, 5.0)
    
    print("\n最終狀態:")
    print(agent.get_mini_dashboard())
    print("\n無極洞察:")
    print(agent._generate_insights())

if __name__ == "__main__":
    test_dashboard_features()