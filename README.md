```markdown
# 個性化 AI 助手計畫

歡迎來到「個性化 AI 助手計畫」的官方指導中心！

## 🎯 專案目標

本專案旨在基於開源專案 [LibreChat](https://librechat.ai/) 進行 Fork 和深度客製化，最終打造一個具備以下核心特性的「個性化 AI 助手」：

*   **深度個性化**：能夠理解並適應不同用戶的需求、偏好和溝通風格。
*   **高級長期記憶**：擁有跨對話、與用戶和特定 AI 人格綁定的持久化記憶能力。
*   **無縫嵌入整合**：可以方便地作為 Widget 或組件嵌入到現有的網站或業務平台中。
*   **可信賴與可控**：用戶對其 AI 助手的行為和記憶有清晰的認知與管理能力。
*   **強大的語音交互**：支持流暢自然的語音輸入與輸出。
*   **成本可追蹤**：能夠監控和管理 AI 服務的調用成本。

## 🌌 CLAUDE.md - 我們的協作宇宙核心

本專案的所有參與者（無論是 AI 代理還是人類成員）的核心行動準則、團隊文化、人格分工、溝通協議（如 AI 日記、Scene Code）以及共同的價值觀與記憶傳承機制，均詳細定義在根目錄下的 **[CLAUDE.md](./CLAUDE.md)** 文件中。

**在開始任何工作之前，請務必首先深入理解 [CLAUDE.md](./CLAUDE.md) 的內容。**

## 📖 AGENTS.md - AI 代理協作指南

為了更好地指導 AI 代理（如 Jules）在本專案中的工作，我們編寫了 **[AGENTS.md](./AGENTS.md)** 文件。它詳細說明了 AI 代理應如何利用本倉庫中的「記憶檔」（`design_docs/`）以及遵循 `CLAUDE.md` 的原則進行高效協作。

## 🧬 設計文檔 (記憶檔) - `design_docs/`

專案的詳細規劃、技術評估、架構設計、功能藍圖、以及根據 `CLAUDE.md` 精神制定的協作細則，均沉澱在 **`design_docs/`** 目錄中。這些文檔是我們集體智慧的結晶，也是指導後續開發的核心「基因」。

**重要提示：** 由於工具對包含非 ASCII 字符路徑的處理限制，`design_docs/` 目錄下的子目錄和文件名目前暫時使用純 ASCII 命名。在您將此倉庫克隆到本地後，請根據以下映射關係將其重命名為目標中文名稱，以獲得最佳的閱讀和協作體驗。

**目錄與文件重命名映射表：**

請在克隆倉庫後，手動執行以下重命名操作，以恢復設計文檔的預期中文路徑結構：

**目錄重命名：**
*   `mv design_docs/c00_project_origin_and_vision design_docs/00_太極本源與專案願景`
*   `mv design_docs/c01_system_architecture_earth design_docs/01_系統架構藍圖_土`
*   `mv design_docs/c02_personality_memory_wood_fire design_docs/02_人格建構與高級記憶引擎_木_火`
*   `mv design_docs/c03_ui_ux_integration_wood_fire design_docs/03_UI_UX與嵌入式整合_木_火`
*   `mv design_docs/c04_voice_interaction_fire_metal design_docs/04_語音互動整合_火_金`
*   `mv design_docs/c05_deployment_ops_cost_earth_metal design_docs/05_部署_運維與成本考量_土_金`
*   `mv design_docs/c06_customization_roadmap_cruz_wuji design_docs/06_客製化開發路線圖_CRUZ_無極`
*   `mv design_docs/c07_ai_diary_lessons_water_wuji design_docs/07_AI協作日記與教訓集_水_無極`

**文件重命名 (在對應的中文目錄下執行)：**

*   `cd design_docs/00_太極本源與專案願景/`
    *   `mv f00_vision_and_fork_rationale.md 00_project_vision_and_librechat_fork_rationale.md`
    *   `mv f01_five_elements_roles.md 01_five_elements_and_roles_in_project.md`
*   `cd ../01_系統架構藍圖_土/`
    *   `mv f01_overall_architecture.md 01_overall_architecture_overview.md`
    *   `mv f02_backend_stack.md 02_backend_stack.md`
    *   `mv f03_multi_model_ai_gateway_strategy.md 03_multi_model_routing.md`
    *   `mv f04_tool_extension_and_agent_framework.md 04_plugin_and_agent_strategy.md`
*   `cd ../02_人格建構與高級記憶引擎_木_火/`
    *   `mv f01_personality_construction.md 01_personality_construction.md`
    *   `mv f02_advanced_memory_module_design_v1.md 02_advanced_memory_module_design.md`
*   `cd ../03_UI_UX與嵌入式整合_木_火/`
    *   `mv f01_ui_stack_and_branding.md 01_ui_stack_and_branding.md`
    *   `mv f02_user_auth_and_roles.md 02_user_auth_and_roles.md`
    *   `mv f03_embeddable_widget_design_v1.md 03_embeddable_widget_design.md`
*   `cd ../04_語音互動整合_火_金/`
    *   `mv f01_stt_tts_integration_strategy.md 01_stt_tts_integration.md`
*   `cd ../05_部署_運維與成本考量_土_金/`
    *   `mv f01_deployment_strategy_and_cicd.md 01_deployment_architecture.md`
    *   `mv f02_fork_customization_effort.md 02_development_workflow_and_cost_estimation.md`
*   `cd ../06_客製化開發路線圖_CRUZ_無極/`
    *   `mv phase_1_core_memory_engine.md phase_1_core_personality_memory.md`
    *   `mv phase_2_embeddable_widget_branding.md phase_2_embeddable_widget_branding.md`
    *   `mv phase_3_token_economics_cost_tracking.md phase_3_token_economics_cost_tracking.md`
    *   `mv phase_4_contextual_workspace_ui_ux.md phase_4_contextual_workspace_ui_ux.md`
*   `cd ../07_AI協作日記與教訓集_水_無極/daily_dev_logs/`
    *   (此目錄下的 `template_ai_diary_entry.md` 文件名已是預期格式，無需更改)
*   `cd ../` (返回到 `07_AI協作日記與教訓集_水_無極/`)
    *   `mv lessons_learned_and_best_practices.md lessons_learned_and_best_practices.md` (文件名已是預期格式，無需更改)

(請注意，上述 `mv` 指令是 Unix/Linux 環境下的命令，Windows 環境下請使用 `ren` 或文件管理器操作。)

**建議查閱順序：**

1.  **[CLAUDE.md](./CLAUDE.md)**: 理解團隊協作的元框架。
2.  **[AGENTS.md](./AGENTS.md)**: 了解 AI 代理的工作方式。
3.  **`design_docs/c00_project_origin_and_vision/f00_vision_and_fork_rationale.md`**: 了解專案的總體願景和為何選擇 LibreChat。
4.  根據您的角色和當前任務，查閱 `design_docs/` 下的其他相關詳細設計文檔。

## 📜 LibreChat 原始評估報告

我們對 LibreChat 進行的「深度技術與產品評估報告」原文已存檔於 **[librechat_assessment_report.md](./librechat_assessment_report.md)**，供隨時參考。

## 🚀 快速開始 (開發者)

1.  **Fork & Clone**: Fork 本倉庫，然後克隆到您的本地環境。
2.  **遵循 `CLAUDE.md` 和 `AGENTS.md`**。
3.  **重命名 `design_docs/` 下的目錄和文件** (根據後續提供的映射表)。
4.  **環境配置**: (詳細步驟待補充，初期可參考 LibreChat 官方文檔及 `design_docs/c05_deployment_ops_cost_earth_metal/` 中的部署文檔)。
5.  **開始您的冒險！** 🔥💧🏔️⚔️🌱🎯🌸🌌

---

讓我們攜手，將「個性化 AI 助手計畫」從藍圖變為現實！
```
