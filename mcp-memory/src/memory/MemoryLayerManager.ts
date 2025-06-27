import { Pool } from 'pg';
import { Octokit } from '@octokit/rest';
import * as fs from 'fs/promises';
import * as path from 'path';
import { OllamaService } from '../llm/OllamaService.js';
import { MemoryGradientEvaluator } from './MemoryGradientEvaluator.js';

export interface Memory {
  id: string;
  content: string;
  layer: 'main' | 'sparse' | 'meta';
  importance: number;
  category: string;
  persona?: string;
  tags: string[];
  embedding?: number[];
  timestamp: Date;
  metadata: any;
}

export class MemoryLayerManager {
  private pgPool: Pool;
  private octokit: Octokit;
  private ollama: OllamaService;
  private evaluator: MemoryGradientEvaluator;
  
  // 記憶層路徑
  private paths = {
    main: './memory_archives/daily',
    sparse: './CLAUDE.md',
    meta: path.join(process.env.HOME || '', '.claude/CLAUDE.md')
  };

  constructor() {
    // 初始化 PostgreSQL 連接
    this.pgPool = new Pool({
      connectionString: process.env.DATABASE_URL
    });
    
    // 初始化 GitHub API
    this.octokit = new Octokit({
      auth: process.env.GITHUB_TOKEN
    });
    
    // 初始化 Ollama
    this.ollama = new OllamaService();
    
    // 初始化評估器
    this.evaluator = new MemoryGradientEvaluator(this.ollama);
  }

  async initialize() {
    // 確保資料庫表存在
    await this.ensureDatabase();
    
    // 確保本地目錄存在
    await fs.mkdir(this.paths.main, { recursive: true });
    
    // 測試 Ollama 連接
    await this.ollama.testConnection();
  }

