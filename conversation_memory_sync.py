"""
對話記憶同步系統
將開發對話自動同步到 CRUZ 記憶庫
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import re
import logging

logger = logging.getLogger(__name__)

class ConversationMemorySync:
    """對話記憶同步器"""
    
    def __init__(self, corpus_path: str = "data/cruz_corpus.json"):
        self.corpus_path = corpus_path
        self.conversation_buffer = []
        self.load_corpus()
        
    def load_corpus(self):
        """載入現有語料庫"""
        try:
            with open(self.corpus_path, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Corpus file not found at {self.corpus_path}")
            self.corpus = self._create_empty_corpus()
    
    def _create_empty_corpus(self) -> Dict:
        """創建空語料庫結構"""
        return {
            "metadata": {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "total_quotes": 0
            },
            "quotes": [],
            "development_conversations": []  # 新增開發對話區
        }
    
    def add_conversation_turn(self, speaker: str, message: str, context: str = "開發對話"):
        """添加一輪對話"""
        turn = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "message": message,
            "context": context
        }
        self.conversation_buffer.append(turn)
        
        # 每5輪對話自動分析並保存
        if len(self.conversation_buffer) >= 5:
            self.process_and_save_conversations()
    
    def process_and_save_conversations(self):
        """處理並保存對話到記憶庫"""
        if not self.conversation_buffer:
            return
        
        # 分析對話內容
        insights = self._extract_insights(self.conversation_buffer)
        
        # 轉換為 CRUZ 風格的語料
        for insight in insights:
            quote = {
                "id": self._get_next_id(),
                "content": insight["content"],
                "date": datetime.now().strftime("%Y-%m-%d"),
                "context": insight["context"],
                "tags": insight["tags"],
                "usage_count": 0,
                "imported_at": datetime.now().isoformat(),
                "source": "development_conversation"
            }
            self.corpus["quotes"].append(quote)
        
        # 保存原始對話記錄
        conversation_record = {
            "id": f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "turns": self.conversation_buffer.copy(),
            "insights_extracted": len(insights)
        }
        
        if "development_conversations" not in self.corpus:
            self.corpus["development_conversations"] = []
        
        self.corpus["development_conversations"].append(conversation_record)
        
        # 更新元數據
        self.corpus["metadata"]["last_updated"] = datetime.now().isoformat()
        self.corpus["metadata"]["total_quotes"] = len(self.corpus["quotes"])
        
        # 保存到檔案
        self.save_corpus()
        
        # 清空緩衝區
        self.conversation_buffer = []
        
        logger.info(f"Saved {len(insights)} insights from conversation")
    
    def _extract_insights(self, conversations: List[Dict]) -> List[Dict]:
        """從對話中提取洞察"""
        insights = []
        
        # 合併連續的同一說話者訊息
        merged_conversations = self._merge_consecutive_messages(conversations)
        
        for conv in merged_conversations:
            # 提取關鍵決策和想法
            if self._is_important_insight(conv["message"]):
                content = self._clean_message(conv["message"])
                
                insight = {
                    "content": content,
                    "context": self._determine_context(content),
                    "tags": self._extract_tags(content)
                }
                insights.append(insight)
        
        return insights
    
    def _merge_consecutive_messages(self, conversations: List[Dict]) -> List[Dict]:
        """合併連續的同一說話者訊息"""
        if not conversations:
            return []
        
        merged = []
        current = conversations[0].copy()
        
        for conv in conversations[1:]:
            if conv["speaker"] == current["speaker"]:
                current["message"] += " " + conv["message"]
            else:
                merged.append(current)
                current = conv.copy()
        
        merged.append(current)
        return merged
    
    def _is_important_insight(self, message: str) -> bool:
        """判斷是否為重要洞察"""
        # 關鍵詞檢測
        important_keywords = [
            "我想", "我覺得", "應該", "可以", "建議",
            "重要", "關鍵", "核心", "原則", "價值",
            "為什麼", "因為", "所以", "目標", "願景"
        ]
        
        message_lower = message.lower()
        
        # 檢查是否包含關鍵詞
        if any(keyword in message for keyword in important_keywords):
            return True
        
        # 檢查是否為決策性語句
        if any(pattern in message for pattern in ["決定", "選擇", "優先", "先做"]):
            return True
        
        # 檢查是否包含個人經驗分享
        if "經驗" in message or "我曾經" in message or "我發現" in message:
            return True
        
        # 長度檢查（太短的訊息可能不是洞察）
        if len(message) < 20:
            return False
        
        return False
    
    def _clean_message(self, message: str) -> str:
        """清理訊息內容"""
        # 移除多餘空白
        message = re.sub(r'\s+', ' ', message).strip()
        
        # 移除網址
        message = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', message)
        
        # 截取合適長度
        if len(message) > 200:
            # 找到適合的斷句點
            for i in range(190, 150, -1):
                if message[i] in '。！？，；':
                    message = message[:i+1]
                    break
            else:
                message = message[:197] + "..."
        
        return message
    
    def _determine_context(self, content: str) -> str:
        """判斷內容的情境"""
        contexts = {
            "技術決策": ["技術", "架構", "程式", "系統", "API", "資料庫"],
            "產品規劃": ["功能", "需求", "用戶", "體驗", "介面"],
            "開發流程": ["流程", "開發", "測試", "部署", "TDD"],
            "團隊協作": ["團隊", "溝通", "協作", "分工"],
            "個人見解": ["我想", "我覺得", "我認為", "建議"]
        }
        
        for context, keywords in contexts.items():
            if any(keyword in content for keyword in keywords):
                return context
        
        return "開發洞察"
    
    def _extract_tags(self, content: str) -> List[str]:
        """提取標籤"""
        tags = []
        
        # 技術標籤
        tech_tags = {
            "AI": ["AI", "人工智慧", "機器學習", "LLM", "GPT", "Claude"],
            "開發": ["開發", "程式", "coding", "TDD", "測試"],
            "架構": ["架構", "系統", "設計", "模組"],
            "創新": ["創新", "創意", "新想法", "改進"]
        }
        
        for tag, keywords in tech_tags.items():
            if any(keyword.lower() in content.lower() for keyword in keywords):
                tags.append(tag)
        
        # 情感標籤
        if any(word in content for word in ["相信", "信心", "能力", "潛能"]):
            tags.append("信念")
        
        if any(word in content for word in ["創造", "創作", "打造"]):
            tags.append("創造")
        
        return list(set(tags))  # 去重
    
    def _get_next_id(self) -> int:
        """獲取下一個可用的 ID"""
        if not self.corpus.get("quotes"):
            return 1
        
        max_id = max(quote["id"] for quote in self.corpus["quotes"] if isinstance(quote.get("id"), int))
        return max_id + 1
    
    def save_corpus(self):
        """保存語料庫"""
        try:
            with open(self.corpus_path, 'w', encoding='utf-8') as f:
                json.dump(self.corpus, f, ensure_ascii=False, indent=2)
            logger.info(f"Corpus saved to {self.corpus_path}")
        except Exception as e:
            logger.error(f"Failed to save corpus: {e}")
    
    def get_recent_insights(self, limit: int = 5) -> List[Dict]:
        """獲取最近的洞察"""
        dev_quotes = [q for q in self.corpus.get("quotes", []) 
                     if q.get("source") == "development_conversation"]
        
        # 按匯入時間排序
        dev_quotes.sort(key=lambda x: x.get("imported_at", ""), reverse=True)
        
        return dev_quotes[:limit]
    
    def force_save(self):
        """強制保存當前緩衝區的對話"""
        if self.conversation_buffer:
            self.process_and_save_conversations()


# 使用範例
if __name__ == "__main__":
    sync = ConversationMemorySync()
    
    # 模擬對話
    sync.add_conversation_turn("User", "我想建立一個能理解用戶情緒的系統")
    sync.add_conversation_turn("Claude", "這是個很好的想法，我們可以從用戶心理分析開始")
    sync.add_conversation_turn("User", "對，而且要能根據情緒給出不同的回應")
    sync.add_conversation_turn("Claude", "我建議使用三階段架構：分析、搜尋、生成")
    sync.add_conversation_turn("User", "太好了，這樣能讓系統更有人性")
    
    # 獲取最近的洞察
    recent = sync.get_recent_insights()
    for insight in recent:
        print(f"- {insight['content'][:50]}...")