#!/usr/bin/env python3
"""
CRUZ 語料匯入腳本
用於將 Threads 內容匯入到語料庫
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cruz_persona_system import CruzPersonaSystem
import argparse

def main():
    parser = argparse.ArgumentParser(description='匯入 CRUZ 語料到系統')
    parser.add_argument('file', help='要匯入的文字檔路徑')
    parser.add_argument('--show-stats', action='store_true', 
                       help='匯入後顯示統計資訊')
    
    args = parser.parse_args()
    
    # 初始化系統
    persona_system = CruzPersonaSystem()
    
    print(f"正在匯入檔案: {args.file}")
    print("=" * 50)
    
    # 執行匯入
    imported_count = persona_system.import_text_file(args.file)
    
    if imported_count > 0:
        print(f"\n✅ 成功匯入 {imported_count} 則語料")
        
        if args.show_stats:
            print("\n📊 語料庫統計:")
            stats = persona_system.get_statistics()
            print(f"- 總語料數: {stats['total_quotes']}")
            print(f"- 涵蓋主題: {', '.join(stats['topics'])}")
            
            if stats['most_used_quotes']:
                print("\n🔥 最常使用的語料:")
                for i, quote in enumerate(stats['most_used_quotes'][:3], 1):
                    print(f"{i}. {quote['content'][:50]}... (使用 {quote['usage_count']} 次)")
    else:
        print("\n❌ 沒有匯入任何語料，請檢查檔案格式")
        print("預期格式：")
        print("===")
        print("日期")
        print("內容")
        print("===")

if __name__ == "__main__":
    main()