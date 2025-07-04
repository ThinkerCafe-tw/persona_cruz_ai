```markdown
# 💧🌌 開發教訓、最佳實踐與記憶口訣

**主導人格**: 💧 水 (記錄/歸納), 🌌 無極 (反思/提煉)
**貢獻者**: 所有團隊人格

本文件旨在沉澱「個性化 AI 助手計畫」在開發過程中積累的寶貴經驗、遇到的典型問題、形成的有效解決方案以及提煉出的最佳實踐和記憶口訣。它是我們團隊集體智慧的結晶，是避免重複犯錯、提升開發效率和質量的關鍵。

本文檔將持續更新。所有 AI 代理和人類協作者在遇到有價值的教訓或總結出良好實踐時，都應提議將其補充到此處。💧水 負責初步整理，🌌無極 負責審核與提煉。

## 一、核心開發教訓 (Lessons Learned)

此部分記錄在專案中遇到的、對我們有深刻啟示的錯誤、挑戰及其反思。格式參考 `CLAUDE.md` 中的「開發教訓與記憶」部分。

---

### 🚨 教訓 L001 (日期: YYYY-MM-DD) - [事件簡述，例如：環境變量配置混淆導致部署失敗]

**人格Emoji與名稱**: (例如: 🔥火)

**事件描述**:
[詳細描述事件發生的背景、過程和直接後果。]

**錯誤分析**:
1.  [分析導致錯誤的直接原因1]
2.  [分析導致錯誤的深層原因2]
3.  [其他相關因素]

**教訓總結**:
*   ❌ **錯誤做法**: [總結當時的錯誤行為或思路]
*   ✅ **正確做法**: [闡述應該如何正確處理]
*   💡 **核心領悟**: [從事件中提煉出的核心啟示]

**相關人格的反思 (可選)**:
*   [相關人格對此事件的簡短反思，例如：🔥火：過於自信，未仔細檢查配置文件。]

**預防措施 - 開發前N問/檢查清單**:
1.  □ [針對此類問題的預防性檢查點1]
2.  □ [針對此類問題的預防性檢查點2]

**記憶口訣**: "[一句簡短、易記的口訣，用於警示未來]"

---

### 🚨 教訓 L002 (日期: YYYY-MM-DD) - [事件簡述]

... (以此類推) ...

---

## 二、最佳實踐 (Best Practices)

此部分記錄在專案中被證明行之有效的開發方法、工具使用技巧、協作模式等。

---

### BP001: API 設計 - 清晰、一致、可擴展

*   **實踐描述**: 在設計新的後端 API 接口 (尤其是 Node.js 與 Python RAG API 之間的接口) 時，應遵循 RESTful 原則，確保命名清晰、參數一致、響應格式規範。優先使用 OpenAPI (Swagger) 進行接口定義和文檔化。
*   **貢獻者**: 🏔️土, 🔥火
*   **適用場景**: 所有後端 API 設計與開發。
*   **益處**: 提高接口的可理解性、可維護性和團隊協作效率。減少集成錯誤。
*   **相關工具/原則**: RESTful, OpenAPI Specification, Postman (測試)。

---

### BP002: 前端狀態管理 - 集中與分層

*   **實踐描述**: 對於複雜的前端應用 (如「語境工作區」)，應採用成熟的狀態管理方案 (如 Recoil, Zustand, Redux Toolkit)。全局狀態集中管理，組件內部狀態盡量本地化。數據流應單向、可預測。
*   **貢獻者**: 🔥火, 🌸Serena
*   **適用場景**: React 前端開發，特別是涉及多組件共享狀態或複雜交互時。
*   **益處**: 提高應用的可維護性，簡化調試，避免不必要的 props drilling。
*   **相關工具/原則**: Recoil/Zustand/Redux, 單向數據流。

---

### BP003: Docker 環境配置 - 最小化與安全性

*   **實踐描述**: Dockerfile 應遵循最小權限原則，避免使用 root 用戶運行應用。多階段構建 (multi-stage builds) 用於減小最終鏡像體積。環境變量通過 `.env` 文件 (本地) 和安全的部署平台變量注入 (生產)，而非硬編碼。
*   **貢獻者**: 🏔️土, ⚔️金
*   **適用場景**: Docker 鏡像構建與容器化部署。
*   **益處**: 提升安全性，縮短部署時間，節省存儲資源。
*   **相關工具/原則**: Docker multi-stage builds, `.dockerignore`, 安全的環境變量管理。

---

... (持續補充更多最佳實踐) ...

## 三、記憶口訣集 (Mnemonic Maxims)

此部分彙總從教訓和實踐中提煉出的簡短、易記的口訣，作為團隊的行為提示。

*   "空檔案不代表沒程式，先搜尋再動手" (源自 `CLAUDE.md` - Line Bot Handler 重寫事件)
*   "測試是護欄，不是終點線" (源自 `CLAUDE.md` - TDD 完成後的過度自信)
*   "配置即代碼，版本化管理" (針對 `librechat.yaml` 等重要配置文件)
*   "先畫靶再射箭，需求不明不動手" (強調需求分析的重要性)
*   "日拱一卒無有盡，每日記錄莫等閒" (鼓勵 AI 日記的習慣)
*   "安全無小事，時刻記心間" (提醒關注開發中的安全問題)
*   "模塊要解耦，依賴需倒轉" (關於良好架構設計)

---

**本文檔是活的文檔，需要所有成員共同維護和豐富。每一次記錄的教訓都是團隊成長的階梯，每一條總結的實踐都是未來效率的保障。**
```
