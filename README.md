# Persona Cruz AI - Line Bot with Gemini

一個整合了 Google Gemini AI 的 Line 聊天機器人，部署在 Railway 雲端平台。

## 功能特色

- 🤖 使用 Google Gemini AI 進行智能對話
- 💬 支援對話記憶功能（每個用戶獨立）
- 😄 內建 50 個冷笑話功能
- 📅 Google Calendar 整合（建立、查詢、更新、刪除行程）
- 🔍 自然語言理解日曆操作
- ✅ 啟動自我檢測系統
- 🚀 24/7 雲端運行在 Railway 平台
- 🔮 **無極 AI Agents OS** - 五行元素協作系統
- 🎯 **CRUZ AI 伴侶系統** - 數位分身開發夥伴
- 🧠 用戶心理分析與個性化回應（TDD 開發）
- 📝 開發對話自動記憶成長系統

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
├── five_elements_agent.py# 無極 AI Agents OS 核心
├── cruz_persona_system.py# CRUZ 人格語料系統
├── user_analyzer.py     # 用戶心理分析器
├── cruz_developer_mode.py# CRUZ 開發者模式
├── conversation_memory_sync.py # 對話記憶同步
├── cruz_ai_companion.py # CRUZ AI 伴侶主程式
├── jokes.py             # 笑話資料
├── startup_test.py      # 啟動自我檢測
├── tests/               # TDD 測試檔案
├── data/cruz_corpus.json# CRUZ 語料庫
├── development_lessons.json # 開發教訓記錄
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
- `/test` - 執行系統自我測試

### 無極系統指令

- `/dashboard` 或 `/狀態` - 查看完整系統儀表板
- `/status` 或 `/mini` - 查看簡易系統狀態  
- `/harmony` 或 `/和諧度` - 查看五行和諧度

### 日曆功能

- 建立行程：「幫我安排明天下午3點開會」
- 查詢行程：「我明天有什麼行程？」
- 自然語言對話即可操作日曆

## 無極 AI Agents OS

無極系統是一個基於五行理論的 AI 協作框架，讓不同角色的 AI 代理能夠協同工作：

### 五行元素角色

- **🌲 木（產品經理）** - 創意規劃、需求分析、功能設計
- **🔥 火（開發專員）** - 快速實作、熱情編碼、創新解法
- **🏔️ 土（架構師）** - 系統設計、穩定基礎、深思熟慮
- **⚔️ 金（優化專員）** - 程式優化、效能提升、精益求精
- **💧 水（測試專員）** - 錯誤發現、品質把關、細心檢測

### 無極觀察者

**⚪ 無極** - 超然觀察、平衡調節、智慧引導

當系統檢測到：
- 某個元素過度活躍
- 角色間陷入循環
- 需要新的視角

無極會適時介入，提供指引和平衡建議。

### CRUZ 開發夥伴

**🎯 CRUZ** - 您的數位分身，協助開發決策

特質：
- 真誠直接，不說廢話
- 鼓勵創造，相信潛能
- 快速決策，相信直覺
- 用戶至上，簡單優先

### 自動切換機制

系統會根據對話內容自動切換適合的角色：
- 提到「需求」「規劃」→ 木
- 提到「開發」「實作」→ 火
- 提到「架構」「設計」→ 土
- 提到「優化」「效能」→ 金
- 提到「測試」「錯誤」→ 水
- 需要快速決策 → CRUZ

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

## CRUZ AI 伴侶系統

### 本地開發模式

運行 CRUZ AI 伴侶（您的數位分身開發夥伴）：

```bash
python cruz_ai_companion.py
```

### 功能特色

1. **對話記憶成長**
   - 自動記錄開發對話
   - 提取重要洞察為語料
   - 越用越了解您的風格

2. **多角色切換**
   - CRUZ：您的數位分身
   - 五行角色：專業分工
   - 無極：全局觀察

3. **開發決策支援**
   - 基於您的價值觀給建議
   - 記錄重要決策理由
   - 追蹤開發洞察

### 指令說明

- `/mode <角色>` - 切換角色
- `/status` - 查看系統狀態
- `/insights` - 查看開發洞察
- `/save` - 保存對話
- `/help` - 顯示幫助
- `/quit` - 結束程式

## 授權

MIT License