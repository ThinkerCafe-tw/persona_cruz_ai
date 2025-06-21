# Claude Code 專案文件

此文件記錄專案的重要資訊，供 Claude Code 參考使用。

## 專案概述

這是一個整合 Google Gemini AI 的 Line Bot，主要功能包括：
- 使用 Gemini AI 進行智能對話
- 提供笑話功能
- 支援對話記憶

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
- **LINE_CHANNEL_SECRET**: Line Bot 的頻道密鑰
- **GEMINI_API_KEY**: Google Gemini AI 的 API 金鑰
- **GOOGLE_CALENDAR_CREDENTIALS**: Google 服務帳戶憑證（JSON 格式，選用）
- **PORT**: 應用程式監聽的連接埠（Railway 會自動設定）
- **FLASK_ENV**: Flask 環境（development/production）

## 專案結構

```
persona_cruz_ai/
├── .env                    # 環境變數（本地開發用）
├── .env.example           # 環境變數範例
├── .gitignore            # Git 忽略檔案
├── requirements.txt      # Python 套件清單
├── Procfile             # Railway 啟動指令
├── railway.json         # Railway 配置檔
├── app.py               # Flask 主程式
├── config.py            # 設定檔
├── line_bot_handler.py  # Line Bot 處理邏輯
├── gemini_service.py    # Gemini API 整合
├── jokes.py             # 笑話資料
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

## 維護提醒

- 定期檢查 Railway 的免費額度使用情況
- 更新相依套件時記得測試相容性
- 保持 API 金鑰的安全性，不要提交到版本控制