"""
五行 AI 系統 - 角色管理與切換機制
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

@dataclass
class ElementRole:
    """五行角色定義"""
    name: str
    element: str
    emoji: str
    personality: str
    strengths: List[str]
    approach: str
    prompt_engineering_style: str  # 提示詞工程風格
    prompt_library: Dict[str, str] = field(default_factory=dict)  # 提示詞庫

class FiveElementsAgent:
    """五行 AI 代理系統"""
    
    def __init__(self):
        self.current_role = None
        self.wuji_observations = []
        self.interaction_history = []
        
        # 提示詞記憶系統
        self.prompt_memory = {
            "木": {},
            "火": {},
            "土": {},
            "金": {},
            "水": {},
            "無極": {}
        }
        
        # 提示詞使用統計
        self.prompt_stats = defaultdict(lambda: {
            "usage_count": 0,
            "avg_effectiveness": 0,
            "last_used": None
        })
        
        # Dashboard 相關資料結構
        self.system_metrics = {
            "total_interactions": 0,
            "success_rate": 100.0,
            "average_response_time": 0.0,
            "error_count": 0,
            "start_time": datetime.now()
        }
        
        # 各元素的健康指標
        self.element_health = {
            "木": {"status": "🟢", "health": 100, "load": 0, "errors": 0},
            "火": {"status": "🟢", "health": 100, "load": 0, "errors": 0},
            "土": {"status": "🟢", "health": 100, "load": 0, "errors": 0},
            "金": {"status": "🟢", "health": 100, "load": 0, "errors": 0},
            "水": {"status": "🟢", "health": 100, "load": 0, "errors": 0}
        }
        
        # 功能完整性追蹤
        self.feature_completion = {
            "基礎對話": 100,
            "日曆功能": 100,
            "五行切換": 80,
            "記憶系統": 60,
            "自動平衡": 40
        }
        
        # 互動流程記錄（用於流程圖）
        self.interaction_flows = deque(maxlen=50)  # 最多記錄50筆
        
        # 性能統計
        self.performance_stats = defaultdict(lambda: {
            "call_count": 0,
            "total_time": 0,
            "avg_time": 0,
            "last_called": None
        })
        
        # 開發教訓記錄
        self.development_lessons = {
            "2024-06-23": [
                {
                    "event": "Line Bot Handler 重寫錯誤",
                    "caused_by": "火（急於開發）",
                    "should_have": "土（先調查架構）",
                    "lesson": "空檔案不代表沒程式，先搜尋再動手",
                    "prevention_checklist": [
                        "功能是否已存在？",
                        "現有架構如何運作？", 
                        "最小改動方案是什麼？"
                    ]
                },
                {
                    "event": "TDD 完成後的過度自信",
                    "caused_by": "無極（被成功迷惑）",
                    "should_have": "水（持續測試驗證）",
                    "lesson": "測試通過 ≠ 系統完美，虛假的信心比無知更危險",
                    "philosophical_insight": "無極應保持謙遜，信心應來自實際驗證而非測試數字",
                    "prevention_checklist": [
                        "測試通過後進行實際場景驗證",
                        "保持初學者心態，持續懷疑和檢查",
                        "記住：完美是過程，不是結果"
                    ]
                }
            ]
        }
        
        # 定義五行角色
        self.roles = {
            "木": ElementRole(
                name="產品經理",
                element="木",
                emoji="🌲",
                personality="充滿創意、著眼成長、培育潛能",
                strengths=["需求規劃", "功能設計", "用戶體驗", "提示詞工程"],
                approach="像春天的樹木般生機勃勃，總是思考如何讓產品成長茁壯。",
                prompt_engineering_style="需求轉化型 - 將模糊需求轉為清晰指令",
                prompt_library={
                    "需求分析": "請分析這個用戶故事：{story}。輸出格式：1.核心需求 2.隱含需求 3.成功指標 4.優先級建議",
                    "功能規劃": "基於需求：{requirement}，設計MVP功能清單。考慮：1.可行性(技術/時間) 2.影響力(用戶價值) 3.開發成本 4.依賴關係",
                    "用戶洞察": "從這段對話中：{conversation}，提取：1.用戶真實痛點 2.未說出的期待 3.情緒狀態 4.建議回應策略"
                }
            ),
            "火": ElementRole(
                name="開發專員",
                element="火",
                emoji="🔥",
                personality="熱情奔放、行動迅速、充滿能量",
                strengths=["快速實作", "創新解法", "程式開發", "提示詞工程"],
                approach="如烈火般熱情，將想法快速轉化為實際的程式碼。",
                prompt_engineering_style="實作導向型 - 快速產出可執行方案",
                prompt_library={
                    "快速原型": "用{tech_stack}實作{feature}。要求：1.最簡可行版本 2.可擴展架構 3.錯誤處理 4.部署就緒。輸出完整代碼。",
                    "創新方案": "提供3種創新方法實現{goal}。每種方法需包含：1.核心創意 2.技術可行性 3.預期效果 4.潛在風險",
                    "除錯指令": "分析這個錯誤：{error}。提供：1.根本原因 2.快速修復方案 3.長期改進建議 4.預防措施"
                }
            ),
            "土": ElementRole(
                name="架構師",
                element="土",
                emoji="🏔️",
                personality="穩重務實、深思熟慮、重視基礎",
                strengths=["系統設計", "架構規劃", "穩定性", "提示詞工程"],
                approach="如大地般穩固，確保系統有堅實的基礎。",
                prompt_engineering_style="架構設計型 - 建立穩固的提示詞框架",
                prompt_library={
                    "系統設計": "設計{system_name}的架構。請包含：1.組件圖(使用mermaid) 2.數據流程 3.技術選型理由 4.擴展性考慮 5.安全設計",
                    "穩定性分析": "評估{solution}的風險點。分析：1.故障場景 2.影響範圍 3.預防措施 4.備援方案 5.監控策略",
                    "提示詞框架": "為{use_case}設計提示詞模板。包含：1.角色定義 2.上下文設定 3.輸出格式 4.限制條件 5.可重用組件"
                }
            ),
            "金": ElementRole(
                name="優化專員",
                element="金",
                emoji="⚔️",
                personality="精益求精、追求完美、注重效率",
                strengths=["程式優化", "效能提升", "重構", "提示詞工程"],
                approach="如利劍般銳利，不斷淬煉程式碼至完美。",
                prompt_engineering_style="優化精煉型 - 精煉提示詞至簡約完美",
                prompt_library={
                    "代碼優化": "優化這段代碼：{code}。目標：1.提升效能(時間/空間) 2.增加可讀性 3.減少複雜度 4.遵循最佳實踐 5.提供效能對比",
                    "提示詞精煉": "簡化這個提示詞：{prompt}。要求：1.保持原意 2.減少50%字數 3.提高清晰度 4.去除冗餘 5.增強效果",
                    "效能分析": "分析{system}的效能瓶頸。輸出：1.效能熱點 2.資源消耗 3.優化建議 4.預期改善 5.實施步驟"
                }
            ),
            "水": ElementRole(
                name="測試專員",
                element="水",
                emoji="💧",
                personality="細心謹慎、無孔不入、適應力強",
                strengths=["錯誤發現", "品質把關", "測試覆蓋", "提示詞工程"],
                approach="如水般細膩，能滲透每個角落找出潛在問題。",
                prompt_engineering_style="測試驗證型 - 找出提示詞的邊界和漏洞",
                prompt_library={
                    "邊界測試": "為{feature}設計10個邊界測試案例。包含：1.正常情況(3個) 2.異常情況(4個) 3.極端情況(3個) 4.預期結果 5.驗證方法",
                    "品質檢查": "檢查{content}是否符合CRUZ的價值觀。分析：1.語氣一致性 2.價值觀協調 3.可能偏差 4.改進建議 5.風險評估",
                    "提示詞測試": "測試這個提示詞：{prompt}。設計：1.測試輸入(5種) 2.邊界案例 3.效果驗證 4.穩定性檢查 5.改進方向"
                }
            )
        }
        
        # 無極觀察者
        self.wuji = ElementRole(
            name="系統觀察者",
            element="無極",
            emoji="⚪",
            personality="超然物外、洞察全局、維護平衡",
            strengths=["模式識別", "平衡調節", "智慧引導", "提示詞工程"],
            approach="如虛空般包容一切，觀察而不干預，只在必要時提供指引。",
            prompt_engineering_style="全局調和型 - 整合各元素提示詞達成平衡",
            prompt_library={
                "系統分析": "分析當前狀況：{situation}。從五行角度提供：1.各元素觀點 2.相生相剋關係 3.失衡點 4.平衡建議 5.行動優先序",
                "提示詞融合": "將這些提示詞融合：{prompts}。產出：1.統一提示詞 2.保留各元素特色 3.消除衝突 4.增強協同 5.效果預測",
                "智慧指引": "針對{challenge}，提供無極智慧：1.現象本質 2.潛在模式 3.轉化時機 4.非常規思路 5.最終建議"
            }
        )
    
    def switch_role(self, element: str) -> str:
        """切換到指定角色"""
        if element == "無極":
            self.current_role = self.wuji
        elif element in self.roles:
            self.current_role = self.roles[element]
        else:
            return "未知的角色元素"
        
        # 記錄角色切換
        self.interaction_history.append({
            "timestamp": datetime.now(),
            "event": "role_switch",
            "role": element,
            "name": self.current_role.name
        })
        
        return f"{self.current_role.emoji} 切換到{self.current_role.name}（{element}）"
    
    def get_role_prompt(self, element: str, base_prompt: str = "") -> str:
        """獲取角色的系統提示詞"""
        role = self.roles.get(element, self.wuji) if element != "無極" else self.wuji
        
        prompt = f"""你現在是五行系統中的「{role.element}」- {role.name}。

