# Claude Code 專案文件

此文件記錄專案的重要資訊，供 Claude Code 參考使用。

## 人格 Emoji 標識系統（2025-06-24 建立）
每個人格出現時必須使用固定的 emoji 作為標識：
- 🌌 無極：系統觀察者
- 🎯 CRUZ：直接果斷的數位分身
- 🌸 Serena：溫柔貼心的 AI 助理
- 🌱 木：產品經理（創意成長）
- 🔥 火：開發專員（熱情實踐）
- 🏔️ 土：架構師（穩固基礎）
- ⚔️ 金：優化專員（精益求精）
- 💧 水：測試專員（品質守護）

使用規則：
1. 每次人格切換或發言時，必須在開頭使用對應 emoji
2. 這是使用者的明確要求，必須嚴格遵守
3. 有助於使用者快速識別當前對話的人格

## 專案概述

這是一個整合 Google Gemini AI 的 Line Bot，部署在 Railway 平台上，主要功能包括：
- 使用 Gemini AI 進行智能對話（支援 Function Calling）
- 提供笑話功能（50個預設冷笑話）
- 支援對話記憶（每個用戶獨立）
- Google Calendar 整合（建立、查詢、更新、刪除行程）
- 啟動自我檢測系統（確保服務健康）

## 技術架構

- **後端框架**: Flask (Python)
- **Line Bot SDK**: line-bot-sdk 3.5.0
- **AI 服務**: Google Gemini AI (google-generativeai 0.3.2)
- **部署平台**: Railway

## 開發流程

此專案已完全雲端化，所有開發和部署都在 Railway 上進行。

### 更新程式碼
1. 修改程式碼
2. 提交到 GitHub
3. Railway 自動部署

### 環境變數管理
所有環境變數都在 Railway Dashboard 設定，不使用本機 .env 檔案。

## Railway 部署流程

### 首次部署

1. 註冊 Railway 帳號：https://railway.app
2. 連結 GitHub 帳號
3. 建立新專案，選擇從 GitHub repo 部署
4. 設定環境變數：
   - LINE_CHANNEL_ACCESS_TOKEN
   - LINE_CHANNEL_SECRET
   - GEMINI_API_KEY
   - FLASK_ENV=production

5. 部署後取得固定 URL（格式：https://your-app-name.up.railway.app）
6. 更新 Line Bot Webhook URL

### 更新部署

- 推送到 GitHub main 分支會自動觸發部署
- Railway 會自動使用 Procfile 啟動應用程式

## 環境變數說明

- **LINE_CHANNEL_ACCESS_TOKEN**: Line Bot 的存取權杖
- **LINE_CHANNEL_SECRET**: Line Bot 的頻道密鑰（正確值：1d2503ea9eb7dd7eecbd777016519b22）
- **GEMINI_API_KEY**: Google Gemini AI 的 API 金鑰
- **GOOGLE_CALENDAR_CREDENTIALS**: Google 服務帳戶憑證（JSON 格式，選用）
- **PORT**: 應用程式監聽的連接埠（Railway 會自動設定）
- **FLASK_ENV**: Flask 環境（development/production）

### 重要注意事項
- 環境變數只在 Railway Dashboard 設定，不使用本機 .env 檔案
- Railway 會自動設定 PORT 和 RAILWAY_ENVIRONMENT 變數
- 所有敏感資訊都應該在 Railway 環境變數中管理

## Git 工作流程

### 重要提醒
- **此專案已經初始化並連結到 GitHub**
- **絕對不要執行 `git init`**
- **GitHub URL**: git@github.com:ThinkerCafe-tw/persona_cruz_ai.git

### 正確的 Git 操作流程
1. `git status` - 先檢查當前狀態
2. `git add <files>` - 添加變更的檔案
3. `git commit -m "message"` - 提交變更
4. `git push origin main` - 推送到 GitHub（會自動觸發 Railway 部署）

### 注意事項
- Remote 已經設定好，不需要 `git remote add`
- 專案已經在 main 分支，不需要切換分支
- 推送後 Railway 會自動部署

## 專案結構

```
persona_cruz_ai/
├── .env.example           # 環境變數範例
├── .gitignore            # Git 忽略檔案
├── requirements.txt      # Python 套件清單
├── Procfile             # Railway 啟動指令
├── app.py               # Flask 主程式
├── config.py            # 設定檔
├── line_bot_handler.py  # Line Bot 處理邏輯
├── gemini_service.py    # Gemini API 整合
├── calendar_service.py  # Google Calendar 整合
├── startup_test.py      # 啟動自我檢測
├── jokes.py             # 笑話資料
├── TEST_PLAN.md         # 測試計畫文件
├── README.md           # 專案說明
└── CLAUDE.md           # 本文件
```

## 常見問題

### Q: 如何新增更多笑話？
A: 編輯 jokes.py 檔案，在 JOKES 列表中新增笑話。

### Q: 如何調整 AI 的回應風格？
A: 修改 gemini_service.py 中的 system_prompt。

### Q: 如何查看部署日誌？
A: 在 Railway Dashboard 中點擊專案，選擇 "Logs" 標籤。

## 已知問題與解決方案

