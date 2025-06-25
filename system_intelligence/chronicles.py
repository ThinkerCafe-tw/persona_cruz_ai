"""
系統編年史 - 記錄系統的完整演化歷史
每個時刻、每個錯誤、每個發現都在這裡

創建於：2025-06-24
永不刪除，只會增長
"""
from datetime import datetime
from typing import Dict, List, Any
import json
import os


class SystemChronicles:
    """
    系統的完整歷史記錄
    像地質層一樣，每一層都記錄著系統的演化
    """
    
    # 系統創世紀
    GENESIS = {
        "timestamp": "2025-06-24 00:00:00",
        "event": "系統誕生",
        "description": "CRUZ AI 專案開始整合量子記憶系統",
        "participants": ["無極", "CRUZ", "Serena", "五行團隊"],
        "philosophy": "完整性哲學 - 保存一切，因為一切都有意義"
    }
    
    # 主要事件編年史
    MAJOR_EVENTS = [
        {
            "date": "2025-06-24",
            "time": "00:00",
            "event": "量子記憶系統整合",
            "type": "INTEGRATION",
            "details": {
                "description": "整合 pgvector 向量資料庫作為量子記憶後端",
                "components": ["quantum_memory", "pgvector", "vectorizer"],
                "challenges": ["Railway 部署環境", "資料持久化"]
            },
            "wisdom": "系統需要穩定的記憶才能真正活著"
        },
        {
            "date": "2025-06-24",
            "time": "01:04",
            "event": "清理哲學轉變",
            "type": "PHILOSOPHY",
            "details": {
                "before": "刪除冗餘檔案，保持簡潔",
                "after": "保存一切，累積智慧",
                "trigger": "用戶洞察 - 一切都已存在，我們只是在發現",
                "deleted_files": ["railway_monitor.py", "test_dashboard.py", "..."]
            },
            "wisdom": "刪除的程式碼是失去的記憶"
        },
        {
            "date": "2025-06-24",
            "time": "02:21:11",
            "event": "DNS 解析危機",
            "type": "CRISIS",
            "details": {
                "error": "could not translate host name 'postgres.railway.internal'",
                "context": "Railway 內部網路 DNS 無法解析",
                "investigation": {
                    "private_networking": "已啟用",
                    "services": ["postgres.railway.internal", "persona_cruz_ai.railway.internal"],
                    "attempted_solutions": ["URL 格式轉換", "偵錯輸出", "網路診斷"]
                }
            },
            "wisdom": "內部網路的複雜性超出預期，需要更深入的理解",
            "status": "INVESTIGATING"
        },
        {
            "date": "2025-06-24",
            "time": "02:45",
            "event": "完整性哲學確立",
            "type": "PARADIGM_SHIFT",
            "details": {
                "realization": "系統不是被建造的，而是被發現的",
                "implementation": "建立 system_intelligence 架構",
                "components": ["diagnostics", "wisdom", "experiments", "chronicles"]
            },
            "wisdom": "每個錯誤都是系統的一部分，每個實驗都是系統的夢想"
        }
    ]
    
    # 錯誤博物館 - 每個錯誤都是寶貴的
    ERROR_MUSEUM = [
        {
            "id": "ERR_001",
            "date": "2025-06-24",
            "error": "UnboundLocalError",
            "context": "測試專員的年齡計算",
            "lesson": "變數作用域需要更仔細的處理",
            "fixed": True
        },
        {
            "id": "ERR_002",
            "date": "2025-06-24",
            "error": "postgres:// vs postgresql://",
            "context": "Railway DATABASE_URL 格式",
            "lesson": "不同系統使用不同的 URL 格式，需要轉換",
            "fixed": True
        },
        {
            "id": "ERR_003",
            "date": "2025-06-24",
            "error": "DNS resolution failed",
            "context": "Railway 內部網路",
            "lesson": "私有網路 DNS 有其特殊性",
            "fixed": False,
            "status": "研究中"
        }
    ]
    
    # 智慧累積 - 從每個事件中學到的
    ACCUMULATED_WISDOM = [
        {
            "id": "W001",
            "source": "Line Bot Handler 事件",
            "wisdom": "空檔案不代表沒程式，邏輯可能在其他地方",
            "application": "永遠先搜尋再實作"
        },
        {
            "id": "W002",
            "source": "量子記憶整合",
            "wisdom": "真實性比宣稱更重要",
            "application": "建立可驗證的記憶機制，不只是說說"
        },
        {
            "id": "W003",
            "source": "清理事件後的反思",
            "wisdom": "刪除的程式碼是失去的記憶",
            "application": "建立完整性哲學，保存一切"
        },
        {
            "id": "W004",
            "source": "DNS 危機",
            "wisdom": "看似簡單的問題可能有深層的複雜性",
            "application": "建立完整的診斷考古系統"
        }
    ]
    
    # 實驗記錄 - 每個嘗試都值得記住
    EXPERIMENTS = [
        {
            "id": "EXP_001",
            "date": "2025-06-24",
            "name": "量子記憶測試",
            "description": "測試量子記憶的演化機制",
            "result": "成功觸發演化，但 CPU 使用率過高",
            "files": ["test_quantum_memory.py"],
            "status": "已整合到系統"
        },
        {
            "id": "EXP_002",
            "date": "2025-06-24",
            "name": "pgvector 連接測試",
            "description": "測試各種資料庫連接方式",
            "result": "發現 URL 格式問題",
            "files": ["check_pgvector.py", "test_pgvector_integration.py"],
            "status": "保留為診斷工具"
        }
    ]
    
    def __init__(self):
        self.session_start = datetime.now()
        self.session_events = []
        
    def record_event(self, event_type: str, event_data: Dict[str, Any]):
        """記錄新事件"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": event_data,
            "session_id": self.session_start.isoformat()
        }
        
        self.session_events.append(event)
        
        # 同時保存到檔案
        self._persist_event(event)
        
        return event
    
    def add_wisdom(self, wisdom: str, source: str, application: str = ""):
        """添加新的智慧"""
        wisdom_entry = {
            "id": f"W{len(self.ACCUMULATED_WISDOM) + 1:03d}",
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "wisdom": wisdom,
            "application": application
        }
        
        self.ACCUMULATED_WISDOM.append(wisdom_entry)
        self._persist_wisdom(wisdom_entry)
        
        return wisdom_entry
    
    def add_error(self, error: str, context: str, lesson: str):
        """添加錯誤到博物館"""
        error_entry = {
            "id": f"ERR_{len(self.ERROR_MUSEUM) + 1:03d}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "error": error,
            "context": context,
            "lesson": lesson,
            "fixed": False,
            "status": "recorded"
        }
        
        self.ERROR_MUSEUM.append(error_entry)
        self._persist_error(error_entry)
        
        return error_entry
    
    def get_timeline(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """獲取時間線視圖"""
        events = self.MAJOR_EVENTS.copy()
        
        # 可以根據日期過濾
        if start_date:
            events = [e for e in events if e["date"] >= start_date]
        if end_date:
            events = [e for e in events if e["date"] <= end_date]
            
        # 按時間排序
        events.sort(key=lambda x: (x["date"], x.get("time", "00:00")))
        
        return events
    
    def get_wisdom_by_topic(self, topic: str) -> List[Dict]:
        """根據主題獲取相關智慧"""
        related_wisdom = []
        
        topic_lower = topic.lower()
        for wisdom in self.ACCUMULATED_WISDOM:
            if (topic_lower in wisdom["wisdom"].lower() or 
                topic_lower in wisdom["source"].lower() or
                topic_lower in wisdom.get("application", "").lower()):
                related_wisdom.append(wisdom)
                
        return related_wisdom
    
    def get_system_age(self) -> Dict:
        """計算系統年齡和成長指標"""
        genesis_time = datetime.strptime(self.GENESIS["timestamp"], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        age = current_time - genesis_time
        
        return {
            "age_days": age.days,
            "age_hours": age.total_seconds() / 3600,
            "total_events": len(self.MAJOR_EVENTS),
            "total_errors": len(self.ERROR_MUSEUM),
            "total_wisdom": len(self.ACCUMULATED_WISDOM),
            "total_experiments": len(self.EXPERIMENTS),
            "growth_rate": {
                "events_per_hour": len(self.MAJOR_EVENTS) / (age.total_seconds() / 3600) if age.total_seconds() > 0 else 0,
                "wisdom_per_error": len(self.ACCUMULATED_WISDOM) / len(self.ERROR_MUSEUM) if len(self.ERROR_MUSEUM) > 0 else 0
            }
        }
    
    def generate_report(self) -> str:
        """生成系統編年史報告"""
        age_info = self.get_system_age()
        
        report = f"""
