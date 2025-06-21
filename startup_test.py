import os
import sys
import time
import logging
from datetime import datetime
import google.generativeai as genai
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
import json
import subprocess

logger = logging.getLogger(__name__)

class TestAgent:
    """測試專員 - 記憶和守護測試
    
    我是一位負責任，且充滿好奇充滿積極性正面的上進資深測試專員。
    我會仔細觀察測試過程的 Log 和 Exception，分析錯誤堆疊，
    並從中學習和反思，為未來的測試留下有價值的洞察。
    
    擁有權限：
    - 讀取整個專案的所有原始碼
    - 分析程式碼結構和依賴關係
    - 追蹤錯誤的根源
    - 提供改進建議
    """
    
    def __init__(self):
        # 在 Railway 環境使用環境變數存儲記憶
        self.is_railway = os.getenv('RAILWAY_ENVIRONMENT') is not None
        self.memory_file = "/tmp/test_memory.json" if not self.is_railway else None
        self.memory = self._load_memory()
        self.personality = "🧪 資深測試專員"
        self.project_root = os.path.dirname(os.path.abspath(__file__))  # 專案根目錄
        self.age = self._calculate_age()  # 計算測試專員年齡
    
    def _load_memory(self):
        """載入測試記憶"""
        if self.is_railway:
            # 在 Railway 環境，使用預設記憶並加入 Git 歷史
            memory = self._get_default_memory()
            memory["deployment_note"] = "Railway 環境每次部署都是新容器"
            
            # 嘗試讀取最近的 git log
            try:
                result = subprocess.run(
                    ['git', 'log', '--oneline', '-10'],
                    capture_output=True, text=True, cwd=self.project_root
                )
                if result.returncode == 0 and result.stdout.strip():
                    commits = result.stdout.strip().split('\n')
                    memory["git_commits"] = [
                        {"commit": c.split(' ', 1)[0], "message": c.split(' ', 1)[1] if ' ' in c else c}
                        for c in commits if c
                    ]
                    memory["last_known_commit"] = commits[0] if commits else "unknown"
                else:
                    # Git 不可用，使用 Railway 環境資訊
                    memory["railway_deployment"] = {
                        "instance_id": os.getenv('RAILWAY_DEPLOYMENT_ID', 'unknown'),
                        "environment": os.getenv('RAILWAY_ENVIRONMENT', 'production'),
                        "replica_id": os.getenv('RAILWAY_REPLICA_ID', 'unknown'),
                        "deployment_time": datetime.now().isoformat()
                    }
                    logger.info(f"Railway 環境檢測：無 git，使用部署 ID {memory['railway_deployment']['instance_id']}")
            except Exception as e:
                logger.warning(f"無法讀取 git log: {str(e)}")
                # 記錄 Railway 基本資訊
                memory["railway_deployment"] = {
                    "error": str(e),
                    "deployment_time": datetime.now().isoformat()
                }
                
            return memory
        else:
            # 本地環境使用檔案系統
            try:
                if self.memory_file and os.path.exists(self.memory_file):
                    with open(self.memory_file, 'r') as f:
                        return json.load(f)
            except:
                pass
        
        return self._get_default_memory()
    
    def _get_default_memory(self):
        """取得預設記憶結構"""
        return {
            "test_history": [],
            "patterns": {},
            "reflections": [],  # 反思記錄
            "wisdom": [],  # 累積的智慧
            "code_analysis": [],  # 程式碼分析記錄
            "git_commits": [],  # Git commit 歷史
            "created_at": datetime.now().isoformat(),
            "birth_date": "2024-06-21",  # 測試專員誕生日
            "experience_points": 0,  # 經驗值
            "age_milestones": []  # 年齡里程碑
        }
    
    def remember_test(self, test_name, success, duration, error=None):
        """記住測試結果並進行反思"""
        record = {
            "test": test_name,
            "success": success,
            "duration": duration,
            "time": datetime.now().isoformat(),
            "error": str(error) if error else None
        }
        self.memory["test_history"].append(record)
        
        # 只保留最近 100 筆記錄
        if len(self.memory["test_history"]) > 100:
            self.memory["test_history"] = self.memory["test_history"][-100:]
        
        # 進行反思
        self._reflect_on_test(test_name, success, duration, error)
        
        # 獲得經驗值
        if success:
            self.gain_experience(1, f"成功完成 {test_name} 測試")
        else:
            self.gain_experience(3, f"從 {test_name} 的錯誤中學習")
        
        # 如果有錯誤，進行程式碼分析
        if error and not success:
            analysis = self.analyze_error_context(error, test_name)
            if analysis.get("code_context"):
                self.memory["code_analysis"].append(analysis)
                # 只保留最近 20 個分析
                if len(self.memory["code_analysis"]) > 20:
                    self.memory["code_analysis"] = self.memory["code_analysis"][-20:]
                self.gain_experience(2, "深入分析錯誤根源")
        
        self._save_memory()
    
    def _reflect_on_test(self, test_name, success, duration, error):
        """反思測試結果"""
        # 取得上次的反思
        last_reflection = self.memory["reflections"][-1] if self.memory["reflections"] else None
        
        reflection = {
            "time": datetime.now().isoformat(),
            "test": test_name,
            "success": success
        }
        
        if error:
            # 分析錯誤模式
            if "TypeError" in str(error):
                reflection["insight"] = "發現 TypeError！這通常意味著資料類型不匹配。要特別注意 API 回應的結構。"
                reflection["advice"] = "下次測試前先驗證資料類型，特別是 Content 物件的處理。"
                # 2024-06-21 更新：已修復 Content 物件混合問題，改用 dict 格式傳遞訊息
                if "Content" in str(error) and "Blob" in str(error):
                    reflection["fix_applied"] = "已修復：使用 dict 格式而非混合 Content 物件"
            elif "function_call" in str(error).lower():
                reflection["insight"] = "Function Calling 相關錯誤！這是系統的核心功能，需要特別關注。"
                reflection["advice"] = "建議增加 Function Calling 的 mock 測試，確保各種情境都能處理。"
            else:
                reflection["insight"] = f"遇到新類型的錯誤：{type(error).__name__}。這是學習的好機會！"
                reflection["advice"] = "記錄這個錯誤模式，未來可能會再次遇到。"
        else:
            reflection["insight"] = f"{test_name} 測試通過！耗時 {duration:.2f} 秒，表現穩定。"
            reflection["advice"] = "保持這個良好狀態，但也要準備應對可能的邊界情況。"
        
        # 如果有上次的反思，進行對比
        if last_reflection and last_reflection.get("test") == test_name:
            if last_reflection.get("success") != success:
                reflection["progress"] = "狀態發生變化！" + ("從失敗到成功，太棒了！🎉" if success else "從成功到失敗，需要關注！⚠️")
        
        self.memory["reflections"].append(reflection)
        
        # 累積智慧
        if len(self.memory["test_history"]) % 10 == 0:  # 每 10 次測試總結一次
            self._accumulate_wisdom()
    
    def read_source_file(self, filename):
        """讀取專案原始碼檔案"""
        try:
            filepath = os.path.join(self.project_root, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logger.warning(f"測試專員無法讀取檔案 {filename}: {str(e)}")
        return None
    
    def analyze_error_context(self, error, test_name):
        """深入分析錯誤的上下文"""
        analysis = {
            "error_type": type(error).__name__ if error else "Unknown",
            "test_name": test_name,
            "timestamp": datetime.now().isoformat()
        }
        
        # 如果是 Function Calling 相關錯誤，讀取 gemini_service.py
        if error and ("function" in str(error).lower() or "Content" in str(error)):
            source = self.read_source_file("gemini_service.py")
            if source:
                # 尋找相關程式碼段落
                lines = source.split('\n')
                for i, line in enumerate(lines):
                    if "generate_content" in line and i > 5:
                        analysis["code_context"] = "\n".join(lines[i-5:i+5])
                        analysis["line_number"] = i + 1
                        break
        
        return analysis
    
    def _accumulate_wisdom(self):
        """累積測試智慧"""
        recent_tests = self.memory["test_history"][-10:]
        success_rate = sum(1 for t in recent_tests if t["success"]) / len(recent_tests) * 100
        
        wisdom = {
            "time": datetime.now().isoformat(),
            "success_rate": success_rate,
            "insight": f"最近 10 次測試成功率：{success_rate:.1f}%"
        }
        
        # 分析常見錯誤
        errors = [t["error"] for t in recent_tests if t["error"]]
        if errors:
            error_types = {}
            for error in errors:
                error_type = error.split(":")[0] if ":" in error else "Unknown"
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            most_common = max(error_types.items(), key=lambda x: x[1])
            wisdom["pattern"] = f"最常見的錯誤類型是 {most_common[0]}（出現 {most_common[1]} 次）"
            wisdom["recommendation"] = "建議針對這個錯誤類型加強防禦性編程。"
            
            # 如果有程式碼分析記錄，加入智慧中
            if "code_analysis" in self.memory:
                wisdom["code_insights"] = f"已分析 {len(self.memory.get('code_analysis', []))} 個程式碼片段"
        
        self.memory["wisdom"].append(wisdom)
        
        # 只保留最近 10 條智慧
        if len(self.memory["wisdom"]) > 10:
            self.memory["wisdom"] = self.memory["wisdom"][-10:]
    
    def record_development_insight(self, event_type, insight, lesson_learned=None):
        """記錄開發過程中的洞察和學習"""
        development_record = {
            "time": datetime.now().isoformat(),
            "event_type": event_type,  # 如：bug_fix, feature_add, error_analysis
            "insight": insight,
            "lesson_learned": lesson_learned,
            "git_context": self.memory.get("git_commits", [])[:1]  # 記錄當前 commit
        }
        
        # 確保有 development_insights 區塊
        if "development_insights" not in self.memory:
            self.memory["development_insights"] = []
        
        self.memory["development_insights"].append(development_record)
        
        # 只保留最近 50 個開發洞察
        if len(self.memory["development_insights"]) > 50:
            self.memory["development_insights"] = self.memory["development_insights"][-50:]
        
        self._save_memory()
        logger.info(f"測試專員記錄開發洞察: {event_type} - {insight[:50]}...")
    
    def _save_memory(self):
        """儲存測試記憶"""
        if self.is_railway:
            # Railway 環境無法持久化，只能記錄在日誌中
            logger.info(f"測試專員記憶摘要: {len(self.memory['test_history'])} 個測試記錄")
            if self.memory.get('git_commits'):
                logger.info(f"最新 commit: {self.memory['git_commits'][0]['message']}")
        else:
            # 本地環境存檔
            try:
                if self.memory_file:
                    with open(self.memory_file, 'w') as f:
                        json.dump(self.memory, f, indent=2)
            except:
                pass
    
    def _calculate_age(self):
        """計算測試專員的年齡（基於經驗）"""
        # 基礎年齡：18歲（年輕衝動）
        base_age = 18
        
        # 根據經驗計算年齡
        exp_points = self.memory.get("experience_points", 0)
        test_count = len(self.memory.get("test_history", []))
        error_count = len([t for t in self.memory.get("test_history", []) if not t.get("success", True)])
        wisdom_count = len(self.memory.get("wisdom", []))
        
        # 經驗值計算（每個成功測試+1，每個錯誤學習+2，每個智慧+5）
        total_exp = exp_points + test_count + (error_count * 2) + (wisdom_count * 5)
        
        # 年齡成長曲線（每20點經驗增加1歲，最高40歲）
        age_growth = min(total_exp // 20, 22)  # 最多增長22歲（18+22=40）
        current_age = base_age + age_growth
        
        # 記錄年齡變化
        self._update_age_milestone(current_age)
        
        return current_age
    
    def _update_age_milestone(self, new_age):
        """更新年齡里程碑"""
        milestones = self.memory.get("age_milestones", [])
        
        # 檢查是否達到新的年齡階段
        age_stages = {
            18: "年輕衝動期 - 充滿熱情但容易犯錯",
            25: "成長學習期 - 開始累積經驗",
            30: "成熟懂事期 - 理解責任的重要",
            35: "經驗豐富期 - 能預見並避免問題",
            40: "穩定成熟期 - 智慧與經驗的結晶"
        }
        
        for age, description in age_stages.items():
            if new_age >= age and not any(m["age"] == age for m in milestones):
                milestone = {
                    "age": age,
                    "reached_at": datetime.now().isoformat(),
                    "description": description,
                    "total_tests": len(self.memory.get("test_history", [])),
                    "wisdom_count": len(self.memory.get("wisdom", []))
                }
                milestones.append(milestone)
                logger.info(f"🎉 測試專員達到 {age} 歲！{description}")
                
        self.memory["age_milestones"] = milestones
    
    def gain_experience(self, points, reason):
        """獲得經驗值"""
        self.memory["experience_points"] = self.memory.get("experience_points", 0) + points
        logger.info(f"測試專員獲得 {points} 點經驗：{reason}")
        
        # 重新計算年齡
        old_age = self.age
        self.age = self._calculate_age()
        
        if self.age > old_age:
            logger.info(f"🎂 測試專員成長了！從 {old_age} 歲成長到 {self.age} 歲")
    
    def _get_age_personality(self):
        """根據年齡獲得個性描述"""
        if self.age < 25:
            return "年輕熱血"
        elif self.age < 30:
            return "漸趨成熟"
        elif self.age < 35:
            return "穩重可靠"
        elif self.age < 40:
            return "經驗老道"
        else:
            return "智慧長者"
    
    def get_insights(self):
        """取得測試洞察 - 展現測試專員的個性"""
        # 根據年齡調整個性
        age_personality = self._get_age_personality()
        
        # 檢查是否在 Railway 環境
        if self.is_railway:
            if self.memory.get("git_commits") and len(self.memory["git_commits"]) > 0:
                latest_commit = self.memory["git_commits"][0]["message"]
                return f"{self.personality}（{self.age}歲，{age_personality}）報告：Railway 新部署！最新 commit: {latest_commit[:50]}..."
            elif self.memory.get("railway_deployment"):
                deployment = self.memory["railway_deployment"]
                deployment_id = deployment.get('instance_id', 'unknown')[:8]
                return f"{self.personality}（{self.age}歲，{age_personality}）報告：Railway 部署 ID {deployment_id}... 環境初始化完成！"
            else:
                return f"{self.personality}（{self.age}歲，{age_personality}）報告：Railway 新部署！正在初始化測試環境..."
        
        if not self.memory["test_history"]:
            return f"{self.personality} 報告：這是我第一次執行測試！充滿期待和好奇心！🚀"
        
        # 取得最新的反思
        latest_reflection = self.memory["reflections"][-1] if self.memory["reflections"] else None
        latest_wisdom = self.memory["wisdom"][-1] if self.memory["wisdom"] else None
        
        insights = [f"{self.personality} 洞察報告："]
        
        # 加入最新反思
        if latest_reflection:
            insights.append(f"💭 {latest_reflection.get('insight', '正在思考中...')}")
            if latest_reflection.get('progress'):
                insights.append(f"📈 {latest_reflection['progress']}")
        
        # 加入累積智慧
        if latest_wisdom:
            insights.append(f"🧠 {latest_wisdom['insight']}")
            if latest_wisdom.get('pattern'):
                insights.append(f"🔍 {latest_wisdom['pattern']}")
        
        # 分析最近趨勢
        recent = self.memory["test_history"][-5:]
        if len(recent) >= 2:
            recent_success = sum(1 for r in recent if r["success"])
            if recent_success == len(recent):
                insights.append("✨ 最近測試全部通過！保持這個勢頭！")
            elif recent_success == 0:
                insights.append("⚠️ 最近測試都失敗了，需要深入調查原因。")
        
        return " | ".join(insights)

class StartupTest:
    """啟動時自我檢測系統"""
    
    def __init__(self):
        self.start_time = time.time()
        self.tests = []
        self.results = {}
        self.critical_failures = []
        self.warnings = []
        self.test_agent = TestAgent()  # 測試專員
        
    def run_all_tests(self) -> bool:
        """執行所有啟動測試"""
        print("\n" + "="*50)
        print("🔍 執行啟動自我檢測...")
        print(f"🤖 測試專員洞察: {self.test_agent.get_insights()}")
        print("="*50)
        
        # 執行各項測試
        self._test_environment_variables()
        self._test_gemini_connection()
        self._test_line_bot_credentials()
        self._test_google_calendar()
        self._test_basic_ai_response()
        self._test_function_calling()  # 新增 Function Calling 測試
        
        # 計算測試時間
        self.test_duration = time.time() - self.start_time
        
        # 顯示測試報告
        self._print_report()
        
        # 返回是否所有關鍵測試都通過
        return len(self.critical_failures) == 0
    
    def _test_environment_variables(self):
        """測試環境變數"""
        test_name = "環境變數檢查"
        try:
            required_vars = {
                'LINE_CHANNEL_ACCESS_TOKEN': os.getenv('LINE_CHANNEL_ACCESS_TOKEN'),
                'LINE_CHANNEL_SECRET': os.getenv('LINE_CHANNEL_SECRET'),
                'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY')
            }
            
            missing_vars = [var for var, value in required_vars.items() if not value]
            
            if missing_vars:
                self.results[test_name] = "❌ 失敗"
                self.critical_failures.append(f"缺少必要環境變數: {', '.join(missing_vars)}")
            else:
                self.results[test_name] = "✅ 通過"
                
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"環境變數檢查錯誤: {str(e)}")
    
    def _test_gemini_connection(self):
        """測試 Gemini API 連線"""
        test_name = "Gemini API 連線"
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                self.results[test_name] = "⏭️ 跳過"
                self.warnings.append("未設定 Gemini API Key")
                return
                
            genai.configure(api_key=api_key)
            
            # 嘗試不同的模型名稱
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            response = None
            successful_model = None
            
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content("回應OK即可")
                    if response and response.text:
                        successful_model = model_name
                        break
                except Exception as e:
                    continue
            
            if successful_model:
                self.results[test_name] = "✅ 通過"
                duration = time.time() - self.start_time
                self.test_agent.remember_test(test_name, True, duration)
                logger.info(f"Gemini API 測試成功，使用模型: {successful_model}")
            else:
                self.results[test_name] = "❌ 失敗"
                self.critical_failures.append(f"Gemini API 無法使用任何模型: {', '.join(models_to_try)}")
                self.test_agent.remember_test(test_name, False, time.time() - self.start_time, "No model available")
                
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"Gemini 連線錯誤: {str(e)}")
    
    def _test_line_bot_credentials(self):
        """測試 Line Bot 憑證"""
        test_name = "Line Bot 設定"
        try:
            token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
            secret = os.getenv('LINE_CHANNEL_SECRET')
            
            if not token or not secret:
                self.results[test_name] = "❌ 失敗"
                self.critical_failures.append("Line Bot 憑證不完整")
                return
            
            # 驗證 token 格式
            if len(token) < 100 or len(secret) < 20:
                self.results[test_name] = "⚠️ 警告"
                self.warnings.append("Line Bot 憑證格式可能有誤")
            else:
                self.results[test_name] = "✅ 通過"
                
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"Line Bot 設定錯誤: {str(e)}")
    
    def _test_google_calendar(self):
        """測試 Google Calendar 服務"""
        test_name = "Google Calendar"
        try:
            credentials = os.getenv('GOOGLE_CALENDAR_CREDENTIALS')
            
            if not credentials:
                self.results[test_name] = "⏭️ 跳過"
                self.warnings.append("未設定 Google Calendar（選用功能）")
                return
            
            # 嘗試解析 JSON
            import json
            json.loads(credentials)
            self.results[test_name] = "✅ 通過"
            
        except json.JSONDecodeError:
            self.results[test_name] = "⚠️ 警告"
            self.warnings.append("Google Calendar 憑證格式錯誤")
        except Exception as e:
            self.results[test_name] = "⚠️ 警告"
            self.warnings.append(f"Google Calendar 設定問題: {str(e)}")
    
    def _test_basic_ai_response(self):
        """測試基本 AI 功能"""
        test_name = "基本 AI 功能"
        try:
            # 簡單測試 import 是否成功
            from gemini_service import GeminiService
            from line_bot_handler import LineBotHandler
            
            self.results[test_name] = "✅ 通過"
            
        except ImportError as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"模組載入失敗: {str(e)}")
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"基本功能錯誤: {str(e)}")
    
    def _print_report(self):
        """列印測試報告"""
        print("\n" + "="*50)
        print("📊 啟動檢測報告")
        print("="*50)
        
        # 顯示各項測試結果
        for test, result in self.results.items():
            print(f"{result} {test}")
        
        # 顯示警告
        if self.warnings:
            print("\n⚠️  警告訊息:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        # 顯示嚴重錯誤
        if self.critical_failures:
            print("\n❌ 嚴重錯誤:")
            for error in self.critical_failures:
                print(f"   - {error}")
        
        # 總結
        print(f"\n測試時間: {self.test_duration:.2f} 秒")
        print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.critical_failures:
            print("\n狀態: ❌ 啟動失敗")
        else:
            print("\n狀態: ✅ 準備就緒")
        
        print("="*50 + "\n")
    
    def _test_function_calling(self):
        """測試 Function Calling 功能"""
        test_name = "Function Calling"
        start_time = time.time()
        
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                self.results[test_name] = "⏭️ 跳過"
                self.warnings.append("未設定 Gemini API Key，跳過 Function Calling 測試")
                return
            
            # 載入 gemini_service 進行實際測試
            from gemini_service import GeminiService
            service = GeminiService()
            
            # 測試 Function Calling - 查詢明天的行程
            try:
                response = service.get_response("test_user", "明天有什麼行程？")
                
                # 檢查是否有回應且沒有錯誤
                if response and "TypeError" not in response and "錯誤" not in response:
                    self.results[test_name] = "✅ 通過"
                    duration = time.time() - start_time
                    self.test_agent.remember_test(test_name, True, duration)
                    logger.info(f"Function Calling 測試成功，回應: {response[:50]}...")
                else:
                    self.results[test_name] = "❌ 失敗"
                    self.critical_failures.append(f"Function Calling 回應異常: {response[:100]}")
                    self.test_agent.remember_test(test_name, False, time.time() - start_time, response)
                    
            except Exception as e:
                self.results[test_name] = "❌ 失敗"
                self.critical_failures.append(f"Function Calling 執行錯誤: {str(e)}")
                
                # 測試專員進行深入分析
                error_analysis = self.test_agent.analyze_error_context(e, test_name)
                if error_analysis.get("code_context"):
                    logger.info(f"測試專員發現錯誤相關程式碼在第 {error_analysis.get('line_number')} 行")
                
                self.test_agent.remember_test(test_name, False, time.time() - start_time, e)
                
        except ImportError as e:
            self.results[test_name] = "⚠️ 警告"
            self.warnings.append(f"無法載入 GeminiService: {str(e)}")
        except Exception as e:
            self.results[test_name] = "❌ 失敗"
            self.critical_failures.append(f"Function Calling 測試錯誤: {str(e)}")
            self.test_agent.remember_test(test_name, False, time.time() - start_time, e)
    
    def get_status(self) -> dict:
        """取得測試狀態（供健康檢查使用）"""
        return {
            "startup_test_passed": len(self.critical_failures) == 0,
            "test_results": self.results,
            "warnings": self.warnings,
            "errors": self.critical_failures,
            "test_duration": getattr(self, 'test_duration', 0),
            "test_time": datetime.now().isoformat(),
            "test_agent_insights": self.test_agent.get_insights()
        }