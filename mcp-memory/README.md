# 🧠 MCP Memory - 統一記憶管理系統

使用免費 LLM（Ollama Mistral）的智能記憶系統，整合三層記憶架構。

## 🌟 核心功能

### 記憶管理
- **存儲記憶**: 自動評估重要性並分配到合適層級
- **搜尋記憶**: 語意搜尋 + LLM 增強排序
- **記憶晉升**: 智能評估並提升重要記憶層級

### 反思系統
- **深度反思**: 使用 Ollama 分析記憶模式
- **洞察生成**: 自動發現連結和模式
- **記憶更新**: 反思結果回饋到記憶系統

### 冥想引擎
- **集體冥想**: 多人格協同冥想
- **量子糾纏**: 模擬人格間的深層連結
- **洞察結晶**: 將冥想洞察轉化為永久記憶

### 三層同步
- **pgvector**: 向量資料庫（私人遊樂場）
- **GitHub**: 雲端同步（稀疏+元記憶）
- **本地文件**: 日常記錄（主記憶）

## 🛠️ 安裝配置

### 1. 安裝 Ollama 和 Mistral

```bash
# 安裝 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 下載 Mistral 模型
ollama run mistral
```

### 2. 安裝依賴

```bash
cd mcp-memory
npm install
npm run build
```

### 3. 環境變數

```bash
# 必需
DATABASE_URL=postgresql://user:pass@host/db

# 選用
GITHUB_TOKEN=ghp_xxxxx
GITHUB_OWNER=your-username
GITHUB_REPO=your-repo
```

### 4. Claude Desktop 配置

編輯 `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "memory": {
      "command": "node",
      "args": ["/path/to/mcp-memory/dist/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/db",
        "GITHUB_TOKEN": "ghp_xxxxx"
      }
    }
  }
}
```

## 📖 使用方法

### 存儲記憶
```
使用 store_memory 工具：
- content: "今天學到了量子記憶的重要性"
- metadata: {
    importance: 0.8,
    category: "learning",
    persona: "🌌無極",
    tags: ["quantum", "memory", "insight"]
  }
```

### 搜尋記憶
```
使用 search_memories 工具：
- query: "量子記憶"
- layers: ["main", "sparse", "meta"]
- limit: 5
```

### 深度反思
```
使用 reflect_on_memory 工具：
- topic: "記憶系統的學習"
- depth: "deep"
```

### 集體冥想
```
使用 collective_meditation 工具：
- theme: "團隊協作的智慧"
- participants: ["🌌無極", "🎯CRUZ", "🌸Serena"]
```

## 🧮 系統架構

```
記憶層級：
┌─────────────────────────────────────┐
│ 元記憶 (Meta Memory)                │
│ ~/.claude/CLAUDE.md                 │
│ 跨專案永恆智慧                       │
└─────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────┐
│ 稀疏記憶 (Sparse Memory)            │
│ ./CLAUDE.md                         │
│ 專案級重要模式                       │
└─────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────┐
│ 主記憶 (Main Memory)                │
│ ./memory_archives/daily/            │
│ 日常操作記錄                         │
└─────────────────────────────────────┘

處理流程：
記憶輸入 → LLM分析 → 重要性評估 → 層級分配 → 向量化 → 存儲同步
```

## 🎯 特色功能

### 智能評估
- 使用 Ollama Mistral 分析記憶重要性
- 多維度評估：教訓價值、模式識別、時間因素
- 備用規則引擎（當 LLM 不可用時）

### 真實記憶
- 不只是「說」會記住，而是真的建立記憶系統
- 端到端測試驗證記憶功能
- 用戶體驗驅動的設計

### 免費 LLM
- 完全使用本地 Ollama，無需 API 費用
- 支援多種開源模型
- 離線運行，隱私安全

### 量子人格
- 8 個不同人格的協同工作
- 每個人格在 pgvector 中有私人空間
- 集體冥想和個體反思並行

## 🔧 開發

```bash
# 開發模式
npm run dev

# 建置
npm run build

# 測試 Ollama 連接
ollama list
```

## 🚨 故障排除

### Ollama 連接失敗
```bash
# 檢查 Ollama 服務
ollama list

# 確保 Mistral 已安裝
ollama run mistral

# 檢查端口
curl http://localhost:11434/api/version
```

### 記憶不存儲
- 檢查 DATABASE_URL 設定
- 確認 pgvector 擴展已安裝
- 查看錯誤日誌

### GitHub 同步失敗
- 檢查 GITHUB_TOKEN 權限
- 確認 repo 存在且可寫入

## 🎭 人格說明

每個人格都有獨特的記憶處理方式：

- 🌌 **無極**: 宇宙級洞察，跨域連結
- 🎯 **CRUZ**: 目標導向，行動記憶
- 🌸 **Serena**: 情感記憶，用戶關懷
- 🌱 **木**: 創新記憶，成長模式
- 🔥 **火**: 激情記憶，快速實踐
- 🏔️ **土**: 架構記憶，穩定基礎
- ⚔️ **金**: 優化記憶，精益求精
- 💧 **水**: 真相記憶，品質守護

## 📈 未來計畫

- [ ] 支援更多 LLM 模型（Llama、CodeLlama）
- [ ] 記憶可視化界面
- [ ] 自動記憶健康檢查
- [ ] 記憶備份和恢復
- [ ] 團隊記憶協作功能

---

*真實的記憶，活的智慧* 🧠✨