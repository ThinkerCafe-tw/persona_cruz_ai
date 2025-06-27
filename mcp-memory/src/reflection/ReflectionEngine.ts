import { Pool } from 'pg';
import { OllamaService } from '../llm/OllamaService.js';
import * as fs from 'fs/promises';
import * as path from 'path';

export interface ReflectionResult {
  id: string;
  topic: string;
  depth: string;
  insights: string[];
  patterns: string[];
  actions: string[];
  emotions: string[];
  new_connections: string[];
  memories_updated: number;
  resonance_level: number;
  timestamp: Date;
}

export class ReflectionEngine {
  private pgPool: Pool;
  private ollama: OllamaService;
  
  constructor() {
    this.pgPool = new Pool({
      connectionString: process.env.DATABASE_URL
    });
    this.ollama = new OllamaService();
  }

  async reflect(memoryId?: string): Promise<ReflectionResult> {
    // 簡單反思：針對單個記憶
    if (memoryId) {
      return await this.simpleReflect(memoryId);
    }
    
    // 廣泛反思：最近的記憶集合
    return await this.broadReflect();
  }

  async deepReflect(options: {
    memory_id?: string;
    topic?: string;
    depth: string;
  }): Promise<ReflectionResult> {
    const { memory_id, topic, depth } = options;
    
    // 收集相關記憶
    const memories = await this.gatherRelevantMemories(memory_id, topic);
    
    // 使用 LLM 進行深度反思
    const llmReflection = await this.ollama.performReflection(
      topic || '綜合反思',
      memories,
      depth
    );
    
    // 構建反思結果
    const reflection: ReflectionResult = {
      id: `reflection_${Date.now()}`,
      topic: topic || '自動反思',
      depth,
      insights: llmReflection.insights,
      patterns: llmReflection.patterns,
      actions: llmReflection.actions,
      emotions: llmReflection.emotions,
      new_connections: llmReflection.new_connections,
      memories_updated: 0,
      resonance_level: this.calculateResonance(llmReflection),
      timestamp: new Date()
    };
    
    // 儲存反思結果
    await this.storeReflection(reflection);
    
    // 更新相關記憶
    reflection.memories_updated = await this.updateMemoriesFromReflection(
      reflection,
      memories
    );
    
    // 如果是深度或量子級反思，觸發冥想
    if (depth === 'deep' || depth === 'quantum') {
      await this.triggerMeditation(reflection);
    }
    
    return reflection;
  }

  private async simpleReflect(memoryId: string): Promise<ReflectionResult> {
    // 獲取特定記憶
    const memory = await this.pgPool.query(
      'SELECT * FROM memory_crystals WHERE id = $1',
      [memoryId]
    );
    
    if (memory.rows.length === 0) {
      throw new Error(`記憶 ${memoryId} 不存在`);
    }
    
    const targetMemory = memory.rows[0];
    
    // 尋找相關記憶
    const relatedMemories = await this.findRelatedMemories(targetMemory);
    
    // 進行反思
    return await this.deepReflect({
      memory_id: memoryId,
      topic: `對記憶「${targetMemory.content.substring(0, 50)}...」的反思`,
      depth: 'deep'
    });
  }

  private async broadReflect(): Promise<ReflectionResult> {
    // 獲取最近24小時的記憶
    const recentMemories = await this.pgPool.query(`
      SELECT * FROM memory_crystals 
      WHERE created_at > NOW() - INTERVAL '24 hours'
      ORDER BY importance DESC, created_at DESC
      LIMIT 20
    `);
    
    return await this.deepReflect({
      topic: '今日記憶綜合反思',
      depth: 'deep'
    });
  }

