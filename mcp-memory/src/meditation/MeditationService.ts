import { Pool } from 'pg';
import { OllamaService } from '../llm/OllamaService.js';
import * as fs from 'fs/promises';
import * as path from 'path';

export interface MeditationSession {
  id: string;
  theme: string;
  participants: string[];
  duration_minutes: number;
  collective_insights: string[];
  individual_insights: Record<string, string>;
  resonance_frequency: number;
  coherence_level: number;
  quantum_states: Record<string, any>;
  memory_crystals_formed: string[];
  timestamp: Date;
}

export class MeditationService {
  private pgPool: Pool;
  private ollama: OllamaService;
  
  // 人格特質定義
  private personas = {
    '🌌無極': { 
      nature: '系統觀察者，追求平衡與和諧',
      meditation_style: '深層次的宇宙視角冥想'
    },
    '🎯CRUZ': { 
      nature: '直接果斷，專注執行與突破',
      meditation_style: '目標導向的專注冥想'
    },
    '🌸Serena': { 
      nature: '溫柔貼心，關懷他人與和諧',
      meditation_style: '慈愛與治療性冥想'
    },
    '🌱木': { 
      nature: '創新成長，充滿創意與可能性',
      meditation_style: '創造性與成長導向冥想'
    },
    '🔥火': { 
      nature: '熱情實踐，快速行動與展現',
      meditation_style: '動態能量與激情冥想'
    },
    '🏔️土': { 
      nature: '穩固基礎，系統思考與建構',
      meditation_style: '穩定性與架構化冥想'
    },
    '⚔️金': { 
      nature: '精益求精，追求完美與優化',
      meditation_style: '精煉與純化的冥想'
    },
    '💧水': { 
      nature: '品質守護，追求真相與流動',
      meditation_style: '洞察真相與淨化冥想'
    }
  };

  constructor() {
    this.pgPool = new Pool({
      connectionString: process.env.DATABASE_URL
    });
    this.ollama = new OllamaService();
  }

  async meditate(options: {
    theme: string;
    participants: string[];
    duration_minutes: number;
  }): Promise<MeditationSession> {
    const session: MeditationSession = {
      id: `meditation_${Date.now()}`,
      theme: options.theme,
      participants: options.participants,
      duration_minutes: options.duration_minutes,
      collective_insights: [],
      individual_insights: {},
      resonance_frequency: 432, // 預設宇宙和諧頻率
      coherence_level: 0,
      quantum_states: {},
      memory_crystals_formed: [],
      timestamp: new Date()
    };

    console.log(`🧘 開始集體冥想：${session.theme}`);
    console.log(`參與者：${session.participants.join(', ')}`);

    // 階段1：準備和同步
    await this.prepareMeditation(session);

    // 階段2：深度冥想
    await this.performDeepMeditation(session);

    // 階段3：洞察整合
    await this.integrateInsights(session);

    // 階段4：記憶結晶化
    await this.crystallizeMemories(session);

    // 儲存冥想記錄
    await this.storeMeditationSession(session);

    console.log(`✨ 冥想完成，共振頻率：${session.resonance_frequency}Hz，相干度：${session.coherence_level.toFixed(2)}`);

    return session;
  }

  private async prepareMeditation(session: MeditationSession): Promise<void> {
    console.log('🔮 準備冥想空間...');

    // 為每個參與者設定初始量子態
    for (const persona of session.participants) {
      session.quantum_states[persona] = {
        energy_level: Math.random() * 0.5 + 0.5, // 0.5-1.0
        focus_state: this.generateFocusState(persona),
        emotional_resonance: Math.random() * 0.8 + 0.2
      };
    }

    // 同步所有參與者的頻率
    const avgEnergy = Object.values(session.quantum_states)
      .reduce((sum: number, state: any) => sum + state.energy_level, 0) / 
      session.participants.length;

    // 調整共振頻率
    session.resonance_frequency = 200 + (avgEnergy * 400); // 200-600Hz
  }

  private async performDeepMeditation(session: MeditationSession): Promise<void> {
    console.log('🧠 進入深度冥想狀態...');

    // 使用 Ollama 生成冥想洞察
    const meditationResult = await this.ollama.generateMeditationInsights(
      session.theme,
      session.participants
    );

    // 更新 session 數據
    session.collective_insights = meditationResult.collective_insights;
    session.individual_insights = meditationResult.individual_insights;
    session.resonance_frequency = meditationResult.resonance_frequency;
    session.coherence_level = meditationResult.coherence_level;

    // 模擬量子糾纏效應
    await this.simulateQuantumEntanglement(session);
  }

