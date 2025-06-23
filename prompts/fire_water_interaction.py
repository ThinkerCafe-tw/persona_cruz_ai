"""
火與水的首次互動 - 開發與測試的對話實例
"""
import json
from datetime import datetime
from typing import Dict, List

class FireWaterInteraction:
    """實作火（開發）與水（測試）的互動案例"""
    
    def __init__(self):
        self.dialogue_history = []
        self.code_versions = []
        self.test_results = []
    
    def start_interaction(self):
        """開始火與水的互動"""
        print("=== 五行AI系統：火與水的首次對話 ===\n")
        
        # 第一回合：火（開發）提交初版程式碼
        self.round_1_fire_develops()
        
        # 第二回合：水（測試）發現問題
        self.round_2_water_tests()
        
        # 第三回合：火（開發）修復問題
        self.round_3_fire_fixes()
        
        # 第四回合：水（測試）確認修復
        self.round_4_water_confirms()
        
        # 顯示互動總結
        self.show_interaction_summary()
    
    def round_1_fire_develops(self):
        """第一回合：火提交程式碼"""
        fire_message = {
            "role": "🔥 開發專員（火）",
            "timestamp": datetime.now().isoformat(),
            "content": "我已經完成用戶登入功能的初版實作！",
            "code": """
def handle_user_login(line_id, display_name):
    if line_id in users:
        return f"歡迎回來，{users[line_id]['name']}！"
    else:
        users[line_id] = {"name": display_name}
        return f"歡迎新用戶 {display_name}！"
""",
            "confidence": "這個實作簡潔明瞭，應該能滿足基本需求。"
        }
        
        self.dialogue_history.append(fire_message)
        self.code_versions.append({
            "version": "v1.0",
            "code": fire_message["code"],
            "status": "待測試"
        })
        
        print(f"{fire_message['role']}")
        print(f"💬 {fire_message['content']}")
        print(f"🔥 {fire_message['confidence']}")
        print(f"\n程式碼：")
        print(fire_message['code'])
        print("\n" + "="*50 + "\n")
    
    def round_2_water_tests(self):
        """第二回合：水發現問題"""
        water_message = {
            "role": "💧 測試專員（水）",
            "timestamp": datetime.now().isoformat(),
            "content": "我發現了幾個需要注意的問題...",
            "test_results": [
                {
                    "test": "測試 display_name 為 None",
                    "result": "❌ 失敗",
                    "error": "TypeError: 無法連接 None 和字串"
                },
                {
                    "test": "測試全域變數 users 未定義",
                    "result": "❌ 失敗", 
                    "error": "NameError: name 'users' is not defined"
                },
                {
                    "test": "測試缺少時間記錄",
                    "result": "⚠️ 功能缺失",
                    "error": "需求中要求記錄登入時間，但程式碼中沒有實作"
                }
            ],
            "suggestion": "程式碼需要更完善的錯誤處理和功能實作。"
        }
        
        self.dialogue_history.append(water_message)
        self.test_results.append({
            "version": "v1.0",
            "passed": 0,
            "failed": 3,
            "coverage": "40%"
        })
        
        print(f"{water_message['role']}")
        print(f"💬 {water_message['content']}")
        print("\n測試結果：")
        for test in water_message['test_results']:
            print(f"  • {test['test']}: {test['result']}")
            if test['error']:
                print(f"    錯誤：{test['error']}")
        print(f"\n💧 {water_message['suggestion']}")
        print("\n" + "="*50 + "\n")
    
    def round_3_fire_fixes(self):
        """第三回合：火修復問題"""
        fire_message = {
            "role": "🔥 開發專員（火）",
            "timestamp": datetime.now().isoformat(),
            "content": "感謝測試專員的細心測試！我已經修復所有問題。",
            "code": """
from datetime import datetime

# 初始化用戶字典
users = {}

def handle_user_login(line_id, display_name=None):
    '''處理用戶登入，包含完整的錯誤處理'''
    current_time = datetime.now()
    
    # 處理 display_name 為 None 的情況
    if display_name is None:
        display_name = f"用戶_{line_id[:8]}"
    
    if line_id in users:
        # 返回用戶
        user = users[line_id]
        last_login = user.get('last_login', '首次登入')
        user['last_login'] = current_time
        
        return {
            "status": "success",
            "message": f"歡迎回來，{user['name']}！上次登入：{last_login}",
            "is_new_user": False
        }
    else:
        # 新用戶註冊
        users[line_id] = {
            "name": display_name,
            "created_at": current_time,
            "last_login": current_time
        }
        
        return {
            "status": "success", 
            "message": f"歡迎新朋友 {display_name}！",
            "is_new_user": True
        }
""",
            "improvements": [
                "加入 display_name 的 None 檢查",
                "初始化 users 字典",
                "加入時間記錄功能",
                "改善回傳格式，包含更多資訊"
            ]
        }
        
        self.dialogue_history.append(fire_message)
        self.code_versions.append({
            "version": "v2.0",
            "code": fire_message["code"],
            "status": "修復完成"
        })
        
        print(f"{fire_message['role']}")
        print(f"💬 {fire_message['content']}")
        print("\n改進項目：")
        for imp in fire_message['improvements']:
            print(f"  ✓ {imp}")
        print(f"\n更新的程式碼：")
        print(fire_message['code'])
        print("\n" + "="*50 + "\n")
    
    def round_4_water_confirms(self):
        """第四回合：水確認修復"""
        water_message = {
            "role": "💧 測試專員（水）",
            "timestamp": datetime.now().isoformat(),
            "content": "太好了！所有測試都通過了！",
            "test_results": [
                {
                    "test": "測試 display_name 為 None",
                    "result": "✅ 通過",
                    "note": "正確處理，使用預設名稱"
                },
                {
                    "test": "測試全域變數 users",
                    "result": "✅ 通過",
                    "note": "users 字典已正確初始化"
                },
                {
                    "test": "測試時間記錄功能",
                    "result": "✅ 通過",
                    "note": "正確記錄登入時間"
                },
                {
                    "test": "測試新用戶註冊",
                    "result": "✅ 通過",
                    "note": "新用戶能正確註冊"
                },
                {
                    "test": "測試返回用戶登入",
                    "result": "✅ 通過",
                    "note": "顯示上次登入時間"
                }
            ],
            "final_assessment": "程式碼品質良好，功能完整，可以進入下一階段。"
        }
        
        self.dialogue_history.append(water_message)
        self.test_results.append({
            "version": "v2.0",
            "passed": 5,
            "failed": 0,
            "coverage": "95%"
        })
        
        print(f"{water_message['role']}")
        print(f"💬 {water_message['content']}")
        print("\n測試結果：")
        for test in water_message['test_results']:
            print(f"  • {test['test']}: {test['result']}")
            if test.get('note'):
                print(f"    備註：{test['note']}")
        print(f"\n💧 最終評估：{water_message['final_assessment']}")
        print("\n" + "="*50 + "\n")
    
    def show_interaction_summary(self):
        """顯示互動總結"""
        print("=== 互動總結 ===\n")
        
        print("📊 版本演進：")
        for version in self.code_versions:
            print(f"  • {version['version']}: {version['status']}")
        
        print("\n📈 測試改善：")
        for result in self.test_results:
            total = result['passed'] + result['failed']
            pass_rate = (result['passed'] / total * 100) if total > 0 else 0
            print(f"  • {result['version']}: {result['passed']}/{total} 通過 ({pass_rate:.0f}%) - 覆蓋率 {result['coverage']}")
        
        print("\n🎯 關鍵學習：")
        learnings = [
            "火的快速開發需要水的細心測試來保證品質",
            "相剋關係（水剋火）實際上是一種建設性的制衡",
            "透過多輪互動，程式碼品質顯著提升",
            "測試不是找碴，而是幫助開發者完善作品"
        ]
        for learning in learnings:
            print(f"  • {learning}")
        
        print("\n✨ 這次互動展示了五行相剋如何促進系統進步！")


def demonstrate_wuji_observation():
    """展示無極如何觀察這次互動"""
    print("\n\n=== 無極的觀察 ===\n")
    
    print("⚪ 無極觀察者：")
    print("我觀察到火與水的首次互動呈現了完美的相剋相生：")
    print()
    print("1. 🔥 火的熱情快速產出了初版程式碼")
    print("2. 💧 水的冷靜發現了潛在的問題")
    print("3. 🔥 火接受了水的建議，沒有抗拒而是積極改進")
    print("4. 💧 水確認了改進，給予正面回饋")
    print()
    print("系統和諧度：85/100")
    print("火的能量：從 100 降至 70（健康的消耗）")
    print("水的能量：從 80 升至 90（因成功測試而提升）")
    print()
    print("建議：這是一個良好的開始。")
    print("下一步可以引入土（架構師）來鞏固這個功能，")
    print("讓整個系統更加穩定。")


# 執行演示
if __name__ == "__main__":
    interaction = FireWaterInteraction()
    interaction.start_interaction()
    demonstrate_wuji_observation()