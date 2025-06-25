"""
DNS 考古學 - Railway 內部網路 DNS 解析的完整歷史
創建於：2025-06-24 - DNS 無法解析 postgres.railway.internal 事件

歷史時刻：
- 2025-06-24 02:21:11 - 首次遭遇 "could not translate host name" 錯誤
- 私有網路已啟用但 DNS 無法解析的謎團
"""
import socket
import time
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class DNSArchaeology:
    """DNS 問題的考古學研究 - 每個細節都被永久保存"""
    
    # 歷史時刻 - 每個重要的發現
    HISTORICAL_MOMENTS = [
        {
            "timestamp": "2025-06-24 02:21:11",
            "error": "could not translate host name 'postgres.railway.internal' to address: Name or service not known",
            "context": "首次嘗試連接內部網路，兩個服務都已啟用私有網路",
            "environment": {
                "service": "persona_cruz_ai",
                "target": "postgres (pgvector service)",
                "network_status": "Both services have private networking enabled"
            },
            "attempted_solutions": [
                "檢查私有網路設定 - 已確認啟用",
                "等待 DNS 傳播 - 問題持續",
                "考慮使用公開 URL - 待定"
            ],
            "wisdom": "內部 DNS 可能需要特殊處理或有未知的啟用條件"
        }
    ]
    
    # 已知的主機名格式 - 累積的知識庫
    KNOWN_HOSTNAME_FORMATS = [
        # Railway 官方格式
        ("postgres.railway.internal", "官方文檔格式 - 完整服務名"),
        ("postgres", "簡短格式 - Railway 說可以這樣用"),
        
        # 可能的變體
        ("pgvector.railway.internal", "基於服務類型的名稱"),
        ("pgvector", "服務類型簡短名"),
        
        # 基於環境變數的格式
        ("${RAILWAY_SERVICE_NAME}.railway.internal", "使用服務名變數"),
        ("${RAILWAY_SERVICE_NAME}", "服務名變數簡短版"),
        
        # IPv6 相關（Railway 顯示是 IPv6）
        ("postgres.railway.internal.", "帶結尾點的 FQDN"),
        
        # 其他可能性
        ("postgres.internal", "省略 railway 的格式"),
        ("postgres-prod.railway.internal", "可能包含環境的格式"),
    ]
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.discoveries = []  # 本次會話的所有發現
        self.start_time = datetime.now()
        
    def archaeological_dig(self, context: Dict = None) -> Dict:
        """
        進行完整的 DNS 考古挖掘
        每次執行都會增加我們對系統的理解
        """
        logger.info(f"🏺 開始 DNS 考古挖掘 - 會話 {self.session_id}")
        
        findings = {
            "dig_session": self.session_id,
            "dig_time": self.start_time.isoformat(),
            "context": context or {},
            "environment_scan": self._deep_environment_scan(),
            "dns_resolution_attempts": self._comprehensive_dns_attempts(),
            "network_state_analysis": self._analyze_network_state(),
            "timing_experiments": self._conduct_timing_experiments(),
            "railway_specific_probe": self._probe_railway_specifics(),
            "historical_comparison": self._compare_with_history(),
            "wisdom_gained": [],
            "recommendations": []
        }
        
        # 深度分析所有發現
        findings["wisdom_gained"] = self._extract_wisdom(findings)
        findings["recommendations"] = self._generate_recommendations(findings)
        
        # 永久保存這次挖掘結果
        self._preserve_archaeological_findings(findings)
        
        # 更新歷史記錄
        self._update_historical_record(findings)
        
        return findings
    
    def _deep_environment_scan(self) -> Dict:
        """深度環境掃描 - 保存所有可能相關的環境資訊"""
        logger.info("🔍 執行深度環境掃描...")
        
        env_data = {
            "timestamp": datetime.now().isoformat(),
            "railway_variables": {},
            "database_related": {},
            "network_hints": {},
            "service_discovery": {},
            "all_env_keys": [],  # 保存所有鍵名
            "special_observations": []
        }
        
        # 掃描所有環境變數
        for key, value in os.environ.items():
            # Railway 特定
            if key.startswith('RAILWAY_'):
                env_data["railway_variables"][key] = value
                
            # 資料庫相關
            if any(db_hint in key.upper() for db_hint in ['DATABASE', 'POSTGRES', 'PGVECTOR', 'DB_', 'SQL']):
                # 保護密碼但保留結構資訊
                env_data["database_related"][key] = self._analyze_database_url(value)
                
            # 網路相關
            if any(net_hint in key.upper() for net_hint in ['HOST', 'DOMAIN', 'NETWORK', 'DNS', 'ADDR', 'INTERNAL']):
                env_data["network_hints"][key] = value
                
            # 服務發現相關
            if any(svc_hint in key.upper() for svc_hint in ['SERVICE', 'CONTAINER', 'POD', 'NODE']):
                env_data["service_discovery"][key] = value
        
        # 保存所有環境變數鍵（幫助未來的考古）
        env_data["all_env_keys"] = sorted(list(os.environ.keys()))
        
        # 特殊觀察
        if 'RAILWAY_ENVIRONMENT' in os.environ:
            env_data["special_observations"].append(
                f"運行在 Railway 環境: {os.environ['RAILWAY_ENVIRONMENT']}"
            )
            
        if 'RAILWAY_PRIVATE_DOMAIN' in os.environ:
            env_data["special_observations"].append(
                f"私有域名設定: {os.environ['RAILWAY_PRIVATE_DOMAIN']}"
            )
            
        return env_data
    
    def _comprehensive_dns_attempts(self) -> List[Dict]:
        """全面的 DNS 解析嘗試 - 測試所有可能的格式"""
        logger.info("🔬 開始全面 DNS 解析測試...")
        
        results = []
        
        for hostname_format, description in self.KNOWN_HOSTNAME_FORMATS:
            # 處理模板變數
            hostname = self._expand_template(hostname_format)
            
            result = {
                "format": hostname_format,
                "expanded": hostname,
                "description": description,
                "timestamp": datetime.now().isoformat(),
                "attempts": [],
                "analysis": {}
            }
            
            # 多種解析方法
            resolution_methods = [
                ("getaddrinfo", self._try_getaddrinfo),
                ("gethostbyname", self._try_gethostbyname),
                ("socket.create_connection", self._try_create_connection),
            ]
            
            for method_name, method_func in resolution_methods:
                attempt_result = method_func(hostname)
                attempt_result["method"] = method_name
                result["attempts"].append(attempt_result)
            
            # 分析結果模式
            result["analysis"] = self._analyze_resolution_pattern(result["attempts"])
            
            results.append(result)
            
        return results
    
    def _try_getaddrinfo(self, hostname: str) -> Dict:
        """使用 getaddrinfo 嘗試解析"""
        attempt = {
            "start_time": time.time(),
            "hostname": hostname,
            "success": False,
            "results": [],
            "error": None,
            "duration_ms": 0
        }
        
        try:
            infos = socket.getaddrinfo(hostname, None)
            attempt["success"] = True
            attempt["results"] = [
                {
                    "family": info[0],  # AF_INET 或 AF_INET6
                    "type": info[1],
                    "proto": info[2],
                    "addr": info[4]
                }
                for info in infos
            ]
        except Exception as e:
            attempt["error"] = {
                "type": type(e).__name__,
                "message": str(e),
                "errno": getattr(e, 'errno', None)
            }
        
        attempt["duration_ms"] = (time.time() - attempt["start_time"]) * 1000
        return attempt
    
    def _try_gethostbyname(self, hostname: str) -> Dict:
        """使用傳統 gethostbyname"""
        attempt = {
            "start_time": time.time(),
            "hostname": hostname,
            "success": False,
            "ip": None,
            "error": None,
            "duration_ms": 0
        }
        
        try:
            ip = socket.gethostbyname(hostname)
            attempt["success"] = True
            attempt["ip"] = ip
        except Exception as e:
            attempt["error"] = {
                "type": type(e).__name__,
                "message": str(e)
            }
        
        attempt["duration_ms"] = (time.time() - attempt["start_time"]) * 1000
        return attempt
    
    def _try_create_connection(self, hostname: str) -> Dict:
        """嘗試實際建立連接"""
        attempt = {
            "start_time": time.time(),
            "hostname": hostname,
            "port": 5432,  # PostgreSQL 預設
            "success": False,
            "error": None,
            "duration_ms": 0
        }
        
        try:
            # 短暫超時避免卡住
            sock = socket.create_connection((hostname, 5432), timeout=2)
            sock.close()
            attempt["success"] = True
        except Exception as e:
            attempt["error"] = {
                "type": type(e).__name__,
                "message": str(e),
                "stage": "connection"  # 標記失敗階段
            }
        
        attempt["duration_ms"] = (time.time() - attempt["start_time"]) * 1000
        return attempt
    
    def _analyze_network_state(self) -> Dict:
        """分析網路狀態"""
        return {
            "hostname": socket.gethostname(),
            "fqdn": socket.getfqdn(),
            "default_timeout": socket.getdefaulttimeout(),
            "has_ipv6": socket.has_ipv6,
            "interfaces": self._get_network_interfaces(),
            "routing": self._check_routing_table(),
            "dns_config": self._examine_dns_config()
        }
    
    def _conduct_timing_experiments(self) -> Dict:
        """時間實驗 - 測試 DNS 是否需要預熱"""
        experiments = {
            "hypothesis": "DNS 可能需要時間來傳播或初始化",
            "tests": []
        }
        
        test_hostname = "postgres.railway.internal"
        
        # 立即測試
        experiments["tests"].append({
            "delay": 0,
            "result": self._test_resolution_with_delay(test_hostname, 0)
        })
        
        # 逐漸延遲測試
        for delay in [1, 3, 5, 10]:
            logger.info(f"⏰ 等待 {delay} 秒後測試...")
            experiments["tests"].append({
                "delay": delay,
                "result": self._test_resolution_with_delay(test_hostname, delay)
            })
            
        return experiments
    
    def _probe_railway_specifics(self) -> Dict:
        """探測 Railway 特定的網路配置"""
        probe_results = {
            "railway_network_mode": self._detect_railway_network_mode(),
            "service_aliases": self._find_service_aliases(),
            "internal_endpoints": self._discover_internal_endpoints(),
            "ipv6_readiness": self._check_ipv6_readiness()
        }
        
        return probe_results
    
    def _compare_with_history(self) -> Dict:
        """與歷史記錄比較，找出模式"""
        comparison = {
            "historical_errors": len(self.HISTORICAL_MOMENTS),
            "recurring_patterns": [],
            "evolution": []
        }
        
        # 分析錯誤模式
        error_types = {}
        for moment in self.HISTORICAL_MOMENTS:
            error = moment.get("error", "")
            if error:
                error_type = error.split(":")[0]
                error_types[error_type] = error_types.get(error_type, 0) + 1
                
        comparison["error_frequency"] = error_types
        
        return comparison
    
    def _extract_wisdom(self, findings: Dict) -> List[str]:
        """從發現中提取智慧"""
        wisdom = []
        
        # 分析 DNS 成功率
        total_attempts = 0
        successful_attempts = 0
        
        for dns_result in findings.get("dns_resolution_attempts", []):
            for attempt in dns_result.get("attempts", []):
                total_attempts += 1
                if attempt.get("success"):
                    successful_attempts += 1
                    
        if total_attempts > 0:
            success_rate = (successful_attempts / total_attempts) * 100
            wisdom.append(f"DNS 解析成功率: {success_rate:.1f}% ({successful_attempts}/{total_attempts})")
            
        # 分析時間模式
        timing_results = findings.get("timing_experiments", {}).get("tests", [])
        if timing_results:
            delay_success = [(t["delay"], t["result"].get("success", False)) for t in timing_results]
            if any(success for _, success in delay_success):
                first_success_delay = next((delay for delay, success in delay_success if success), None)
                if first_success_delay is not None:
                    wisdom.append(f"DNS 在 {first_success_delay} 秒延遲後首次成功")
                    
        # 更多智慧提取...
        
        return wisdom
    
    def _generate_recommendations(self, findings: Dict) -> List[str]:
        """基於發現生成建議"""
        recommendations = []
        
        # 基於發現的問題生成具體建議
        all_failed = all(
            not attempt.get("success", False)
            for dns_result in findings.get("dns_resolution_attempts", [])
            for attempt in dns_result.get("attempts", [])
        )
        
        if all_failed:
            recommendations.append("所有內部 DNS 解析都失敗，建議使用公開 URL 作為解決方案")
            recommendations.append("考慮在 Railway 設定中檢查服務的網路配置")
            recommendations.append("可能需要等待服務完全啟動後再連接")
            
        return recommendations
    
    def _preserve_archaeological_findings(self, findings: Dict):
        """永久保存考古發現"""
        # 保存到檔案系統
        findings_dir = "system_intelligence/archaeological_records"
        os.makedirs(findings_dir, exist_ok=True)
        
        filename = f"{findings_dir}/dns_dig_{self.session_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(findings, f, indent=2, ensure_ascii=False, default=str)
            
        logger.info(f"💾 考古發現已永久保存至: {filename}")
        
    def _update_historical_record(self, findings: Dict):
        """更新歷史記錄"""
        # 這裡可以更新類別的 HISTORICAL_MOMENTS
        # 或寫入更永久的存儲
        pass
    
    # === 輔助方法 ===
    
    def _expand_template(self, template: str) -> str:
        """展開模板變數"""
        if '${' not in template:
            return template
            
        # 替換已知的環境變數
        result = template
        for key, value in os.environ.items():
            result = result.replace(f"${{{key}}}", value)
            
        return result
    
    def _analyze_database_url(self, url: str) -> Dict:
        """分析資料庫 URL 但保護敏感資訊"""
        if not url:
            return {"status": "NOT_SET"}
            
        analysis = {
            "format": "unknown",
            "host_type": "unknown",
            "has_port": False,
            "has_password": False
        }
        
        if url.startswith('postgresql://') or url.startswith('postgres://'):
            analysis["format"] = url.split('://')[0]
            
            if '@' in url:
                analysis["has_password"] = True
                host_part = url.split('@')[1]
                
                if '.railway.internal' in host_part:
                    analysis["host_type"] = "railway_internal"
                elif '.proxy.rlwy.net' in host_part:
                    analysis["host_type"] = "railway_public"
                elif 'localhost' in host_part or '127.0.0.1' in host_part:
                    analysis["host_type"] = "local"
                else:
                    analysis["host_type"] = "external"
                    
                if ':' in host_part.split('/')[0]:
                    analysis["has_port"] = True
                    
        return analysis
    
    def _get_network_interfaces(self) -> List[Dict]:
        """獲取網路介面資訊"""
        # 這需要更複雜的實作，暫時返回基本資訊
        return [{"note": "需要 psutil 或其他套件來獲取詳細介面資訊"}]
    
    def _check_routing_table(self) -> Dict:
        """檢查路由表"""
        # 需要系統呼叫，暫時返回基本資訊
        return {"note": "需要系統權限來檢查路由表"}
    
    def _examine_dns_config(self) -> Dict:
        """檢查 DNS 配置"""
        config = {}
        
        # 嘗試讀取 /etc/resolv.conf (Unix-like)
        try:
            with open('/etc/resolv.conf', 'r') as f:
                config["resolv_conf"] = f.read()
        except:
            config["resolv_conf"] = "無法讀取"
            
        return config
    
    def _test_resolution_with_delay(self, hostname: str, delay: int) -> Dict:
        """延遲後測試解析"""
        if delay > 0:
            time.sleep(delay)
            
        return self._try_getaddrinfo(hostname)
    
    def _detect_railway_network_mode(self) -> str:
        """偵測 Railway 網路模式"""
        if os.getenv('RAILWAY_PRIVATE_DOMAIN'):
            return "private_networking_enabled"
        return "unknown"
    
    def _find_service_aliases(self) -> List[str]:
        """尋找服務別名"""
        aliases = []
        
        # 從環境變數推測
        service_name = os.getenv('RAILWAY_SERVICE_NAME', '')
        if service_name:
            aliases.extend([
                service_name,
                f"{service_name}.railway.internal",
                service_name.lower(),
                service_name.upper()
            ])
            
        return list(set(aliases))
    
    def _discover_internal_endpoints(self) -> List[str]:
        """發現內部端點"""
        endpoints = []
        
        # 基於 Railway 慣例
        common_services = ['postgres', 'mysql', 'redis', 'mongo']
        for service in common_services:
            endpoints.extend([
                f"{service}.railway.internal",
                service
            ])
            
        return endpoints
    
    def _check_ipv6_readiness(self) -> Dict:
        """檢查 IPv6 準備狀態"""
        return {
            "has_ipv6": socket.has_ipv6,
            "can_create_ipv6_socket": self._can_create_ipv6_socket()
        }
    
    def _can_create_ipv6_socket(self) -> bool:
        """測試是否能建立 IPv6 socket"""
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.close()
            return True
        except:
            return False
    
    def _analyze_resolution_pattern(self, attempts: List[Dict]) -> Dict:
        """分析解析模式"""
        pattern = {
            "all_failed": all(not a.get("success") for a in attempts),
            "all_succeeded": all(a.get("success") for a in attempts),
            "failure_types": list(set(
                a.get("error", {}).get("type", "Unknown")
                for a in attempts
                if not a.get("success")
            ))
        }
        
        return pattern