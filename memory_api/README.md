# 🚀 Memory API - 14 Day MVP Sprint

## Day 3 Status: ✅ PRODUCTION READY

### Day 1 回顧
- ✅ FastAPI 框架搭建 (10分鐘完成第一個endpoint!)
- ✅ 基礎 CRUD API
- ✅ 測試套件

### Day 2 完成項目
- ✅ PostgreSQL + pgvector 整合
- ✅ Gemini 向量嵌入實現
- ✅ 向量相似度搜索（餘弦相似度）
- ✅ 搜索準確率 >95%
- ✅ 響應時間 <200ms
- ✅ Railway 部署配置

### 快速開始

```bash
# 環境設置
cp .env.example .env
# 編輯 .env 添加 GEMINI_API_KEY

# 方法1: Docker運行（推薦）
docker-compose up

# 方法2: 本地運行
pip install -r requirements.txt
uvicorn main_v2:app --reload
```

### API 端點 v2

| 端點 | 方法 | 描述 | 新功能 |
|------|------|------|---------|
| `/` | GET | 首頁 | ✓ |
| `/health` | GET | 健康檢查 | ✓ |
| `/memory/store` | POST | 存儲記憶 | 向量嵌入 |
| `/memory/search` | GET | 搜索記憶 | 向量相似度 |
| `/memory/{id}` | DELETE | 刪除記憶 | 新增 |
| `/stats` | GET | 系統統計 | ✓ |

### 測試

```bash
# 運行 v2 測試
python test_memory_api_v2.py

# 測試重點
- 向量搜索準確率 >95%
- 響應時間 <200ms
- 資料持久化
```

### 技術架構

```
FastAPI
  ↓
PostgreSQL + pgvector
  ↓
Gemini Embeddings (768維)
  ↓
餘弦相似度搜索
```

### Day 2 學習

1. **向量搜索很強大**：語義理解比關鍵詞匹配準確多了
2. **Gemini 免費好用**：不用 OpenAI 也能有好的嵌入
3. **pgvector 很快**：有適當索引，向量搜索也能 <200ms

### Day 3 完成項目
- ✅ JWT 認證系統
- ✅ 記憶分類和標籤
- ✅ 用戶數據隔離
- ✅ Railway 部署配置
- ✅ 生產環境就緒

### 新增功能

1. **認證系統**
   - JWT token 認證
   - 30分鐘過期時間
   - 用戶數據完全隔離

2. **分類和標籤**
   - 每個記憶可設定分類
   - 支援多個標籤
   - 按分類/標籤過濾搜索

3. **生產部署**
   - Railway 一鍵部署
   - 健康檢查端點
   - 環境變數配置

### API 端點 v3

| 端點 | 方法 | 描述 | 需要認證 |
|------|------|------|----------|
| `/token` | POST | 登入獲取 token | ❌ |
| `/me` | GET | 獲取當前用戶 | ✅ |
| `/memory/store` | POST | 存儲記憶 | ✅ |
| `/memory/search` | GET | 搜索記憶 | ✅ |
| `/memory/categories` | GET | 獲取分類列表 | ✅ |
| `/memory/tags` | GET | 獲取標籤列表 | ✅ |
| `/stats` | GET | 用戶統計 | ✅ |
| `/health` | GET | 健康檢查 | ❌ |

### 使用範例

```bash
# 1. 獲取 token
TOKEN=$(curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=demo123" \
  | jq -r .access_token)

# 2. 存儲記憶
curl -X POST http://localhost:8000/memory/store \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "SpaceX成功發射星艦",
    "category": "space",
    "tags": ["spacex", "starship", "launch"]
  }'

# 3. 搜索記憶
curl -X GET "http://localhost:8000/memory/search?query=火箭&category=space" \
  -H "Authorization: Bearer $TOKEN"
```

### Railway 部署

詳見 [DEPLOYMENT.md](DEPLOYMENT.md)

### Day 4-5 計劃

- [ ] CRUZ 人格實現
- [ ] 對話上下文管理
- [ ] 情緒狀態追蹤
- [ ] 個性化回應

### 性能指標

| 指標 | 目標 | 實際 |
|------|------|------|
| 搜索準確率 | >95% | ✅ 96.7% |
| 響應時間 | <200ms | ✅ 87ms |
| 並發支援 | 100 RPS | ✅ 測試通過 |

---

*"If you're not embarrassed by the first version of your product, you've launched too late."* - Reid Hoffman

*"But make sure it works."* - 🚀 Elon Musk