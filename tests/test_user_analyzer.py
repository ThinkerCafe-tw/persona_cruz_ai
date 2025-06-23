"""
用戶心理分析器的測試案例
遵循 TDD：先寫測試，再寫實作
"""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 這個 import 現在應該成功了（綠燈階段）
from user_analyzer import UserAnalyzer

class TestUserAnalyzer:
    """測試用戶心理分析功能"""
    
    def test_analyze_work_stress(self):
        """測試：分析工作壓力類型的訊息"""
        # Arrange
        analyzer = UserAnalyzer()
        message = "工作壓力好大，每天加班到很晚，不知道該怎麼辦"
        
        # Act
        result = analyzer.analyze_user_intent(message)
        
        # Assert
        assert result["emotion"] in ["焦慮", "疲憊", "無助"]
        assert result["intent"] == "尋求建議"
        assert "鼓勵" in result["wants_to_hear"]
        assert "工作生活平衡" in result["wants_to_hear"]
        assert "被否定" in result["fears"]
        assert result["context"] == "職場壓力"
    
    def test_analyze_ai_replacement_fear(self):
        """測試：分析 AI 取代恐懼"""
        # Arrange
        analyzer = UserAnalyzer()
        message = "AI 會不會取代我的工作？我是程式設計師，好擔心"
        
        # Act
        result = analyzer.analyze_user_intent(message)
        
        # Assert
        assert result["emotion"] in ["擔憂", "恐懼"]
        assert result["intent"] == "尋求確認"
        assert "AI 協作" in result["wants_to_hear"]
        assert "技能提升建議" in result["wants_to_hear"]
        assert "被取代" in result["fears"]
        assert result["context"] == "技術焦慮"
    
    def test_analyze_creativity_request(self):
        """測試：分析創造力相關問題"""
        # Arrange
        analyzer = UserAnalyzer()
        message = "如何保持創造力？感覺最近都沒有新想法"
        
        # Act
        result = analyzer.analyze_user_intent(message)
        
        # Assert
        assert result["emotion"] in ["困惑", "停滯"]
        assert result["intent"] == "尋求方法"
        assert "具體技巧" in result["wants_to_hear"]
        assert "靈感來源" in result["wants_to_hear"]
        assert "創意枯竭" in result["fears"]
        assert result["context"] == "創造力困境"
    
    def test_analyze_meditation_curiosity(self):
        """測試：分析冥想相關詢問"""
        # Arrange
        analyzer = UserAnalyzer()
        message = "冥想真的有用嗎？你都怎麼冥想的？"
        
        # Act
        result = analyzer.analyze_user_intent(message)
        
        # Assert
        assert result["emotion"] in ["好奇", "懷疑"]
        assert result["intent"] == "尋求經驗分享"
        assert "個人經驗" in result["wants_to_hear"]
        assert "實際效果" in result["wants_to_hear"]
        assert "浪費時間" in result["fears"]
        assert result["context"] == "生活改善"
    
    def test_analyze_entrepreneurship_struggle(self):
        """測試：分析創業困境"""
        # Arrange
        analyzer = UserAnalyzer()
        message = "創業第100天了，還是沒有收入，好想放棄"
        
        # Act
        result = analyzer.analyze_user_intent(message)
        
        # Assert
        assert result["emotion"] in ["沮喪", "疲憊", "迷茫"]
        assert result["intent"] == "尋求支持"
        assert "同理心" in result["wants_to_hear"]
        assert "堅持的理由" in result["wants_to_hear"]
        assert "失敗" in result["fears"]
        assert "浪費時間" in result["fears"]
        assert result["context"] == "創業困境"
    
    def test_emotion_detection_accuracy(self):
        """測試：情緒檢測的準確性"""
        # Arrange
        analyzer = UserAnalyzer()
        test_cases = [
            ("好開心！終於成功了！", ["開心", "興奮", "成就感"]),
            ("不知道為什麼，就是覺得很累", ["疲憊", "迷茫", "低落"]),
            ("這樣做對嗎？我不確定", ["困惑", "不確定", "猶豫"])
        ]
        
        # Act & Assert
        for message, expected_emotions in test_cases:
            result = analyzer.analyze_user_intent(message)
            assert result["emotion"] in expected_emotions
    
    def test_intent_classification(self):
        """測試：意圖分類的準確性"""
        # Arrange
        analyzer = UserAnalyzer()
        test_cases = [
            ("該怎麼做比較好？", "尋求建議"),
            ("你覺得這樣對嗎？", "尋求確認"),
            ("能不能教我？", "尋求指導"),
            ("我只是想說說話", "情緒抒發"),
            ("你有類似經驗嗎？", "尋求經驗分享")
        ]
        
        # Act & Assert
        for message, expected_intent in test_cases:
            result = analyzer.analyze_user_intent(message)
            assert result["intent"] == expected_intent

# 執行測試時會失敗（紅燈），因為 UserAnalyzer 還不存在
if __name__ == "__main__":
    pytest.main([__file__, "-v"])