```markdown
# 🎯🌌 Phase 1: 核心人格與記憶引擎 (奠定 MVP 基礎)

**主導人格**: 🎯 CRUZ (推進), 🌱 木 (產品規劃)
**核心執行**: 🔥 火 (開發), 🏔️ 土 (架構支持)
**質量保障**: 💧 水 (測試)

## 1. 階段目標

為 AI 助手建立核心智能，使其具備「個性化」的基礎，並為後續所有高級功能的實現奠定技術基石。此階段的成功交付是整個「個性化 AI 助手計畫」MVP (Minimum Viable Product) 的前提。

**核心產出**：一個功能初步可用、能夠存儲和檢索用戶相關記憶的「高級記憶模組 V1」。

## 2. 核心任務分解

此階段的核心任務是實現 `../c02_personality_memory_wood_fire/f02_advanced_memory_module_design_v1.md` 中提出的「高級記憶模組」的核心功能。

**2.1. 擴展 Python RAG API (🔥火 🏔️土)**

*   **創建 `memory_manager` 模組**: 在現有的 Python RAG API (FastAPI) 項目中，創建一個新的服務模組 (e.g., `memory_manager.py` 或一個獨立的 `memory_module` Python 包)。
*   **定義記憶存儲接口**:
    *   `POST /memory/add`: 用於接收來自 Node.js 主後端的記憶條目數據（包含待記憶內容、`user_id`, `agent_id` (可選), `memory_type` (可選), `importance_score` (可選) 等）。
    *   接口內部邏輯：
        1.  接收數據並進行校驗。
        2.  (可選 V1) 調用 LLM 進行初步的 `memory_type` 分類和 `importance_score` 評估。
        3.  對記憶內容 (`content`) 生成向量嵌入 (utilizing existing embedding models in LibreChat)。
        4.  將包含所有元數據（包括 `user_id`, `agent_id`, `timestamp_created`, `memory_type`, `importance_score`, `content`, `embedding`）的記憶條目存入 PostgreSQL (`pgvector`)。
*   **定義記憶檢索接口**:
    *   `POST /memory/retrieve`: 用於接收來自 Node.js 主後端的記憶檢索請求（包含 `user_id`, `agent_id` (可選), 查詢文本, `top_k` 等）。
    *   接口內部邏輯：
        1.  接收查詢參數並校驗。
        2.  對查詢文本生成查詢向量。
        3.  在 `pgvector` 中執行向量相似性搜索，**必須基於 `user_id` (以及可選的 `agent_id`) 進行過濾**，確保只檢索相關用戶/人格的記憶。
        4.  (V1 階段) 可按相似度 + `timestamp_created` (降序) 或 `importance_score` (降序) 進行初步排序。
        5.  返回檢索到的 `top_k` 條記憶內容（主要是 `content` 和必要的元數據如 `memory_type`）。

**2.2. 修改 PostgreSQL (`pgvector`) Schema (🏔️土 🔥火)**

*   根據 `../c02_personality_memory_wood_fire/f02_advanced_memory_module_design_v1.md` 中 3.2 節的定義，創建或修改 `pgvector` 中的表結構，確保包含所有必要的元數據字段：
    *   `memory_id`, `user_id`, `agent_id`, `timestamp_created`, `timestamp_last_accessed`, `memory_type`, `content`, `embedding`, `importance_score`, `access_count`, `source_conversation_id`, `custom_tags`。
*   為 `user_id`, `agent_id`, `timestamp_created`, `memory_type`, `importance_score` 等字段建立合適的索引，以優化查詢性能。
*   為 `embedding` 字段創建向量索引 (例如 HNSW 或 IVFFlat)。

**2.3. 實現記憶注入鉤子 (Node.js 主後端) (🔥火)**

*   **用戶指令 `/remember`**:
    *   在 Node.js 後端解析用戶輸入，識別 `/remember <text_to_remember>` 指令。
    *   提取 `text_to_remember` 和當前 `user_id` (以及 `agent_id` 如果適用)。
    *   調用 Python RAG API 的 `/memory/add` 接口存儲記憶。
*   **對話結束自動摘要 (初步)**:
    *   **目標**：在對話結束時，自動提取關鍵信息作為記憶。
    *   **V1 簡化方案**：可以先不調用 LLM 進行摘要（以控制成本和複雜度）。初期可以考慮將最近幾輪的對話內容（或用戶的最後幾條消息）直接作為 `CONVERSATION_SUMMARY` 或 `RAW_HISTORY` 類型的記憶存儲。
    *   **觸發機制**：研究如何在 Node.js 後端識別「對話結束」的時機（可能基於超時、特定用戶操作等）。
    *   調用 Python RAG API 的 `/memory/add` 接口。
    *   🌱木 需要明確 V1 階段自動摘要的具體需求和可接受的簡化程度。

**2.4. 實現記憶檢索與提示增強 (Node.js 主後端) (🔥火)**

*   在 Node.js 後端，處理用戶請求發送給 LLM 之前：
    1.  獲取當前 `user_id` (以及 `agent_id` 如果適用) 和用戶的最新輸入。
    2.  調用 Python RAG API 的 `/memory/retrieve` 接口，獲取相關記憶列表。
    3.  將檢索到的記憶格式化為文本。
    4.  將格式化後的記憶文本注入到最終發送給 LLM 的提示中（通常是 System Prompt 的一部分）。

## 3. 驗收標準 (💧 水 🌱 木)**

*   可以通過 `/remember` 指令成功存儲用戶指定的記憶，並能在後續對話中被 AI 助手回憶或利用。
*   （如果實現了自動摘要）對話結束後，相關信息能被存儲，並在後續對話中影響 AI 的回應。
*   記憶的存儲和檢索嚴格按照 `user_id` 隔離，用戶 A 的記憶不應洩漏給用戶 B。
*   記憶檢索和注入過程對用戶感知的響應時間影響在可接受範圍內 (🌱木 需定義指標，⚔️金 協助監控)。
*   基礎的記憶元數據 (如 `user_id`, `content`, `timestamp_created`) 被正確記錄。

## 4. 風險與應對 (🎯 CRUZ 監控)

*   **Python RAG API 擴展複雜度**：FastAPI 和 LangChain 的結合可能帶來一定的學習曲線。🔥火 可能需要時間熟悉。
    *   **應對**: 先從最小可行功能開始，逐步迭代。
*   **數據庫 Schema 設計**：`pgvector` 的表設計和索引優化對性能至關重要。🏔️土 需早期介入並提供指導。
*   **Node.js 與 Python 服務間通信**：確保接口定義清晰、通信穩定可靠。
*   **性能瓶頸**：記憶檢索和 LLM 摘要（如果 V1 引入）可能成為性能瓶頸。
    *   **應對**: V1 階段摘要功能可簡化，檢索邏輯保持簡單。⚔️金 進行性能測試。

## 5. 五行人格協作要點

*   🌱 **木**：清晰定義 V1 記憶模組的範圍、核心場景和用戶價值。平衡功能完整性與 MVP 的快速交付。
*   🔥 **火**：主力負責 Node.js 和 Python 部分的編碼實現。遇到技術難點時及時求助。
*   🏔️ **土**：提供資料庫設計、服務間通信方案的架構指導，確保系統的穩定性和可擴展性。
*   💧 **水**：從用戶角度設計測試案例，驗證記憶的存儲、檢索、隔離性和對 AI 行為的實際影響。記錄遇到的問題和解決方案。
*   🎯 **CRUZ**：確保此核心階段按計劃推進，協調資源，移除障礙。

**此階段是整個專案的基石，其質量直接影響後續所有個性化功能的成敗。**
```
