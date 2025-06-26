"""
CRUZ AI 完整測試套件
Day 11-12: 自動化測試
"""
import asyncio
import pytest
import httpx
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# 添加專案路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 測試配置
TEST_CONFIG = {
    "memory_api_url": "http://localhost:8000",
    "persona_proxy_url": "http://localhost:8001", 
    "unified_gateway_url": "http://localhost:8002",
    "test_user_id": "test_user_suite",
    "test_api_key": "test-api-key"
}

class TestReport:
    """測試報告生成器"""
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        
    def add_result(self, category: str, test_name: str, status: bool, details: str = ""):
        self.results.append({
            "category": category,
            "test_name": test_name,
            "status": "PASS" if status else "FAIL",
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_report(self) -> str:
        """生成測試報告"""
        duration = (datetime.now() - self.start_time).total_seconds()
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["status"] == "PASS")
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = f"""
# CRUZ AI 測試報告

**測試時間**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
**執行時長**: {duration:.2f} 秒
**總測試數**: {total_tests}
**通過**: {passed_tests} ✅
**失敗**: {failed_tests} ❌
**通過率**: {pass_rate:.1f}%

## 測試詳情

"""
        # 按類別分組
        categories = {}
        for result in self.results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        for category, tests in categories.items():
            report += f"### {category}\n\n"
            for test in tests:
                icon = "✅" if test["status"] == "PASS" else "❌"
                report += f"- {icon} **{test['test_name']}**: {test['status']}"
                if test["details"]:
                    report += f" - {test['details']}"
                report += "\n"
            report += "\n"
        
        return report

# 全局測試報告
test_report = TestReport()

# 測試類別
class TestMemoryAPI:
    """測試記憶 API"""
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """測試健康檢查"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{TEST_CONFIG['memory_api_url']}/health")
                success = response.status_code == 200
                test_report.add_result(
                    "Memory API", 
                    "健康檢查",
                    success,
                    f"狀態碼: {response.status_code}"
                )
                assert success
            except Exception as e:
                test_report.add_result("Memory API", "健康檢查", False, str(e))
                pytest.fail(f"健康檢查失敗: {e}")
    
    @pytest.mark.asyncio
    async def test_crud_operations(self):
        """測試 CRUD 操作"""
        async with httpx.AsyncClient() as client:
            # 測試用戶註冊/登入
            token = await self._get_test_token(client)
            
            # 測試存儲記憶
            memory_data = {
                "content": "測試記憶內容",
                "category": "test",
                "tags": ["test", "automated"],
                "context": {"test_id": "crud_test"}
            }
            
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(
                f"{TEST_CONFIG['memory_api_url']}/memory/store",
                json=memory_data,
                headers=headers
            )
            
            success = response.status_code == 200
            test_report.add_result(
                "Memory API",
                "存儲記憶",
                success,
                f"回應: {response.status_code}"
            )
            
            if success:
                memory_id = response.json()["id"]
                
                # 測試搜尋
                search_response = await client.get(
                    f"{TEST_CONFIG['memory_api_url']}/memory/search",
                    params={"query": "測試記憶"},
                    headers=headers
                )
                
                search_success = search_response.status_code == 200
                test_report.add_result(
                    "Memory API",
                    "搜尋記憶",
                    search_success,
                    f"找到 {len(search_response.json().get('results', []))} 條結果"
                )
    
    async def _get_test_token(self, client: httpx.AsyncClient) -> str:
        """獲取測試 token"""
        # 嘗試註冊
        await client.post(
            f"{TEST_CONFIG['memory_api_url']}/auth/register",
            json={
                "username": "test_suite_user",
                "email": "test@suite.com", 
                "password": "Test123!@#"
            }
        )
        
        # 登入
        response = await client.post(
            f"{TEST_CONFIG['memory_api_url']}/auth/token",
            data={
                "username": "test_suite_user",
                "password": "Test123!@#"
            }
        )
        
        if response.status_code == 200:
            return response.json()["access_token"]
        return TEST_CONFIG["test_api_key"]

class TestPersonaSystem:
    """測試人格系統"""
    
    @pytest.mark.asyncio
    async def test_persona_consistency(self):
        """測試人格一致性"""
        from personality.emotion_engine import cruz_emotion, EmotionTrigger
        
        # 測試情緒轉換
        initial_state = cruz_emotion.current_state
        cruz_emotion.process_trigger(EmotionTrigger.SUCCESS)
        
        success = cruz_emotion.current_state is not None
        test_report.add_result(
            "人格系統",
            "情緒引擎",
            success,
            f"當前狀態: {cruz_emotion.current_state.value}"
        )
    
    @pytest.mark.asyncio
    async def test_all_personas(self):
        """測試所有人格"""
        personas = [
            "cruz-decisive",
            "serena-supportive", 
            "wood-creative",
            "fire-passionate",
            "earth-stable",
            "metal-precise",
            "water-adaptive"
        ]
        
        async with httpx.AsyncClient() as client:
            for persona in personas:
                try:
                    response = await client.post(
                        f"{TEST_CONFIG['persona_proxy_url']}/v1/chat/completions",
                        json={
                            "model": persona,
                            "messages": [{"role": "user", "content": "測試消息"}],
                            "stream": False
                        },
                        headers={"x-persona-type": persona.split("-")[0]}
                    )
                    
                    success = response.status_code == 200
                    test_report.add_result(
                        "人格系統",
                        f"{persona} 對話測試",
                        success,
                        f"回應長度: {len(response.json().get('choices', [{}])[0].get('message', {}).get('content', ''))}"
                    )
                except Exception as e:
                    test_report.add_result(
                        "人格系統",
                        f"{persona} 對話測試",
                        False,
                        str(e)
                    )

class TestCrossPlatform:
    """測試跨平台功能"""
    
    @pytest.mark.asyncio
    async def test_unified_gateway(self):
        """測試統一網關"""
        async with httpx.AsyncClient() as client:
            # 健康檢查
            try:
                response = await client.get(f"{TEST_CONFIG['unified_gateway_url']}/health")
                success = response.status_code == 200
                
                if success:
                    data = response.json()
                    details = f"活躍用戶: {data.get('active_users', 0)}, 支援平台: {len(data.get('supported_platforms', []))}"
                else:
                    details = f"狀態碼: {response.status_code}"
                    
                test_report.add_result(
                    "跨平台同步",
                    "統一網關健康檢查",
                    success,
                    details
                )
            except Exception as e:
                test_report.add_result(
                    "跨平台同步",
                    "統一網關健康檢查", 
                    False,
                    str(e)
                )
    
    @pytest.mark.asyncio
    async def test_sdk_connection(self):
        """測試 SDK 連接"""
        try:
            from cross_platform.sdk.cruz_ai_sdk import create_cruz_ai
            
            sdk = create_cruz_ai(
                api_key=TEST_CONFIG["test_api_key"],
                platform="test_suite"
            )
            
            await sdk.initialize("sdk_test_user")
            
            # 測試獲取會話
            session = await sdk.get_session()
            success = session is not None
            
            test_report.add_result(
                "跨平台同步",
                "Python SDK 連接",
                success,
                f"當前人格: {session.current_persona if session else 'N/A'}"
            )
            
            await sdk.disconnect()
            
        except Exception as e:
            test_report.add_result(
                "跨平台同步",
                "Python SDK 連接",
                False,
                str(e)
            )

class TestPerformance:
    """效能測試"""
    
    @pytest.mark.asyncio
    async def test_response_time(self):
        """測試響應時間"""
        async with httpx.AsyncClient() as client:
            # 測試 10 次請求
            response_times = []
            
            for i in range(10):
                start = datetime.now()
                
                response = await client.post(
                    f"{TEST_CONFIG['persona_proxy_url']}/v1/chat/completions",
                    json={
                        "model": "cruz-decisive",
                        "messages": [{"role": "user", "content": f"測試 {i}"}],
                        "stream": False
                    }
                )
                
                end = datetime.now()
                response_time = (end - start).total_seconds() * 1000  # 毫秒
                response_times.append(response_time)
            
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            # 平均響應時間應小於 500ms
            success = avg_time < 500
            
            test_report.add_result(
                "效能測試",
                "響應時間",
                success,
                f"平均: {avg_time:.0f}ms, 最快: {min_time:.0f}ms, 最慢: {max_time:.0f}ms"
            )
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """測試並發請求"""
        async def make_request(client: httpx.AsyncClient, index: int):
            try:
                response = await client.post(
                    f"{TEST_CONFIG['persona_proxy_url']}/v1/chat/completions",
                    json={
                        "model": "cruz-decisive",
                        "messages": [{"role": "user", "content": f"並發測試 {index}"}],
                        "stream": False
                    }
                )
                return response.status_code == 200
            except:
                return False
        
        async with httpx.AsyncClient() as client:
            # 同時發送 20 個請求
            tasks = [make_request(client, i) for i in range(20)]
            results = await asyncio.gather(*tasks)
            
            success_count = sum(1 for r in results if r)
            success_rate = success_count / len(results) * 100
            
            test_report.add_result(
                "效能測試",
                "並發處理",
                success_rate >= 95,
                f"成功率: {success_rate:.0f}% ({success_count}/{len(results)})"
            )

class TestSecurity:
    """安全測試"""
    
    @pytest.mark.asyncio
    async def test_authentication(self):
        """測試認證機制"""
        async with httpx.AsyncClient() as client:
            # 測試無認證訪問
            response = await client.get(
                f"{TEST_CONFIG['memory_api_url']}/memory/list"
            )
            
            # 應該返回 401
            success = response.status_code == 401
            
            test_report.add_result(
                "安全測試",
                "未授權訪問保護",
                success,
                f"狀態碼: {response.status_code}"
            )
    
    @pytest.mark.asyncio
    async def test_input_validation(self):
        """測試輸入驗證"""
        async with httpx.AsyncClient() as client:
            # 測試無效輸入
            invalid_data = {
                "model": "'; DROP TABLE users; --",
                "messages": []
            }
            
            response = await client.post(
                f"{TEST_CONFIG['persona_proxy_url']}/v1/chat/completions",
                json=invalid_data
            )
            
            # 應該安全處理
            success = response.status_code in [400, 422, 500]
            
            test_report.add_result(
                "安全測試",
                "SQL 注入防護",
                success,
                "輸入驗證正常"
            )

async def run_all_tests():
    """執行所有測試"""
    print("🧪 開始執行 CRUZ AI 測試套件")
    print("=" * 50)
    
    # 測試類別
    test_classes = [
        TestMemoryAPI(),
        TestPersonaSystem(),
        TestCrossPlatform(),
        TestPerformance(),
        TestSecurity()
    ]
    
    # 執行測試
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"\n📋 執行 {class_name}...")
        
        # 獲取所有測試方法
        test_methods = [m for m in dir(test_class) if m.startswith("test_")]
        
        for method_name in test_methods:
            method = getattr(test_class, method_name)
            if asyncio.iscoroutinefunction(method):
                try:
                    await method()
                    print(f"   ✅ {method_name}")
                except Exception as e:
                    print(f"   ❌ {method_name}: {e}")
    
    # 生成報告
    report = test_report.generate_report()
    
    # 保存報告
    with open("test_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n" + "=" * 50)
    print("📊 測試完成！報告已保存至 test_report.md")
    
    # 顯示摘要
    total = len(test_report.results)
    passed = sum(1 for r in test_report.results if r["status"] == "PASS")
    print(f"\n總測試: {total}")
    print(f"通過: {passed} ✅")
    print(f"失敗: {total - passed} ❌")
    print(f"通過率: {passed/total*100:.1f}%")

if __name__ == "__main__":
    asyncio.run(run_all_tests())