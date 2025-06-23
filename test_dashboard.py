#!/usr/bin/env python3
"""
測試五行系統 Dashboard 功能
"""
from five_elements_agent import FiveElementsAgent
import time
import random

def simulate_interactions():
    """模擬系統互動"""
    agent = FiveElementsAgent()
    
    print("=== 開始模擬五行系統互動 ===\n")
    
    # 模擬一些互動
    elements = ["木", "火", "水", "土", "金"]
    
    # 模擬10次互動
    for i in range(10):
        # 隨機選擇元素
        from_element = random.choice(elements)
        to_element = random.choice([e for e in elements if e != from_element])
        
        # 切換角色
        agent.switch_role(from_element)
        print(f"互動 {i+1}: {from_element} → {to_element}")
        
        # 記錄互動
        actions = ["需求分析", "程式開發", "測試檢查", "架構設計", "程式優化"]
        action = random.choice(actions)
        agent.record_flow(from_element, to_element, action)
        
        # 更新指標（隨機成功或失敗）
        success = random.random() > 0.2  # 80% 成功率
        response_time = random.uniform(0.5, 3.0)
        agent.update_metrics(from_element, success, response_time)
        
        time.sleep(0.5)  # 短暫延遲
    
    # 顯示迷你儀表板
    print("\n" + "="*60)
    print("迷你儀表板：")
    print(agent.get_mini_dashboard())
    
    # 顯示完整儀表板
    print("\n" + "="*60)
    print(agent.get_dashboard())
    
    # 模擬一些錯誤
    print("\n=== 模擬錯誤情況 ===\n")
    for i in range(5):
        element = "火"  # 讓火元素出現多次錯誤
        agent.update_metrics(element, success=False, response_time=5.0)
    
    # 再次顯示儀表板
    print("\n" + "="*60)
    print("錯誤後的儀表板：")
    print(agent.get_dashboard())

if __name__ == "__main__":
    simulate_interactions()