import { OllamaService } from '../llm/OllamaService.js';

export interface MemoryEvaluation {
  score: number;           // 0-1，記憶重要性評分
  reason: string;          // 評分原因
  category: string;        // 重新分類
  suggested_layer: string; // 建議的存儲層級
  promotion_ready: boolean; // 是否可以晉升
  patterns: string[];      // 發現的模式
}

export class MemoryGradientEvaluator {
  private ollama: OllamaService;
  
  // 評估權重
  private weights = {
    has_lesson: 0.3,        // 包含教訓
    reusable_pattern: 0.25, // 可重複應用的模式
    paradigm_shift: 0.2,    // 認知框架改變
    cross_project: 0.15,    // 跨專案價值
    emotional_impact: 0.1   // 情緒影響
  };

  constructor(ollama: OllamaService) {
    this.ollama = ollama;
  }

  async evaluate(memory: any): Promise<MemoryEvaluation> {
    // 多維度評估
    const [
      llmAnalysis,
      patternScore,
      temporalScore,
      contextScore
    ] = await Promise.all([
      this.getLLMAnalysis(memory),
      this.analyzePatterns(memory),
      this.evaluateTemporalValue(memory),
      this.evaluateContext(memory)
    ]);

    // 綜合評分
    const finalScore = this.calculateFinalScore({
      llm: llmAnalysis.score,
      pattern: patternScore,
      temporal: temporalScore,
      context: contextScore
    });

    return {
      score: finalScore,
      reason: this.generateReason(llmAnalysis, patternScore, temporalScore, contextScore),
      category: llmAnalysis.category,
      suggested_layer: this.suggestLayer(finalScore, memory),
      promotion_ready: this.isPromotionReady(finalScore, memory),
      patterns: await this.extractPatterns(memory)
    };
  }

  private async getLLMAnalysis(memory: any): Promise<{
    score: number;
    reason: string;
    category: string;
  }> {
    try {
      return await this.ollama.analyzeMemoryImportance(memory);
    } catch (error) {
      console.error('LLM 分析失敗，使用規則引擎:', error);
      return this.fallbackRuleBasedAnalysis(memory);
    }
  }

  private fallbackRuleBasedAnalysis(memory: any): {
    score: number;
    reason: string;
    category: string;
  } {
    let score = 0.5; // 基礎分數
    const reasons = [];

    // 關鍵詞分析
    const content = memory.content.toLowerCase();
    const keywords = {
      high_importance: ['教訓', '錯誤', '失敗', '突破', '發現', '洞察', '領悟'],
      medium_importance: ['學習', '改進', '優化', '修復', '實現'],
      low_importance: ['測試', '運行', '檢查', '確認']
    };

    // 檢查高重要性關鍵詞
    const highMatches = keywords.high_importance.filter(kw => content.includes(kw));
    if (highMatches.length > 0) {
      score += 0.3;
      reasons.push(`包含重要關鍵詞: ${highMatches.join(', ')}`);
    }

    // 檢查人格參與度
    if (memory.persona && memory.persona !== '系統') {
      score += 0.1;
      reasons.push('有明確的人格歸屬');
    }

    // 檢查標籤豐富度
    if (memory.tags && memory.tags.length > 2) {
      score += 0.1;
      reasons.push('標籤豐富，涵蓋多個維度');
    }

    // 檢查內容長度（適中的長度通常包含更多信息）
    if (memory.content.length > 100 && memory.content.length < 1000) {
      score += 0.1;
      reasons.push('內容長度適中，信息密度較高');
    }

    return {
      score: Math.min(score, 1.0),
      reason: reasons.join('; ') || '自動評估',
      category: memory.category || 'general'
    };
  }

  private async analyzePatterns(memory: any): Promise<number> {
    // 分析記憶中的模式
    const content = memory.content.toLowerCase();
    
    // 檢查是否包含可重複的模式
    const patterns = [
      /if.*then.*else/g,           // 條件邏輯
      /\d+\.\s+/g,                 // 步驟列表
      /\b(always|never|每次|永遠)\b/g, // 絕對性描述
      /\b(模式|pattern|規律)\b/g,   // 明確提到模式
    ];

    let patternScore = 0;
    patterns.forEach(pattern => {
      const matches = content.match(pattern);
      if (matches) {
        patternScore += Math.min(matches.length * 0.1, 0.3);
      }
    });

    return Math.min(patternScore, 1.0);
  }

  private async evaluateTemporalValue(memory: any): Promise<number> {
    // 評估記憶的時間價值
    const now = new Date();
    const memoryTime = new Date(memory.timestamp || memory.created_at);
    const ageInHours = (now.getTime() - memoryTime.getTime()) / (1000 * 60 * 60);

    // 新鮮的記憶可能還需要時間驗證
    if (ageInHours < 1) return 0.3;
    
    // 1-24小時：觀察期
    if (ageInHours < 24) return 0.5;
    
    // 1-7天：證明價值期
    if (ageInHours < 168) return 0.7;
    
    // 超過一週：經過時間考驗
    return 0.9;
  }

