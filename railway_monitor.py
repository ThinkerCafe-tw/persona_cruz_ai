"""
Railway API 監控模組
用於抓取部署日誌和監控服務狀態
"""
import os
import json
import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class RailwayMonitor:
    """Railway 監控器 - 測試專員的眼睛"""
    
    def __init__(self, project_token=None):
        self.project_token = project_token or os.getenv('RAILWAY_PROJECT_TOKEN')
        self.api_url = "https://backboard.railway.com/graphql/v2"
        self.headers = {
            'Content-Type': 'application/json',
            'Project-Access-Token': self.project_token
        } if self.project_token else {}
        
    def get_deployment_logs(self, limit=100):
        """獲取部署日誌"""
        if not self.project_token:
            logger.warning("無 Railway Project Token，無法獲取日誌")
            return None
            
        query = """
        query GetLogs {
            deploymentLogs(
                input: {
                    limit: %d
                    filter: {
                        projectId: "%s"
                        environmentId: "%s"
                    }
                }
            ) {
                edges {
                    node {
                        id
                        message
                        severity
                        timestamp
                    }
                }
            }
        }
        """ % (
            limit,
            os.getenv('RAILWAY_PROJECT_ID', ''),
            os.getenv('RAILWAY_ENVIRONMENT_ID', '')
        )
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={'query': query}
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'deploymentLogs' in data['data']:
                    return data['data']['deploymentLogs']['edges']
                else:
                    logger.error(f"Railway API 回應格式錯誤: {data}")
            else:
                logger.error(f"Railway API 錯誤: {response.status_code}")
                
        except Exception as e:
            logger.error(f"無法連接 Railway API: {str(e)}")
            
        return None
    
    def analyze_recent_errors(self, logs):
        """分析最近的錯誤"""
        if not logs:
            return []
            
        errors = []
        for edge in logs:
            log = edge.get('node', {})
            if log.get('severity') in ['ERROR', 'CRITICAL']:
                errors.append({
                    'message': log.get('message', ''),
                    'timestamp': log.get('timestamp', ''),
                    'severity': log.get('severity', '')
                })
                
        return errors[:10]  # 只返回最近 10 個錯誤
    
    def get_deployment_status(self):
        """獲取部署狀態"""
        # 這裡可以擴展查詢部署狀態的功能
        return {
            'deployment_id': os.getenv('RAILWAY_DEPLOYMENT_ID', 'unknown'),
            'environment': os.getenv('RAILWAY_ENVIRONMENT', 'unknown'),
            'replica_id': os.getenv('RAILWAY_REPLICA_ID', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

# 測試專員可以使用的快速函數
def get_recent_errors():
    """快速獲取最近的錯誤"""
    monitor = RailwayMonitor()
    logs = monitor.get_deployment_logs(50)
    return monitor.analyze_recent_errors(logs)