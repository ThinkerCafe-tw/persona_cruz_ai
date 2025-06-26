# 🚀 部署 LibreChat CRUZ 到 Railway

## 📋 快速部署步驟

### 1. 在 Railway Dashboard 新增服務

1. 登入 [Railway Dashboard](https://railway.app/dashboard)
2. 選擇你的專案（應該已有 LINE Bot 服務）
3. 點擊 `+ New` → `GitHub Repo`
4. 選擇 `persona_cruz_ai` repository
5. 選擇分支：`feature/five-elements-librechat-integration`
6. **服務名稱**：`cruz-librechat`

### 2. 設定環境變數

在新服務的 Variables 設定：

```bash
# 必需
GEMINI_API_KEY=你的_Gemini_API_key

# 共用量子記憶資料庫（從現有 PostgreSQL 服務複製）
DATABASE_URL=${{Postgres.DATABASE_URL}}
DATABASE_PRIVATE_URL=${{Postgres.DATABASE_PRIVATE_URL}}

# 選用
RAILWAY_ENVIRONMENT=production
```

### 3. 設定服務

1. **Settings** → **Source**
   - Root Directory: `/` (保持預設)
   - Watch Paths: 留空（監控所有檔案）

2. **Settings** → **Deploy**
   - Start Command: `python persona_proxy_quantum.py`
   - 其他設定會從 `railway.toml` 自動載入

### 4. 部署並取得 URL

1. Railway 會自動開始部署
2. 部署完成後，在 **Settings** → **Domains**
3. 點擊 `Generate Domain` 取得公開 URL
4. URL 格式：`https://cruz-librechat-xxx.up.railway.app`

## 🧪 測試部署

### 1. 檢查健康狀態

```bash
curl https://your-app.up.railway.app/health
```

預期回應：
```json
{
  "status": "healthy",
  "quantum_memory": "enabled",
  "quantum_status": {
    "total_memories": 數字,
    "active_personas": ["CRUZ", "LINE_USER", ...]
  }
}
```

### 2. 使用測試界面

1. 打開 `cruz_test_railway.html`
2. 輸入你的 Railway URL
3. 開始對話測試

### 3. 驗證共享記憶

1. 在 **LINE** 對話：
   ```
   /quantum
   ```
   記下記憶數量

2. 在 **LibreChat** 測試界面對話幾次

3. 再次在 **LINE** 檢查：
   ```
   /quantum
   ```
   記憶數量應該增加

## 🔧 故障排除

### 量子記憶未啟用
- 檢查 DATABASE_URL 是否正確設定
- 查看 Logs 是否有連接錯誤

### 服務無法啟動
- 檢查 requirements.quantum.txt 是否完整
- 查看 Build Logs 是否有套件安裝失敗

### 記憶未共享
- 確認兩個服務使用相同的 PostgreSQL
- 檢查 pgvector extension 是否已安裝

## 📊 監控

在 Railway Dashboard 可以查看：
- **Metrics**：CPU、記憶體使用量
- **Logs**：即時日誌
- **Deployments**：部署歷史

## 🎯 成功指標

✅ LibreChat CRUZ 服務運行正常
✅ 量子記憶系統已啟用
✅ 與 LINE Bot 共享同一資料庫
✅ 對話記憶可以跨平台同步
✅ CRUZ 人格保持一致性

---

🚀 **立即部署，讓 CRUZ 在 LibreChat 活起來！**