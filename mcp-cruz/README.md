# CRUZ MCP Server

簡單實用的 MCP 服務，幫助 AI 更好地理解和記住對話。

## 功能

1. **記住對話** - 儲存用戶對話和上下文
2. **搜尋記憶** - 快速找到相關的過往對話
3. **分析理解** - 檢測 AI 理解與用戶意圖的差距
4. **用戶上下文** - 獲取用戶的完整對話歷史

## 安裝

```bash
npm install
npm run build
```

## 使用

### 在 Claude Desktop 配置

編輯 `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cruz": {
      "command": "node",
      "args": ["/path/to/mcp-cruz/dist/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/cruz_memory"
      }
    }
  }
}
```

### 資料庫設置

```sql
CREATE DATABASE cruz_memory;
```

服務會自動創建需要的表格。

## 工具使用範例

### 記住對話
```
使用 remember_conversation 工具：
- user_id: "user123"
- user_message: "我想學習 Python"
- ai_response: "建議從基礎語法開始..."
```

### 搜尋記憶
```
使用 search_memory 工具：
- query: "Python"
- user_id: "user123" (可選)
- limit: 5
```

### 獲取用戶上下文
```
使用 get_user_context 工具：
- user_id: "user123"
```

## 特點

- ✅ 簡單直接，專注核心功能
- ✅ 使用 PostgreSQL，穩定可靠
- ✅ 易於擴展和客製化
- ✅ 完整的錯誤處理

## License

MIT