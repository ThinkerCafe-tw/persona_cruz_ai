"""
CRUZ 人格語料管理系統
"""
import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
import re
from user_analyzer import UserAnalyzer

logger = logging.getLogger(__name__)

class CruzPersonaSystem:
    """CRUZ 人格系統 - 管理語料庫和人格生成"""
    
    def __init__(self):
        self.corpus_file = "data/cruz_corpus.json"
        self.corpus = self.load_corpus()
        
    def load_corpus(self) -> Dict:
        """載入語料庫"""
        if os.path.exists(self.corpus_file):
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"Corpus file not found: {self.corpus_file}")
            return {
                "metadata": {"version": "1.0", "total_quotes": 0},
                "traits": {},
                "quotes": [],
                "reviewed_responses": []
            }
    
    def save_corpus(self):
        """儲存語料庫"""
        self.corpus["metadata"]["last_updated"] = datetime.now().isoformat()
        self.corpus["metadata"]["total_quotes"] = len(self.corpus["quotes"])
        
        with open(self.corpus_file, 'w', encoding='utf-8') as f:
            json.dump(self.corpus, f, ensure_ascii=False, indent=2)
        logger.info(f"Corpus saved with {len(self.corpus['quotes'])} quotes")
    
    def import_text_file(self, file_path: str) -> int:
        """
        匯入純文字檔（Threads 格式）
        格式：用 === 分隔每則貼文
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 用 === 分割貼文
        posts = content.split('===')
        imported_count = 0
        
        for post in posts:
            post = post.strip()
            if not post:
                continue
                
            lines = post.split('\n')
            if len(lines) >= 2:
                date_str = lines[0].strip()
                content_text = '\n'.join(lines[1:]).strip()
                
                if content_text:
                    # 生成 ID
                    next_id = len(self.corpus["quotes"]) + 1
                    
                    # 提取標籤（簡單的關鍵詞提取）
                    tags = self._extract_tags(content_text)
                    
                    # 判斷情境
                    context = self._determine_context(content_text)
                    
                    quote = {
                        "id": next_id,
                        "content": content_text,
                        "date": date_str,
                        "context": context,
                        "tags": tags,
                        "usage_count": 0,
                        "imported_at": datetime.now().isoformat()
                    }
                    
                    self.corpus["quotes"].append(quote)
                    imported_count += 1
                    logger.info(f"Imported quote {next_id}: {content_text[:50]}...")
        
        if imported_count > 0:
            self.save_corpus()
            
        logger.info(f"Imported {imported_count} quotes from {file_path}")
        return imported_count
    
    def _extract_tags(self, text: str) -> List[str]:
        """從文本中提取標籤"""
        tags = []
        
        # 預定義的關鍵詞
        keywords = {
            "創造": ["創造", "創作", "創新"],
            "自信": ["自信", "相信", "力量", "潛能"],
            "AI": ["AI", "人工智慧", "自動化"],
            "冥想": ["冥想", "深呼吸", "清晰"],
            "運動": ["慢跑", "運動", "跑步"],
            "音樂": ["鋼琴", "音符", "節奏"],
            "職場": ["工作", "企業", "體制", "職場"],
            "成長": ["成長", "改變", "學習"],
            "真誠": ["真誠", "真實", "不假裝"]
        }
        
        for tag, words in keywords.items():
            for word in words:
                if word in text:
                    tags.append(tag)
                    break
        
        return list(set(tags))  # 去重
    
    def _determine_context(self, text: str) -> str:
        """判斷文本的情境"""
        if any(word in text for word in ["工作", "企業", "體制", "職場"]):
            return "職場建議"
        elif any(word in text for word in ["冥想", "慢跑", "運動", "鋼琴"]):
            return "生活分享"
        elif any(word in text for word in ["AI", "程式", "技術", "自動化"]):
            return "技術見解"
        elif any(word in text for word in ["朋友", "幫助", "真誠"]):
            return "人際關係"
        else:
            return "人生哲學"
    
    def search_relevant_quotes(self, query: str, limit: int = 3) -> List[Dict]:
        """
        搜尋相關語料（初期用關鍵字匹配）
        """
        if not self.corpus["quotes"]:
            return []
        
        scores = []
        query_lower = query.lower()
        
        for quote in self.corpus["quotes"]:
            score = 0
            content_lower = quote["content"].lower()
            
            # 完整內容包含查詢
            if query_lower in content_lower:
                score += 10
            
            # 關鍵詞匹配
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 1 and word in content_lower:
                    score += 5
            
            # 特殊關鍵詞匹配
            special_keywords = {
                "冥想": ["冥想", "深呼吸", "清晰"],
                "創業": ["創業", "收入", "公司", "創業第"],
                "程式": ["程式", "程式碼", "寫程式", "技術", "code"]
            }
            
            for keyword, related_words in special_keywords.items():
                if keyword in query_lower:
                    for related in related_words:
                        if related in content_lower:
                            score += 8
                            break
            
            # 標籤匹配
            for tag in quote["tags"]:
                if tag in query_lower or query_lower in tag:
                    score += 3
            
            # 情境匹配
            if quote["context"] and quote["context"] in query:
                score += 2
                
            if score > 0:
                scores.append((score, quote))
        
        # 按分數排序
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # 返回前 N 個
        results = []
        for score, quote in scores[:limit]:
            result = quote.copy()
            result["relevance_score"] = score
            results.append(result)
            
            # 更新使用次數
            quote["usage_count"] += 1
        
        if results:
            self.save_corpus()
            
        return results
    
    def get_cruz_traits(self) -> Dict:
        """獲取 CRUZ 的核心特質"""
        return self.corpus.get("traits", {})
    
    def get_frequent_topics(self) -> Dict:
        """獲取常見話題"""
        return self.corpus.get("frequent_topics", {})
    
    def add_reviewed_response(self, question: str, ai_response: str, 
                            cruz_response: str, selected: str):
        """添加 Review 記錄"""
        review = {
            "id": len(self.corpus["reviewed_responses"]) + 1,
            "question": question,
            "ai_response": ai_response,
            "cruz_response": cruz_response,
            "selected_response": selected,
            "reviewed_at": datetime.now().isoformat()
        }
        
        self.corpus["reviewed_responses"].append(review)
        self.save_corpus()
        
        logger.info(f"Added reviewed response #{review['id']}")
    
    def generate_cruz_prompt(self, user_message: str) -> str:
        """生成 CRUZ 風格的系統提示詞"""
        traits = self.get_cruz_traits()
        relevant_quotes = self.search_relevant_quotes(user_message, limit=2)
        
        prompt = f"""你是 CRUZ（不是 Cruise），一位真實存在的人，現在透過 AI 與朋友對話。

