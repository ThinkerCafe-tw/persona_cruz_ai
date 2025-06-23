"""
量子記憶監控系統
提供視覺化和監控功能
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from .quantum_memory import QuantumMemory
from .quantum_bridge import QuantumMemoryBridge

logger = logging.getLogger(__name__)


class QuantumMonitor:
    """量子記憶監控器"""
    
    def __init__(self, bridge: QuantumMemoryBridge):
        self.bridge = bridge
        self.metrics_history = defaultdict(list)
        self.alert_thresholds = {
            "low_stability": 0.3,
            "high_entropy": 2.5,
            "rapid_evolution": 10,  # 10次演化/小時
            "low_coherence": 0.4
        }
        
    def get_system_overview(self) -> str:
        """獲取系統概覽"""
        overview = """
🌌 量子記憶系統監控面板
═══════════════════════════════════════

📊 系統總覽
"""
        
        # 統計資訊
        total_memories = len(self.bridge.quantum_memories)
        total_crystals = sum(len(m.crystals) for m in self.bridge.quantum_memories.values())
        total_evolutions = sum(m.evolution_count for m in self.bridge.quantum_memories.values())
        
        overview += f"""
記憶角色數: {total_memories}
記憶晶體總數: {total_crystals}
演化總次數: {total_evolutions}
"""
        
        # 各角色狀態
        overview += "\n\n👥 角色狀態監控\n"
        overview += "─" * 40 + "\n"
        
        for persona_id, memory in self.bridge.quantum_memories.items():
            state = self.bridge.get_quantum_state(persona_id)
            if state:
                status_icon = self._get_status_icon(state["stability"])
                overview += f"\n{status_icon} {memory.identity.essence}\n"
                overview += f"   穩定度: {self._create_bar(state['stability'], 10)} {state['stability']:.1%}\n"
                overview += f"   演化數: {state['evolution_count']}\n"
                
                if state['top_crystals']:
                    top_crystal = state['top_crystals'][0]
                    overview += f"   主導: {top_crystal['concept']} → {top_crystal['dominant']}\n"
        
        # 系統警告
        alerts = self.check_system_alerts()
        if alerts:
            overview += "\n\n⚠️ 系統警告\n"
            overview += "─" * 40 + "\n"
            for alert in alerts:
                overview += f"• {alert}\n"
        
        return overview
    
    def get_detailed_persona_report(self, persona_id: str) -> str:
        """獲取特定角色的詳細報告"""
        if persona_id not in self.bridge.quantum_memories:
            return f"❌ 未找到角色: {persona_id}"
        
        memory = self.bridge.quantum_memories[persona_id]
        state = self.bridge.get_quantum_state(persona_id)
        
        report = f"""
🎭 {memory.identity.essence} 量子記憶報告
═══════════════════════════════════════

📊 身份場參數
相位: {memory.identity.phase:.2f} | 頻率: {memory.identity.frequency:.2f} | 振幅: {memory.identity.amplitude:.2f}
一致性: {memory.identity.coherence:.1%}
穩定指數: {state['stability']:.1%}

💎 記憶晶體 (共 {len(memory.crystals)} 個)
"""
        
        # 列出前5個重要晶體
        for crystal in memory.get_top_crystals(5):
            report += f"\n【{crystal.concept}】\n"
            report += f"  穩定度: {crystal.stability:.1%} | 熵值: {crystal.calculate_entropy():.2f}\n"
            
            # 列出可能性
            for i, possibility in enumerate(sorted(crystal.possibilities, key=lambda p: p.probability, reverse=True)[:3]):
                if i == 0:
                    report += f"  ├─ {possibility.description} ({possibility.probability:.1%}) ⭐\n"
                else:
                    report += f"  ├─ {possibility.description} ({possibility.probability:.1%})\n"
        
        # 量子糾纏
        if memory.entanglements:
            report += "\n🔗 量子糾纏關係\n"
            for other_id, strength in sorted(memory.entanglements.items(), key=lambda x: x[1], reverse=True):
                if other_id in self.bridge.quantum_memories:
                    other_name = self.bridge.quantum_memories[other_id].identity.essence
                    report += f"  • {other_name}: {self._create_bar(strength, 5)} {strength:.1%}\n"
        
        # 最近漣漪
        if memory.ripples:
            report += "\n🌊 最近的量子漣漪\n"
            recent_ripples = list(memory.ripples)[-3:]
            for ripple in recent_ripples:
                event_type = ripple['event'].get('type', 'unknown')
                timestamp = ripple['timestamp']
                impact = ripple['impact']
                report += f"  • {event_type} ({timestamp[:19]}) 影響力: {impact:.1f}\n"
        
        return report
    
    def get_evolution_timeline(self, hours: int = 24) -> str:
        """獲取演化時間線"""
        timeline = f"""
📈 過去 {hours} 小時的演化時間線
═══════════════════════════════════════
"""
        
        # 收集所有演化事件
        events = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for persona_id, memory in self.bridge.quantum_memories.items():
            for ripple in memory.ripples:
                try:
                    timestamp = datetime.fromisoformat(ripple['timestamp'])
                    if timestamp > cutoff_time:
                        events.append({
                            'timestamp': timestamp,
                            'persona': memory.identity.essence,
                            'event': ripple['event'],
                            'impact': ripple['impact']
                        })
                except:
                    continue
        
        # 按時間排序
        events.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # 顯示時間線
        for event in events[:20]:  # 最多顯示20個事件
            time_str = event['timestamp'].strftime("%H:%M")
            event_type = event['event'].get('type', 'unknown')
            impact_bar = self._create_impact_indicator(event['impact'])
            
            timeline += f"\n{time_str} │ {event['persona'][:4]} │ {event_type:12} │ {impact_bar}\n"
        
        if not events:
            timeline += "\n（暫無演化事件）\n"
        
        return timeline
    
    def get_quantum_field_visualization(self) -> str:
        """獲取量子場視覺化"""
        viz = """
