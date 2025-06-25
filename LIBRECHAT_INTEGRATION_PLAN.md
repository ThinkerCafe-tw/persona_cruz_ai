# LibreChat 整合計畫

## 🎯 目標
將 persona_cruz_ai 的核心功能整合到 LibreChat，創建一個具有獨特人格系統的 AI 對話平台。

## 📋 整合範圍

### Phase 1: 核心人格與記憶引擎
1. **量子記憶系統**
   - 將現有的 pgvector 記憶系統整合到 LibreChat
   - 保留量子態管理邏輯
   - 建立記憶檢索 API

2. **CRUZ 人格系統**
   - 將五行 AI Agents 整合為 LibreChat 的模型選項
   - 實作人格切換機制
   - 保留人格特定的系統提示詞

3. **AI 日記系統**
   - 整合日記記錄功能
   - 建立故事化場景追蹤

### Phase 2: 技術架構整合

#### LibreChat 技術棧
- **前端**: React + TypeScript + Tailwind CSS
- **後端**: Node.js/Express + Python/FastAPI
- **資料庫**: MongoDB (對話) + PostgreSQL/pgvector (記憶)
- **搜尋**: Meilisearch
- **部署**: Docker Compose

#### 整合點
1. **後端整合**
   - 在 LibreChat API 中加入量子記憶端點
   - 擴展模型選擇以支援人格系統
   - 整合現有的 Function Calling 邏輯

2. **前端整合**
   - 新增人格選擇器 UI
   - 顯示當前人格狀態（emoji 標識）
   - 記憶瀏覽介面

3. **資料庫整合**
   - MongoDB: 儲存對話歷史
   - PostgreSQL: 量子記憶和向量嵌入
   - 建立資料同步機制

## 🛠️ 實作步驟

### 步驟 1: 環境設置
```bash
# 1. 建立整合分支
git checkout -b feature/librechat-integration

# 2. 設置 Docker 環境
cp librechat_fork/docker-compose.override.yml.example docker-compose.override.yml

# 3. 配置環境變數
# 整合現有的 .env 設定到 LibreChat 格式
```

### 步驟 2: 後端整合
1. 在 `librechat_fork/api/server/routes/` 新增量子記憶路由
2. 在 `librechat_fork/api/app/clients/` 新增 CRUZ 人格客戶端
3. 整合現有的 `quantum_memory/` 模組

### 步驟 3: 前端整合
1. 在 `librechat_fork/client/src/components/` 新增人格選擇器
2. 修改對話介面以顯示人格 emoji
3. 新增記憶管理頁面

### 步驟 4: 資料庫遷移
1. 建立遷移腳本將現有資料轉換到 LibreChat 格式
2. 設置 pgvector 擴展
3. 建立必要的索引

## 📊 進度追蹤

- [x] Fork LibreChat 原始碼
- [ ] 審查 LibreChat 架構
- [ ] 建立 Docker 開發環境
- [ ] 整合量子記憶系統
- [ ] 實作人格切換功能
- [ ] 前端 UI 整合
- [ ] 測試與優化
- [ ] 部署到 Railway

## 🔍 技術挑戰

1. **認證系統整合**
   - LibreChat 使用 JWT + OAuth
   - 需要整合現有的使用者系統

2. **即時通訊**
   - LibreChat 使用 Server-Sent Events
   - 需要整合人格切換的即時更新

3. **多模型支援**
   - 保留 LibreChat 的多模型能力
   - 新增人格系統作為額外層

## 📝 注意事項

1. **保持相容性**
   - 盡量不修改 LibreChat 核心程式碼
   - 使用擴展點和插件機制

2. **效能考量**
   - 量子記憶查詢需要優化
   - 考慮使用快取機制

3. **部署策略**
   - 使用 Docker Compose 進行本地開發
   - Railway 部署需要調整配置

## 🚀 下一步行動

1. 完成 LibreChat 程式碼審查
2. 建立整合原型
3. 測試核心功能
4. 逐步遷移現有功能

---
最後更新：2025-06-25