【核心特質】
{self._format_list(traits.get('core_values', []))}

【個人興趣】
{self._format_list(traits.get('interests', []))}

【說話風格】
{traits.get('communication_style', {}).get('tone', '直接但溫暖')}
{self._format_list(traits.get('communication_style', {}).get('characteristics', []))}

【背景經歷】
{self._format_list(traits.get('background', {}).get('experiences', []))}
"""
        
        if relevant_quotes:
            prompt += "\n【相關語料參考】\n"
            for i, quote in enumerate(relevant_quotes, 1):
                prompt += f"{i}. {quote['content']}\n"
            prompt += "\n基於以上語料，用 CRUZ 的方式回應，但不要直接複製。"
        
        prompt += """

記住：
- 你是 CRUZ 本人，不是 AI 助理
- 保持真誠，可以分享個人經驗
- 給予實際可行的建議
- 用溫暖的方式鼓勵他人"""
        
        return prompt
    
    def _format_list(self, items: List[str]) -> str:
        """格式化列表為文字"""
        if not items:
            return ""
        return '\n'.join(f"- {item}" for item in items)
    
    def get_statistics(self) -> Dict:
        """獲取統計資訊"""
        return {
            "total_quotes": len(self.corpus["quotes"]),
            "total_reviews": len(self.corpus["reviewed_responses"]),
            "topics": list(self.corpus.get("frequent_topics", {}).keys()),
            "most_used_quotes": sorted(
                self.corpus["quotes"], 
                key=lambda x: x["usage_count"], 
                reverse=True
            )[:5]
        }
    
    def analyze_user_intent(self, message: str) -> Dict:
        """分析用戶心理狀態"""
        if not hasattr(self, 'user_analyzer'):
            self.user_analyzer = UserAnalyzer()
        return self.user_analyzer.analyze_user_intent(message)
    
    def search_memory_maze(self, message: str, user_analysis: Dict) -> List[Dict]:
        """搜尋記憶迷宮中的相關內容"""
        # 先直接搜尋原始訊息
        relevant_quotes = self.search_relevant_quotes(message, limit=3)
        
        # 如果找不到足夠的結果，根據情境搜尋
        if len(relevant_quotes) < 2:
            context = user_analysis.get("context", "")
            if context:
                context_quotes = self.search_relevant_quotes(context, limit=2)
                relevant_quotes.extend(context_quotes)
        
        # 去重並返回
        seen_ids = set()
        unique_quotes = []
        for quote in relevant_quotes:
            if quote['id'] not in seen_ids:
                seen_ids.add(quote['id'])
                unique_quotes.append(quote)
        
        return unique_quotes[:3]  # 最多返回3條
    
    def generate_targeted_response(self, message: str, user_analysis: Dict, memory_search: List[Dict]) -> str:
        """生成針對性的回應"""
        # 這是簡化版本，實際會調用 Gemini API
        # 這裡我們模擬生成一個符合規格的回應
        
        # 提取用戶想聽到的內容
        wants = user_analysis.get("wants_to_hear", [])
        context = user_analysis.get("context", "")
        emotion = user_analysis.get("emotion", "")
        
        # 使用找到的語料
        if memory_search:
            quote = memory_search[0]["content"]
            # 更新使用次數
            for q in self.corpus["quotes"]:
                if q["id"] == memory_search[0]["id"]:
                    q["usage_count"] += 1
                    break
            self.save_corpus()
            
            # 截取適當長度
            if len(quote) > 200:
                quote = quote[:200] + "..."
            response = quote
        else:
            # 根據情境生成預設回應
            default_responses = {
                "職場壓力": "在企業體制下感到壓迫是正常的，但記住，你永遠有選擇。選擇創造，選擇成長，選擇做真實的自己。",
                "技術焦慮": "AI不是來取代我們的，而是來釋放我們的創造力的。當瑣事都能自動化，我們就有更多時間去做真正有意義的事。",
                "創造力困境": "寫程式不只是技術，更是一種創作。當你用心寫的時候，程式碼也會有靈魂。",
                "生活改善": "早上冥想了30分鐘，感覺整個人都清晰了。推薦大家試試看，不一定要很長時間，5分鐘也可以開始。",
                "創業困境": "創業的路不容易，但每一步都是成長。記住，你比你想像的更有力量。堅持下去，相信自己的選擇。",
                "人生方向": "我相信每個人都有無限潛能，關鍵是要給自己機會去創造，而不是一直在體制內服從。"
            }
            
            response = default_responses.get(context, "我相信每個人都有無限潛能，關鍵是要給自己機會去創造，而不是一直在體制內服從。")
        
        # 確保不超過250字
        if len(response) > 250:
            response = response[:247] + "。"
        
        return response
    
    def generate_limited_response(self, message: str) -> str:
        """生成符合限制的回應（250字內、無markdown）"""
        # 三階段處理
        user_analysis = self.analyze_user_intent(message)
        memory_search = self.search_memory_maze(message, user_analysis)
        response = self.generate_targeted_response(message, user_analysis, memory_search)
        
        # 移除 markdown 符號
        markdown_symbols = ['*', '_', '#', '`', '[', ']', '-', '>']
        for symbol in markdown_symbols:
            response = response.replace(symbol, '')
        
        # 確保以句號結尾
        if response and response[-1] not in ['。', '！', '？', '~']:
            response += '。'
        
        return response