import os
import json
from datetime import datetime
import sys

# Add project root to sys.path to allow imports from other directories
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from prompts.wuji_observer import WujiObserver, Element

def main():
    """
    主函數，用於啟動無極觀察者並生成和諧度報告。
    """
    print("🌌 無極觀察者正在啟動...")
    observer = WujiObserver()
    
    # 根據 CLAUDE.md 和記憶檔案定義人格與五行的映射關係
    persona_to_element = {
        "wood": Element.WOOD,
        "fire": Element.FIRE,
        "earth": Element.EARTH,
        "avery": Element.WATER,  # Avery 在 CLAUDE.md 中被定義為支持與關懷者(水)
        "cruz": Element.METAL,   # Cruz 的決斷與推進特質，在此腳本中對應金
        "wuji": None # 無極本身不參與五行，而是作為觀察者
    }

    memory_dir = os.path.join(project_root, "quantum_memory", "memories")
    print(f"🔍 正在掃描記憶目錄: {memory_dir}")

    found_files = 0
    for persona_id, element in persona_to_element.items():
        if element is None:
            continue

        file_path = os.path.join(memory_dir, f"{persona_id}.json")
        if os.path.exists(file_path):
            found_files += 1
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            state = observer.element_states[element]
            if data.get("last_save"):
                state.last_active = datetime.fromisoformat(data["last_save"])
            
            # 簡化模擬：漣漪數量代表活躍度，振幅代表能量
            ripple_count = len(data.get("ripples", []))
            amplitude = data.get("identity", {}).get("amplitude", 1.0)

            # 活躍度以漣漪數量為基礎，能量以振幅為基礎
            state.activity_level = min(100, ripple_count * 20)
            state.energy_level = min(100, amplitude * 100)
            
            print(f"  - 觀察到 {persona_id} ({element.value}) | 活躍度: {state.activity_level:<3.0f} | 能量: {state.energy_level:<3.0f}")

    if found_files == 0:
        print("⚠️ 未找到任何記憶檔案，無法生成報告。")
        return

    # 基於當前快照重新計算和諧度
    observer._calculate_harmony()
    
    print("\n" + "="*50)
    report = observer.generate_harmony_report()
    print(report)
    print("="*50 + "\n")
    print("🌌 無極觀察者報告完畢。")

if __name__ == "__main__":
    main() 