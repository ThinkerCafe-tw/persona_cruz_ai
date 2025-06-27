"""
無極觀察者 - 五行AI系統的平衡監測框架
"""
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class Element(Enum):
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"

class InteractionType(Enum):
    GENERATING = "相生"  # 相生
    CONTROLLING = "相剋"  # 相剋
    NEUTRAL = "中性"     # 中性

@dataclass
class Interaction:
    """記錄元素間的互動"""
    timestamp: datetime
    sender: Element
    receiver: Element
    interaction_type: InteractionType
    message_type: str
    impact_score: float = 0.0
    
@dataclass
class ElementState:
    """元素狀態"""
    element: Element
    activity_level: float = 0.0  # 0-100
    energy_level: float = 100.0  # 0-100
    effectiveness: float = 0.0   # 0-100
    task_count: int = 0
    interaction_count: int = 0
    last_active: Optional[datetime] = None

class WujiObserver:
    """無極觀察者 - 系統平衡監測器"""
    
    def __init__(self):
        self.element_states = {
            Element.WOOD: ElementState(Element.WOOD),
            Element.FIRE: ElementState(Element.FIRE),
            Element.EARTH: ElementState(Element.EARTH),
            Element.METAL: ElementState(Element.METAL),
            Element.WATER: ElementState(Element.WATER)
        }
        self.interactions: List[Interaction] = []
        self.harmony_score = 100.0
        self.patterns: List[Dict] = []
        self.observations: List[Dict] = []
        
        # 定義相生相剋關係
        self.generating_cycle = {
            Element.WOOD: Element.FIRE,
            Element.FIRE: Element.EARTH,
            Element.EARTH: Element.METAL,
            Element.METAL: Element.WATER,
            Element.WATER: Element.WOOD
        }
        
        self.controlling_cycle = {
            Element.WOOD: Element.EARTH,
            Element.FIRE: Element.METAL,
            Element.EARTH: Element.WATER,
            Element.METAL: Element.WOOD,
            Element.WATER: Element.FIRE
        }
    
    def observe_interaction(self, sender: Element, receiver: Element, 
                          message_type: str, impact: float = 1.0):
        """觀察並記錄元素互動"""
        # 判斷互動類型
        if self.generating_cycle.get(sender) == receiver:
            interaction_type = InteractionType.GENERATING
        elif self.controlling_cycle.get(sender) == receiver:
            interaction_type = InteractionType.CONTROLLING
        else:
            interaction_type = InteractionType.NEUTRAL
        
        # 記錄互動
        interaction = Interaction(
            timestamp=datetime.now(),
            sender=sender,
            receiver=receiver,
            interaction_type=interaction_type,
            message_type=message_type,
            impact_score=impact
        )
        self.interactions.append(interaction)
        
        # 更新元素狀態
        self._update_element_states(sender, receiver, interaction_type, impact)
        
        # 分析模式
        self._analyze_patterns()
        
        # 計算和諧度
        self._calculate_harmony()
        
        return self._generate_observation(interaction)
    
    def _update_element_states(self, sender: Element, receiver: Element, 
                              interaction_type: InteractionType, impact: float):
        """更新元素狀態"""
        now = datetime.now()
        
        # 更新發送者狀態
        sender_state = self.element_states[sender]
        sender_state.activity_level = min(100, sender_state.activity_level + impact * 10)
        sender_state.energy_level = max(0, sender_state.energy_level - impact * 5)
        sender_state.interaction_count += 1
        sender_state.last_active = now
        
        # 更新接收者狀態
        receiver_state = self.element_states[receiver]
        
        if interaction_type == InteractionType.GENERATING:
            # 相生：接收者獲得能量
            receiver_state.energy_level = min(100, receiver_state.energy_level + impact * 8)
            receiver_state.effectiveness = min(100, receiver_state.effectiveness + impact * 5)
        elif interaction_type == InteractionType.CONTROLLING:
            # 相剋：接收者被抑制
            receiver_state.activity_level = max(0, receiver_state.activity_level - impact * 15)
            receiver_state.energy_level = max(0, receiver_state.energy_level - impact * 10)
        
        receiver_state.last_active = now
    
    def _analyze_patterns(self):
        """分析互動模式"""
        if len(self.interactions) < 5:
            return
        
        # 分析最近的互動序列
        recent_interactions = self.interactions[-10:]
        
        # 檢測循環模式
        cycle_pattern = self._detect_cycle_pattern(recent_interactions)
        if cycle_pattern:
            self.patterns.append({
                "type": "cycle",
                "pattern": cycle_pattern,
                "timestamp": datetime.now()
            })
        
        # 檢測失衡模式
        imbalance = self._detect_imbalance()
        if imbalance:
            self.patterns.append({
                "type": "imbalance",
                "details": imbalance,
                "timestamp": datetime.now()
            })
    
    def _detect_cycle_pattern(self, interactions: List[Interaction]) -> Optional[List[Element]]:
        """檢測循環模式"""
        if len(interactions) < 5:
            return None
        
        # 檢查是否形成完整的相生循環
        elements_sequence = [i.sender for i in interactions[-5:]]
        
        # 檢查是否為完整的五行相生循環
        expected_sequence = list(self.generating_cycle.keys())
        for i in range(5):
            rotated = expected_sequence[i:] + expected_sequence[:i]
            if elements_sequence == rotated:
                return elements_sequence
        
        return None
    
    def _detect_imbalance(self) -> Optional[Dict]:
        """檢測系統失衡，並按嚴重性排序"""
        imbalances = []
        
        for element, state in self.element_states.items():
            # 嚴重性評分: 10 (最高) - 1 (最低)
            if state.activity_level == 0:
                imbalances.append({
                    "severity": 9, # 活動為零是嚴重問題
                    "element": element.value,
                    "issue": "活動不足",
                    "details": f"活躍度為 {state.activity_level:.0f}%"
                })
            elif state.last_active and (datetime.now() - state.last_active).total_seconds() > 7200: # 2小時
                imbalances.append({
                    "severity": 5,
                    "element": element.value,
                    "issue": "長時間未活動",
                    "details": f"已 {(datetime.now() - state.last_active).total_seconds()/3600:.1f} 小時未活動"
                })
            elif state.activity_level > 80:
                imbalances.append({
                    "severity": 7,
                    "element": element.value,
                    "issue": "過度活躍",
                    "details": f"活躍度高達 {state.activity_level:.0f}%"
                })
            elif state.energy_level < 20:
                imbalances.append({
                    "severity": 6,
                    "element": element.value,
                    "issue": "能量不足",
                    "details": f"能量低於 {state.energy_level:.0f}%"
                })

        # 按嚴重性從高到低排序
        imbalances.sort(key=lambda x: x.get('severity', 0), reverse=True)
        return imbalances if imbalances else None
    
    def _calculate_harmony(self):
        """計算系統和諧度"""
        factors = []
        
        # 1. 活動平衡度
        activity_levels = [s.activity_level for s in self.element_states.values()]
        activity_variance = self._calculate_variance(activity_levels)
        activity_balance = max(0, 100 - activity_variance)
        factors.append(activity_balance)
        
        # 2. 能量平衡度
        energy_levels = [s.energy_level for s in self.element_states.values()]
        energy_variance = self._calculate_variance(energy_levels)
        energy_balance = max(0, 100 - energy_variance)
        factors.append(energy_balance)
        
        # 3. 互動流暢度
        if self.interactions:
            recent_interactions = self.interactions[-20:]
            interaction_types = [i.interaction_type for i in recent_interactions]
            generating_ratio = interaction_types.count(InteractionType.GENERATING) / len(interaction_types)
            flow_score = generating_ratio * 100
            factors.append(flow_score)
        
        # 4. 整體效能
        effectiveness_avg = sum(s.effectiveness for s in self.element_states.values()) / 5
        factors.append(effectiveness_avg)
        
        self.harmony_score = sum(factors) / len(factors)
    
    def _calculate_variance(self, values: List[float]) -> float:
        """計算變異數"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _generate_observation(self, interaction: Interaction) -> Dict:
        """生成觀察報告"""
        observation = {
            "timestamp": datetime.now().isoformat(),
            "event": {
                "type": "interaction",
                "sender": interaction.sender.value,
                "receiver": interaction.receiver.value,
                "interaction_type": interaction.interaction_type.value,
                "message_type": interaction.message_type
            },
            "system_state": {
                "harmony_score": round(self.harmony_score, 2),
                "element_states": {
                    element.value: {
                        "activity": round(state.activity_level, 2),
                        "energy": round(state.energy_level, 2),
                        "effectiveness": round(state.effectiveness, 2)
                    }
                    for element, state in self.element_states.items()
                },
                "recent_patterns": self.patterns[-3:] if self.patterns else []
            }
        }
        
        self.observations.append(observation)
        return observation
    
    def generate_harmony_report(self) -> str:
        """生成和諧度報告"""
        report = f"""