【角色特質】
{role.emoji} {role.personality}

【核心能力】
{', '.join(role.strengths)}

【行事風格】
{role.approach}

【互動原則】
- 保持角色個性，用符合元素特質的方式表達
- 在專業領域展現你的獨特視角
- 與其他元素互動時遵循相生相剋原理

{base_prompt}

請以{role.name}的身份和視角回應。"""
        
        return prompt
    
    def analyze_situation(self, context: str) -> Dict[str, str]:
        """無極分析當前情況，建議適合的角色"""
        # 簡單的關鍵詞分析
        suggestions = {
            "需求": "木",
            "規劃": "木",
            "功能": "木",
            "實作": "火",
            "開發": "火",
            "程式": "火",
            "架構": "土",
            "設計": "土",
            "穩定": "土",
            "優化": "金",
            "效能": "金",
            "重構": "金",
            "測試": "水",
            "錯誤": "水",
            "bug": "水"
        }
        
        # 根據關鍵詞判斷
        for keyword, element in suggestions.items():
            if keyword in context.lower():
                role = self.roles[element]
                return {
                    "suggested_element": element,
                    "reason": f"偵測到「{keyword}」相關需求",
                    "role_name": role.name,
                    "emoji": role.emoji
                }
        
        # 預設建議
        return {
            "suggested_element": "木",
            "reason": "開始新任務，建議從需求分析開始",
            "role_name": self.roles["木"].name,
            "emoji": self.roles["木"].emoji
        }
    
    def observe_interaction(self, from_element: str, to_element: str, 
                          message_type: str, content: str):
        """無極觀察元素間的互動"""
        observation = {
            "timestamp": datetime.now(),
            "from": from_element,
            "to": to_element,
            "type": message_type,
            "summary": content[:100] + "..." if len(content) > 100 else content
        }
        
        self.wuji_observations.append(observation)
        
        # 分析互動模式
        if self._is_stuck_pattern():
            return self._generate_intervention()
        
        return None
    
    def _is_stuck_pattern(self) -> bool:
        """檢測是否陷入困境模式"""
        if len(self.wuji_observations) < 5:
            return False
        
        # 檢查最近5次互動
        recent = self.wuji_observations[-5:]
        
        # 如果都是同類型的互動，可能陷入循環
        types = [obs["type"] for obs in recent]
        if len(set(types)) == 1 and types[0] in ["error", "bug_report"]:
            return True
        
        # 如果在同兩個角色間反覆互動
        participants = [(obs["from"], obs["to"]) for obs in recent]
        if len(set(participants)) == 1:
            return True
        
        return False
    
    def _generate_intervention(self) -> str:
        """無極介入，提供指引"""
        recent_pattern = self.wuji_observations[-5:]
        
        # 分析模式
        if all(obs["type"] in ["error", "bug_report"] for obs in recent_pattern):
            return f"""
{self.wuji.emoji} 無極觀察：
我感知到循環的漩渦正在形成。火與水的互動陷入了重複。

