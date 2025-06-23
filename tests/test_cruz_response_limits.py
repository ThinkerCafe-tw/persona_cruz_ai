"""
測試 CRUZ 回應的限制條件
確保回應符合規格：250字內、無markdown、保持人格
"""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cruz_persona_system import CruzPersonaSystem

class TestCruzResponseLimits:
    """測試 CRUZ 回應的各種限制"""
    
    def test_response_under_250_chars(self):
        """測試：回應必須在 250 字以內"""
        # Arrange
        persona = CruzPersonaSystem()
        test_messages = [
            "工作壓力很大怎麼辦",
            "如何保持創造力",
            "AI會取代人類嗎",
            "創業好難想放棄"
        ]
        
        # Act & Assert
        for message in test_messages:
            response = persona.generate_limited_response(message)
            assert len(response) <= 250, f"回應超過250字: {len(response)}字"
    
    def test_no_markdown_symbols(self):
        """測試：回應不能包含 markdown 符號"""
        # Arrange
        persona = CruzPersonaSystem()
        markdown_symbols = ['*', '_', '#', '`', '[', ']', '!', '-', '>']
        message = "請給我一些建議"
        
        # Act
        response = persona.generate_limited_response(message)
        
        # Assert
        for symbol in markdown_symbols:
            # 允許句號、逗號、問號、驚嘆號
            if symbol not in ['!']:
                assert symbol not in response, f"回應包含 markdown 符號: {symbol}"
    
    def test_maintains_cruz_personality(self):
        """測試：回應保持 CRUZ 的人格特質"""
        # Arrange
        persona = CruzPersonaSystem()
        cruz_traits = ["創造", "真誠", "鼓勵", "經驗分享"]
        message = "我對未來感到迷茫"
        
        # Act
        response = persona.generate_limited_response(message)
        
        # Assert
        # 至少包含一個 CRUZ 特質相關詞彙
        trait_found = any(trait in response for trait in cruz_traits)
        assert trait_found, "回應未展現 CRUZ 人格特質"
    
    def test_no_ai_assistant_language(self):
        """測試：不使用 AI 助理的語言"""
        # Arrange
        persona = CruzPersonaSystem()
        ai_phrases = [
            "我是AI", "我是助理", "我無法", "我不能",
            "作為AI", "身為助理", "程式限制"
        ]
        message = "你是誰？"
        
        # Act
        response = persona.generate_limited_response(message)
        
        # Assert
        for phrase in ai_phrases:
            assert phrase not in response, f"回應包含 AI 助理用語: {phrase}"
    
    def test_response_coherence(self):
        """測試：回應的連貫性和完整性"""
        # Arrange
        persona = CruzPersonaSystem()
        message = "如何在壓力下保持創造力？"
        
        # Act
        response = persona.generate_limited_response(message)
        
        # Assert
        # 檢查基本的句子完整性
        assert response.strip(), "回應不能為空"
        assert response[-1] in ['。', '！', '？', '~'], "回應應以適當標點結尾"
        assert len(response.split('。')) >= 2, "回應應包含至少兩個完整句子"
    
    def test_response_relevance(self):
        """測試：回應與問題的相關性"""
        # Arrange
        persona = CruzPersonaSystem()
        test_cases = [
            ("冥想有用嗎", ["冥想", "呼吸", "清晰", "練習"]),
            ("創業很難", ["創業", "堅持", "收入", "相信"]),
            ("程式設計", ["程式", "創作", "程式碼", "技術"])
        ]
        
        # Act & Assert
        for message, keywords in test_cases:
            response = persona.generate_limited_response(message)
            keyword_found = any(keyword in response for keyword in keywords)
            assert keyword_found, f"回應與問題 '{message}' 不相關"
    
    def test_three_stage_prompt_integration(self):
        """測試：三段式提示詞的整合"""
        # Arrange
        persona = CruzPersonaSystem()
        message = "工作壓力大，不知道該怎麼辦"
        
        # Act
        # 應該要有三個階段的處理
        user_analysis = persona.analyze_user_intent(message)
        memory_search = persona.search_memory_maze(message, user_analysis)
        final_response = persona.generate_targeted_response(
            message, user_analysis, memory_search
        )
        
        # Assert
        assert isinstance(user_analysis, dict), "用戶分析應返回字典"
        assert len(memory_search) > 0, "記憶搜尋應返回結果"
        assert len(final_response) <= 250, "最終回應不超過250字"
        assert final_response != "", "最終回應不能為空"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])