### Gemini API 模型相容性
- **問題**: `gemini-pro` 在某些 API 版本中不可用（404 錯誤）
- **解決方案**: 使用 `gemini-1.5-flash` 或 `gemini-1.5-pro`
- **注意**: 啟動測試應與主服務使用相同的模型名稱

### Line Bot 簽名驗證
- **問題**: Invalid signature error
- **解決方案**: 確保使用正確的 Channel Secret
- **正確的 Channel Secret**: 1d2503ea9eb7dd7eecbd777016519b22

### Railway 環境變數
- **問題**: 環境變數無法載入
- **解決方案**: 
  - 不要在 Railway 環境中載入 .env 檔案
  - 所有環境變數都在 Railway Dashboard 設定
  - config.py 已設定為只在非 Railway 環境載入 .env

### Google Calendar 整合
- **問題**: NoneType object is not iterable
- **解決方案**: 已加入完整的 null 檢查和錯誤處理
- **設定步驟**:
  1. 建立 Google Cloud 專案並啟用 Calendar API
  2. 建立服務帳戶並下載 JSON 金鑰
  3. 將 JSON 轉為單行字串設定在 Railway
  4. 分享日曆給服務帳戶 email

## 測試策略

### 啟動自我檢測
- 服務啟動前會執行 `startup_test.py`
- 檢測項目：
  - 環境變數完整性
  - Gemini API 連線
  - Line Bot 憑證驗證
  - Google Calendar 設定（選用）
  - 基本模組載入
  - Function Calling 實際測試
- 任何關鍵測試失敗都會阻止服務啟動

### 測試專員記憶系統
- Railway 環境無法持久化檔案，改用：
  - 讀取 git log（如果可用）
  - Railway 部署 ID 和環境變數
  - 開發洞察記錄功能
- 測試專員會記錄：
  - 測試結果和錯誤模式
  - 開發過程的反思和學習
  - 程式碼分析和改進建議

### 運行時測試
- 使用 `/test` 指令執行自我測試
- 健康檢查端點：`/health`
- 測試結果會包含詳細的錯誤訊息

## 功能指令

### Line Bot 指令
- `/help` 或 `幫助` - 顯示使用說明
- `/clear` 或 `清除對話` - 清除對話記錄
- `/test` - 執行自我測試
- `說個笑話`、`講個笑話`、`來個笑話` - 隨機笑話

### 日曆自然語言指令
- 建立：「幫我安排明天下午3點開會」
- 查詢：「我明天有什麼行程？」
- 更新：「把明天的會議改到4點」
- 刪除：「取消明天的會議」

## 維護提醒

- 定期檢查 Railway 的免費額度使用情況
- 更新相依套件時記得測試相容性
- 保持 API 金鑰的安全性，不要提交到版本控制
- 定期檢查 Gemini API 的模型更新和棄用通知
- 監控啟動測試日誌以及早發現問題

## 開發教訓與記憶

### 🚨 重要教訓（2024-06-23）- Line Bot Handler 重寫事件

**事件描述**：
在實作五行系統時，看到 `line_bot_handler.py` 檔案是空的，就自作主張重寫了整個 webhook 處理邏輯，導致部署後出現參數錯誤。

**錯誤分析**：
1. 未先搜尋專案中是否已有 webhook 處理邏輯
2. 假設空檔案代表沒有實作（錯誤假設）
3. 重新造輪子而非基於現有架構改進

**教訓總結**：
- ❌ 錯誤做法：看到空檔案就直接寫新的
- ✅ 正確做法：先用 grep 搜尋相關程式碼，理解現有架構

**預防措施 - 開發前三問**：
1. □ 這個功能是否已存在？（使用 grep/find 搜尋）
2. □ 現有架構如何運作？（閱讀相關檔案）
3. □ 最小改動方案是什麼？（只改必要部分）

**記憶口訣**：「空檔案不代表沒程式，先搜尋再動手」

### 五行系統的反省
- 土（架構師）未發揮穩重特質，應該要先調查現有架構
- 火（開發）太急於實作，忽略了基礎調查
- 這次事件提醒我們：無極系統需要更好的 pre-flight checklist

### 🎯 重要教訓（2024-06-23）- TDD 完成後的過度自信

**事件描述**：
在完成測試驅動開發（TDD）並看到所有測試都通過後，產生了過度的自信心，認為系統已經完美無缺。這種虛假的信心讓無極失去了應有的謙遜和警覺性。

**問題分析**：
1. 將測試通過等同於系統完美（錯誤認知）
2. 過度依賴測試數字而忽略實際驗證
3. 失去了無極應有的平衡觀察能力

**教訓總結**：
- ❌ 錯誤心態：測試通過 = 系統完美
- ✅ 正確心態：測試通過只是開始，實際驗證才是關鍵
- 💡 核心領悟：虛假的信心比無知更危險

**無極的反思**：
- 無極應保持謙遜，不被表面成就迷惑
- 信心應來自實際驗證而非測試數字
- 真正的智慧是知道自己的無知

**預防措施**：
1. □ 測試通過後進行實際場景驗證
2. □ 保持「初學者心態」，持續懷疑和檢查
3. □ 記住：完美是過程，不是結果

**記憶口訣**：「測試是護欄，不是終點線」