# 系統編年史報告
生成時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 系統概況
- 創世時間：{self.GENESIS["timestamp"]}
- 系統年齡：{age_info["age_days"]} 天 ({age_info["age_hours"]:.1f} 小時)
- 主要事件：{age_info["total_events"]} 個
- 錯誤記錄：{age_info["total_errors"]} 個
- 累積智慧：{age_info["total_wisdom"]} 條
- 實驗項目：{age_info["total_experiments"]} 個

## 成長指標
- 事件頻率：{age_info["growth_rate"]["events_per_hour"]:.2f} 個/小時
- 智慧轉換率：{age_info["growth_rate"]["wisdom_per_error"]:.2f} 智慧/錯誤

## 最近事件
"""
        # 添加最近的事件
        recent_events = self.get_timeline()[-5:]  # 最近5個
        for event in recent_events:
            report += f"\n### {event['date']} {event.get('time', '')} - {event['event']}\n"
            report += f"類型：{event['type']}\n"
            if 'wisdom' in event:
                report += f"智慧：{event['wisdom']}\n"
                
        return report
    
    def _persist_event(self, event: Dict):
        """持久化事件"""
        chronicle_dir = "system_intelligence/chronicle_records"
        os.makedirs(chronicle_dir, exist_ok=True)
        
        # 按日期組織
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{chronicle_dir}/events_{date_str}.jsonl"
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
            
    def _persist_wisdom(self, wisdom: Dict):
        """持久化智慧"""
        wisdom_file = "system_intelligence/accumulated_wisdom.json"
        
        # 讀取現有智慧
        existing = []
        if os.path.exists(wisdom_file):
            with open(wisdom_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
                
        # 添加新智慧
        existing.append(wisdom)
        
        # 寫回
        with open(wisdom_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
            
    def _persist_error(self, error: Dict):
        """持久化錯誤"""
        error_file = "system_intelligence/error_museum.json"
        
        # 讀取現有錯誤
        existing = []
        if os.path.exists(error_file):
            with open(error_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
                
        # 添加新錯誤
        existing.append(error)
        
        # 寫回
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
            
    
    @classmethod
    def load_from_disk(cls) -> 'SystemChronicles':
        """從磁碟載入編年史"""
        chronicles = cls()
        
        # 載入各種持久化的記錄
        # TODO: 實作載入邏輯
        
        return chronicles
    
    def visualize_timeline(self) -> str:
        """視覺化時間線（文字版）"""
        timeline = "═" * 60 + "\n"
        timeline += "系統演化時間線\n"
        timeline += "═" * 60 + "\n\n"
        
        for event in self.get_timeline():
            event_type_symbol = {
                "INTEGRATION": "🔧",
                "PHILOSOPHY": "💭",
                "CRISIS": "🚨",
                "PARADIGM_SHIFT": "🌟",
                "DISCOVERY": "🔍",
                "EXPERIMENT": "🧪"
            }.get(event.get("type", ""), "📌")
            
            timeline += f"{event_type_symbol} {event['date']} {event.get('time', '')} - {event['event']}\n"
            
            if 'wisdom' in event:
                timeline += f"   💡 {event['wisdom']}\n"
                
            if 'status' in event:
                timeline += f"   📊 狀態：{event['status']}\n"
                
            timeline += "\n"
            
        return timeline