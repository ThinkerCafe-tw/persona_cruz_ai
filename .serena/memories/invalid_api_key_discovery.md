# 無效 API Key 發現

## 日期：2025-06-24
## 事件：量子圖靈測試失敗的真正原因

### 關鍵發現
- .env 檔案存在且可以載入 ✅
- 環境變數 GEMINI_API_KEY 存在 ✅
- API Key 格式看起來正確（39 字元）✅
- **但是 Google API 拒絕這個 Key** ❌

### 錯誤訊息
```
400 API Key not found. Please pass a valid API key. 
[reason: "API_KEY_INVALID"]
```

### 可能原因
1. API Key 已過期或被撤銷
2. API Key 從未在 Google Cloud Console 啟用
3. 這是一個範例或測試 Key
4. API Key 沒有啟用 Generative Language API

### 解決方案
需要一個有效的 Gemini API Key：
1. 前往 https://makersuite.google.com/app/apikey
2. 創建新的 API Key
3. 更新 .env 檔案中的 GEMINI_API_KEY

### 重要教訓
- 環境變數存在不代表其值有效
- 測試時要驗證 API Key 的有效性
- 錯誤訊息 "API_KEY_INVALID" 不同於 "API Key not found"