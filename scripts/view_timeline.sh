#!/bin/bash
#
# 時光儀 (Chronoscope) - v2 "Cute" Edition
#
# 由無極重新設計，將 Git 歷史轉化為更可愛、更易讀的時間線。

# --- 顏色代碼 ---
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
MAGENTA='\033[1;35m'
NC='\033[0m' # No Color

# --- 核心邏輯 ---

# 定義一個 mapping，將 git 作者名稱映射到 AI 人格 emoji
get_persona_emoji() {
    # 轉換為小寫以方便比對
    local name=$(echo "$1" | tr '[:upper:]' '[:lower:]')
    case "$name" in
        "cruz" | "cruz tang" | "thinkercafe")
            echo "🎯"
            ;;
        "rhaenyra")
            echo "🏔️"
            ;;
        "leo")
            echo "🔥"
            ;;
        *)
            # 預設 emoji
            echo "🌌"
            ;;
    esac
}

# 使用 git log 搭配 --pretty=format 來客製化輸出
# 我們需要逐行讀取 git log，以便為每一行加上 emoji
# 🕰️ emoji 作為一個可靠的錨點，幫助我們定位作者
while IFS= read -r line; do
    # 從每行中提取作者名 (在 'by' 和 '🕰️' 之間)
    author=$(echo "$line" | sed -n 's/.*by \(.*\) 🕰️.*/\1/p')
    
    if [ -n "$author" ]; then
        emoji=$(get_persona_emoji "$author")
        
        # 安全地取代 'by 作者名' 為 'by emoji 作者名'
        # 使用 sed 的替換功能，並用 & 來代表找到的完整作者名
        new_line=$(echo "$line" | sed "s/by $author/by $emoji $author/")
        echo -e "$new_line"
    else
        # 如果行內沒有 "by 作者名 🕰️" 的結構，代表是純圖形行，直接印出
        echo -e "$line"
    fi

done < <(git log --graph --pretty=format:"%C(cyan)💫 %s %C(reset)%C(bold blue)(%h)%C(reset) %C(green)by %an 🕰️  %ar%C(reset) %C(yellow)%d%C(reset)" --all)

echo ""
echo -e "${MAGENTA}---  🕰️  Timeline End  🕰️  ---${NC}" 