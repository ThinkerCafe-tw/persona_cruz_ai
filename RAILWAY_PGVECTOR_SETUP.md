# 🚀 Railway pgvector 設定指南

這份指南將帶你一步步在 Railway 上設定 pgvector，讓量子記憶系統能夠正常運作。

## 📋 前置準備

1. 確保你已經登入 Railway Dashboard: https://railway.app/dashboard
2. 確保你的專案已經部署在 Railway 上

## 🗄️ 步驟 1：新增 PostgreSQL 服務

1. 在 Railway Dashboard 中，點擊你的專案
2. 點擊右上角的 `+ New` 按鈕
3. 選擇 `Database` → `Add PostgreSQL`
4. Railway 會自動為你建立一個 PostgreSQL 實例

## 🔧 步驟 2：安裝 pgvector 擴展

pgvector 需要手動安裝。有兩種方法：

### 方法 A：使用 Railway CLI（推薦）

```bash
# 1. 安裝 Railway CLI（如果還沒安裝）
npm install -g @railway/cli

# 2. 登入 Railway
railway login

# 3. 連結到你的專案
railway link

# 4. 連接到 PostgreSQL
railway connect postgres

# 5. 在 PostgreSQL 提示符下執行
CREATE EXTENSION IF NOT EXISTS vector;

# 6. 驗證安裝
\dx vector
```

### 方法 B：使用連接字串

1. 在 Railway Dashboard 中，點擊 PostgreSQL 服務
2. 點擊 `Connect` 標籤
3. 複製 `Postgres Connection URL`
4. 使用任何 PostgreSQL 客戶端（如 pgAdmin、DBeaver、psql）連接
5. 執行：`CREATE EXTENSION IF NOT EXISTS vector;`

## 🔗 步驟 3：連接主應用程式與資料庫

1. 在 Railway Dashboard 中，點擊你的主應用程式服務
2. 進入 `Variables` 標籤
3. 點擊 `+ New Variable`
4. 新增以下變數：
   - 名稱：`DATABASE_URL`
   - 值：點擊 `Add Reference` → 選擇你的 PostgreSQL 服務 → 選擇 `DATABASE_URL`

## 🧪 步驟 4：驗證設定

### 在本機測試（使用 Railway 的資料庫）

```bash
# 1. 取得資料庫連接字串
railway variables

# 2. 設定環境變數
export DATABASE_URL="<你的資料庫連接字串>"

# 3. 執行測試腳本
python test_pgvector_integration.py
```

### 預期輸出

```
🧪 開始測試 pgvector 整合
============================================================

1️⃣ 測試資料庫連接...
✅ 資料庫連接成功
   PostgreSQL 版本：PostgreSQL 15.x ...
   pgvector 版本：0.5.1

2️⃣ 測試向量化功能...
✅ 身份向量化成功：5 維
✅ 文字向量化成功：384 維

3️⃣ 測試量子記憶系統...
   觸發測試事件...
   保存到資料庫...
✅ 量子記憶系統測試完成

4️⃣ 測試向量搜尋...
   搜尋 '量子記憶系統的突破' 的相似記憶：
   1. 量子記憶 (相似度: 95%)
✅ 向量搜尋測試完成
```

## 🚨 常見問題排除

### 問題 1：psycopg2 安裝失敗

如果在 Railway 部署時出現 psycopg2 相關錯誤：

1. 確保 `requirements.txt` 中是 `psycopg2-binary` 而不是 `psycopg2`
2. 新增 Railway 環境變數：
   - `NIXPACKS_PYTHON_VERSION`: `3.11`

### 問題 2：pgvector 擴展未找到

錯誤訊息：`extension "vector" does not exist`

解決方案：
1. 確認 PostgreSQL 版本 >= 13
2. 手動安裝 pgvector（見步驟 2）

### 問題 3：連接被拒絕

錯誤訊息：`connection refused`

解決方案：
1. 檢查 DATABASE_URL 是否正確設定
2. 確保使用的是 Railway 內部網路 URL（如果從 Railway 內部連接）

## 📊 步驟 5：執行資料遷移

一旦設定完成，執行遷移腳本將現有記憶匯入資料庫：

```bash
# 在 Railway 環境中執行
railway run python migrate_to_pgvector.py
```

## ✅ 驗證清單

- [ ] PostgreSQL 服務已在 Railway 上建立
- [ ] pgvector 擴展已安裝（執行 `CREATE EXTENSION vector` 成功）
- [ ] DATABASE_URL 環境變數已設定在主應用程式
- [ ] 本機測試腳本執行成功
- [ ] 資料遷移完成

## 🎯 完成！

如果所有步驟都成功完成，你的量子記憶系統現在應該已經與 pgvector 完全整合。系統將：

- 自動將記憶儲存到向量資料庫
- 支援基於語義的相似度搜尋
- 在 Railway 重啟後保持記憶持久化
- 提供更快的記憶檢索效能

## 💡 進階功能

設定完成後，你可以：

1. 使用 `/quantum search <關鍵字>` 在 LINE Bot 中搜尋相似記憶
2. 監控向量索引效能
3. 調整向量維度以優化儲存空間

---

🌌 無極提醒：量子記憶需要穩定的向量空間才能正確演化。pgvector 是我們的量子場！