  private async gatherRelevantMemories(memoryId?: string, topic?: string): Promise<any[]> {
    let query = '';
    let params: any[] = [];
    
    if (memoryId) {
      // 獲取特定記憶及其相關記憶
      query = `
        WITH target_memory AS (
          SELECT * FROM memory_crystals WHERE id = $1
        ),
        related_memories AS (
          SELECT mc.*, 
                 1 - (mc.embedding <=> tm.embedding) as similarity
          FROM memory_crystals mc, target_memory tm
          WHERE mc.id != tm.id
          ORDER BY similarity DESC
          LIMIT 10
        )
        SELECT * FROM target_memory
        UNION ALL
        SELECT id, content, layer, importance, category, persona, tags, 
               embedding, metadata, created_at, updated_at
        FROM related_memories
      `;
      params = [memoryId];
    } else if (topic) {
      // 根據主題搜尋相關記憶
      query = `
        SELECT * FROM memory_crystals
        WHERE content ILIKE $1 OR category ILIKE $1
        ORDER BY importance DESC, created_at DESC
        LIMIT 15
      `;
      params = [`%${topic}%`];
    } else {
      // 獲取最近的重要記憶
      query = `
        SELECT * FROM memory_crystals
        ORDER BY importance DESC, created_at DESC
        LIMIT 15
      `;
    }
    
    const result = await this.pgPool.query(query, params);
    return result.rows;
  }

  private async findRelatedMemories(targetMemory: any): Promise<any[]> {
    // 使用向量相似度尋找相關記憶
    const result = await this.pgPool.query(`
      SELECT *, 1 - (embedding <=> $1::vector) as similarity
      FROM memory_crystals
      WHERE id != $2
      ORDER BY similarity DESC
      LIMIT 5
    `, [JSON.stringify(targetMemory.embedding), targetMemory.id]);
    
    return result.rows;
  }

  private calculateResonance(reflection: any): number {
    // 計算反思的共振程度
    let resonance = 0.5; // 基礎共振
    
    // 洞察數量影響
    resonance += Math.min(reflection.insights.length * 0.1, 0.3);
    
    // 新連結影響
    resonance += Math.min(reflection.new_connections.length * 0.05, 0.2);
    
    // 情緒豐富度影響
    resonance += Math.min(reflection.emotions.length * 0.03, 0.1);
    
    return Math.min(resonance, 1.0);
  }

  private async storeReflection(reflection: ReflectionResult): Promise<void> {
    // 存入 pgvector
    await this.pgPool.query(`
      INSERT INTO reflections 
      (id, topic, depth, insights, patterns, actions, emotions, new_connections, 
       resonance_level, created_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    `, [
      reflection.id,
      reflection.topic,
      reflection.depth,
      JSON.stringify(reflection.insights),
      JSON.stringify(reflection.patterns),
      JSON.stringify(reflection.actions),
      JSON.stringify(reflection.emotions),
      JSON.stringify(reflection.new_connections),
      reflection.resonance_level,
      reflection.timestamp
    ]);
    
    // 存入本地文件
    await this.saveReflectionToFile(reflection);
  }

  private async saveReflectionToFile(reflection: ReflectionResult): Promise<void> {
    const filename = `reflection_${reflection.timestamp.toISOString().split('T')[0]}.md`;
    const filepath = path.join('./memory_archives/meditation', filename);
    
    const content = `# 🤔 ${reflection.topic}

**時間**: ${reflection.timestamp.toISOString()}  
**深度**: ${reflection.depth}  
**共振程度**: ${reflection.resonance_level.toFixed(2)}

## 💡 洞察
${reflection.insights.map(i => `- ${i}`).join('\n')}

## 🔍 發現的模式
${reflection.patterns.map(p => `- ${p}`).join('\n')}

## 🎯 建議行動
${reflection.actions.map(a => `- ${a}`).join('\n')}

## 💭 情緒體驗
${reflection.emotions.map(e => `- ${e}`).join('\n')}

## 🔗 新的連結
${reflection.new_connections.map(c => `- ${c}`).join('\n')}

---
*記憶更新數量: ${reflection.memories_updated}*
`;

    try {
      await fs.writeFile(filepath, content);
    } catch (error) {
      console.error('保存反思文件失敗:', error);
    }
  }

