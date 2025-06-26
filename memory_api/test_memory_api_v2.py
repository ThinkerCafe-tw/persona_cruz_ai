"""
Memory API v2 測試套件 - Day 2
測試向量搜索準確率
"""
import pytest
import httpx
from datetime import datetime
import asyncio

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_vector_search_accuracy():
    """測試向量搜索準確率 >95%"""
    async with httpx.AsyncClient() as client:
        # 準備測試數據
        test_memories = [
            {"content": "我喜歡去火星旅行", "context": {"topic": "space"}},
            {"content": "SpaceX正在開發星際飛船", "context": {"topic": "space"}},
            {"content": "特斯拉是電動車公司", "context": {"topic": "tesla"}},
            {"content": "我今天吃了披薩", "context": {"topic": "food"}},
            {"content": "Python是很好的程式語言", "context": {"topic": "tech"}},
        ]
        
        user_id = "test_vector_user"
        
        # 存儲測試記憶
        for memory in test_memories:
            await client.post(
                f"{BASE_URL}/memory/store",
                json={
                    "user_id": user_id,
                    "content": memory["content"],
                    "context": memory["context"]
                }
            )
        
        # 測試相關搜索
        test_queries = [
            ("火星探索", ["火星", "SpaceX"]),  # 應該找到太空相關
            ("電動車", ["特斯拉"]),  # 應該找到特斯拉
            ("程式設計", ["Python"]),  # 應該找到編程相關
        ]
        
        total_tests = 0
        correct_results = 0
        
        for query, expected_keywords in test_queries:
            response = await client.get(
                f"{BASE_URL}/memory/search",
                params={
                    "user_id": user_id,
                    "query": query,
                    "limit": 3,
                    "threshold": 0.5
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # 檢查是否找到相關內容
            found_relevant = False
            for result in data["results"]:
                if any(keyword in result["content"] for keyword in expected_keywords):
                    found_relevant = True
                    correct_results += 1
                    break
            
            total_tests += 1
            print(f"Query: {query} - Found: {found_relevant}")
        
        # 計算準確率
        accuracy = (correct_results / total_tests) * 100
        print(f"🎯 Search accuracy: {accuracy}%")
        
        # 必須達到 >95% 準確率
        assert accuracy >= 95, f"Accuracy {accuracy}% is below 95% threshold"

@pytest.mark.asyncio
async def test_performance_with_vectors():
    """測試向量搜索性能 <200ms"""
    async with httpx.AsyncClient() as client:
        # 存儲一個測試記憶
        await client.post(
            f"{BASE_URL}/memory/store",
            json={
                "user_id": "perf_test_v2",
                "content": "Performance test with vector embeddings",
                "context": {}
            }
        )
        
        # 測試搜索性能
        start_time = datetime.now()
        response = await client.get(
            f"{BASE_URL}/memory/search",
            params={
                "user_id": "perf_test_v2",
                "query": "performance test",
                "limit": 10
            }
        )
        search_time = (datetime.now() - start_time).total_seconds() * 1000
        
        assert response.status_code == 200
        assert search_time < 200, f"Search took {search_time}ms, should be <200ms"
        print(f"⚡ Vector search time: {search_time}ms")

@pytest.mark.asyncio
async def test_database_persistence():
    """測試資料持久化"""
    async with httpx.AsyncClient() as client:
        # 存儲記憶
        memory_data = {
            "user_id": "persistence_test",
            "content": "This should persist in PostgreSQL",
            "context": {"test": True}
        }
        
        response = await client.post(f"{BASE_URL}/memory/store", json=memory_data)
        assert response.status_code == 200
        memory_id = response.json()["memory_id"]
        
        # 立即搜索應該能找到
        search_response = await client.get(
            f"{BASE_URL}/memory/search",
            params={
                "user_id": "persistence_test",
                "query": "PostgreSQL",
                "limit": 1
            }
        )
        
        assert search_response.status_code == 200
        results = search_response.json()["results"]
        assert len(results) > 0
        assert results[0]["memory_id"] == memory_id

# 運行所有測試
if __name__ == "__main__":
    print("🧪 Running Memory API v2 Tests - Day 2")
    print("🎯 Target: >95% accuracy, <200ms response")
    pytest.main([__file__, "-v", "--tb=short"])