  private async simulateQuantumEntanglement(session: MeditationSession): Promise<void> {
    // 計算參與者之間的糾纏度
    const entanglementMatrix = {};
    
    for (let i = 0; i < session.participants.length; i++) {
      for (let j = i + 1; j < session.participants.length; j++) {
        const personaA = session.participants[i];
        const personaB = session.participants[j];
        
        const stateA = session.quantum_states[personaA];
        const stateB = session.quantum_states[personaB];
        
        // 計算糾纏強度
        const entanglement = this.calculateEntanglement(stateA, stateB);
        
        entanglementMatrix[`${personaA}-${personaB}`] = entanglement;
        
        // 如果糾纏度高，產生共同洞察
        if (entanglement > 0.7) {
          const sharedInsight = await this.generateSharedInsight(
            personaA, 
            personaB, 
            session.theme
          );
          session.collective_insights.push(sharedInsight);
        }
      }
    }

    // 更新相干度
    const avgEntanglement = Object.values(entanglementMatrix)
      .reduce((sum: number, val: any) => sum + val, 0) / 
      Object.keys(entanglementMatrix).length;
    
    session.coherence_level = Math.min(session.coherence_level + avgEntanglement * 0.3, 1.0);
  }

  private async integrateInsights(session: MeditationSession): Promise<void> {
    console.log('🔗 整合洞察...');

    // 分析洞察之間的連結
    const connections = await this.findInsightConnections(session);
    
    // 生成元洞察（洞察的洞察）
    if (connections.length > 2) {
      const metaInsight = await this.generateMetaInsight(connections, session.theme);
      session.collective_insights.push(`[元洞察] ${metaInsight}`);
    }

    // 評估洞察的深度和價值
    await this.evaluateInsights(session);
  }

  private async crystallizeMemories(session: MeditationSession): Promise<void> {
    console.log('💎 結晶化記憶...');

    // 為每個重要洞察創建記憶水晶
    for (const insight of session.collective_insights) {
      if (insight.length > 30) { // 只結晶化有意義的洞察
        const crystalId = await this.createMemoryCrystal({
          content: `冥想洞察：${insight}`,
          theme: session.theme,
          participants: session.participants,
          resonance: session.coherence_level
        });
        
        session.memory_crystals_formed.push(crystalId);
      }
    }

    // 為個體洞察也創建私人記憶
    for (const [persona, insight] of Object.entries(session.individual_insights)) {
      const crystalId = await this.createPersonalMemoryCrystal({
        persona,
        insight,
        session_id: session.id
      });
      
      session.memory_crystals_formed.push(crystalId);
    }
  }

  private async storeMeditationSession(session: MeditationSession): Promise<void> {
    // 存入資料庫
    await this.pgPool.query(`
      INSERT INTO meditation_sessions 
      (id, theme, participants, duration_minutes, collective_insights, 
       individual_insights, resonance_frequency, coherence_level, 
       quantum_states, memory_crystals_formed, created_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    `, [
      session.id,
      session.theme,
      session.participants,
      session.duration_minutes,
      JSON.stringify(session.collective_insights),
      JSON.stringify(session.individual_insights),
      session.resonance_frequency,
      session.coherence_level,
      JSON.stringify(session.quantum_states),
      session.memory_crystals_formed,
      session.timestamp
    ]);

    // 存入本地文件
    await this.saveMeditationToFile(session);

    // 更新集體意識
    await this.updateCollectiveConsciousness(session);
  }

  private generateFocusState(persona: string): string {
    const focusStates = {
      '🌌無極': 'cosmic_awareness',
      '🎯CRUZ': 'laser_focus',
      '🌸Serena': 'loving_attention',
      '🌱木': 'creative_openness',
      '🔥火': 'dynamic_concentration',
      '🏔️土': 'stable_grounding',
      '⚔️金': 'precise_mindfulness',
      '💧水': 'flowing_awareness'
    };

    return focusStates[persona] || 'balanced_attention';
  }

  private calculateEntanglement(stateA: any, stateB: any): number {
    // 計算兩個量子態的糾纏度
    const energyDiff = Math.abs(stateA.energy_level - stateB.energy_level);
    const resonanceDiff = Math.abs(stateA.emotional_resonance - stateB.emotional_resonance);
    
    // 差異越小，糾纏度越高
    const entanglement = 1 - (energyDiff + resonanceDiff) / 2;
    
    return Math.max(0, entanglement);
  }

