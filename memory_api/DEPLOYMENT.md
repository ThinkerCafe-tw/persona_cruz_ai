# 🚀 Railway 部署指南

## 快速部署步驟

### 1. 準備 Railway 帳號
- 註冊：https://railway.app
- 連結 GitHub

### 2. 創建新專案
```bash
# 在 Railway Dashboard
1. New Project
2. Deploy from GitHub repo
3. 選擇 persona_cruz_ai
```

### 3. 添加 PostgreSQL
```bash
# 在專案內
1. New Service
2. Database > PostgreSQL
3. 等待部署完成
```

### 4. 設定環境變數
在 Railway 專案設定中添加：
```
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your-secret-key-for-jwt
DATABASE_URL=（自動從 PostgreSQL 服務獲取）
```

### 5. 部署設定
Railway 會自動：
- 檢測 Python 專案
- 安裝 requirements.txt
- 使用 railway.toml 配置
- 分配 PORT 環境變數

### 6. 初始化資料庫
部署後第一次需要：
1. 進入 PostgreSQL 服務
2. 連接資料庫
3. 執行：`CREATE EXTENSION IF NOT EXISTS vector;`

### 7. 測試部署
```bash
# 獲取部署 URL
https://your-app.up.railway.app

# 測試健康檢查
curl https://your-app.up.railway.app/health

# 獲取 token
curl -X POST https://your-app.up.railway.app/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=demo123"

# 使用 API
curl https://your-app.up.railway.app/memory/store \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"My first memory in production!"}'
```

## 預設測試帳號
- Email: demo@example.com
- Password: demo123

## 監控
Railway 提供：
- 即時日誌
- 資源使用圖表
- 自動重啟
- 健康檢查

## 成本估算
- Starter Plan: $5/月
- 包含：
  - 512MB RAM
  - 1 vCPU
  - PostgreSQL
  - 自動 SSL

## 故障排除

### pgvector 安裝失敗
如果看到 pgvector 相關錯誤：
1. 在 PostgreSQL 中手動執行：`CREATE EXTENSION vector;`
2. 重新部署服務

### 記憶體不足
升級到 Developer Plan ($20/月) 獲得更多資源

### 連接超時
檢查：
- DATABASE_URL 是否正確
- PostgreSQL 服務是否運行
- 健康檢查端點是否正常

---

*"If it's not in production, it doesn't exist."* - 🚀 Elon Musk