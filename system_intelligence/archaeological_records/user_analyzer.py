"""
用戶心理分析器
分析用戶訊息的情緒、意圖、期待和恐懼
"""
import re
from typing import Dict, List

class UserAnalyzer:
    """分析用戶心理狀態的工具"""
    
    def __init__(self):
        # 情緒關鍵詞映射
        self.emotion_keywords = {
            "焦慮": ["壓力", "擔心", "不安", "緊張", "害怕"],
            "疲憊": ["累", "疲倦", "沒力", "耗盡", "加班"],
            "無助": ["不知道", "怎麼辦", "沒辦法", "無力"],
            "擔憂": ["擔心", "害怕", "恐懼", "會不會"],
            "恐懼": ["怕", "恐懼", "擔心", "害怕"],
            "困惑": ["不懂", "為什麼", "如何", "怎麼"],
            "停滯": ["沒有", "停", "卡住", "不動"],
            "好奇": ["真的嗎", "是嗎", "怎麼樣"],
            "懷疑": ["真的", "有用嗎", "可以嗎"],
            "沮喪": ["失望", "難過", "想放棄", "失敗"],
            "迷茫": ["不知道", "迷失", "方向", "迷茫"],
            "開心": ["開心", "高興", "成功", "太好了"],
            "興奮": ["興奮", "期待", "太棒了", "終於"],
            "成就感": ["成功", "做到", "完成", "達成"],
            "低落": ["低落", "沮喪", "不開心", "難過"],
            "不確定": ["不確定", "不知道", "或許", "可能"],
            "猶豫": ["猶豫", "要不要", "該不該", "是否"]
        }
        
        # 意圖分類關鍵詞
        self.intent_keywords = {
            "尋求建議": ["怎麼辦", "該怎麼", "建議"],
            "尋求確認": ["對嗎", "是嗎", "可以嗎", "這樣好嗎", "會不會", "會嗎"],
            "尋求指導": ["教我", "怎麼做", "步驟", "方法"],
            "情緒抒發": ["只是想", "想說", "覺得", "感覺"],
            "尋求經驗分享": ["你會", "你都", "你的經驗", "類似經驗", "怎麼冥想"],
            "尋求支持": ["想放棄", "撐不下去", "好難", "加油"],
            "尋求方法": ["如何", "怎麼", "方法", "技巧"]
        }
        
        # 情境分類
        self.context_keywords = {
            "職場壓力": ["工作", "加班", "老闆", "同事", "公司", "職場"],
            "技術焦慮": ["AI", "程式", "技術", "取代", "工程師"],
            "創造力困境": ["創造", "想法", "靈感", "創意", "創新"],
            "生活改善": ["冥想", "運動", "生活", "習慣", "改變"],
            "創業困境": ["創業", "收入", "公司", "產品", "客戶"],
            "人生方向": ["未來", "方向", "目標", "人生", "意義"]
        }
    
    def analyze_user_intent(self, message: str) -> Dict[str, any]:
        """分析用戶的心理狀態"""
        message_lower = message.lower()
        
        # 檢測情緒
        emotion = self._detect_emotion(message_lower)
        
        # 檢測意圖
        intent = self._detect_intent(message_lower)
        
        # 預測用戶想聽到什麼
        wants_to_hear = self._predict_wants(message_lower, emotion, intent)
        
        # 識別用戶的恐懼
        fears = self._identify_fears(message_lower, emotion)
        
        # 判斷情境
        context = self._detect_context(message_lower)
        
        return {
            "emotion": emotion,
            "intent": intent,
            "wants_to_hear": wants_to_hear,
            "fears": fears,
            "context": context
        }
    
    def _detect_emotion(self, message: str) -> str:
        """檢測訊息中的主要情緒"""
        # 優先檢查特定模式
        if "想放棄" in message:
            return "沮喪"
        if "沒有新想法" in message or "都沒有新想法" in message:
            return "停滯"
        
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message)
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            return max(emotion_scores, key=emotion_scores.get)
        
        return "中性"
    
    def _detect_intent(self, message: str) -> str:
        """檢測用戶的意圖"""
        # 優先檢查特定模式
        if "如何" in message and not "怎麼" in message:
            return "尋求方法"
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    return intent
        
        return "一般對話"
    
    def _predict_wants(self, message: str, emotion: str, intent: str) -> List[str]:
        """預測用戶想聽到什麼"""
        wants = []
        
        # 根據情緒添加期待
        emotion_wants = {
            "焦慮": ["鼓勵", "工作生活平衡", "具體建議"],
            "疲憊": ["理解", "休息建議", "工作生活平衡"],
            "無助": ["方向指引", "鼓勵", "具體步驟", "工作生活平衡"],
            "擔憂": ["安慰", "實際分析", "正面觀點", "技能提升建議"],
            "恐懼": ["安全感", "實際案例", "技能提升建議"],
            "困惑": ["清晰解釋", "具體方法", "個人經驗", "靈感來源"],
            "停滯": ["突破方法", "新觀點", "靈感來源", "同理心", "堅持的理由"],
            "好奇": ["個人經驗", "實際效果", "具體做法"],
            "懷疑": ["真實案例", "科學依據", "個人體驗", "個人經驗", "實際效果"],
            "沮喪": ["同理心", "成功案例", "堅持的理由"],
            "迷茫": ["方向建議", "人生經驗", "價值確認"]
        }
        
        if emotion in emotion_wants:
            wants.extend(emotion_wants[emotion])
        else:
            # 加上預設的期待
            wants.extend(["理解", "支持"])
        
        # 根據意圖添加期待
        intent_wants = {
            "尋求建議": ["具體步驟", "實用建議"],
            "尋求確認": ["肯定", "支持", "技能提升建議"],
            "尋求指導": ["詳細步驟", "個人經驗"],
            "尋求經驗分享": ["真實故事", "個人體會", "個人經驗"],
            "尋求支持": ["同理心", "鼓勵"],
            "尋求方法": ["具體技巧", "實際做法"]
        }
        
        if intent in intent_wants:
            wants.extend(intent_wants[intent])
        
        # 特殊關鍵詞
        if "ai" in message.lower():
            wants.append("AI 協作")
        if "創" in message:
            wants.append("創造力啟發")
        
        return list(set(wants))  # 去重
    
    def _identify_fears(self, message: str, emotion: str) -> List[str]:
        """識別用戶的恐懼"""
        fears = []
        
        # 基於關鍵詞的恐懼
        fear_keywords = {
            "被取代": ["取代", "失業", "沒用"],
            "失敗": ["失敗", "做不到", "放棄"],
            "被否定": ["不好", "不對", "錯誤"],
            "浪費時間": ["浪費", "沒用", "白費"],
            "創意枯竭": ["沒想法", "沒靈感", "想不出", "沒有新想法"],
            "停滯": ["沒有", "沒", "停"]
        }
        
        for fear, keywords in fear_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    fears.append(fear)
        
        # 基於情緒的恐懼
        emotion_fears = {
            "焦慮": ["被否定", "做不好"],
            "擔憂": ["失敗", "被取代"],
            "恐懼": ["未知", "改變"],
            "沮喪": ["失敗", "浪費時間"],
            "無助": ["被否定", "失敗"],
            "疲憊": ["做不好", "被否定"],
            "好奇": ["浪費時間"],
            "懷疑": ["浪費時間"]
        }
        
        if emotion in emotion_fears:
            fears.extend(emotion_fears[emotion])
        
        return list(set(fears))  # 去重
    
    def _detect_context(self, message: str) -> str:
        """檢測訊息的情境"""
        context_scores = {}
        
        for context, keywords in self.context_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message)
            if score > 0:
                context_scores[context] = score
        
        if context_scores:
            return max(context_scores, key=context_scores.get)
        
        return "一般對話"