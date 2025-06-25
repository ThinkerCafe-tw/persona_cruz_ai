#!/usr/bin/env python3
"""
測試 DNS 考古學系統
"""
import os
import sys
from datetime import datetime

# 添加專案路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system_intelligence.diagnostics import DNSArchaeology
from system_intelligence import SystemChronicles

def test_dns_archaeology():
    print("🏺 DNS 考古學測試")
    print("=" * 60)
    
    # 創建考古學家和編年史
    archaeologist = DNSArchaeology()
    chronicles = SystemChronicles()
    
    # 模擬 Railway 環境
    test_context = {
        "error": "could not translate host name 'postgres.railway.internal' to address: Name or service not known",
        "environment": "Railway",
        "service": "persona_cruz_ai",
        "target_service": "postgres",
        "private_networking": "enabled",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"\n📋 測試環境：")
    print(f"   - 錯誤: DNS 無法解析 postgres.railway.internal")
    print(f"   - 平台: Railway")
    print(f"   - 私有網路: 已啟用")
    
    # 執行考古挖掘
    print(f"\n🔍 開始 DNS 考古挖掘...")
    findings = archaeologist.archaeological_dig(test_context)
    
    # 顯示結果
    print(f"\n📊 考古發現：")
    print(f"   - 會話 ID: {findings['dig_session']}")
    print(f"   - DNS 測試數: {len(findings.get('dns_resolution_attempts', []))}")
    
    # 顯示智慧
    wisdom_gained = findings.get('wisdom_gained', [])
    if wisdom_gained:
        print(f"\n💡 獲得的智慧：")
        for w in wisdom_gained:
            print(f"   - {w}")
    
    # 顯示建議
    recommendations = findings.get('recommendations', [])
    if recommendations:
        print(f"\n🎯 建議：")
        for r in recommendations:
            print(f"   - {r}")
    
    # 檢查是否有成功的解析
    successful_attempts = 0
    total_attempts = 0
    
    for dns_result in findings.get('dns_resolution_attempts', []):
        for attempt in dns_result.get('attempts', []):
            total_attempts += 1
            if attempt.get('success'):
                successful_attempts += 1
                print(f"\n✅ 成功解析: {dns_result['expanded']}")
                print(f"   方法: {attempt['method']}")
    
    print(f"\n📈 統計：")
    print(f"   - 總測試數: {total_attempts}")
    print(f"   - 成功數: {successful_attempts}")
    print(f"   - 成功率: {(successful_attempts/total_attempts*100) if total_attempts > 0 else 0:.1f}%")
    
    # 記錄到編年史
    chronicles.record_event("DNS_ARCHAEOLOGY_TEST", {
        "findings_summary": {
            "total_tests": total_attempts,
            "successful": successful_attempts,
            "recommendations_count": len(recommendations),
            "wisdom_count": len(wisdom_gained)
        }
    })
    
    # 如果全部失敗，添加錯誤到博物館
    if successful_attempts == 0:
        chronicles.add_error(
            error="DNS resolution failed for all Railway internal hostnames",
            context="DNS archaeology test",
            lesson="Railway internal DNS may require specific conditions or timing"
        )
    
    print(f"\n✨ 測試完成！")
    print(f"   考古發現已保存至: system_intelligence/archaeological_records/")
    
    # 生成編年史報告
    print(f"\n📜 系統編年史摘要：")
    age_info = chronicles.get_system_age()
    print(f"   - 系統年齡: {age_info['age_hours']:.1f} 小時")
    print(f"   - 累積錯誤: {age_info['total_errors']} 個")
    print(f"   - 累積智慧: {age_info['total_wisdom']} 條")

if __name__ == "__main__":
    test_dns_archaeology()