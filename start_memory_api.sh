#!/bin/bash
# 啟動 Memory API 服務

echo "🚀 Starting Memory API for Day 5 Integration..."

# 檢查 PostgreSQL 是否運行
if ! pg_isready -q; then
    echo "⚠️  PostgreSQL is not running. Please start it first."
    echo "   On macOS: brew services start postgresql@14"
    exit 1
fi

# 設置環境變數
export DATABASE_URL="postgresql://postgres:postgres@localhost/persona_cruz_memory"
export JWT_SECRET="your-secret-key-change-in-production"
export GEMINI_API_KEY="${GEMINI_API_KEY}"

# 切換到 API 目錄
cd memory_api

# 安裝依賴（如果需要）
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# 啟動虛擬環境
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

echo "🏃 Starting Memory API on http://localhost:8000..."
echo "📊 API docs available at http://localhost:8000/docs"

# 啟動 API
uvicorn main_v3:app --reload --host 0.0.0.0 --port 8000