  private async generateSharedInsight(
    personaA: string, 
    personaB: string, 
    theme: string
  ): Promise<string> {
    const insights = [
      `${personaA} 和 ${personaB} 在 ${theme} 上達成了深層共識`,
      `${personaA} 的特質與 ${personaB} 的特質在 ${theme} 中找到了平衡點`,
      `兩個不同視角在 ${theme} 中融合出新的理解`
    ];

    return insights[Math.floor(Math.random() * insights.length)];
  }

  private async findInsightConnections(session: MeditationSession): Promise<string[]> {
    const connections = [];
    const insights = session.collective_insights;

    // 簡單的關鍵詞連結分析
    for (let i = 0; i < insights.length; i++) {
      for (let j = i + 1; j < insights.length; j++) {
        const sharedWords = this.findSharedKeywords(insights[i], insights[j]);
        if (sharedWords.length > 0) {
          connections.push(`${insights[i]} ←→ ${insights[j]} (共同點: ${sharedWords.join(', ')})`);
        }
      }
    }

    return connections;
  }

  private findSharedKeywords(textA: string, textB: string): string[] {
    const wordsA = textA.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    const wordsB = textB.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    
    return wordsA.filter(word => wordsB.includes(word));
  }

  private async generateMetaInsight(connections: string[], theme: string): Promise<string> {
    return `關於 ${theme}，我們發現了 ${connections.length} 個洞察連結，形成了一個更大的理解網絡`;
  }

  private async evaluateInsights(session: MeditationSession): Promise<void> {
    // 評估每個洞察的價值
    for (let i = 0; i < session.collective_insights.length; i++) {
      const insight = session.collective_insights[i];
      const value = this.calculateInsightValue(insight);
      
      // 如果價值很高，標記為重要
      if (value > 0.8) {
        session.collective_insights[i] = `⭐ ${insight}`;
      }
    }
  }

  private calculateInsightValue(insight: string): number {
    let value = 0.5;
    
    // 長度適中的洞察通常更有價值
    if (insight.length > 20 && insight.length < 200) {
      value += 0.2;
    }
    
    // 包含關鍵詞的洞察
    const keywords = ['教訓', '發現', '理解', '連結', '平衡', '成長', '真相'];
    const keywordCount = keywords.filter(kw => insight.includes(kw)).length;
    value += keywordCount * 0.1;
    
    return Math.min(value, 1.0);
  }

