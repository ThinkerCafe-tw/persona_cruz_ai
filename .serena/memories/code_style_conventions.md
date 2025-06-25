# 程式碼風格與慣例

## Python 程式碼風格
1. **命名規範**
   - 檔案名：snake_case (例如：quantum_memory.py)
   - 類別名：PascalCase (例如：FiveElementsAgent)
   - 函數名：snake_case (例如：get_response)
   - 常數：UPPER_SNAKE_CASE (例如：JOKES)

2. **型別提示**
   - 使用 Python type hints
   - 例如：def get_response(self, user_id: str, message: str) -> str:

3. **註解風格**
   - 中文註解為主（配合專案特色）
   - 重要功能都有中文說明
   - 錯誤處理包含詳細的中文錯誤訊息

4. **檔案結構**
   - 主要功能模組化分離
   - 每個服務都有獨立的檔案
   - 測試檔案放在 tests/ 目錄

## 特殊慣例
1. **人格系統**
   - 每個人格必須使用固定的 emoji 標識
   - 人格切換時必須顯示對應 emoji

2. **錯誤處理**
   - 使用 try-except 包裹所有外部 API 呼叫
   - 詳細記錄錯誤日誌
   - 提供友善的中文錯誤訊息給用戶

3. **日誌記錄**
   - 使用 Python logging 模組
   - 格式：'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   - 重要操作都要記錄日誌

4. **環境變數**
   - 不使用本地 .env 檔案
   - 所有環境變數在 Railway Dashboard 設定
   - 使用 config.py 統一管理

## 開發原則
1. **最小改動原則**
   - 優先修改現有程式碼而非重寫
   - 空檔案不代表沒有實作（先搜尋再動手）

2. **測試優先**
   - 啟動時執行 startup_test.py
   - 重要功能都要有測試

3. **記憶與反思**
   - 重要的開發教訓要記錄在 CLAUDE.md
   - 錯誤模式要記錄供未來參考