"""
Memory API v3 測試套件 - Day 3
測試認證、分類和標籤功能
"""
import pytest
import httpx
from datetime import datetime

BASE_URL = "http://localhost:8000"

# 測試用戶
TEST_USER = {
    "username": "demo@example.com",
    "password": "demo123"
}

@pytest.fixture
async def auth_headers():
    """獲取認證 headers"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/token",
            data=TEST_USER
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_authentication():
    """測試認證流程"""
    async with httpx.AsyncClient() as client:
        # 測試登入
        response = await client.post(
            f"{BASE_URL}/token",
            data=TEST_USER
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        # 測試錯誤密碼
        response = await client.post(
            f"{BASE_URL}/token",
            data={"username": "demo@example.com", "password": "wrong"}
        )
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoints(auth_headers):
    """測試需要認證的端點"""
    async with httpx.AsyncClient() as client:
        # 沒有 token 應該失敗
        response = await client.get(f"{BASE_URL}/me")
        assert response.status_code == 401
        
        # 有 token 應該成功
        response = await client.get(f"{BASE_URL}/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "demo@example.com"

@pytest.mark.asyncio
async def test_memory_with_categories_and_tags(auth_headers):
    """測試分類和標籤功能"""
    async with httpx.AsyncClient() as client:
        # 存儲帶分類和標籤的記憶
        memories = [
            {
                "content": "SpaceX將在2024年嘗試登陸火星",
                "category": "space",
                "tags": ["spacex", "mars", "2024"]
            },
            {
                "content": "特斯拉Cybertruck開始量產",
                "category": "tesla",
                "tags": ["tesla", "cybertruck", "ev"]
            },
            {
                "content": "Neuralink開始人體試驗",
                "category": "neuralink",
                "tags": ["neuralink", "bci", "medical"]
            }
        ]
        
        for memory in memories:
            response = await client.post(
                f"{BASE_URL}/memory/store",
                json=memory,
                headers=auth_headers
            )
            assert response.status_code == 200
            data = response.json()
            assert data["category"] == memory["category"]
            assert data["tags"] == memory["tags"]
        
        # 測試按分類搜索
        response = await client.get(
            f"{BASE_URL}/memory/search",
            params={"query": "科技", "category": "space"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        # 應該只返回 space 分類的記憶
        for result in data["results"]:
            assert result["category"] == "space"

@pytest.mark.asyncio
async def test_get_categories_and_tags(auth_headers):
    """測試獲取分類和標籤列表"""
    async with httpx.AsyncClient() as client:
        # 獲取分類
        response = await client.get(
            f"{BASE_URL}/memory/categories",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert isinstance(data["categories"], list)
        
        # 獲取標籤
        response = await client.get(
            f"{BASE_URL}/memory/tags",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "tags" in data
        assert isinstance(data["tags"], list)

@pytest.mark.asyncio
async def test_user_isolation(auth_headers):
    """測試用戶數據隔離"""
    async with httpx.AsyncClient() as client:
        # 用戶只能看到自己的統計
        response = await client.get(
            f"{BASE_URL}/stats",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "demo_user_001"

@pytest.mark.asyncio
async def test_production_readiness():
    """測試生產就緒檢查"""
    async with httpx.AsyncClient() as client:
        # 健康檢查不需要認證
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        
        # Railway 部署檢查
        response = await client.get(f"{BASE_URL}/railway/deploy-check")
        assert response.status_code == 200
        data = response.json()
        assert data["deploy_ready"] == True

# 性能測試
@pytest.mark.asyncio
async def test_performance_with_auth(auth_headers):
    """測試認證後的性能"""
    async with httpx.AsyncClient() as client:
        start_time = datetime.now()
        
        # 存儲記憶
        await client.post(
            f"{BASE_URL}/memory/store",
            json={"content": "Performance test with auth"},
            headers=auth_headers
        )
        
        # 搜索記憶
        response = await client.get(
            f"{BASE_URL}/memory/search",
            params={"query": "performance"},
            headers=auth_headers
        )
        
        total_time = (datetime.now() - start_time).total_seconds() * 1000
        assert response.status_code == 200
        assert total_time < 500, f"Total time {total_time}ms should be <500ms with auth"
        print(f"⚡ Authenticated request time: {total_time}ms")

if __name__ == "__main__":
    print("🧪 Running Memory API v3 Tests - Day 3")
    print("🔐 Testing authentication, categories, and tags")
    print("☁️ Testing production readiness")
    pytest.main([__file__, "-v", "--tb=short"])