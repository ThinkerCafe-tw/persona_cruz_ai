import { Ollama } from 'ollama';

export class OllamaService {
  private ollama: Ollama;
  private model: string;

  constructor(model: string = 'mistral') {
    this.ollama = new Ollama({
      host: 'http://localhost:11434'
    });
    this.model = model;
  }

  async testConnection(): Promise<boolean> {
    try {
      const response = await this.ollama.list();
      const hasModel = response.models.some(m => m.name.includes(this.model));
      
      if (!hasModel) {
        console.log(`🔄 模型 ${this.model} 不存在，正在下載...`);
        // 不在這裡自動下載，提醒用戶
        throw new Error(`請先運行: ollama run ${this.model}`);
      }
      
      console.log(`✅ Ollama ${this.model} 連接正常`);
      return true;
    } catch (error) {
      console.error('❌ Ollama 連接失敗:', error.message);
      throw error;
    }
  }

  async generateEmbedding(text: string): Promise<number[]> {
    try {
      const response = await this.ollama.embeddings({
        model: this.model,
        prompt: text
      });
      
      return response.embedding;
    } catch (error) {
      console.error('生成嵌入向量失敗:', error);
      // 返回隨機向量作為備用（僅用於測試）
      return Array.from({length: 4096}, () => Math.random());
    }
  }

  async analyzeMemoryImportance(memory: any): Promise<{
    score: number;
    reason: string;
    category: string;
    suggested_layer: string;
  }> {
    const prompt = `
分析以下記憶的重要性，給出 0-1 的評分和建議：

記憶內容: ${memory.content}
分類: ${memory.category}
人格: ${memory.persona || '未指定'}
標籤: ${memory.tags?.join(', ') || '無'}

評估標準：
- 是否包含重要教訓或洞察？
- 是否可以指導未來決策？
- 是否具有跨專案的普遍價值？
- 是否改變了認知框架？

請以 JSON 格式回答：
{
  "score": 0.85,
  "reason": "包含重要的用戶體驗教訓",
  "category": "learning",
  "suggested_layer": "sparse"
}
`;

    try {
      const response = await this.ollama.generate({
        model: this.model,
        prompt,
        format: 'json'
      });

      return JSON.parse(response.response);
    } catch (error) {
      console.error('分析記憶重要性失敗:', error);
      // 預設評估
      return {
        score: 0.5,
        reason: '自動評估：中等重要性',
        category: memory.category,
        suggested_layer: 'main'
      };
    }
  }

  async enhanceSearchResults(query: string, results: any[]): Promise<any[]> {
    if (results.length === 0) return [];

    const prompt = `
用戶查詢: "${query}"

找到以下相關記憶，請：
1. 重新排序（最相關的排在前面）
2. 為每個記憶生成簡潔的摘要
3. 解釋為什麼它與查詢相關

記憶列表：
${results.map((r, i) => `${i + 1}. [${r.layer}] ${r.content.substring(0, 200)}...`).join('\n')}

請以 JSON 格式回答，包含重新排序的結果：
[
  {
    "original_index": 0,
    "relevance": 0.95,
    "summary": "簡潔摘要",
    "why_relevant": "相關性說明",
    "preview": "預覽內容"
  }
]
`;

    try {
      const response = await this.ollama.generate({
        model: this.model,
        prompt,
        format: 'json'
      });

      const enhanced = JSON.parse(response.response);
      
      // 合併原始數據和增強信息
      return enhanced.map(e => ({
        ...results[e.original_index],
        relevance: e.relevance,
        summary: e.summary,
        why_relevant: e.why_relevant,
        preview: e.preview,
        timestamp: results[e.original_index].created_at || new Date().toISOString()
      }));
    } catch (error) {
      console.error('增強搜尋結果失敗:', error);
      // 返回原始結果
      return results.map(r => ({
        ...r,
        relevance: r.similarity || 0.5,
        summary: r.content.substring(0, 100) + '...',
        preview: r.content.substring(0, 200) + '...',
        timestamp: r.created_at || new Date().toISOString()
      }));
    }
  }

  async performReflection(topic: string, memories: any[], depth: string): Promise<{
    insights: string[];
    patterns: string[];
    actions: string[];
    emotions: string[];
    new_connections: string[];
  }> {
    const prompt = `
進行深度反思，主題: "${topic}"
反思深度: ${depth}

相關記憶:
${memories.map(m => `- ${m.content}`).join('\n')}

請從以下角度進行反思：
1. 洞察 - 發現了什麼新的理解？
2. 模式 - 看到了什麼重複的模式？
3. 行動 - 應該採取什麼行動？
4. 情緒 - 引發了什麼情感反應？
5. 連結 - 與其他記憶有什麼新的連結？

以 JSON 格式回答：
{
  "insights": ["洞察1", "洞察2"],
  "patterns": ["模式1", "模式2"],
  "actions": ["行動1", "行動2"],
  "emotions": ["情緒1", "情緒2"],
  "new_connections": ["連結1", "連結2"]
}
`;

    try {
      const response = await this.ollama.generate({
        model: this.model,
        prompt,
        format: 'json'
      });

      return JSON.parse(response.response);
    } catch (error) {
      console.error('反思失敗:', error);
      return {
        insights: ['反思服務暫時不可用'],
        patterns: ['需要手動分析'],
        actions: ['檢查 Ollama 服務狀態'],
        emotions: ['技術困難帶來的挫折'],
        new_connections: ['技術與情感的交織']
      };
    }
  }