  private async evaluateContext(memory: any): Promise<number> {
    // 評估記憶的上下文價值
    let contextScore = 0.5;

    // 檢查是否是錯誤修復記錄
    if (memory.category === 'bug' || memory.category === 'fix') {
      contextScore += 0.2;
    }

    // 檢查是否是架構決策
    if (memory.category === 'architecture' || memory.category === 'decision') {
      contextScore += 0.3;
    }

    // 檢查是否是學習心得
    if (memory.category === 'learning' || memory.category === 'insight') {
      contextScore += 0.25;
    }

    return Math.min(contextScore, 1.0);
  }

  private calculateFinalScore(scores: {
    llm: number;
    pattern: number;
    temporal: number;
    context: number;
  }): number {
    // 加權平均
    const weights = {
      llm: 0.4,      // LLM 分析最重要
      pattern: 0.25, // 模式識別
      temporal: 0.2, // 時間因素
      context: 0.15  // 上下文
    };

    return (
      scores.llm * weights.llm +
      scores.pattern * weights.pattern +
      scores.temporal * weights.temporal +
      scores.context * weights.context
    );
  }

  private generateReason(
    llmAnalysis: any,
    patternScore: number,
    temporalScore: number,
    contextScore: number
  ): string {
    const reasons = [llmAnalysis.reason];

    if (patternScore > 0.3) {
      reasons.push('包含可重複應用的模式');
    }

    if (temporalScore > 0.7) {
      reasons.push('經過時間驗證的價值');
    }

    if (contextScore > 0.7) {
      reasons.push('在當前上下文中具有重要意義');
    }

    return reasons.filter(r => r).join('; ');
  }

  private suggestLayer(score: number, memory: any): string {
    // 根據評分建議存儲層級
    if (score >= 0.8) {
      return 'meta';    // 元記憶：跨專案的永恆智慧
    } else if (score >= 0.5) {
      return 'sparse';  // 稀疏記憶：專案級的重要模式
    } else {
      return 'main';    // 主記憶：日常操作記錄
    }
  }

  private isPromotionReady(score: number, memory: any): boolean {
    const currentLayer = memory.layer || 'main';
    const suggestedLayer = this.suggestLayer(score, memory);
    
    // 只有建議層級高於當前層級才可以晉升
    const layerOrder = { main: 1, sparse: 2, meta: 3 };
    return layerOrder[suggestedLayer] > layerOrder[currentLayer];
  }

  private async extractPatterns(memory: any): Promise<string[]> {
    const content = memory.content.toLowerCase();
    const patterns = [];

    // 檢測常見模式
    if (content.includes('如果') || content.includes('if')) {
      patterns.push('條件邏輯模式');
    }

    if (content.match(/\d+\.\s+/g)) {
      patterns.push('步驟序列模式');
    }

    if (content.includes('教訓') || content.includes('lesson')) {
      patterns.push('經驗學習模式');
    }

    if (content.includes('錯誤') || content.includes('error') || content.includes('bug')) {
      patterns.push('問題解決模式');
    }

    if (content.includes('優化') || content.includes('improve') || content.includes('optimize')) {
      patterns.push('持續改進模式');
    }

    return patterns;
  }

  // 批次評估多個記憶
  async batchEvaluate(memories: any[]): Promise<MemoryEvaluation[]> {
    const evaluations = [];
    
    // 使用併發但限制並發數量避免過載
    const batchSize = 5;
    for (let i = 0; i < memories.length; i += batchSize) {
      const batch = memories.slice(i, i + batchSize);
      const batchResults = await Promise.all(
        batch.map(memory => this.evaluate(memory))
      );
      evaluations.push(...batchResults);
      
      // 小延遲避免過載 Ollama
      if (i + batchSize < memories.length) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
    
    return evaluations;
  }

  // 生成評估報告
  generateEvaluationReport(evaluations: MemoryEvaluation[]): string {
    const totalCount = evaluations.length;
    const highValue = evaluations.filter(e => e.score >= 0.8).length;
    const mediumValue = evaluations.filter(e => e.score >= 0.5 && e.score < 0.8).length;
    const lowValue = evaluations.filter(e => e.score < 0.5).length;
    
    const avgScore = evaluations.reduce((sum, e) => sum + e.score, 0) / totalCount;
    
    const promotionReady = evaluations.filter(e => e.promotion_ready).length;
    
    return `# 記憶評估報告

## 總覽
- 總記憶數: ${totalCount}
- 平均評分: ${avgScore.toFixed(2)}
- 待晉升記憶: ${promotionReady}

## 價值分布
- 高價值 (≥0.8): ${highValue} (${(highValue/totalCount*100).toFixed(1)}%)
- 中價值 (0.5-0.8): ${mediumValue} (${(mediumValue/totalCount*100).toFixed(1)}%)
- 低價值 (<0.5): ${lowValue} (${(lowValue/totalCount*100).toFixed(1)}%)

## 建議
${promotionReady > 0 ? `- 考慮晉升 ${promotionReady} 條高價值記憶` : '- 當前記憶層級配置合理'}
${avgScore < 0.6 ? '- 記憶質量偏低，建議加強重要信息的捕獲' : ''}
${highValue / totalCount > 0.3 ? '- 高價值記憶較多，系統學習效果良好' : ''}
`;
  }
}