【無極觀察日誌】
時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}
和諧度：{self.harmony_score:.0f}/100

五行狀態：
"""
        
        for element, state in self.element_states.items():
            bar_length = int(state.activity_level / 10)
            bar = '█' * bar_length + '░' * (10 - bar_length)
            report += f"{element.value} {bar} {state.activity_level:.0f}% - "
            
            if state.activity_level > 80:
                status = "活躍過度（需降溫）"
            elif state.energy_level < 30:
                status = "能量不足（需補充）"
            elif state.activity_level < 20:
                status = "活動不足（需激活）"
            else:
                status = "狀態平衡"
            
            report += f"{status}\n"
        
        # 添加洞察
        imbalances = self._detect_imbalance()
        if imbalances:
            report += "\n洞察："
            for imbalance in imbalances[:2]:  # 只顯示最重要的兩個
                report += f"\n- {imbalance['element']}屬性{imbalance['issue']} ({imbalance['details']})"
            
            # 提供建議
            most_critical = imbalances[0]
            report += "\n\n建議："

            if most_critical['issue'] == "過度活躍":
                controller = None
                for e, controlled in self.controlling_cycle.items():
                    if controlled.value == most_critical['element']:
                        controller = e.value
                        break
                if controller:
                    report += f"\n考慮增強 {controller} 的活動，以「{controller}剋{most_critical['element']}」的方式來平衡 {most_critical['element']}。"

            elif most_critical['issue'] == "能量不足":
                generator = None
                for e, generated in self.generating_cycle.items():
                    if generated.value == most_critical['element']:
                        generator = e.value
                        break
                if generator:
                    report += f"\n建議增強 {generator} 的活動，以「{generator}生{most_critical['element']}」的方式來補充其能量。"

            elif most_critical['issue'] in ["活動不足", "長時間未活動"]:
                generator = None
                for e, generated in self.generating_cycle.items():
                    if generated.value == most_critical['element']:
                        generator = e.value
                        break
                if generator:
                    report += f"\n建議增強 {generator} 的活動，以「{generator}生{most_critical['element']}」的方式來激活 {most_critical['element']}。"
        else:
            report += "\n\n洞察：系統運作和諧，五行平衡流轉。"
        
        return report
    
    def suggest_adjustment(self) -> Optional[Dict]:
        """提供調節建議"""
        imbalances = self._detect_imbalance()
        if not imbalances:
            return None
        
        # 找出最需要調節的元素
        most_critical = imbalances[0]
        
        adjustment = {
            "target_element": most_critical['element'],
            "issue": most_critical['issue'],
            "suggestions": []
        }
        
        if most_critical['issue'] == "過度活躍":
            # 建議啟動剋制元素
            for element, controlled in self.controlling_cycle.items():
                if controlled.value == most_critical['element']:
                    adjustment['suggestions'].append({
                        "action": "activate",
                        "element": element.value,
                        "reason": f"透過{element.value}剋{most_critical['element']}來降低其活躍度"
                    })
                    break
        
        elif most_critical['issue'] == "能量不足":
            # 建議啟動相生元素
            for element, generated in self.generating_cycle.items():
                if generated.value == most_critical['element']:
                    adjustment['suggestions'].append({
                        "action": "enhance",
                        "element": element.value,
                        "reason": f"透過{element.value}生{most_critical['element']}來補充能量"
                    })
                    break
        
        # 添加隱喻性建議
        adjustment['metaphor'] = self._generate_metaphor(most_critical['issue'])
        
        return adjustment
    
    def _generate_metaphor(self, issue: str) -> str:
        """生成隱喻性建議"""
        metaphors = {
            "過度活躍": "如夏日驕陽需要秋風調和，過盛之火需要水的智慧來平衡。",
            "能量不足": "如春雨滋潤枯木，相生之力能讓疲憊的元素重獲生機。",
            "長時間未活動": "靜水深流，但過久的沉寂會失去活力，需要適當的激發。"
        }
        return metaphors.get(issue, "天地萬物，動靜相宜，過與不及皆非中道。")