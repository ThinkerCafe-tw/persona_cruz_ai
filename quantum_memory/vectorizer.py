"""
量子記憶向量化模組
將量子態和文字內容轉換為向量表示
"""
import logging
import hashlib
import numpy as np
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from datetime import datetime

logger = logging.getLogger(__name__)


class QuantumVectorizer:
    """量子記憶向量化器"""
    
    def __init__(self, model_name: str = "models/embedding-001"):
        """
        初始化向量化器
        
        Args:
            model_name: Gemini embedding 模型名稱
        """
        self.model_name = model_name
        self._embedding_cache = {}  # 簡單的快取機制
        
    def vectorize_identity(self, identity: Dict[str, Any]) -> List[float]:
        """
        將量子身份轉換為5維向量
        
        向量結構：[phase, frequency, amplitude, coherence, essence_hash]
        """
        # 將 essence 轉換為 0-1 之間的數值
        essence_hash = hashlib.md5(identity.get('essence', '').encode()).hexdigest()
        essence_value = int(essence_hash[:8], 16) / 0xFFFFFFFF  # 正規化到 0-1
        
        vector = [
            identity.get('phase', 0.0),
            identity.get('frequency', 1.0),
            identity.get('amplitude', 1.0),
            identity.get('coherence', 1.0),
            essence_value
        ]
        
        return vector
    
    def vectorize_text(self, text: str, use_cache: bool = True) -> Optional[List[float]]:
        """
        使用 Gemini embedding API 將文字轉換為向量
        
        Args:
            text: 要向量化的文字
            use_cache: 是否使用快取
            
        Returns:
            384 維的向量，失敗時返回 None
        """
        if use_cache and text in self._embedding_cache:
            return self._embedding_cache[text]
        
        try:
            # 使用 Gemini embedding API
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            
            embedding = result['embedding']
            
            # 快取結果
            if use_cache:
                self._embedding_cache[text] = embedding
                
            return embedding
            
        except Exception as e:
            logger.error(f"文字向量化失敗: {e}")
            # 返回隨機向量作為後備方案
            return self._generate_fallback_vector(text)
    
    def _generate_fallback_vector(self, text: str) -> List[float]:
        """
        當 API 失敗時生成後備向量
        使用文字的統計特徵生成確定性的向量
        """
        # 基於文字內容生成種子
        seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        np.random.seed(seed)
        
        # 生成 384 維向量
        vector = np.random.randn(384) * 0.1
        
        # 加入一些文字特徵
        features = [
            len(text) / 1000.0,  # 文字長度
            text.count(' ') / 100.0,  # 單詞數
            text.count('\n') / 10.0,  # 行數
            len(set(text)) / 256.0,  # 字符多樣性
        ]
        
        # 將特徵混入向量的前幾個維度
        for i, feature in enumerate(features):
            if i < len(vector):
                vector[i] = np.clip(feature, -1, 1)
        
        return vector.tolist()
    
    def vectorize_event(self, event: Dict[str, Any]) -> Optional[List[float]]:
        """
        將事件轉換為向量
        
        Args:
            event: 事件資料
            
        Returns:
            384 維向量
        """
        # 組合事件的關鍵資訊
        event_text_parts = []
        
        # 事件類型
        if 'type' in event:
            event_text_parts.append(f"類型: {event['type']}")
        
        # 事件內容
        if 'content' in event:
            event_text_parts.append(f"內容: {event['content']}")
        elif 'message' in event:
            event_text_parts.append(f"訊息: {event['message']}")
        
        # 事件標籤
        if 'tags' in event and isinstance(event['tags'], list):
            event_text_parts.append(f"標籤: {', '.join(event['tags'])}")
        
        # 事件影響
        if 'impact' in event:
            event_text_parts.append(f"影響程度: {event['impact']}")
        
        # 事件來源
        if 'source' in event:
            event_text_parts.append(f"來源: {event['source']}")
        
        # 組合成完整文字
        event_text = '\n'.join(event_text_parts)
        
        return self.vectorize_text(event_text)
    
    def vectorize_concept(self, concept: str, possibilities: List[Dict] = None) -> Optional[List[float]]:
        """
        將概念和其可能性轉換為向量
        
        Args:
            concept: 概念名稱
            possibilities: 可能性列表
            
        Returns:
            384 維向量
        """
        # 組合概念資訊
        concept_parts = [f"概念: {concept}"]
        
        if possibilities:
            # 加入主要的可能性描述
            sorted_possibilities = sorted(
                possibilities,
                key=lambda p: p.get('probability', 0),
                reverse=True
            )[:3]  # 只取前三個最可能的
            
            for p in sorted_possibilities:
                desc = p.get('description', '')
                prob = p.get('probability', 0)
                concept_parts.append(f"可能性 ({prob:.2f}): {desc}")
        
        concept_text = '\n'.join(concept_parts)
        
        return self.vectorize_text(concept_text)
    
    def calculate_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """
        計算兩個向量的餘弦相似度
        
        Args:
            vector1: 第一個向量
            vector2: 第二個向量
            
        Returns:
            相似度分數 (0-1)
        """
        if len(vector1) != len(vector2):
            logger.error(f"向量維度不匹配: {len(vector1)} vs {len(vector2)}")
            return 0.0
        
        # 轉換為 numpy 陣列
        v1 = np.array(vector1)
        v2 = np.array(vector2)
        
        # 計算餘弦相似度
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        # 正規化到 0-1
        return (similarity + 1) / 2
    
    def find_resonance_concepts(self, 
                              event_vector: List[float],
                              concept_vectors: Dict[str, List[float]],
                              threshold: float = 0.7) -> List[tuple]:
        """
        找出與事件產生共振的概念
        
        Args:
            event_vector: 事件向量
            concept_vectors: 概念向量字典 {概念名稱: 向量}
            threshold: 共振閾值
            
        Returns:
            [(概念名稱, 相似度分數)] 的列表
        """
        resonances = []
        
        for concept, vector in concept_vectors.items():
            similarity = self.calculate_similarity(event_vector, vector)
            if similarity >= threshold:
                resonances.append((concept, similarity))
        
        # 按相似度排序
        resonances.sort(key=lambda x: x[1], reverse=True)
        
        return resonances
    
    def merge_vectors(self, vectors: List[List[float]], weights: Optional[List[float]] = None) -> List[float]:
        """
        合併多個向量
        
        Args:
            vectors: 向量列表
            weights: 權重列表（可選）
            
        Returns:
            合併後的向量
        """
        if not vectors:
            return []
        
        if weights is None:
            weights = [1.0] * len(vectors)
        
        # 確保權重總和為 1
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        
        # 加權平均
        result = np.zeros(len(vectors[0]))
        for vector, weight in zip(vectors, weights):
            result += np.array(vector) * weight
        
        return result.tolist()
    
    def clear_cache(self):
        """清除向量快取"""
        self._embedding_cache.clear()
        logger.info("向量快取已清除")