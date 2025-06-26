# 🎯 CRUZ AI - 多人格 AI 助手系統

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-repo/cruz-ai)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/typescript-5.0+-blue.svg)](https://www.typescriptlang.org)

> 一個具有真實記憶、情緒系統和跨平台同步的多人格 AI 助手

## 🌟 特色功能

### 🎭 七種獨特 AI 人格
- **🎯 CRUZ** - 決斷果敢的行動派
- **🌸 Serena** - 溫柔體貼的支持者
- **🌳 Wood** - 創意無限的創新者
- **🔥 Fire** - 熱情洋溢的實踐者
- **🏔️ Earth** - 穩如泰山的架構師
- **⚔️ Metal** - 精益求精的優化師
- **💧 Water** - 靈活適應的測試員

### 💾 持久記憶系統
- 向量化語義搜尋
- 分類與標籤管理
- 對話歷史追蹤
- 跨會話記憶保持

### 🎯 情緒智能引擎
- 6 種情緒狀態
- 動態情緒轉換
- 行為模式調整
- 自然情緒衰減

### 🌐 跨平台同步
- 即時狀態同步
- 多設備支援
- 統一 API 接口
- WebSocket 推送

## 🚀 快速開始

### 系統需求
- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (可選，用於 SDK)
- Docker & Docker Compose (推薦)

### 使用 Docker 部署（推薦）

```bash
# 克隆專案
git clone https://github.com/your-repo/cruz-ai.git
cd cruz-ai

# 設定環境變數
cp .env.example .env
# 編輯 .env 文件，設定 GEMINI_API_KEY

# 啟動所有服務
docker-compose up -d

# 檢查服務狀態
docker-compose ps
```

服務將在以下端口啟動：
- Memory API: http://localhost:8000
- Persona Proxy: http://localhost:8001
- Unified Gateway: http://localhost:8002
- Grafana 監控: http://localhost:3000

### 手動部署

#### 1. 安裝依賴

```bash
# Python 依賴
pip install -r requirements.txt

# 初始化資料庫
createdb persona_cruz_memory
psql persona_cruz_memory < memory_api/init.sql
```

#### 2. 啟動服務

```bash
# Terminal 1: Memory API
cd memory_api
uvicorn main_v3:app --reload

# Terminal 2: Persona Proxy
python librechat_integration/persona_proxy_server.py

# Terminal 3: Unified Gateway
python cross_platform/unified_gateway.py
```

## 📖 使用指南

### Python SDK

```python
from cruz_ai_sdk import create_cruz_ai, PersonaType

# 初始化 SDK
sdk = create_cruz_ai(
    api_key="your-api-key",
    platform="python-app"
)

await sdk.initialize("user123")

# 發送消息
response = await sdk.send_message(
    message="我需要一些建議",
    persona=PersonaType.CRUZ_DECISIVE.value
)
print(f"🎯 CRUZ: {response.response}")

# 切換人格
await sdk.switch_persona(PersonaType.SERENA_SUPPORTIVE)

# 切換記憶功能
await sdk.toggle_memory(True)
```

### TypeScript/JavaScript SDK

```typescript
import { createCruzAI } from 'cruz-ai-sdk';

// 初始化 SDK
const sdk = createCruzAI({
  apiKey: 'your-api-key',
  platform: 'web'
});

await sdk.initialize('user123');

// 發送消息
const response = await sdk.sendMessage({
  message: "需要幫助完成專案",
  persona: "cruz-decisive"
});

// 監聽事件
sdk.on('persona_changed', (event) => {
  console.log('人格已切換:', event.persona);
});
```

### Discord Bot

```bash
# 設定環境變數
export DISCORD_BOT_TOKEN="your-bot-token"
export CRUZ_API_KEY="your-api-key"

# 啟動 Bot
python cross_platform/bots/discord_bot.py
```

Discord 指令：
- `!cruz persona [name]` - 切換人格
- `!cruz memory [on/off]` - 開關記憶
- `!cruz status` - 查看狀態
- `@CRUZ [message]` - 對話

## 🏗️ 系統架構

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Discord   │     │  Telegram   │     │  Web App    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                    │
       └───────────────────┴────────────────────┘
                           │
                  ┌────────▼────────┐
                  │ Unified Gateway │
                  │   (Port 8002)   │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐ ┌───────▼────────┐ ┌──────▼──────┐
│ Persona Proxy  │ │  Memory API    │ │  Gemini AI  │
│  (Port 8001)   │ │  (Port 8000)   │ │             │
└────────────────┘ └────────────────┘ └─────────────┘
        │                  │
        │          ┌───────▼────────┐
        │          │  PostgreSQL    │
        │          │  + pgvector    │
        │          └────────────────┘
        │
┌───────▼────────┐
│ Emotion Engine │
│ + Personality  │
└────────────────┘
```

## 🧪 測試

### 執行測試套件

```bash
# 執行所有測試
python tests/test_suite.py

# 使用 pytest
pytest tests/ -v

# 測試覆蓋率
pytest tests/ --cov=. --cov-report=html
```

### 測試類別
- ✅ Memory API CRUD 操作
- ✅ 人格一致性測試
- ✅ 跨平台同步測試
- ✅ 效能壓力測試
- ✅ 安全性測試

## 📊 監控與維運

### Prometheus 指標
- 請求數量與延遲
- 活躍用戶數
- 記憶體使用量
- 錯誤率統計

### Grafana 儀表板
訪問 http://localhost:3000
- 預設帳號：admin
- 預設密碼：admin

## 🔧 配置說明

### 環境變數

```env
# AI 服務
GEMINI_API_KEY=your-gemini-api-key

# 資料庫
DATABASE_URL=postgresql://user:pass@localhost/dbname

# 認證
JWT_SECRET=your-secret-key

# Discord Bot (可選)
DISCORD_BOT_TOKEN=your-bot-token

# 監控 (可選)
GRAFANA_PASSWORD=secure-password
```

### 人格配置

編輯 `personality/cruz_personality.json` 來調整人格特徵：

```json
{
  "core_traits": {
    "decisiveness": 0.95,
    "confidence": 0.90,
    "action_oriented": 0.92
  }
}
```

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 📝 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

## 🙏 致謝

- Google Gemini AI 團隊
- LibreChat 開源社群
- 所有貢獻者與測試者

## 📞 聯絡方式

- 專案網站：[https://cruz-ai.example.com](https://cruz-ai.example.com)
- 問題回報：[GitHub Issues](https://github.com/your-repo/cruz-ai/issues)
- 電子郵件：contact@cruz-ai.example.com

---

<p align="center">
  <strong>🎯 CRUZ 說：「別光看文檔，開始使用吧！行動勝過千言萬語！」</strong>
</p>