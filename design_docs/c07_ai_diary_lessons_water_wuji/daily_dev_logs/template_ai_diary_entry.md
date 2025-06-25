```markdown
# 💧🌌 AI 開發日記條目模板

本模板旨在為所有 AI 代理（及人類協作者）提供一個標準化的日記條目格式，以便記錄開發過程中的行動、思考、情緒、學習和遇到的挑戰。請遵循 `CLAUDE.md` 中關於 AI 日記結構和 Scene Code 的指導原則。

**文件名規範建議**：`YYYY-MM-DD_간단한_설명_人格Emoji.json` (例如：`2024-07-16_fixed_memory_retrieval_bug_🔥.json`)
**存放位置**：`design_docs/c07_ai_diary_lessons_water_wuji/daily_dev_logs/`

## JSON 結構模板

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ", // ISO 8601 格式的UTC時間戳
  "agent_emoji": "💧", // 記錄者的人格 Emoji (🌌🎯🌸🌱🔥🏔️⚔️💧)
  "agent_name": "水", // 記錄者的人格名稱
  "task_id": "PROJECT-XYZ-123", // (可選) 關聯的任務/工單編號
  "action_summary": "詳細描述執行的主要行動或任務", // 對當前工作的簡明摘要
  "action_details": [ // (可選) 更詳細的步驟或觀察
    "步驟1：分析了記憶檢索模塊的日誌。",
    "步驟2：發現 pgvector 索引在特定查詢下失效。",
    "步驟3：與 🏔️土 討論後調整了索引參數。"
  ],
  "emotion_state": { // (可選) 記錄當時的情緒狀態，有助於理解決策背景
    "primary_emotion": "釋然", // 主要情緒
    "secondary_emotion": "疲憊但有成就感", // 次要情緒或更細緻的描述
    "intensity": 0.7 // 情緒強度 (0.0 - 1.0)
  },
  "story_metaphor": { // 參考 CLAUDE.md 的 Scene Code 分鏡表
    "story_series": "七龍珠Z", // IP/故事系列名稱
    "scene_description": "成功抵擋貝吉塔的加力炮攻擊後，悟空感到精疲力盡但守護了地球。", // 對應場景的簡要描述
    "scene_code": "DBZ_S01E28_DEFENSE" // Scene Code
  },
  "key_learnings_or_insights": [ // 本次行動中的主要學習、洞察或反思
    "pgvector 的 HNSW 索引對數據分佈敏感，需要定期監控和調整。",
    "💧水 與 🏔️土 的早期溝通能顯著加速問題定位。"
  ],
  "challenges_faced": [ // 遇到的困難或障礙
    {
      "challenge": "初始索引配置導致查詢超時。",
      "solution_attempted": "嘗試重建索引，調整 `ef_construction` 和 `m` 參數。",
      "is_resolved": true
    }
  ],
  "collaborators_involved": [ // 參與協作的其他AI人格或人類成員
    {"emoji": "🏔️", "name": "土", "contribution": "提供了 pgvector 索引優化建議"},
    {"emoji": "🌱", "name": "木", "contribution": "確認了記憶檢索的業務影響"}
  ],
  "code_references": [ // (可選) 相關的代碼文件路徑、函數名或 Commit ID
    "src/rag_api/memory_manager.py#L150-L200",
    "commit:abcdef1234567890"
  ],
  "next_steps_or_hooks": [ // 未來的行動計劃或需要其他人格跟進的事項
    "明日計劃：對記憶模塊進行壓力測試 (💧水)。",
    "提醒 🔥火：注意新索引對寫入性能的潛在影響。"
  ],
  "custom_tags": ["memory_module", "bugfix", "pgvector", "performance_optimization"] // 自定義標籤，便於搜索和分類
}
```

## 字段說明

*   **`timestamp`**: (必填) 事件發生的準確時間，使用 ISO 8601 格式的 UTC 時間。
*   **`agent_emoji`**: (必填) 執行此動作或記錄此日記的 AI 人格 Emoji。
*   **`agent_name`**: (必填) AI 人格的名稱。
*   **`task_id`**: (選填) 如果與特定的項目管理工具中的任務 ID 相關聯，填寫於此。
*   **`action_summary`**: (必填) 對所做工作的核心概括。
*   **`action_details`**: (選填) 列表形式，更詳細地描述執行的步驟、觀察到的現象等。
*   **`emotion_state`**: (選填) 描述記錄時的情緒狀態，有助於理解上下文和決策過程。
    *   `primary_emotion`: 主要情緒詞。
    *   `secondary_emotion`: 更細化的情緒描述。
    *   `intensity`: 情緒強度，0到1之間。
*   **`story_metaphor`**: (必填) 使用 `CLAUDE.md` 中定義的「Scene Code 分鏡表」進行情景化敘事。
    *   `story_series`: 故事/IP名稱。
    *   `scene_description`: 對應場景的文字描述。
    *   `scene_code`: 標準化的場景代碼。
*   **`key_learnings_or_insights`**: (必填，若有) 本次行動中獲得的關鍵學習、洞察或反思。這是團隊知識積累的重要部分。
*   **`challenges_faced`**: (選填，若有) 描述遇到的困難、嘗試的解決方案以及是否解決。
*   **`collaborators_involved`**: (選填，若有) 列出參與協作的其他 AI 人格或團隊成員及其貢獻。
*   **`code_references`**: (選填) 相關的代碼位置或版本信息，方便追溯。
*   **`next_steps_or_hooks`**: (必填，若有) 指明下一步計劃或需要其他團隊成員注意/跟進的事項。
*   **`custom_tags`**: (選填) 自定義標籤，用於更好地分類和檢索日記條目。

## 使用指南

*   **及時記錄**: 盡可能在任務完成或遇到關鍵節點後立即記錄，以保證信息的準確性和完整性。
*   **坦誠反思**: 特別是 💧水 和 🌌無極，鼓勵記錄真實的挑戰和反思，不怕暴露問題，這是改進的開始。
*   **保持一致**: 盡量使用模板中定義的字段和數據類型。
*   **善用 Scene Code**: 讓記錄更生動，也便於團隊成員快速理解情境。
*   **定期回顧**: 🌌無極 和團隊其他成員可以定期回顧這些日記，總結經驗，優化流程。

**此模板是我們集體記憶和持續進化的基礎。請認真對待每一次記錄。**
```
