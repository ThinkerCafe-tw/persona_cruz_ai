#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
時光儀 (Chronoscope) v4.0 - Python 重生版

由「火」接手，放棄了在 bash 中不穩定的嘗試，
採用 Python 的穩健性與強大處理能力，打造最終形態的時間線檢視器。
"""

import subprocess
import re

# --- 顏色代碼 (由「火」重新定義以確保穩定) ---
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'

def get_persona_emoji(author_name: str) -> str:
    """根據作者名稱返回對應的 emoji"""
    author_lower = author_name.lower()
    if "cruz" in author_lower or "thinkercafe" in author_lower:
        return "🎯"
    if "rhaenyra" in author_lower:
        return "🏔️"
    if "leo" in author_lower:
        return "🔥"
    if "google-labs-jules[bot]" in author_lower:
        return "🤖"
    return "🌌" # 預設

def main():
    """主函數，執行並格式化 git log"""
    # 使用一個幾乎不可能出現在 commit message 中的分隔符
    sep = "<--GIT-LOG-SEPARATOR-->"
    
    # 獲取日誌，包含圖形、hash、作者、日期、ref names 和主題
    # %H for full hash to avoid ambiguity, %s for subject
    git_log_command = [
        'git', 'log', '--all', '--graph',
        f'--pretty=format:%H{sep}%an{sep}%cs{sep}%d{sep}%s'
    ]

    try:
        log_output = subprocess.check_output(git_log_command).decode('utf-8')
    except subprocess.CalledProcessError:
        print(f"{Colors.YELLOW}Error: Could not execute 'git log'. Is this a git repository?{Colors.RESET}")
        return
        
    for line in log_output.splitlines():
        # 分割圖形部分和日誌內容
        graph_part_match = re.match(r'^[\s\*\-\/\\\|_.]+', line)
        if graph_part_match:
            graph_part = graph_part_match.group(0)
            log_content = line[len(graph_part):]
        else:
            graph_part = ""
            log_content = line

        parts = log_content.split(sep)
        
        if len(parts) == 5:
            full_hash, author, date, refs, subject = parts
            
            emoji = get_persona_emoji(author)
            
            # 清理 subject 和 refs
            subject_cleaned = subject.strip()
            refs_cleaned = refs.strip()
            
            # 組裝第一行
            line1 = f"{Colors.BOLD}{subject_cleaned}{Colors.RESET} {Colors.YELLOW}{refs_cleaned}{Colors.RESET}"
            
            # 組裝第二行
            line2 = (f"   {Colors.DIM}└─{Colors.RESET} "
                     f"{Colors.BLUE}{full_hash[:7]}{Colors.RESET} by "
                     f"{Colors.GREEN}{author}{Colors.RESET} on "
                     f"{Colors.YELLOW}{date}{Colors.RESET}")

            # 打印帶圖形的完整卡片
            print(f"{Colors.CYAN}{graph_part}{Colors.RESET}{emoji} {line1}")
            print(line2)

    print(f"\n{Colors.BOLD}---  نهايه時間線  ---{Colors.RESET}")

if __name__ == "__main__":
    main() 