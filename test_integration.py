#!/usr/bin/env python3
"""
測試五行系統與Line Bot的整合
"""
from gemini_service import GeminiService
import time

def test_five_elements_integration():
    """測試五行系統整合"""
    print("=== 測試五行系統整合 ===\n")
    
    # 初始化服務
    service = GeminiService()
    test_user = "test_user_123"
    
    # 測試1: Dashboard 指令
    print("1. 測試 Dashboard 指令")
    response = service.get_response(test_user, "/dashboard")
    print("回應長度:", len(response))
    print("包含儀表板:", "╔═══" in response)
    print()
    
    # 測試2: 迷你狀態
    print("2. 測試迷你狀態")
    response = service.get_response(test_user, "/status")
    print("回應:", response)
    print()
    
    # 測試3: 角色切換 - 開發
    print("3. 測試角色切換 - 開發專員")
    response = service.get_response(test_user, "我想開發一個新功能")
    print("當前角色:", service.five_elements.current_role.name if service.five_elements.current_role else "無")
    print("回應預覽:", response[:100] + "...")
    print()
    
    # 測試4: 角色切換 - 測試
    print("4. 測試角色切換 - 測試專員")
    response = service.get_response(test_user, "幫我測試這個功能")
    print("當前角色:", service.five_elements.current_role.name if service.five_elements.current_role else "無")
    print("回應預覽:", response[:100] + "...")
    print()
    
    # 測試5: 無極介入
    print("5. 測試無極介入")
    response = service.get_response(test_user, "我卡住了，不知道該怎麼辦")
    print("當前角色:", service.five_elements.current_role.name if service.five_elements.current_role else "無")
    print("回應預覽:", response[:100] + "...")
    print()
    
    # 測試6: 查看最終狀態
    print("6. 最終系統狀態")
    final_status = service.five_elements.get_mini_dashboard()
    print(final_status)
    
    # 顯示系統指標
    print("\n系統指標:")
    metrics = service.five_elements.system_metrics
    print(f"- 總互動數: {metrics['total_interactions']}")
    print(f"- 成功率: {metrics['success_rate']:.1f}%")
    print(f"- 平均響應時間: {metrics['average_response_time']:.2f}s")

if __name__ == "__main__":
    test_five_elements_integration()