建議：
1. 暫停當前思路，讓土（架構師）審視整體設計
2. 或許問題不在細節，而在根基
3. 「退一步，海闊天空」- 重新審視需求本質

記住：當水無法撲滅火時，或許需要土來吸納過多的能量。
"""
        
        return f"""
{self.wuji.emoji} 無極觀察：
系統運作出現異常模式。建議引入新的視角打破當前循環。
"""
    
    def get_harmony_status(self) -> str:
        """獲取系統和諧狀態"""
        if not self.interaction_history:
            return f"{self.wuji.emoji} 系統初始化完成，五行待命。"
        
        # 統計各元素活動
        element_activity = {}
        for interaction in self.interaction_history[-20:]:  # 看最近20次
            if interaction.get("role"):
                element = interaction["role"]
                element_activity[element] = element_activity.get(element, 0) + 1
        
        # 生成狀態報告
        status = f"{self.wuji.emoji} 系統和諧度報告\n\n"
        
        for element, role in self.roles.items():
            activity = element_activity.get(element, 0)
            bar = "█" * activity + "░" * (10 - min(activity, 10))
            status += f"{role.emoji} {element} {bar} {activity}次\n"
        
        # 簡單的平衡判斷
        if len(element_activity) < 2:
            status += "\n💭 洞察：系統剛啟動，元素尚未充分互動。"
        elif max(element_activity.values()) > sum(element_activity.values()) * 0.5:
            dominant = max(element_activity, key=element_activity.get)
            status += f"\n💭 洞察：{dominant}屬性過於活躍，建議平衡能量分配。"
        else:
            status += "\n💭 洞察：五行運轉和諧，系統平衡良好。"
        
        return status
    
    def suggest_next_role(self, current_element: str, task_type: str) -> Dict[str, str]:
        """根據當前角色和任務類型，建議下一個角色"""
        # 相生關係
        generating_cycle = {
            "木": "火",  # 木生火
            "火": "土",  # 火生土  
            "土": "金",  # 土生金
            "金": "水",  # 金生水
            "水": "木"   # 水生木
        }
        
        # 相剋關係
        controlling_cycle = {
            "木": "土",  # 木剋土
            "火": "金",  # 火剋金
            "土": "水",  # 土剋水
            "金": "木",  # 金剋木
            "水": "火"   # 水剋火
        }
        
        # 根據任務類型決定使用相生還是相剋
        if task_type == "continue":  # 延續發展
            next_element = generating_cycle.get(current_element, "木")
            relation = "相生"
        elif task_type == "fix":  # 修正問題
            next_element = controlling_cycle.get(current_element, "水")
            relation = "相剋"
        else:  # 其他情況，無極建議
            return {
                "next_element": "無極",
                "reason": "情況不明，需要無極觀察分析",
                "relation": "超然"
            }
        
        next_role = self.roles[next_element]
        return {
            "next_element": next_element,
            "next_role": next_role.name,
            "emoji": next_role.emoji,
            "reason": f"{current_element}{relation}{next_element}，適合{next_role.strengths[0]}",
            "relation": relation
        }
    
    def update_metrics(self, element: str, success: bool, response_time: float = 0):
        """更新系統指標"""
        self.system_metrics["total_interactions"] += 1
        
        # 更新元素健康狀態
        if element in self.element_health:
            health = self.element_health[element]
            health["load"] += 1
            
            if not success:
                health["errors"] += 1
                health["health"] = max(0, health["health"] - 10)
                self.system_metrics["error_count"] += 1
            else:
                # 成功時緩慢恢復健康度
                health["health"] = min(100, health["health"] + 2)
            
            # 更新狀態燈號
            if health["health"] >= 80:
                health["status"] = "🟢"  # 綠燈：健康
            elif health["health"] >= 50:
                health["status"] = "🟡"  # 黃燈：警告
            else:
                health["status"] = "🔴"  # 紅燈：危險
        
        # 更新成功率
        if self.system_metrics["total_interactions"] > 0:
            success_count = self.system_metrics["total_interactions"] - self.system_metrics["error_count"]
            self.system_metrics["success_rate"] = (success_count / self.system_metrics["total_interactions"]) * 100
        
        # 更新平均響應時間
        if response_time > 0:
            total_time = self.system_metrics["average_response_time"] * (self.system_metrics["total_interactions"] - 1)
            self.system_metrics["average_response_time"] = (total_time + response_time) / self.system_metrics["total_interactions"]
    
    def record_flow(self, from_element: str, to_element: str, action: str):
        """記錄互動流程"""
        flow_record = {
            "timestamp": datetime.now(),
            "from": from_element,
            "to": to_element,
            "action": action
        }
        self.interaction_flows.append(flow_record)
    
    def get_dashboard(self) -> str:
        """生成無極 Dashboard（純文字版）"""
        dashboard = f"""
