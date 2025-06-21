# Persona Cruz AI - Line Bot with Gemini

一個整合了 Google Gemini AI 的 Line 聊天機器人，部署在 Railway 雲端平台。

## 功能特色

- 使用 Google Gemini AI 進行智能對話
- 支援對話記憶功能
- 內建 50 個冷笑話功能
- Google Calendar 整合（建立、查詢行程）
- 簡單的指令系統（/help、/clear、說個笑話）
- 24/7 雲端運行

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
├── jokes.py             # 笑話資料
├── CLAUDE.md           # Claude Code 文件
└── README.md           # 專案說明
```

## 使用說明

### 基本對話

直接在 Line 中傳送訊息給機器人，它會使用 Gemini AI 回應。

### 特殊指令

- `/help` 或 `幫助` - 顯示使用說明
- `/clear` 或 `清除對話` - 清除對話記錄
- `說個笑話` - 隨機回覆一個冷笑話

### 日曆功能

- 建立行程：「幫我安排明天下午3點開會」
- 查詢行程：「我明天有什麼行程？」
- 自然語言對話即可操作日曆

## 部署到 Railway

### 快速部署步驟

1. **註冊 Railway 帳號**
   - 前往 [Railway](https://railway.app) 註冊帳號
   - 連結您的 GitHub 帳號

2. **建立新專案**
   - 點擊 "New Project"
   - 選擇 "Deploy from GitHub repo"
   - 選擇 `persona_cruz_ai` 專案

3. **設定環境變數**
   在 Railway 專案設定中新增以下環境變數：
   ```
   LINE_CHANNEL_ACCESS_TOKEN=您的_Line_Channel_Access_Token
   LINE_CHANNEL_SECRET=您的_Line_Channel_Secret
   GEMINI_API_KEY=您的_Gemini_API_Key
   GOOGLE_CALENDAR_CREDENTIALS=您的_Google_服務帳戶_JSON（選用）
   FLASK_ENV=production
   ```

4. **取得部署 URL**
   - 部署完成後，Railway 會提供一個固定的 HTTPS URL
   - 格式類似：`https://your-app-name.up.railway.app`

5. **更新 Line Bot Webhook**
   - 回到 Line Developers Console
   - 將 Webhook URL 更新為：`https://your-railway-url.up.railway.app/callback`
   - 點擊 Verify 確認連線

## Google Calendar 設定（選用）

1. **建立 Google Cloud 專案**
   - 到 [Google Cloud Console](https://console.cloud.google.com)
   - 啟用 Google Calendar API

2. **建立服務帳戶**
   - 建立服務帳戶並下載 JSON 金鑰
   - 將 JSON 內容轉為單行字串

3. **分享日曆**
   - 在 Google Calendar 分享您的日曆給服務帳戶 email
   - 給予「進行變更及管理共用設定」權限

## 注意事項

1. 所有設定都在 Railway 環境變數中管理
2. 不需要本機 `.env` 檔案
3. 自動從 GitHub 部署更新

## 授權

MIT License