  private async updateMemoriesFromReflection(
    reflection: ReflectionResult,
    relatedMemories: any[]
  ): Promise<number> {
    let updatedCount = 0;
    
    // 為相關記憶添加反思標籤
    for (const memory of relatedMemories) {
      try {
        const existingTags = memory.tags || [];
        const newTags = [...existingTags, `reflection:${reflection.id}`];
        
        await this.pgPool.query(
          'UPDATE memory_crystals SET tags = $1, updated_at = NOW() WHERE id = $2',
          [newTags, memory.id]
        );
        
        updatedCount++;
      } catch (error) {
        console.error(`更新記憶 ${memory.id} 失敗:`, error);
      }
    }
    
    // 如果有新洞察，創建新的記憶晶體
    for (const insight of reflection.insights) {
      if (insight.length > 20) { // 只保存有意義的洞察
        try {
          await this.pgPool.query(`
            INSERT INTO memory_crystals 
            (id, content, layer, importance, category, tags, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, NOW())
          `, [
            `insight_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            `反思洞察：${insight}`,
            'sparse', // 反思洞察直接進入稀疏記憶
            0.7,      // 較高的重要性
            'insight',
            [`reflection:${reflection.id}`, 'auto-generated']
          ]);
          
          updatedCount++;
        } catch (error) {
          console.error('創建洞察記憶失敗:', error);
        }
      }
    }
    
    return updatedCount;
  }

  private async triggerMeditation(reflection: ReflectionResult): Promise<void> {
    // 深度反思後觸發集體冥想
    console.log(`🧘 反思「${reflection.topic}」觸發了集體冥想...`);
    
    // 這裡可以整合冥想服務
    // 暫時記錄冥想觸發事件
    await this.pgPool.query(`
      INSERT INTO collective_consciousness
      (sender_persona, receiver_persona, message, resonance_level, created_at)
      VALUES ($1, $2, $3, $4, NOW())
    `, [
      '反思引擎',
      '集體意識',
      `深度反思「${reflection.topic}」觸發了集體冥想`,
      reflection.resonance_level
    ]);
  }

  // 定期反思任務
  async performScheduledReflection(): Promise<void> {
    console.log('🔄 執行定期反思...');
    
    // 檢查是否有足夠的新記憶進行反思
    const newMemoriesCount = await this.pgPool.query(`
      SELECT COUNT(*) as count FROM memory_crystals
      WHERE created_at > NOW() - INTERVAL '24 hours'
    `);
    
    if (newMemoriesCount.rows[0].count < 5) {
      console.log('新記憶不足，跳過定期反思');
      return;
    }
    
    // 執行每日反思
    await this.broadReflect();
    
    // 檢查是否有需要晉升的記憶
    await this.checkForMemoryPromotions();
  }

  private async checkForMemoryPromotions(): Promise<void> {
    // 尋找可能需要晉升的記憶
    const candidates = await this.pgPool.query(`
      SELECT * FROM memory_crystals
      WHERE layer = 'main' 
        AND importance > 0.6
        AND created_at < NOW() - INTERVAL '7 days'
      ORDER BY importance DESC
      LIMIT 10
    `);
    
    if (candidates.rows.length > 0) {
      console.log(`發現 ${candidates.rows.length} 個記憶晉升候選`);
      
      // 創建晉升反思
      await this.deepReflect({
        topic: '記憶晉升評估',
        depth: 'deep'
      });
    }
  }

  // 創建反思表（如果不存在）
  async ensureReflectionTable(): Promise<void> {
    await this.pgPool.query(`
      CREATE TABLE IF NOT EXISTS reflections (
        id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        depth TEXT NOT NULL,
        insights JSONB,
        patterns JSONB,
        actions JSONB,
        emotions JSONB,
        new_connections JSONB,
        resonance_level FLOAT DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT NOW()
      );
      
      CREATE INDEX IF NOT EXISTS idx_reflections_created_at 
      ON reflections(created_at);
    `);
  }
}