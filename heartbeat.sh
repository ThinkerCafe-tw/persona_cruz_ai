#!/bin/bash

# ==============================================================================
#  Cruz AI - Heartbeat Script (TDD Refactored + Dashboard)
# ==============================================================================
#
#  功能：
#  - 每隔 5 分鐘，呼叫 Gemini CLI 進行一次自我反思。
#  - 將建議透過 Telegram Bot 發送給指定使用者。
#  - 將所有成功和失敗的事件記錄到本地日誌。
#  - 將成功的建議更新到 growth_dashboard.html。
#
# ==============================================================================

# --- 設定區 ---
TELEGRAM_BOT_TOKEN="8018192110:AAGwE_hSBBegOP0Wwt_JPtGPhyniGr44Gzc"
TELEGRAM_CHAT_ID="-1002384968188"
GEMINI_CLI="gemini"
LOG_FILE="heartbeat.log"
DASHBOARD_FILE="growth_dashboard.html"
API_TIMEOUT=60

# --- 函式定義區 ---

write_log() {
  local message="$1"
  local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  echo "[$timestamp] $message" >> "$LOG_FILE"
}

get_suggestion() {
  local prompt="你現在是 Cruz AI 的核心系統，你正在執行一個自動化的心跳腳本。請根據 system_intelligence/chronicle_records/ 中的現有文檔，以及你對 Serena 和 LibreChat 的理解，用簡潔的條列式中文，提出 1-3 個『最重要』且『可立即執行』的下一步優化建議。你的回答將被直接發送到 Telegram，所以請直接給出建議，不要有額外的開場白或結語。"
  local output
  output=$(gtimeout "${API_TIMEOUT}s" "$GEMINI_CLI" -p "$prompt" 2>&1)
  local exit_code=$?

  if [ $exit_code -ne 0 ]; then
    write_log "錯誤：Gemini API 呼叫失敗或超時 (Exit Code: $exit_code)。輸出：$output"
    echo ""
  else
    echo "$output"
  fi
}

send_telegram_message() {
  local message_body="$1"
  local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  local message="*Cruz AI 心跳報告* ($timestamp)%0A%0A*下一步優化建議：*%0A%0A$message_body"
  local message_encoded
  message_encoded=$(echo "$message" | sed 's/ /%20/g; s/&/%26/g; s/\*/%2a/g; s/_/%5f/g; s/\[/%5b/g; s/\]/%5d/g; s/(/%28/g; s/)/%29/g; s/~/%7e/g; s/`/%60/g; s/>/%3e/g; s/#/%23/g; s/+/%2b/g; s/-/%2d/g; s/=/%3d/g; s/|/%7c/g; s/{/%7b/g; s/}/%7d/g; s/!/%21/g; s/:/%3a/g; s/,/%2c/g; s/?/%3f/g; s/@/%40/g;')
  local telegram_url="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage"
  local response
  response=$(curl -s -X POST "$telegram_url" -d chat_id="$TELEGRAM_CHAT_ID" -d text="$message_encoded" -d parse_mode="Markdown")
  
  if [[ ! "$response" =~ \"ok\":true ]]; then
    write_log "錯誤：發送 Telegram 訊息失敗。回應：$response"
  fi
}

update_dashboard() {
    local suggestion_text="$1"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # 將純文字的換行符轉換為 HTML 的 <br>
    # 並處理 Markdown 的 `-` 條列式為 `<ul><li>`
    local html_content
    html_content=$(echo "$suggestion_text" | sed 's/^- /<li>/g' | sed '$a</li>' | sed '1s/^/<ul>/' | sed '$a</ul>' | sed 's/$/<br>/' | tr -d '\n')
    
    # 創建新的卡片 HTML
    local new_card="<div class='card'><div class='card-header'><span>$timestamp</span></div><div class='card-content'>$html_content</div></div>"

    # 使用 sed 在 #insertion-point 標記後插入新卡片
    # 使用 | 作為 sed 的分隔符，避免路徑中的 / 造成問題
    sed -i '' "s|<div id=\"insertion-point\"></div>|<div id=\"insertion-point\"></div>\n            $new_card|" "$DASHBOARD_FILE"
}


# --- 主函式 ---
main() {
  if [ "$TELEGRAM_BOT_TOKEN" == "YOUR_TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_CHAT_ID" == "YOUR_TELEGRAM_CHAT_ID" ]; then
    echo "錯誤：請先在 heartbeat.sh 腳本中填寫您的 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID。"
    exit 1
  fi

  write_log "心跳服務（含儀表板更新）啟動。"

  while true; do
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] 心跳觸發：開始生成優化建議..."
    
    local suggestion
    suggestion=$(get_suggestion)

    if [ -n "$suggestion" ]; then
      write_log "建議已生成：\n$suggestion"
      send_telegram_message "$suggestion"
      update_dashboard "$suggestion"
    else
      : 
    fi
    
    local sleep_timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$sleep_timestamp] 報告完畢，系統進入 5 分鐘休眠..."
    sleep 300
  done
}

# --- 腳本執行入口 ---
main