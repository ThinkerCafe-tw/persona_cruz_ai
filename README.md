# Persona Cruz AI - Line Bot with Gemini

一個整合了 Google Gemini AI 的 Line 聊天機器人。

## 功能特色

- 使用 Google Gemini AI 進行智能對話
- 支援對話記憶功能
- 簡單的指令系統（/help、/clear）
- 使用 Ngrok 進行本地開發測試

## 安裝步驟

### 1. 複製專案

```bash
git clone git@github.com:ThinkerCafe-tw/persona_cruz_ai.git
cd persona_cruz_ai
```

### 2. 建立虛擬環境（建議）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 4. 設定環境變數

編輯 `.env` 檔案，填入您的 API 金鑰：

```
LINE_CHANNEL_ACCESS_TOKEN=您的_Line_Channel_Access_Token
LINE_CHANNEL_SECRET=您的_Line_Channel_Secret
GEMINI_API_KEY=您的_Gemini_API_Key
```

### 5. 啟動應用程式

```bash
python app.py
```

## 使用 Ngrok 設定 Webhook

### 1. 安裝 Ngrok

從 [ngrok.com](https://ngrok.com) 下載並安裝 Ngrok。

### 2. 啟動 Ngrok

```bash
ngrok http 5000
```

### 3. 設定 Line Bot Webhook URL

將 Ngrok 提供的 HTTPS URL 加上 `/callback` 設定到 Line Developers Console：

```
https://your-ngrok-url.ngrok.io/callback
```

## 專案結構

```
persona_cruz_ai/
├── .env                    # 環境變數（不要提交到 Git）
├── .env.example           # 環境變數範例
├── .gitignore            # Git 忽略檔案
├── requirements.txt      # Python 套件清單
├── app.py               # Flask 主程式
├── config.py            # 設定檔
├── line_bot_handler.py  # Line Bot 處理邏輯
├── gemini_service.py    # Gemini API 整合
└── README.md           # 專案說明
```

## 使用說明

### 基本對話

直接在 Line 中傳送訊息給機器人，它會使用 Gemini AI 回應。

### 特殊指令

- `/help` 或 `幫助` - 顯示使用說明
- `/clear` 或 `清除對話` - 清除對話記錄

## 部署建議

開發測試完成後，建議部署到以下平台之一：

- [Render](https://render.com) - 提供免費方案
- [Railway](https://railway.app) - 簡單快速部署
- [Heroku](https://heroku.com) - 成熟的 PaaS 平台
- [Google Cloud Run](https://cloud.google.com/run) - 無伺服器容器平台

## 注意事項

1. 請勿將 `.env` 檔案提交到版本控制系統
2. 定期更新相依套件以確保安全性
3. 在生產環境中請關閉 DEBUG 模式

## 授權

MIT License