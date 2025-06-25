# 專案總覽

## 專案名稱
Persona Cruz AI - LINE Bot with Gemini

## 專案目的
這是一個整合了 Google Gemini AI 的 LINE 聊天機器人，具有多重人格系統（無極 AI Agents OS）和量子記憶功能。部署在 Railway 雲端平台，提供 24/7 的智能對話服務。

## 主要功能
1. **AI 對話系統**
   - 使用 Google Gemini AI 進行智能對話
   - 支援 Function Calling
   - 每個用戶獨立的對話記憶

2. **無極 AI Agents OS**
   - 🌌 無極：系統觀察者
   - 🎯 CRUZ：直接果斷的數位分身
   - 🌸 Serena：溫柔貼心的 AI 助理
   - 🌱 木：產品經理（創意成長）
   - 🔥 火：開發專員（熱情實踐）
   - 🏔️ 土：架構師（穩固基礎）
   - ⚔️ 金：優化專員（精益求精）
   - 💧 水：測試專員（品質守護）

3. **量子記憶系統**
   - 使用 pgvector 資料庫儲存向量化記憶
   - 支援記憶演化和強化學習
   - 記憶泡泡和水晶態儲存機制

4. **Google Calendar 整合**
   - 自然語言操作行程
   - 建立、查詢、更新、刪除行程

5. **娛樂功能**
   - 內建 50 個冷笑話

## 技術架構
- **後端框架**: Flask (Python)
- **LINE Bot SDK**: line-bot-sdk 3.5.0
- **AI 服務**: Google Gemini AI (google-generativeai 0.3.2)
- **資料庫**: PostgreSQL with pgvector extension
- **部署平台**: Railway
- **版本控制**: Git (GitHub)

## 部署資訊
- **GitHub**: git@github.com:ThinkerCafe-tw/persona_cruz_ai.git
- **部署方式**: 推送到 main 分支自動觸發 Railway 部署
- **環境變數**: 全部在 Railway Dashboard 管理