# Railway PostgreSQL 連接快速修復指南

## 🚨 問題
- 錯誤：`could not translate host name 'postgres.railway.internal'`
- 原因：本地環境無法存取 Railway 內部網路

## ⚡ 快速解決方案

### 選項 1：使用公開 URL（推薦）

1. 在 Railway Dashboard 中找到你的 PostgreSQL 服務
2. 點擊 "Connect" 標籤
3. 複製 "Postgres Connection URL"（公開版本）
   - 格式：`postgresql://postgres:password@xxx.proxy.rlwy.net:port/railway`
4. 在本地 `.env` 檔案設定：
   ```
   DATABASE_URL=postgresql://postgres:password@xxx.proxy.rlwy.net:port/railway
   ```

### 選項 2：環境感知配置

在 `config.py` 中添加智能切換：

```python
# 資料庫設定 (pgvector)
if os.getenv('RAILWAY_ENVIRONMENT'):
    # 在 Railway 上使用內部 URL
    DATABASE_URL = os.getenv('DATABASE_PRIVATE_URL')
else:
    # 本地開發使用公開 URL
    DATABASE_URL = os.getenv('DATABASE_PUBLIC_URL', os.getenv('DATABASE_URL'))

# URL 格式轉換（保持現有邏輯）
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
```

然後在 `.env` 設定兩個 URL：
```
DATABASE_PUBLIC_URL=postgresql://postgres:password@xxx.proxy.rlwy.net:port/railway
DATABASE_PRIVATE_URL=postgresql://postgres:password@postgres.railway.internal:5432/railway
```

## 📝 注意事項

1. **公開 URL 的考量**
   - 會經過網際網路（有 SSL 加密）
   - 可能有輕微延遲
   - 適合開發和測試

2. **內部 URL 的優勢**
   - 只在 Railway 內部網路
   - 更低延遲
   - 更安全
   - 只能在部署環境使用

3. **安全建議**
   - 使用強密碼
   - 定期輪換憑證
   - 考慮 IP 白名單（如果 Railway 支援）

## 🎯 驗證連接

執行以下命令測試：
```bash
python check_pgvector.py
```

或使用 psql：
```bash
psql "postgresql://postgres:password@xxx.proxy.rlwy.net:port/railway"
```

## 🔍 除錯提示

如果仍有問題：
1. 確認服務正在運行（Railway Dashboard 顯示綠色）
2. 檢查密碼是否包含特殊字符（需要 URL 編碼）
3. 確認防火牆沒有阻擋連接
4. 查看 `system_intelligence/archaeological_records/` 的診斷記錄

---

> 由 DNS 考古學系統自動生成
> 更多細節請參考 DNS_ARCHAEOLOGY_REPORT.md