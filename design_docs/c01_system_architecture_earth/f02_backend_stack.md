```markdown
# 🏔️ 02. 後端技術棧：混合語言微服務架構詳解

**主導人格**: 🏔️ 土 (架構師)
**協作人格**: 🔥 火 (開發專員), ⚔️ 金 (優化專員)

本文件深入探討 LibreChat 後端所採用的混合語言（Polyglot）微服務系統，旨在為不同任務選擇最優技術棧，實現效能與開發效率的平衡。

## 1. 主應用後端 (Node.js / Express.js)

*   **技術選型**：
    *   **語言/框架**：Node.js，基於靈活且無固定範式的 Express.js 框架。
        *   判斷依據：`package.json` 結構、標準 npm 腳本 (如 `npm run backend`)、缺乏 NestJS 的標誌性特徵 (如 Decorators 和 Modules)。
    *   **核心庫**：`passport` (用戶認證), `jsonwebtoken` (JWT處理)。
*   **核心職責**：作為整個系統的中樞，負責：
    *   用戶註冊、登入、身份驗證。
    *   會話管理。
    *   API 路由：將請求路由到不同的 AI 模型端點或內部服務。
    *   伺服前端 React 應用。
*   **🏔️土的架構考量**：
    *   **優勢**：Node.js 擅長處理高併發的 I/O 密集型任務，適合做 API 網關和請求轉發。Express.js 的靈活性高，易於快速開發。
    *   **挑戰與應對**：
        *   **回調地獄/異步管理**：雖然現代 JavaScript (Async/Await) 已大幅改善，但複雜的異步流程仍需謹慎處理，避免邏輯混亂。🔥火 應注意代碼可讀性。
        *   **錯誤處理**：需要建立統一且健壯的錯誤處理機制。⚔️金 應協助制定規範。
        *   **性能監控**：對於核心 API 接口，需進行性能監控和優化。
    *   **與「個性化AI助手」的關聯**：
        *   用戶身份和會話管理是實現個性化的基礎。
        *   記憶注入鉤子（見 `../c02_personality_memory_wood_fire/f02_advanced_memory_module_design_v1.md`）將在此服務中實現，攔截用戶請求和 AI 回應。
        *   Token 成本統計也可能需要在此層面進行請求攔截和記錄。

## 2. RAG API 微服務 (Python / FastAPI)

*   **技術選型**：
    *   **語言/框架**：Python，基於高效能的 FastAPI 框架。
    *   **核心庫**：`langchain` (與LLM交互、RAG流程編排), `pgvector` (與PostgreSQL向量數據庫交互)。
*   **核心職責**：專門處理計算密集型的檢索增強生成 (RAG) 任務：
    *   文件解析、文本切塊。
    *   向量嵌入生成 (Embedding Generation)。
    *   對向量資料庫的語義搜索查詢。
*   **設計特點**：
    *   **異步處理**：FastAPI 的核心優勢，確保 AI 相關的繁重工作不會阻塞主應用。
    *   **可擴展性**：作為獨立微服務，可以根據負載情況獨立擴展。
*   **🏔️土的架構考量**：
    *   **優勢**：Python 在機器學習和數據處理方面擁有無可比擬的生態系統（如 LangChain, Hugging Face Transformers 等）。FastAPI 性能優越，開發效率高。
    *   **挑戰與應對**：
        *   **服務間通信**：主應用 (Node.js) 與 RAG API (Python) 之間的通信方式（通常是 HTTP/REST）需要高效且可靠。注意超時、重試和錯誤傳遞機制。
        *   **環境隔離**：Python 環境依賴管理（如 venv, conda, poetry）需規範化，避免與系統或其他 Python 項目衝突。🔥火 需注意。
    *   **與「個性化AI助手」的關聯**：
        *   **「高級記憶模組」的核心宿主**：我們計劃在此 Python RAG API 基礎上擴展，構建新的「記憶管理模組」，負責記憶的儲存、檢索、更新和遺忘邏輯。這是專案的技術基石。
        *   LangChain 的整合為未來引入更複雜的記憶檢索策略或與 LLM 的高級交互提供了便利。

## 3. 雙資料庫模型：職責分明

平台預設採用雙資料庫架構，以實現不同數據類型的最優管理：

*   **MongoDB (主應用核心資料庫)**：
    *   **用途**：儲存非結構化或半結構化的應用數據，如用戶資料、對話紀錄、自訂預設 (Presets)、代理人 (Agents) 配置等。
    *   **🏔️土的考量**：
        *   **優勢**：Schema 靈活，適合快速迭代的應用數據。對於聊天記錄這類文檔型數據非常合適。
        *   **挑戰**：複雜查詢和事務支持相對較弱（相比關係型數據庫）。需根據實際查詢需求設計合理的索引。⚔️金 協助優化。

*   **PostgreSQL + pgvector (RAG API 向量資料庫)**：
    *   **用途**：專門作為 RAG API 的向量資料庫，利用 `pgvector` 擴充套件來高效地儲存和查詢向量數據。
    *   **🏔️土的考量**：
        *   **優勢**：pgvector 提供了在成熟的 PostgreSQL 數據庫中進行向量相似性搜索的能力。可以利用 PostgreSQL 本身的穩定性、備份恢復機制和豐富的 SQL 功能。文檔提供了關於如何為 pgvector 建立索引 (如 HNSW, IVFFlat) 以優化查詢效能的詳細指南。
        *   **挑戰**：向量數據庫的性能調優（索引選擇、參數設置）需要專業知識。數據同步（如果需要與 MongoDB 中的數據關聯）需要仔細設計。
        *   **替代方案**：報告中提及，由於 RAG API 基於 LangChain，理論上可支援其他向量資料庫（如 MongoDB Atlas Vector Search, Meilisearch），但 pgvector 是預設且文檔最完善的選擇。除非有極強理由，否則初期建議堅持使用 pgvector 以降低複雜性。

## 4. 混合架構的策略性權衡

開發團隊選擇這種混合語言、雙資料庫的微服務架構，是一個**策略性的權衡**：

*   **以增加運維複雜度為代價，換取在各個專業領域的最佳效能和開發體驗。**
*   使得 AI 團隊 (Python) 和核心應用團隊 (Node.js) 可以相對獨立地開發和部署。

對於我們的「個性化 AI 助手計畫」：

*   我們**繼承這一架構**，並在其基礎上進行擴展。
*   運維團隊（或負責運維的 AI 代理）必須具備管理這四種核心技術棧的能力。
*   在 Docker 環境下，服務間的網絡配置、環境變數傳遞是初期部署調試的重點。🔥火 和 🏔️土 需密切配合。

**下一步**: 分析多模型路由與管理機制 (`f03_multi_model_ai_gateway_strategy.md`)。
```
