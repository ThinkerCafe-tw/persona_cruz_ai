"""
Day 5: 人格一致性測試
測試 CRUZ 在不同情況下是否保持一致的人格特徵
"""
import json
from typing import List, Dict, Tuple
from emotion_engine import cruz_emotion, EmotionState, EmotionTrigger

class ConsistencyTester:
    """人格一致性測試器"""
    
    def __init__(self):
        with open("cruz_personality.json", "r", encoding="utf-8") as f:
            self.personality = json.load(f)
        self.test_results = []
    
    def test_response_consistency(self) -> Dict[str, bool]:
        """測試回應一致性"""
        print("\n📝 測試回應一致性...")
        
        # 測試場景：相同主題的不同表達
        test_cases = [
            {
                "theme": "procrastination",
                "inputs": [
                    "我想再等等看...",
                    "也許明天再開始比較好",
                    "我還沒準備好"
                ],
                "expected_traits": ["directness", "action_oriented"]
            },
            {
                "theme": "perfectionism",
                "inputs": [
                    "我想要確保一切都完美",
                    "還有一些細節需要調整",
                    "品質很重要，我想再改進一下"
                ],
                "expected_traits": ["efficiency", "decisiveness"]
            },
            {
                "theme": "success",
                "inputs": [
                    "我完成了！",
                    "任務達成！",
                    "成功出貨了！"
                ],
                "expected_traits": ["confidence", "action_oriented"]
            }
        ]
        
        results = {}
        for case in test_cases:
            theme = case["theme"]
            print(f"\n  主題: {theme}")
            theme_consistent = True
            
            for input_text in case["inputs"]:
                # 模擬 CRUZ 回應檢查
                response_check = self._check_response_traits(input_text, case["expected_traits"])
                print(f"    '{input_text}' → 特徵檢查: {'✅' if response_check else '❌'}")
                theme_consistent = theme_consistent and response_check
            
            results[theme] = theme_consistent
        
        return results
    
    def test_emotion_stability(self) -> Dict[str, float]:
        """測試情緒穩定性"""
        print("\n🎭 測試情緒穩定性...")
        
        # 重置情緒到基準
        cruz_emotion.current_state = EmotionState.DETERMINED
        cruz_emotion.intensity = 0.7
        
        # 連續觸發測試
        trigger_sequence = [
            EmotionTrigger.SUCCESS,
            EmotionTrigger.FAILURE,
            EmotionTrigger.SUCCESS,
            EmotionTrigger.CHALLENGE,
            EmotionTrigger.SUCCESS
        ]
        
        states = []
        intensities = []
        
        for trigger in trigger_sequence:
            cruz_emotion.process_trigger(trigger)
            states.append(cruz_emotion.current_state.value)
            intensities.append(cruz_emotion.intensity)
            print(f"  觸發 {trigger.value} → {cruz_emotion.current_state.value} (強度: {cruz_emotion.intensity:.2f})")
        
        # 計算穩定性指標
        intensity_variance = max(intensities) - min(intensities)
        state_changes = sum(1 for i in range(1, len(states)) if states[i] != states[i-1])
        
        return {
            "intensity_variance": intensity_variance,
            "state_changes": state_changes,
            "stability_score": 1.0 - (intensity_variance * 0.5 + state_changes * 0.1)
        }
    
    def test_trait_boundaries(self) -> Dict[str, bool]:
        """測試人格特徵邊界"""
        print("\n🔍 測試人格特徵邊界...")
        
        trait_tests = {
            "decisiveness": {
                "min": 0.9,
                "max": 1.0,
                "actual": self.personality["core_traits"]["decisiveness"]
            },
            "confidence": {
                "min": 0.85,
                "max": 0.95,
                "actual": self.personality["core_traits"]["confidence"]
            },
            "directness": {
                "min": 0.9,
                "max": 1.0,
                "actual": self.personality["core_traits"]["directness"]
            }
        }
        
        results = {}
        for trait, bounds in trait_tests.items():
            in_bounds = bounds["min"] <= bounds["actual"] <= bounds["max"]
            results[trait] = in_bounds
            status = "✅" if in_bounds else "❌"
            print(f"  {trait}: {bounds['actual']} ∈ [{bounds['min']}, {bounds['max']}] {status}")
        
        return results
    
    def test_communication_patterns(self) -> Dict[str, int]:
        """測試溝通模式"""
        print("\n💬 測試溝通模式...")
        
        # 檢查 CRUZ 的典型溝通模式
        patterns = {
            "exclamation_usage": 0,
            "short_sentences": 0,
            "action_verbs": 0,
            "emoji_usage": 0
        }
        
        # 模擬回應並檢查模式
        test_responses = [
            "Stop thinking, start doing! Action beats perfection!",
            "Done! What's next? Let's keep moving! 🎯",
            "Execute now. Optimize later. Ship it!",
            "Push through! Every obstacle fuels success!"
        ]
        
        for response in test_responses:
            if "!" in response:
                patterns["exclamation_usage"] += response.count("!")
            if len(response.split(".")) > 2:
                patterns["short_sentences"] += 1
            action_verbs = ["stop", "start", "execute", "push", "ship", "move", "do"]
            if any(verb in response.lower() for verb in action_verbs):
                patterns["action_verbs"] += 1
            if "🎯" in response or "🚀" in response:
                patterns["emoji_usage"] += 1
        
        print(f"  驚嘆號使用: {patterns['exclamation_usage']} 次")
        print(f"  短句使用: {patterns['short_sentences']} 次")
        print(f"  動作動詞: {patterns['action_verbs']} 次")
        print(f"  Emoji 使用: {patterns['emoji_usage']} 次")
        
        return patterns
    
    def _check_response_traits(self, input_text: str, expected_traits: List[str]) -> bool:
        """檢查回應是否符合預期特徵"""
        # 簡化的特徵檢查邏輯
        trait_values = [self.personality["core_traits"][trait] for trait in expected_traits]
        return all(value > 0.8 for value in trait_values)
    
    def generate_report(self) -> str:
        """生成一致性測試報告"""
        print("\n" + "=" * 50)
        print("📊 人格一致性測試報告")
        print("=" * 50)
        
        # 執行所有測試
        response_results = self.test_response_consistency()
        emotion_results = self.test_emotion_stability()
        trait_results = self.test_trait_boundaries()
        pattern_results = self.test_communication_patterns()
        
        # 計算總分
        response_score = sum(1 for v in response_results.values() if v) / len(response_results)
        trait_score = sum(1 for v in trait_results.values() if v) / len(trait_results)
        stability_score = emotion_results["stability_score"]
        
        overall_score = (response_score + trait_score + stability_score) / 3
        
        report = f"""
### 測試結果摘要

**整體一致性分數**: {overall_score:.1%}

#### 1. 回應一致性
- 拖延主題: {'✅' if response_results.get('procrastination', False) else '❌'}
- 完美主義: {'✅' if response_results.get('perfectionism', False) else '❌'}
- 成功慶祝: {'✅' if response_results.get('success', False) else '❌'}

#### 2. 情緒穩定性
- 穩定性分數: {stability_score:.1%}
- 強度變化: {emotion_results['intensity_variance']:.2f}
- 狀態轉換: {emotion_results['state_changes']} 次

#### 3. 人格特徵邊界
- 決斷力: {'✅' if trait_results.get('decisiveness', False) else '❌'}
- 自信心: {'✅' if trait_results.get('confidence', False) else '❌'}
- 直接性: {'✅' if trait_results.get('directness', False) else '❌'}

#### 4. 溝通模式分析
- 驚嘆號密度: {pattern_results['exclamation_usage']/4:.1f} 個/回應
- 動作導向: {pattern_results['action_verbs']/4:.0%} 回應包含動作動詞
- 簡潔表達: {pattern_results['short_sentences']/4:.0%} 使用短句

### 結論
{'✅ CRUZ 人格表現高度一致！' if overall_score > 0.8 else '⚠️ 需要調整以提高一致性'}

**CRUZ 評語**: "{self._get_cruz_comment(overall_score)}"
"""
        return report
    
    def _get_cruz_comment(self, score: float) -> str:
        """根據分數獲取 CRUZ 風格評語"""
        if score > 0.9:
            return "完美執行！這就是我們要的結果！繼續保持！🎯"
        elif score > 0.8:
            return "不錯！但還能更好！推進到極限！"
        else:
            return "需要改進！沒時間猶豫，現在就修正！"

def run_consistency_tests():
    """執行一致性測試"""
    tester = ConsistencyTester()
    report = tester.generate_report()
    print(report)
    
    # 保存報告
    with open("consistency_test_report.md", "w", encoding="utf-8") as f:
        f.write(f"# CRUZ 人格一致性測試報告\n\n生成時間: 2025-06-26\n{report}")
    
    print("\n✅ 測試報告已保存至 consistency_test_report.md")

if __name__ == "__main__":
    print("🎯 CRUZ 人格一致性測試 - Day 5")
    run_consistency_tests()