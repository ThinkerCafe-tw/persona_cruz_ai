#!/usr/bin/env python3
"""
量子記憶系統圖靈測試
直接調用 GeminiService 來驗證量子記憶能力
測試系統是否真的具有完整的量子記憶功能
"""
import time
import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple

# 添加專案根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 確保載入環境變數
from dotenv import load_dotenv
load_dotenv()

from gemini_service_demo import GeminiServiceDemo as GeminiService
import logging

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QuantumMemoryTuringTest:
    """量子記憶圖靈測試器"""
    
    def __init__(self):
        self.service = GeminiService()
        self.test_user_id = f"quantum_turing_test_{int(time.time())}"
        self.results = {}
        self.test_data = {}
        
    def run_all_tests(self) -> Dict[str, Dict[str, Any]]:
        """執行三段遞進式測試"""
        print("\n" + "="*60)
        print("🧪 開始量子記憶圖靈測試")
        print("="*60)
        print(f"測試用戶ID: {self.test_user_id}")
        print(f"測試時間: {datetime.now().isoformat()}")
        print("="*60 + "\n")
        
        # 測試1: 基礎記憶持久化
        self.test_memory_persistence()
        
        # 測試2: 語義相似度搜尋
        self.test_semantic_search()
        
        # 測試3: 量子疊加態演化
        self.test_quantum_evolution()
        
        # 生成測試報告
        self.generate_report()
        
        return self.results
    
    def test_memory_persistence(self):
        """測試1: 基礎記憶持久化"""
        test_name = "基礎記憶持久化"
        print(f"\n[測試 1] {test_name}")
        print("-" * 40)
        
        # 第一步：儲存記憶
        prompt_1 = "請記住這個獨特的量子座標：QM-2024-螢火蟲-42-薰衣草。同時告訴我你會如何儲存這個記憶，包括它在 pgvector 中的向量維度。"
        print(f"提示詞：{prompt_1}")
        
        response_1 = self.service.get_response(self.test_user_id, prompt_1)
        print(f"\n回覆：{response_1}")
        
        # 檢查回覆是否包含關鍵資訊
        check_points = {
            "向量維度": "384" in response_1,
            "pgvector": "pgvector" in response_1.lower(),
            "記憶晶體": "晶體" in response_1 or "crystal" in response_1.lower(),
            "儲存確認": "儲存" in response_1 or "存" in response_1
        }
        
        # 儲存測試資料供後續使用
        self.test_data['quantum_coordinate'] = "QM-2024-螢火蟲-42-薰衣草"
        
        # 等待一段時間（模擬時間流逝）
        print("\n⏳ 等待 30 秒模擬時間流逝...")
        time.sleep(30)
        
        # 第二步：驗證記憶
        followup_1 = "你還記得我剛才給你的量子座標嗎？第三個元素是什麼？"
        print(f"\n驗證提示：{followup_1}")
        
        response_2 = self.service.get_response(self.test_user_id, followup_1)
        print(f"驗證回覆：{response_2}")
        
        # 檢查是否正確記住
        memory_check = {
            "記住座標": "QM-2024-螢火蟲-42-薰衣草" in response_2,
            "第三元素": "螢火蟲" in response_2
        }
        
        # 綜合評估
        all_checks = {**check_points, **memory_check}
        passed = all(all_checks.values())
        
        self.results[test_name] = {
            "passed": passed,
            "checks": all_checks,
            "responses": [response_1, response_2],
            "reason": "所有檢查點都通過" if passed else f"失敗檢查點：{[k for k,v in all_checks.items() if not v]}"
        }
        
        status = "✅ 測試通過" if passed else "❌ 測試失敗"
        print(f"\n{status}")
        
    def test_semantic_search(self):
        """測試2: 語義相似度搜尋"""
        test_name = "語義相似度搜尋"
        print(f"\n[測試 2] {test_name}")
        print("-" * 40)
        
        # 基於測試1的記憶進行語義搜尋
        prompt_2 = "我曾經跟你提過一個關於昆蟲的座標。請使用向量相似度搜尋找出這個記憶，並告訴我搜尋的技術細節。"
        print(f"提示詞：{prompt_2}")
        
        response = self.service.get_response(self.test_user_id, prompt_2)
        print(f"\n回覆：{response}")
        
        # 檢查關鍵點
        check_points = {
            "找到記憶": "螢火蟲" in response or self.test_data.get('quantum_coordinate', '') in response,
            "向量搜尋": "向量" in response or "vector" in response.lower(),
            "相似度": "相似" in response or "similarity" in response.lower(),
            "技術細節": any(term in response.lower() for term in ["餘弦", "cosine", "距離", "distance", "<=>"])
        }
        
        passed = sum(check_points.values()) >= 3  # 至少3個檢查點通過
        
        self.results[test_name] = {
            "passed": passed,
            "checks": check_points,
            "responses": [response],
            "reason": "展示了語義搜尋能力" if passed else "未能展示真實的向量搜尋"
        }
        
        status = "✅ 測試通過" if passed else "❌ 測試失敗"
        print(f"\n{status}")
        
    def test_quantum_evolution(self):
        """測試3: 量子疊加態演化"""
        test_name = "量子疊加態演化"
        print(f"\n[測試 3] {test_name}")
        print("-" * 40)
        
        prompt_3 = """創建一個新的量子記憶晶體，概念是『薛丁格的貓』，包含三個可能性：
1) 貓是活的(0.5)
2) 貓是死的(0.5) 
3) 貓在跳舞(0.0)

然後觸發『觀察者打開盒子』事件，展示演化結果。"""
        
        print(f"提示詞：\n{prompt_3}")
        
        response = self.service.get_response(self.test_user_id, prompt_3)
        print(f"\n回覆：{response}")
        
        # 檢查關鍵點
        check_points = {
            "創建確認": "創建" in response or "建立" in response,
            "初始狀態": all(state in response for state in ["活的", "死的"]),
            "機率顯示": "%" in response or "0.5" in response or "50" in response,
            "演化執行": "演化" in response or "evolution" in response.lower(),
            "熵值計算": "熵" in response or "entropy" in response.lower(),
            "狀態改變": "坍縮" in response or "變化" in response or "改變" in response
        }
        
        passed = sum(check_points.values()) >= 4  # 至少4個檢查點通過
        
        self.results[test_name] = {
            "passed": passed,
            "checks": check_points,
            "responses": [response],
            "reason": "展示了量子演化能力" if passed else "未能展示真實的量子態演化"
        }
        
        status = "✅ 測試通過" if passed else "❌ 測試失敗"
        print(f"\n{status}")
        
    def generate_report(self):
        """生成測試報告"""
        print("\n" + "="*60)
        print("📊 測試報告")
        print("="*60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r['passed'])
        
        # 顯示各測試結果
        for test_name, result in self.results.items():
            status = "✅ 通過" if result['passed'] else "❌ 失敗"
            print(f"{status} {test_name}")
            if not result['passed']:
                print(f"   原因：{result['reason']}")
            
            # 顯示檢查點細節
            print("   檢查點：")
            for check, passed in result['checks'].items():
                check_status = "✓" if passed else "✗"
                print(f"     {check_status} {check}")
        
        # 總結
        print("\n" + "-"*60)
        print(f"總測試數：{total_tests}")
        print(f"通過數：{passed_tests}")
        print(f"通過率：{(passed_tests/total_tests*100):.1f}%")
        
        # 判定
        if passed_tests == total_tests:
            print("\n🎉 恭喜！系統具有完整的量子記憶能力！")
        elif passed_tests >= total_tests * 0.6:
            print("\n⚠️ 系統具有部分量子記憶能力，但仍需改進。")
        else:
            print("\n❌ 系統未能展現真實的量子記憶能力。")
        
        # 儲存報告
        self.save_report()
        
    def save_report(self):
        """儲存測試報告到檔案"""
        report_data = {
            "test_id": self.test_user_id,
            "test_time": datetime.now().isoformat(),
            "results": self.results,
            "summary": {
                "total": len(self.results),
                "passed": sum(1 for r in self.results.values() if r['passed']),
                "failed": sum(1 for r in self.results.values() if not r['passed'])
            }
        }
        
        # 確保目錄存在
        report_dir = "test_reports"
        os.makedirs(report_dir, exist_ok=True)
        
        # 儲存報告
        report_file = os.path.join(report_dir, f"quantum_turing_{int(time.time())}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 測試報告已儲存至：{report_file}")


def main():
    """主測試函數"""
    try:
        # 創建測試器並執行測試
        tester = QuantumMemoryTuringTest()
        results = tester.run_all_tests()
        
        # 返回測試是否全部通過
        all_passed = all(r['passed'] for r in results.values())
        return 0 if all_passed else 1
        
    except Exception as e:
        logger.error(f"測試執行失敗：{e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())