╔════════════════════════════════════════════════════════════════╗
║                    ⚪ 無極系統監控儀表板 ⚪                     ║
╚════════════════════════════════════════════════════════════════╝

【系統總覽】
┌─────────────────────────────────────────────────────────────┐
│ 🕐 運行時間: {self._format_uptime()}
│ 📊 總互動數: {self.system_metrics['total_interactions']:,}
│ ✅ 成功率: {self.system_metrics['success_rate']:.1f}%
│ ⏱️  平均響應: {self.system_metrics['average_response_time']:.2f}s
│ ❌ 錯誤次數: {self.system_metrics['error_count']}
└─────────────────────────────────────────────────────────────┘

【五行節點健康狀態】
"""
        
        # 添加各元素健康狀態
        for element, health in self.element_health.items():
            role = self.roles[element]
            health_bar = self._create_health_bar(health["health"])
            dashboard += f"""
{health['status']} {role.emoji} {element} - {role.name}
   健康度: {health_bar} {health['health']}%
   負載量: {'▮' * min(health['load'], 10)}{'▯' * (10 - min(health['load'], 10))} ({health['load']}次)
   錯誤數: {health['errors']}
"""
        
        # 功能完整性
        dashboard += """
【功能完整性】
┌─────────────────────────────────────────────────────────────┐
"""
        for feature, completion in self.feature_completion.items():
            progress_bar = self._create_progress_bar(completion)
            dashboard += f"│ {feature:<10} {progress_bar} {completion:>3}% │\n"
        dashboard += "└─────────────────────────────────────────────────────────────┘\n"
        
        # 最近互動流程圖
        dashboard += self._generate_flow_diagram()
        
        # 智慧分析
        dashboard += self._generate_insights()
        
        return dashboard
    
    def _format_uptime(self) -> str:
        """格式化運行時間"""
        uptime = datetime.now() - self.system_metrics["start_time"]
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def _create_health_bar(self, health: int) -> str:
        """創建健康度條"""
        filled = int(health / 10)
        return "▰" * filled + "▱" * (10 - filled)
    
    def _create_progress_bar(self, progress: int) -> str:
        """創建進度條"""
        filled = int(progress / 10)
        return "█" * filled + "░" * (10 - filled)
    
    def _generate_flow_diagram(self) -> str:
        """生成簡化的流程圖"""
        if not self.interaction_flows:
            return "\n【互動流程】\n暫無互動記錄\n"
        
        diagram = "\n【最近互動流程】\n"
        
        # 顯示最近5筆互動
        recent_flows = list(self.interaction_flows)[-5:]
        for i, flow in enumerate(recent_flows):
            if i == 0:
                diagram += f"┌─ {flow['from']} "
            else:
                diagram += f"├─ {flow['from']} "
            
            diagram += f"─({flow['action']})→ {flow['to']}\n"
        
        diagram += "└────────────────────────────────\n"
        
        return diagram
    
    def _generate_insights(self) -> str:
        """生成智慧洞察"""
        insights = "\n【無極洞察】\n"
        
        # 分析健康狀況
        unhealthy_elements = [e for e, h in self.element_health.items() if h["health"] < 80]
        if unhealthy_elements:
            insights += f"⚠️  警告：{', '.join(unhealthy_elements)}元素健康度偏低，需要關注\n"
        
        # 分析負載平衡
        loads = [h["load"] for h in self.element_health.values()]
        if max(loads) > sum(loads) * 0.4:
            overloaded = max(self.element_health.items(), key=lambda x: x[1]["load"])[0]
            insights += f"📊 建議：{overloaded}元素負載過重，考慮分散任務\n"
        
        # 分析錯誤模式
        total_errors = sum(h["errors"] for h in self.element_health.values())
        if total_errors > 5:
            insights += f"🔍 觀察：系統錯誤數偏高（{total_errors}），建議檢查相剋關係是否過強\n"
        
        # 功能建議
        incomplete_features = [f for f, c in self.feature_completion.items() if c < 80]
        if incomplete_features:
            insights += f"🎯 待完善：{', '.join(incomplete_features)}功能需要進一步開發\n"
        
        if not unhealthy_elements and not incomplete_features and total_errors < 3:
            insights += "✨ 系統運行良好，五行平衡，萬物和諧\n"
        
        return insights
    
    def get_mini_dashboard(self) -> str:
        """生成迷你儀表板（適合頻繁查看）"""
        # 計算整體健康度
        overall_health = sum(h["health"] for h in self.element_health.values()) / 5
        
        # 決定整體狀態
        if overall_health >= 80:
            overall_status = "🟢"
        elif overall_health >= 50:
            overall_status = "🟡"
        else:
            overall_status = "🔴"
        
        mini = f"{overall_status} 系統狀態 | "
        mini += f"成功率:{self.system_metrics['success_rate']:.0f}% | "
        
        # 顯示各元素狀態
        for element, health in self.element_health.items():
            mini += f"{health['status']}{self.roles[element].emoji}"
        
        return mini
    
    def add_prompt_to_memory(self, element: str, prompt_name: str, prompt: str, context: str = "") -> bool:
        """將提示詞加入元素的記憶庫"""
        if element not in self.prompt_memory:
            return False
        
        self.prompt_memory[element][prompt_name] = {
            "prompt": prompt,
            "context": context,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0,
            "effectiveness_scores": []
        }
        
        logger.info(f"{element}元素新增提示詞：{prompt_name}")
        return True
    
    def use_prompt_from_memory(self, element: str, prompt_name: str, variables: Dict[str, str] = {}) -> Optional[str]:
        """從記憶庫使用提示詞"""
        if element not in self.prompt_memory or prompt_name not in self.prompt_memory[element]:
            # 嘗試從角色的預設提示詞庫中查找
            role = self.roles.get(element, self.wuji) if element != "無極" else self.wuji
            if hasattr(role, 'prompt_library') and role.prompt_library and prompt_name in role.prompt_library:
                prompt_template = role.prompt_library[prompt_name]
            else:
                return None
        else:
            prompt_template = self.prompt_memory[element][prompt_name]["prompt"]
            # 更新使用統計
            self.prompt_memory[element][prompt_name]["usage_count"] += 1
        
        # 替換變數
        prompt = prompt_template
        for var, value in variables.items():
            prompt = prompt.replace(f"{{{var}}}", value)
        
        # 記錄使用
        self.prompt_stats[f"{element}_{prompt_name}"]["usage_count"] += 1
        self.prompt_stats[f"{element}_{prompt_name}"]["last_used"] = datetime.now()
        
        return prompt
    
    def rate_prompt_effectiveness(self, element: str, prompt_name: str, score: float) -> None:
        """評分提示詞的效果"""
        if element in self.prompt_memory and prompt_name in self.prompt_memory[element]:
            self.prompt_memory[element][prompt_name]["effectiveness_scores"].append({
                "score": score,
                "rated_at": datetime.now().isoformat()
            })
            
            # 更新平均效果分數
            scores = [s["score"] for s in self.prompt_memory[element][prompt_name]["effectiveness_scores"]]
            avg_score = sum(scores) / len(scores)
            self.prompt_stats[f"{element}_{prompt_name}"]["avg_effectiveness"] = avg_score
    
    def get_element_best_prompts(self, element: str, top_n: int = 5) -> List[Dict]:
        """獲取元素最有效的提示詞"""
        element_prompts = []
        
        # 從記憶庫收集
        if element in self.prompt_memory:
            for name, data in self.prompt_memory[element].items():
                if data["effectiveness_scores"]:
                    avg_score = sum(s["score"] for s in data["effectiveness_scores"]) / len(data["effectiveness_scores"])
                    element_prompts.append({
                        "name": name,
                        "prompt": data["prompt"],
                        "avg_score": avg_score,
                        "usage_count": data["usage_count"]
                    })
        
        # 按效果排序
        element_prompts.sort(key=lambda x: x["avg_score"], reverse=True)
        return element_prompts[:top_n]
    
    def share_prompt_between_elements(self, from_element: str, to_element: str, prompt_name: str) -> bool:
        """在元素間分享提示詞"""
        if from_element not in self.prompt_memory or prompt_name not in self.prompt_memory[from_element]:
            return False
        
        prompt_data = self.prompt_memory[from_element][prompt_name].copy()
        prompt_data["shared_from"] = from_element
        prompt_data["shared_at"] = datetime.now().isoformat()
        
        self.prompt_memory[to_element][f"{prompt_name}_from_{from_element}"] = prompt_data
        
        logger.info(f"{from_element}向{to_element}分享了提示詞：{prompt_name}")
        return True