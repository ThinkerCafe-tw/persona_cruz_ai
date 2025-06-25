# 建議的開發指令

## 系統資訊
- `uname -a` - 查看系統資訊 (Darwin/macOS)
- `pwd` - 查看當前工作目錄
- `ls -la` - 列出目錄內容（包含隱藏檔案）

## Git 操作（重要！）
- `git status` - 檢查當前狀態（永遠先執行這個）
- `git log --oneline -20` - 查看最近 20 個提交
- `git diff` - 查看未提交的更改
- `git add .` - 加入所有更改
- `git commit -m "message"` - 提交更改
- `git push origin main` - 推送到 GitHub（自動觸發 Railway 部署）

**⚠️ 警告**：
- 絕對不要執行 `git init`（專案已初始化）
- 不需要 `git remote add`（已設定）

## Python 環境
- `python --version` - 查看 Python 版本
- `pip install -r requirements.txt` - 安裝相依套件
- `python app.py` - 本地執行 Flask 應用

## 測試指令
- `python startup_test.py` - 執行啟動測試
- `python -m pytest tests/` - 執行所有測試（如果有 pytest）
- `python tests/test_integration.py` - 執行整合測試

## 搜尋指令（開發前必做！）
- `grep -r "keyword" .` - 搜尋關鍵字
- `grep -r "class\|def" *.py` - 搜尋所有類別和函數定義
- `find . -name "*.py" -type f` - 找出所有 Python 檔案
- `rg "pattern"` - 使用 ripgrep 快速搜尋（推薦）

## 資料庫相關
- `python check_pgvector.py` - 檢查 pgvector 設定
- `python migrate_to_pgvector.py` - 執行資料庫遷移

## 量子記憶測試
- `python test_quantum_memory.py` - 測試量子記憶系統
- `python test_pgvector_integration.py` - 測試 pgvector 整合

## macOS 特定指令
- `open .` - 在 Finder 開啟當前目錄
- `pbcopy < file` - 複製檔案內容到剪貼簿
- `pbpaste > file` - 從剪貼簿貼上到檔案

## 環境變數
- `echo $RAILWAY_ENVIRONMENT` - 檢查是否在 Railway 環境
- `printenv | grep -E "(LINE|GEMINI|DATABASE)"` - 查看相關環境變數

## 程式碼品質檢查
目前專案沒有設定 linter 或 formatter，但建議的指令：
- `black *.py` - 格式化 Python 程式碼（如果安裝）
- `flake8 *.py` - 檢查程式碼風格（如果安裝）
- `mypy *.py` - 型別檢查（如果安裝）

## 重要提醒
1. **永遠先搜尋再實作**（避免空檔案陷阱）
2. **理解現有架構再改動**（避免重寫陷阱）
3. **每次改動後執行測試**（確保沒有破壞功能）