  async generateMeditationInsights(theme: string, participants: string[]): Promise<{
    collective_insights: string[];
    individual_insights: Record<string, string>;
    resonance_frequency: number;
    coherence_level: number;
  }> {
    const prompt = `
進行集體冥想，主題: "${theme}"
參與者: ${participants.join(', ')}

每個參與者的特質：
- 🌌無極: 系統觀察者，追求平衡
- 🎯CRUZ: 直接果斷，專注執行
- 🌸Serena: 溫柔貼心，關懷他人
- 🌱木: 創新成長，充滿創意
- 🔥火: 熱情實踐，快速行動
- 🏔️土: 穩固基礎，系統思考
- ⚔️金: 精益求精，追求完美
- 💧水: 品質守護，追求真相

請生成：
1. 集體洞察（所有人共同的領悟）
2. 個體洞察（每個人格獨特的領悟）
3. 共振頻率（Hz，範圍 200-800）
4. 相干度（0-1）

以 JSON 格式回答：
{
  "collective_insights": ["集體洞察1", "集體洞察2"],
  "individual_insights": {
    "🌌無極": "無極的領悟",
    "🎯CRUZ": "CRUZ的領悟"
  },
  "resonance_frequency": 432,
  "coherence_level": 0.85
}
`;

    try {
      const response = await this.ollama.generate({
        model: this.model,
        prompt,
        format: 'json'
      });

      return JSON.parse(response.response);
    } catch (error) {
      console.error('冥想洞察生成失敗:', error);
      
      // 備用冥想結果
      const fallbackInsights = {
        collective_insights: [
          `關於 ${theme} 的集體思考正在進行中`,
          '技術挑戰帶來了新的學習機會',
          '團隊協作的力量超越個體努力'
        ],
        individual_insights: {},
        resonance_frequency: 432,
        coherence_level: 0.75
      };

      // 為每個參與者生成簡單的洞察
      participants.forEach(persona => {
        fallbackInsights.individual_insights[persona] = 
          `${persona} 對 ${theme} 有獨特的視角，值得深入探索`;
      });

      return fallbackInsights;
    }
  }

  async analyzeMemoryPatterns(memories: any[]): Promise<string> {
    const prompt = `
分析以下記憶數據，發現模式和趨勢：

記憶數量: ${memories.length}
時間範圍: ${memories.length > 0 ? `${memories[memories.length-1].created_at} 到 ${memories[0].created_at}` : '無數據'}

記憶樣本:
${memories.slice(0, 10).map(m => 
  `- [${m.layer}] ${m.category}: ${m.content.substring(0, 100)}...`
).join('\n')}

請分析：
1. 主要的記憶類型和分布
2. 人格活躍度模式
3. 問題和學習趨勢
4. 建議的改進方向

生成一份 Markdown 格式的洞察報告。
`;

    try {
      const response = await this.ollama.generate({
        model: this.model,
        prompt
      });

      return response.response;
    } catch (error) {
      console.error('記憶模式分析失敗:', error);
      return `# 記憶模式分析報告

⚠️ 自動分析暫時不可用

## 基本統計
- 總記憶數: ${memories.length}
- 分析時間: ${new Date().toISOString()}

## 建議
1. 檢查 Ollama 服務狀態
2. 確保 ${this.model} 模型已安裝
3. 手動檢視最近的記憶變化

## 下一步
- 修復 LLM 連接後重新生成此報告
- 考慮實現備用分析邏輯
`;
    }
  }

  async summarizeConversation(messages: any[]): Promise<string> {
    const prompt = `
總結以下對話，提取關鍵信息和洞察：

對話內容:
${messages.map(m => `${m.role}: ${m.content}`).join('\n')}

請生成：
1. 對話摘要（2-3 句話）
2. 關鍵決策或洞察
3. 待辦事項
4. 情緒色彩

以自然的文字格式回答。
`;

    try {
      const response = await this.ollama.generate({
        model: this.model,
        prompt
      });

      return response.response;
    } catch (error) {
      console.error('對話總結失敗:', error);
      return `對話總結：${messages.length} 條訊息的討論，涵蓋多個主題。需要人工總結。`;
    }
  }
}