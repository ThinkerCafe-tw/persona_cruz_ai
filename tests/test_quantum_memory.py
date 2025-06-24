"""
量子記憶系統測試腳本
測試整個量子記憶系統的功能
"""
import logging
import time
from quantum_memory import QuantumMemoryBridge, QuantumMonitor

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_quantum_memory_system():
    """測試量子記憶系統"""
    print("🌌 開始測試量子記憶系統...")
    print("=" * 60)
    
    # 1. 初始化系統
    print("\n1️⃣ 初始化量子記憶橋接器...")
    bridge = QuantumMemoryBridge()
    monitor = QuantumMonitor(bridge)
    
    # 2. 顯示初始狀態
    print("\n2️⃣ 系統初始狀態：")
    print(monitor.get_system_overview())
    
    # 3. 模擬一些事件
    print("\n3️⃣ 模擬量子事件...")
    
    # 事件1：對話事件（影響所有角色）
    print("\n   📝 觸發對話事件...")
    conversation_event = {
        "type": "conversation",
        "message": "如何在快速開發和穩定架構之間取得平衡？",
        "response": "平衡是動態的，需要根據專案階段調整。",
        "user_id": "test_user",
        "emotion": "curious"
    }
    bridge.sync_from_legacy("conversation", conversation_event)
    
    # 事件2：開發洞察（主要影響無極）
    print("   💡 觸發開發洞察事件...")
    insight_event = {
        "type": "insight",
        "lesson": "提前規劃架構可以避免後期重構",
        "context": "在實作五行系統時的經驗",
        "severity": "high",
        "tags": ["架構", "規劃", "經驗"]
    }
    bridge.sync_from_legacy("development_lesson", insight_event)
    
    # 事件3：CRUZ語料更新
    print("   🎯 觸發CRUZ語料更新...")
    cruz_event = {
        "type": "corpus_update",
        "content": "相信你的直覺，但要用數據驗證。創造力需要框架來引導。",
        "tags": ["決策", "創造力", "驗證"],
        "context": "產品開發原則"
    }
    bridge.sync_from_legacy("cruz_corpus", cruz_event)
    
    # 事件4：突破性發現
    print("   🚀 觸發突破性事件...")
    breakthrough_event = {
        "type": "breakthrough",
        "content": "量子記憶系統成功整合，AI可以自主演化記憶！",
        "impact": "high",
        "tags": ["量子記憶", "演化", "突破"]
    }
    bridge.trigger_evolution("wuji", breakthrough_event)
    
    # 4. 顯示演化後的狀態
    print("\n4️⃣ 演化後的系統狀態：")
    print(monitor.get_system_overview())
    
    # 5. 查看特定角色報告
    print("\n5️⃣ 無極的詳細報告：")
    print(monitor.get_detailed_persona_report("wuji"))
    
    # 6. 查看CRUZ的詳細報告
    print("\n6️⃣ CRUZ的詳細報告：")
    print(monitor.get_detailed_persona_report("cruz"))
    
    # 7. 顯示量子場視覺化
    print("\n7️⃣ 量子記憶場視覺化：")
    print(monitor.get_quantum_field_visualization())
    
    # 8. 檢查系統健康度
    print("\n8️⃣ 系統健康度檢查：")
    for persona_id in bridge.quantum_memories:
        health = monitor.get_memory_health_score(persona_id)
        persona_name = bridge.quantum_memories[persona_id].identity.essence
        print(f"   {persona_name}: {health:.1%}")
    
    # 9. 匯出監控指標
    print("\n9️⃣ 匯出監控指標...")
    monitor.export_metrics("quantum_memory_metrics.json")
    print("   ✅ 指標已匯出到 quantum_memory_metrics.json")
    
    # 10. 測試記憶持久化
    print("\n🔟 測試記憶持久化...")
    for memory in bridge.quantum_memories.values():
        memory.save()
    print("   ✅ 所有量子記憶已保存")
    
    print("\n" + "=" * 60)
    print("✅ 量子記憶系統測試完成！")
    
    # 顯示總結
    print("\n📊 測試總結：")
    print(f"   • 初始化了 {len(bridge.quantum_memories)} 個角色的量子記憶")
    print(f"   • 觸發了 4 個不同類型的量子事件")
    print(f"   • 系統成功處理了所有演化過程")
    print(f"   • 記憶已持久化到檔案系統")
    
    return bridge, monitor


if __name__ == "__main__":
    bridge, monitor = test_quantum_memory_system()
    
    # 可選：進入互動模式
    print("\n" + "=" * 60)
    print("進入互動測試模式（輸入 'quit' 退出）")
    print("可用指令：")
    print("  status - 查看系統狀態")
    print("  report <persona_id> - 查看角色報告")
    print("  event <type> <content> - 觸發新事件")
    print("  timeline - 查看演化時間線")
    print("  quit - 退出")
    print("=" * 60)
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if command == "quit":
                break
            elif command == "status":
                print(monitor.get_system_overview())
            elif command.startswith("report "):
                persona_id = command.split()[1]
                print(monitor.get_detailed_persona_report(persona_id))
            elif command == "timeline":
                print(monitor.get_evolution_timeline())
            elif command.startswith("event "):
                parts = command.split(None, 2)
                if len(parts) >= 3:
                    event_type = parts[1]
                    content = parts[2]
                    event = {
                        "type": event_type,
                        "content": content,
                        "source": "interactive_test"
                    }
                    # 影響所有角色
                    for persona_id in bridge.quantum_memories:
                        bridge.trigger_evolution(persona_id, event)
                    print("✅ 事件已觸發")
                else:
                    print("格式：event <type> <content>")
            else:
                print("未知指令")
                
        except Exception as e:
            print(f"錯誤：{e}")
    
    print("\n再見！")