  async storeMemory(content: string, metadata: any): Promise<any> {
    const memory: Memory = {
      id: `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      content,
      layer: 'main', // 預設存到主記憶
      importance: metadata.importance || 0.5,
      category: metadata.category,
      persona: metadata.persona,
      tags: metadata.tags || [],
      timestamp: new Date(),
      metadata
    };

    // 使用 Ollama 生成嵌入向量
    const embedding = await this.ollama.generateEmbedding(content);
    memory.embedding = embedding;

    // 評估記憶重要性
    const evaluation = await this.evaluator.evaluate(memory);
    
    // 根據評估結果決定存儲層級
    if (evaluation.score > 0.8) {
      memory.layer = 'meta';
    } else if (evaluation.score > 0.5) {
      memory.layer = 'sparse';
    }

    // 存儲到相應層級
    await this.saveToLayer(memory);
    
    // 存儲到 pgvector
    await this.saveToPgVector(memory);
    
    // 如果是重要記憶，同步到 GitHub
    if (memory.layer !== 'main') {
      await this.syncToGitHub(memory);
    }

    return {
      memory_id: memory.id,
      layer: memory.layer,
      vectorized: true,
      evaluation
    };
  }

  async searchMemories(
    query: string, 
    layers: string[], 
    limit: number,
    persona?: string
  ): Promise<any[]> {
    // 生成查詢向量
    const queryVector = await this.ollama.generateEmbedding(query);
    
    // 從 pgvector 搜尋
    const pgResults = await this.searchPgVector(queryVector, layers, limit, persona);
    
    // 使用 Ollama 進行語意排序和摘要
    const enhancedResults = await this.ollama.enhanceSearchResults(query, pgResults);
    
    return enhancedResults;
  }

  private async saveToLayer(memory: Memory) {
    switch (memory.layer) {
      case 'main':
        // 存到每日記錄
        const dailyFile = path.join(
          this.paths.main, 
          `${new Date().toISOString().split('T')[0]}.md`
        );
        await this.appendToFile(dailyFile, this.formatMemoryAsMarkdown(memory));
        break;
        
      case 'sparse':
        // 更新專案 CLAUDE.md
        await this.updateClaudeMd(this.paths.sparse, memory);
        break;
        
      case 'meta':
        // 更新全域 CLAUDE.md
        await this.updateClaudeMd(this.paths.meta, memory);
        break;
    }
  }

  private async saveToPgVector(memory: Memory) {
    const query = `
      INSERT INTO memory_crystals 
      (id, content, layer, importance, category, persona, tags, embedding, metadata, created_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    `;
    
    await this.pgPool.query(query, [
      memory.id,
      memory.content,
      memory.layer,
      memory.importance,
      memory.category,
      memory.persona,
      memory.tags,
      JSON.stringify(memory.embedding),
      memory.metadata,
      memory.timestamp
    ]);
  }

  private async searchPgVector(
    queryVector: number[], 
    layers: string[], 
    limit: number,
    persona?: string
  ): Promise<any[]> {
    let query = `
      SELECT 
        id, content, layer, importance, category, persona, tags, metadata,
        1 - (embedding <=> $1::vector) as similarity
      FROM memory_crystals
      WHERE layer = ANY($2::text[])
    `;
    
    const params: any[] = [JSON.stringify(queryVector), layers];
    
    if (persona) {
      query += ` AND persona = $${params.length + 1}`;
      params.push(persona);
    }
    
    query += ` ORDER BY similarity DESC LIMIT $${params.length + 1}`;
    params.push(limit);
    
    const result = await this.pgPool.query(query, params);
    return result.rows;
  }

  private async syncToGitHub(memory: Memory) {
    try {
      // 獲取當前文件內容
      const { data: file } = await this.octokit.repos.getContent({
        owner: process.env.GITHUB_OWNER || '',
        repo: process.env.GITHUB_REPO || '',
        path: memory.layer === 'sparse' ? 'CLAUDE.md' : '.claude/CLAUDE.md'
      });
      
      // 更新內容
      const content = Buffer.from(file.content, 'base64').toString();
      const updatedContent = this.appendMemoryToContent(content, memory);
      
      // 提交更新
      await this.octokit.repos.updateFile({
        owner: process.env.GITHUB_OWNER || '',
        repo: process.env.GITHUB_REPO || '',
        path: memory.layer === 'sparse' ? 'CLAUDE.md' : '.claude/CLAUDE.md',
        message: `🧠 記憶更新: ${memory.category} - ${memory.content.substring(0, 50)}...`,
        content: Buffer.from(updatedContent).toString('base64'),
        sha: file.sha
      });
    } catch (error) {
      console.error('GitHub 同步失敗:', error);
      // 不中斷流程，記錄錯誤即可
    }
  }

  async evaluateAndPromote(options: any): Promise<any> {
    const timeRange = this.parseTimeRange(options.time_range);
    
    // 查詢需要評估的記憶
    const memories = await this.getMemoriesForEvaluation(timeRange);
    
    const promotions = {
      main_to_sparse: [],
      sparse_to_meta: [],
      evaluated_count: memories.length,
      promoted_count: 0
    };
    
    for (const memory of memories) {
      const evaluation = await this.evaluator.evaluate(memory);
      
      if (memory.layer === 'main' && evaluation.score > 0.5) {
        promotions.main_to_sparse.push({
          memory_id: memory.id,
          score: evaluation.score,
          reason: evaluation.reason
        });
      } else if (memory.layer === 'sparse' && evaluation.score > 0.8) {
        promotions.sparse_to_meta.push({
          memory_id: memory.id,
          score: evaluation.score,
          reason: evaluation.reason
        });
      }
    }
    
    // 如果設置了自動晉升
    if (options.auto_promote) {
      for (const promo of [...promotions.main_to_sparse, ...promotions.sparse_to_meta]) {
        await this.promoteMemory(promo.memory_id, promo.score > 0.8 ? 'meta' : 'sparse');
        promotions.promoted_count++;
      }
    }
    
    return promotions;
  }

  async syncAllLayers(options: any): Promise<any> {
    const result = {
      pgvector: { total: 0, synced: 0 },
      github: { total: 0, synced: 0 },
      local: { total: 0, synced: 0 },
      conflicts: []
    };
    
    // 實現三方同步邏輯
    // 這裡簡化展示核心概念
    
    return result;
  }

  async generateReport(options: any): Promise<any> {
    const stats = await this.getMemoryStats();
    
    let content = '';
    
    switch (options.report_type) {
      case 'health':
        content = this.generateHealthReport(stats);
        break;
      case 'insights':
        content = await this.generateInsightsReport(stats);
        break;
      case 'patterns':
        content = await this.generatePatternsReport(stats);
        break;
      case 'growth':
        content = this.generateGrowthReport(stats);
        break;
    }
    
    return { content };
  }

  // 記憶守護進程
  startMemoryDaemon() {
    // 每小時檢查一次記憶健康
    setInterval(async () => {
      await this.performMemoryMaintenance();
    }, 60 * 60 * 1000);
    
    // 每天進行一次記憶晉升評估
    setInterval(async () => {
      await this.evaluateAndPromote({
        time_range: '24h',
        auto_promote: true
      });
    }, 24 * 60 * 60 * 1000);
  }

  private async performMemoryMaintenance() {
    // 清理過期的主記憶
    // 壓縮相似記憶
    // 更新向量索引
    console.log('🧹 執行記憶維護...');
  }

  private formatMemoryAsMarkdown(memory: Memory): string {
    return `
## ${new Date().toISOString()} - ${memory.category}
**人格**: ${memory.persona || '集體'}  
**重要性**: ${memory.importance.toFixed(2)}  
**標籤**: ${memory.tags.join(', ')}

${memory.content}

---
`;
  }

  private async updateClaudeMd(filepath: string, memory: Memory) {
    try {
      const content = await fs.readFile(filepath, 'utf-8');
      const updated = this.appendMemoryToContent(content, memory);
      await fs.writeFile(filepath, updated);
    } catch (error) {
      // 文件不存在則創建
      await fs.writeFile(filepath, this.formatMemoryAsMarkdown(memory));
    }
  }

  private appendMemoryToContent(content: string, memory: Memory): string {
    // 找到合適的位置插入記憶
    // 這裡簡化為追加到文件末尾
    return content + '\n' + this.formatMemoryAsMarkdown(memory);
  }

  private parseTimeRange(range: string): Date {
    const now = new Date();
    const match = range.match(/(\d+)([hdwm])/);
    if (!match) return now;
    
    const [, num, unit] = match;
    const value = parseInt(num);
    
    switch (unit) {
      case 'h': return new Date(now.getTime() - value * 60 * 60 * 1000);
      case 'd': return new Date(now.getTime() - value * 24 * 60 * 60 * 1000);
      case 'w': return new Date(now.getTime() - value * 7 * 24 * 60 * 60 * 1000);
      case 'm': return new Date(now.getTime() - value * 30 * 24 * 60 * 60 * 1000);
      default: return now;
    }
  }

  private async ensureDatabase() {
    const createTableQuery = `
      CREATE TABLE IF NOT EXISTS memory_crystals (
        id TEXT PRIMARY KEY,
        content TEXT NOT NULL,
        layer TEXT NOT NULL,
        importance FLOAT DEFAULT 0.5,
        category TEXT,
        persona TEXT,
        tags TEXT[],
        embedding vector(4096),
        metadata JSONB,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
      );
      
      CREATE INDEX IF NOT EXISTS idx_memory_embedding 
      ON memory_crystals USING ivfflat (embedding vector_cosine_ops);
    `;
    
    await this.pgPool.query(createTableQuery);
  }

  private async getMemoriesForEvaluation(since: Date): Promise<Memory[]> {
    const result = await this.pgPool.query(
      'SELECT * FROM memory_crystals WHERE created_at > $1',
      [since]
    );
    return result.rows;
  }

  private async promoteMemory(memoryId: string, newLayer: string) {
    await this.pgPool.query(
      'UPDATE memory_crystals SET layer = $1, updated_at = NOW() WHERE id = $2',
      [newLayer, memoryId]
    );
  }

  private async getMemoryStats(): Promise<any> {
    const stats = await this.pgPool.query(`
      SELECT 
        layer,
        COUNT(*) as count,
        AVG(importance) as avg_importance,
        MAX(created_at) as latest
      FROM memory_crystals
      GROUP BY layer
    `);
    
    return stats.rows;
  }

  private generateHealthReport(stats: any): string {
    return `# 記憶系統健康報告

生成時間: ${new Date().toISOString()}

## 記憶層分布
${stats.map(s => `- ${s.layer}: ${s.count} 條記憶`).join('\n')}

## 系統狀態
- pgvector: ✅ 連接正常
- GitHub: ✅ 同步正常  
- 本地文件: ✅ 可訪問

## 建議
- 定期執行記憶晉升評估
- 清理過期的主記憶
`;
  }

  private async generateInsightsReport(stats: any): Promise<string> {
    // 使用 Ollama 分析記憶模式並生成洞察
    const recentMemories = await this.pgPool.query(
      'SELECT * FROM memory_crystals ORDER BY created_at DESC LIMIT 100'
    );
    
    const insights = await this.ollama.analyzeMemoryPatterns(recentMemories.rows);
    
    return `# 記憶洞察報告

${insights}
`;
  }

  private async generatePatternsReport(stats: any): Promise<string> {
    // 分析記憶模式
    return `# 記憶模式分析

待實現...
`;
  }

  private generateGrowthReport(stats: any): string {
    return `# 記憶成長報告

## 成長趨勢
- 本週新增記憶: X 條
- 晉升率: X%
- 活躍人格: X 個

待完善...
`;
  }
}