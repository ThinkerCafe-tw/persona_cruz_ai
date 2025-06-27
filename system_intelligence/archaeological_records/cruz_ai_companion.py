#!/usr/bin/env python3
"""
CRUZ AI 伴侶系統
整合所有 CRUZ 功能的主程式
"""
import sys
import logging
from typing import Optional
from cruz_developer_mode import CruzDeveloperMode
from conversation_memory_sync import ConversationMemorySync
from five_elements_agent import FiveElementsAgent

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CruzAICompanion:
    """CRUZ AI 伴侶 - 您的數位分身開發夥伴"""
    
    def __init__(self):
        self.cruz_dev = CruzDeveloperMode()
        self.memory_sync = ConversationMemorySync()
        self.five_elements = FiveElementsAgent()
        self.current_mode = "cruz"  # 預設使用 CRUZ 模式
        
    def start(self):
        """啟動 AI 伴侶"""
        print("\n" + "="*60)
        print("🎯 CRUZ AI 伴侶系統啟動")
        print("="*60)
        print("\n您的數位分身開發夥伴已準備就緒！")
        print("\n可用指令：")
        print("  /mode <角色>  - 切換角色 (cruz/木/火/土/金/水/無極)")
        print("  /status      - 查看系統狀態")
        print("  /insights    - 查看最近的開發洞察")
        print("  /save        - 保存當前對話")
        print("  /help        - 顯示幫助")
        print("  /quit        - 結束程式")
        print("\n" + "-"*60)
        
        # 啟動 CRUZ 開發者模式
        greeting = self.cruz_dev.activate("general")
        print(f"\n🎯 CRUZ: {greeting}")
        print("-"*60 + "\n")
        
        # 主循環
        self.run_interactive_loop()
        
    def run_interactive_loop(self):
        """運行互動循環"""
        while True:
            try:
                # 獲取用戶輸入
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # 處理系統指令
                if user_input.startswith("/"):
                    self.handle_command(user_input)
                    continue
                
                # 處理一般對話
                self.process_conversation(user_input)
                
            except KeyboardInterrupt:
                print("\n\n正在保存對話...")
                self.memory_sync.force_save()
                print("再見！期待下次一起創造。")
                sys.exit(0)
                
            except Exception as e:
                logger.error(f"Error in interactive loop: {e}")
                print(f"發生錯誤：{e}")
                
    def handle_command(self, command: str):
        """處理系統指令"""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == "/quit":
            print("\n正在保存對話...")
            self.memory_sync.force_save()
            print("再見！期待下次一起創造。")
            sys.exit(0)
            
        elif cmd == "/help":
            self.show_help()
            
        elif cmd == "/status":
            self.show_status()
            
        elif cmd == "/insights":
            self.show_insights()
            
        elif cmd == "/save":
            result = self.cruz_dev.save_session()
            print(f"💾 {result}")
            
        elif cmd == "/mode":
            if len(parts) > 1:
                self.switch_mode(parts[1])
            else:
                print("請指定角色：cruz/木/火/土/金/水/無極")
                
        else:
            print(f"未知指令：{command}")
            
    def switch_mode(self, mode: str):
        """切換模式"""
        mode_lower = mode.lower()
        
        if mode_lower == "cruz":
            self.current_mode = "cruz"
            greeting = self.cruz_dev.activate("general")
            print(f"\n🎯 切換到 CRUZ 模式")
            print(f"CRUZ: {greeting}\n")
            
        elif mode in ["木", "火", "土", "金", "水", "無極"]:
            self.current_mode = mode
            result = self.five_elements.switch_role(mode)
            print(f"\n{result}")
            
            # 獲取角色介紹
            if mode == "無極":
                role = self.five_elements.wuji
            else:
                role = self.five_elements.roles[mode]
                
            print(f"特質：{role.personality}")
            print(f"專長：{', '.join(role.strengths)}\n")
            
        else:
            print(f"未知的模式：{mode}")
            
    def process_conversation(self, user_input: str):
        """處理對話"""
        if self.current_mode == "cruz":
            # 使用 CRUZ 開發者模式
            response = self.cruz_dev.process_message(user_input)
            
            print(f"\n🎯 CRUZ: {response['text']}")
            
            if response.get('suggestions'):
                print(f"\n💡 建議下一步：")
                for suggestion in response['suggestions']:
                    print(f"   • {suggestion}")
                    
            print()  # 空行分隔
            
        else:
            # 使用五行系統角色
            # 記錄對話到記憶系統
            self.memory_sync.add_conversation_turn("User", user_input, f"五行對話-{self.current_mode}")
            
            # 這裡簡化處理，實際應該調用 AI API
            role = self.five_elements.current_role
            response = f"【{role.emoji} {role.name}】基於我的{role.element}特質，我的看法是..."
            
            print(f"\n{response}")
            
            # 記錄回應
            self.memory_sync.add_conversation_turn(role.name, response, f"五行對話-{self.current_mode}")
            print()
            
    def show_help(self):
        """顯示幫助信息"""
        help_text = """
🎯 CRUZ AI 伴侶系統幫助

【系統指令】
  /mode <角色>  - 切換到不同角色
                  可選：cruz, 木, 火, 土, 金, 水, 無極
  /status      - 查看當前系統狀態
  /insights    - 查看最近提取的開發洞察
  /save        - 手動保存當前對話（自動每5輪保存）
  /help        - 顯示此幫助信息
  /quit        - 結束程式並保存

【角色說明】
  🎯 CRUZ      - 您的數位分身，直接、鼓勵創造
  🌲 木        - 產品經理，規劃與成長
  🔥 火        - 開發專員，快速實作
  🏔️ 土        - 架構師，穩固基礎
  ⚔️ 金        - 優化專員，精益求精
  💧 水        - 測試專員，品質把關
  ⚪ 無極      - 系統觀察者，全局平衡

【使用提示】
- 對話會自動記錄並提取洞察
- CRUZ 模式最適合產品決策和開發建議
- 五行角色各有專長，選擇適合的角色
- 重要決定會被記錄到記憶庫
"""
        print(help_text)
        
    def show_status(self):
        """顯示系統狀態"""
        status = self.cruz_dev.get_status()
        
        print("\n📊 系統狀態")
        print("-" * 40)
        print(f"當前模式：{self.current_mode}")
        print(f"CRUZ 開發模式：{'啟動' if status['active'] else '未啟動'}")
        print(f"對話緩衝區：{status['conversation_buffer_size']} 條")
        print(f"開發洞察總數：{status['total_insights']} 條")
        print(f"當前情境：{status['context']}")
        print("-" * 40 + "\n")
        
    def show_insights(self):
        """顯示最近的開發洞察"""
        insights = self.cruz_dev.get_development_insights()
        
        print("\n💡 最近的開發洞察")
        print("-" * 40)
        
        for insight in insights:
            print(insight)
            
        print("-" * 40 + "\n")


def main():
    """主程式入口"""
    companion = CruzAICompanion()
    companion.start()
    

if __name__ == "__main__":
    main()