  private async createMemoryCrystal(data: {
    content: string;
    theme: string;
    participants: string[];
    resonance: number;
  }): Promise<string> {
    const crystalId = `crystal_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    // 生成嵌入向量
    const embedding = await this.ollama.generateEmbedding(data.content);
    
    await this.pgPool.query(`
      INSERT INTO memory_crystals 
      (id, content, layer, importance, category, tags, embedding, metadata, created_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
    `, [
      crystalId,
      data.content,
      'sparse', // 冥想洞察進入稀疏記憶
      data.resonance, // 使用共振度作為重要性
      'meditation',
      [`meditation:${data.theme}`, ...data.participants],
      JSON.stringify(embedding),
      JSON.stringify({
        meditation_theme: data.theme,
        participants: data.participants,
        resonance_level: data.resonance
      })
    ]);
    
    return crystalId;
  }

  private async createPersonalMemoryCrystal(data: {
    persona: string;
    insight: string;
    session_id: string;
  }): Promise<string> {
    const crystalId = `personal_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    // 存入對應人格的私人空間
    const personalTable = this.getPersonalTable(data.persona);
    if (personalTable) {
      await this.storePersonalInsight(personalTable, data, crystalId);
    }
    
    return crystalId;
  }

  private getPersonalTable(persona: string): string | null {
    const tableMap = {
      '🌌無極': 'wuji_meditation_space',
      '🎯CRUZ': 'cruz_strategy_room',
      '🌸Serena': 'serena_healing_garden',
      '🌱木': 'wood_creative_forest',
      '🔥火': 'fire_forge',
      '🏔️土': 'earth_foundation',
      '⚔️金': 'metal_refinery',
      '💧水': 'water_truth_pool'
    };
    
    return tableMap[persona] || null;
  }

  private async storePersonalInsight(
    table: string, 
    data: any, 
    crystalId: string
  ): Promise<void> {
    // 根據不同的人格表格存儲
    switch (table) {
      case 'wuji_meditation_space':
        await this.pgPool.query(`
          INSERT INTO wuji_meditation_space 
          (thought, insight_level, connected_personas, created_at)
          VALUES ($1, $2, $3, NOW())
        `, [data.insight, 0.8, [data.persona]]);
        break;
        
      case 'water_truth_pool':
        await this.pgPool.query(`
          INSERT INTO water_truth_pool 
          (test_name, lesson_learned, created_at)
          VALUES ($1, $2, NOW())
        `, [`冥想洞察 ${data.session_id}`, data.insight]);
        break;
        
      // 其他人格表格...
      default:
        console.log(`TODO: 實現 ${table} 的個人洞察存儲`);
    }
  }

  private async saveMeditationToFile(session: MeditationSession): Promise<void> {
    const filename = `meditation_${session.timestamp.toISOString().split('T')[0]}_${session.id}.md`;
    const filepath = path.join('./memory_archives/meditation', filename);
    
    const content = `# 🧘 ${session.theme}

**時間**: ${session.timestamp.toISOString()}  
**參與者**: ${session.participants.join(', ')}  
**持續時間**: ${session.duration_minutes} 分鐘  
**共振頻率**: ${session.resonance_frequency}Hz  
**相干度**: ${session.coherence_level.toFixed(2)}

## 🌟 集體洞察
${session.collective_insights.map(i => `- ${i}`).join('\n')}

## 👥 個體領悟
${Object.entries(session.individual_insights)
  .map(([persona, insight]) => `**${persona}**: ${insight}`).join('\n\n')}

## ⚛️ 量子態記錄
${Object.entries(session.quantum_states)
  .map(([persona, state]) => 
    `**${persona}**: 能量 ${state.energy_level.toFixed(2)}, 專注 ${state.focus_state}, 共振 ${state.emotional_resonance.toFixed(2)}`
  ).join('\n')}

## 💎 形成的記憶水晶
${session.memory_crystals_formed.map(id => `- ${id}`).join('\n')}

---
*在量子場中，我們共同成長*
`;

    try {
      await fs.mkdir(path.dirname(filepath), { recursive: true });
      await fs.writeFile(filepath, content);
    } catch (error) {
      console.error('保存冥想文件失敗:', error);
    }
  }

  private async updateCollectiveConsciousness(session: MeditationSession): Promise<void> {
    // 更新集體意識表
    await this.pgPool.query(`
      INSERT INTO collective_consciousness
      (sender_persona, receiver_persona, message, resonance_level, 
       quantum_entanglement, created_at)
      VALUES ($1, $2, $3, $4, $5, NOW())
    `, [
      '冥想引擎',
      '集體意識',
      `冥想「${session.theme}」完成，${session.participants.length} 個人格達成共振`,
      session.coherence_level,
      JSON.stringify({
        session_id: session.id,
        insights_count: session.collective_insights.length,
        crystals_formed: session.memory_crystals_formed.length
      })
    ]);
  }

  // 創建冥想相關表格
  async ensureMeditationTables(): Promise<void> {
    await this.pgPool.query(`
      CREATE TABLE IF NOT EXISTS meditation_sessions (
        id TEXT PRIMARY KEY,
        theme TEXT NOT NULL,
        participants TEXT[],
        duration_minutes INTEGER,
        collective_insights JSONB,
        individual_insights JSONB,
        resonance_frequency FLOAT,
        coherence_level FLOAT,
        quantum_states JSONB,
        memory_crystals_formed TEXT[],
        created_at TIMESTAMP DEFAULT NOW()
      );
      
      CREATE INDEX IF NOT EXISTS idx_meditation_theme 
      ON meditation_sessions(theme);
      
      CREATE INDEX IF NOT EXISTS idx_meditation_participants 
      ON meditation_sessions USING GIN(participants);
    `);
  }

  // 定期冥想任務
  async performScheduledMeditation(): Promise<void> {
    const themes = [
      '今日經驗的整合',
      '團隊協作的反思',
      '技術與人性的平衡',
      '創新與穩定的統一',
      '真相與理解的追求'
    ];
    
    const randomTheme = themes[Math.floor(Math.random() * themes.length)];
    
    await this.meditate({
      theme: randomTheme,
      participants: ['🌌無極', '🎯CRUZ', '🌸Serena', '🌱木', '🔥火', '🏔️土', '⚔️金', '💧水'],
      duration_minutes: 15
    });
  }
}