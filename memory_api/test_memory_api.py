"""
Memory API 測試套件 - Day 1
極簡但有效的測試
"""
import pytest
import httpx
from datetime import datetime

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_health_check():
    """測試健康檢查端點"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "musk_says" in data

@pytest.mark.asyncio
async def test_store_memory():
    """測試記憶存儲"""
    async with httpx.AsyncClient() as client:
        memory_data = {
            "user_id": "test_user_001",
            "content": "我喜歡效率和第一性原理思考",
            "context": {"mood": "determined", "topic": "philosophy"}
        }
        
        response = await client.post(f"{BASE_URL}/memory/store", json=memory_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["user_id"] == "test_user_001"
        assert result["content"] == memory_data["content"]
        assert "memory_id" in result
        assert "created_at" in result

@pytest.mark.asyncio
async def test_search_memory():
    """測試記憶搜索"""
    async with httpx.AsyncClient() as client:
        # 先存儲一些記憶
        memories = [
            {"user_id": "test_user_002", "content": "SpaceX要去火星", "context": {}},
            {"user_id": "test_user_002", "content": "特斯拉要改變交通", "context": {}},
            {"user_id": "test_user_002", "content": "第一性原理很重要", "context": {}}
        ]
        
        for memory in memories:
            await client.post(f"{BASE_URL}/memory/store", json=memory)
        
        # 搜索記憶
        response = await client.get(
            f"{BASE_URL}/memory/search",
            params={"user_id": "test_user_002", "query": "火星"}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["count"] >= 1
        assert any("火星" in r["content"] for r in result["results"])

@pytest.mark.asyncio
async def test_performance():
    """測試性能 - 響應時間必須 <200ms"""
    async with httpx.AsyncClient() as client:
        # 測試存儲性能
        start_time = datetime.now()
        response = await client.post(f"{BASE_URL}/memory/store", json={
            "user_id": "perf_test",
            "content": "Performance test memory",
            "context": {}
        })
        store_time = (datetime.now() - start_time).total_seconds() * 1000
        
        assert response.status_code == 200
        assert store_time < 200, f"Store took {store_time}ms, should be <200ms"
        
        # 測試搜索性能
        start_time = datetime.now()
        response = await client.get(
            f"{BASE_URL}/memory/search",
            params={"user_id": "perf_test", "query": "test"}
        )
        search_time = (datetime.now() - start_time).total_seconds() * 1000
        
        assert response.status_code == 200
        assert search_time < 200, f"Search took {search_time}ms, should be <200ms"

@pytest.mark.asyncio
async def test_stats_endpoint():
    """測試統計端點"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_users" in data
        assert "total_memories" in data
        assert data["status"] == "Day 1 - On track"

# 運行測試的便捷腳本
if __name__ == "__main__":
    print("🧪 Running Memory API Tests - Day 1")
    print("🚀 Target: All tests pass in <5 seconds")
    pytest.main([__file__, "-v", "--tb=short"])