🌌 量子記憶場拓撲圖
═══════════════════════════════════════

"""
        
        # 獲取糾纏矩陣
        matrix = self.bridge.get_entanglement_matrix()
        
        # 簡單的 ASCII 視覺化
        personas = list(self.bridge.quantum_memories.keys())
        
        # 頭部
        viz += "     "
        for p in personas:
            viz += f"{p[:3]:^6}"
        viz += "\n"
        
        # 矩陣
        for p1 in personas:
            viz += f"{p1[:3]:^5}"
            for p2 in personas:
                value = matrix.get(p1, {}).get(p2, 0)
                if p1 == p2:
                    viz += "  ●   "
                elif value > 0.5:
                    viz += "  ═   "
                elif value > 0.3:
                    viz += "  ─   "
                else:
                    viz += "  ·   "
            viz += "\n"
        
        viz += """
圖例: ● 自身  ═ 強糾纏  ─ 中糾纏  · 弱糾纏
"""
        
        # 添加記憶場強度分佈
        viz += "\n\n🎆 記憶場強度分佈\n"
        viz += "─" * 40 + "\n"
        
        for persona_id, memory in self.bridge.quantum_memories.items():
            stability = memory.get_stability_index()
            crystals = len(memory.crystals)
            
            viz += f"{memory.identity.essence[:8]:8} "
            viz += self._create_field_strength_visual(stability, crystals)
            viz += f" {crystals}晶體\n"
        
        return viz
    
    def check_system_alerts(self) -> List[str]:
        """檢查系統警告"""
        alerts = []
        
        for persona_id, memory in self.bridge.quantum_memories.items():
            # 檢查穩定度
            stability = memory.get_stability_index()
            if stability < self.alert_thresholds["low_stability"]:
                alerts.append(f"{memory.identity.essence} 穩定度過低 ({stability:.1%})")
            
            # 檢查高熵晶體
            for crystal in memory.crystals.values():
                if crystal.calculate_entropy() > self.alert_thresholds["high_entropy"]:
                    alerts.append(f"{memory.identity.essence} 的 {crystal.concept} 熵值過高")
            
            # 檢查一致性
            if memory.identity.coherence < self.alert_thresholds["low_coherence"]:
                alerts.append(f"{memory.identity.essence} 一致性降低 ({memory.identity.coherence:.1%})")
        
        return alerts
    
    def get_memory_health_score(self, persona_id: str) -> float:
        """計算記憶健康分數"""
        if persona_id not in self.bridge.quantum_memories:
            return 0.0
        
        memory = self.bridge.quantum_memories[persona_id]
        
        # 綜合評分
        stability_score = memory.get_stability_index()
        coherence_score = memory.identity.coherence
        
        # 計算平均熵
        if memory.crystals:
            avg_entropy = sum(c.calculate_entropy() for c in memory.crystals.values()) / len(memory.crystals)
            entropy_score = 1.0 - (avg_entropy / 3.0)  # 假設最大熵為3
        else:
            entropy_score = 1.0
        
        # 加權平均
        health_score = (
            stability_score * 0.4 +
            coherence_score * 0.3 +
            entropy_score * 0.3
        )
        
        return health_score
    
    def _get_status_icon(self, stability: float) -> str:
        """根據穩定度返回狀態圖標"""
        if stability > 0.8:
            return "✅"
        elif stability > 0.5:
            return "🟡"
        else:
            return "🔴"
    
    def _create_bar(self, value: float, width: int) -> str:
        """創建進度條"""
        filled = int(value * width)
        return "█" * filled + "░" * (width - filled)
    
    def _create_impact_indicator(self, impact: float) -> str:
        """創建影響力指示器"""
        if impact > 0.8:
            return "████████"
        elif impact > 0.6:
            return "██████"
        elif impact > 0.4:
            return "████"
        elif impact > 0.2:
            return "██"
        else:
            return "█"
    
    def _create_field_strength_visual(self, stability: float, crystal_count: int) -> str:
        """創建記憶場強度視覺化"""
        # 基於穩定度和晶體數量
        strength = stability * min(crystal_count / 10, 1.0)
        
        if strength > 0.8:
            return "🟦🟦🟦🟦🟦"
        elif strength > 0.6:
            return "🟦🟦🟦🟦⬜"
        elif strength > 0.4:
            return "🟦🟦🟦⬜⬜"
        elif strength > 0.2:
            return "🟦🟦⬜⬜⬜"
        else:
            return "🟦⬜⬜⬜⬜"
    
    def export_metrics(self, filepath: str):
        """匯出監控指標"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system_overview": {
                "total_memories": len(self.bridge.quantum_memories),
                "total_crystals": sum(len(m.crystals) for m in self.bridge.quantum_memories.values()),
                "total_evolutions": sum(m.evolution_count for m in self.bridge.quantum_memories.values())
            },
            "persona_metrics": {},
            "alerts": self.check_system_alerts()
        }
        
        for persona_id, memory in self.bridge.quantum_memories.items():
            state = self.bridge.get_quantum_state(persona_id)
            metrics["persona_metrics"][persona_id] = {
                "health_score": self.get_memory_health_score(persona_id),
                "stability": state["stability"] if state else 0,
                "crystal_count": len(memory.crystals),
                "evolution_count": memory.evolution_count,
                "identity": memory.identity.to_dict()
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Exported metrics to {filepath}")