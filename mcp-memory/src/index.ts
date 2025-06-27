#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// 記憶層管理器
import { MemoryLayerManager } from "./memory/MemoryLayerManager.js";
import { ReflectionEngine } from "./reflection/ReflectionEngine.js";
import { MeditationService } from "./meditation/MeditationService.js";

const server = new Server(
  {
    name: "mcp-memory",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 初始化服務
const memoryManager = new MemoryLayerManager();
const reflectionEngine = new ReflectionEngine();
const meditationService = new MeditationService();

// 定義工具
const TOOLS = [
  {
    name: "store_memory",
    description: "儲存記憶到三層系統（主記憶、稀疏記憶、元記憶）",
    inputSchema: z.object({
      content: z.string().describe("記憶內容"),
      metadata: z.object({
        persona: z.string().optional().describe("相關人格"),
        importance: z.number().min(0).max(1).describe("重要性評分"),
        category: z.string().describe("分類：insight|bug|decision|emotion|learning"),
        tags: z.array(z.string()).optional().describe("標籤")
      }),
      trigger_reflection: z.boolean().default(true).describe("是否觸發反思")
    }).strict()
  },
  {
    name: "search_memories", 
    description: "搜尋相關記憶（支援語意搜尋）",
    inputSchema: z.object({
      query: z.string().describe("搜尋關鍵字或問題"),
      layers: z.array(z.enum(["main", "sparse", "meta"])).default(["main", "sparse", "meta"]).describe("搜尋哪些記憶層"),
      limit: z.number().default(10).describe("返回結果數量"),
      persona: z.string().optional().describe("限定特定人格的記憶")
    }).strict()
  },
  {
    name: "reflect_on_memory",
    description: "對記憶進行深度反思並更新",
    inputSchema: z.object({
      memory_id: z.string().optional().describe("特定記憶ID"),
      topic: z.string().optional().describe("反思主題"),
      depth: z.enum(["shallow", "deep", "quantum"]).default("deep").describe("反思深度")
    }).strict()
  },
  {
    name: "collective_meditation",
    description: "進行集體冥想並生成洞察",
    inputSchema: z.object({
      theme: z.string().describe("冥想主題"),
      participants: z.array(z.string()).default(["🌌無極", "🎯CRUZ", "🌸Serena", "🌱木", "🔥火", "🏔️土", "⚔️金", "💧水"]).describe("參與人格"),
      duration_minutes: z.number().default(15).describe("冥想時長")
    }).strict()
  },
  {
    name: "memory_gradient_promotion",
    description: "評估並提升記憶層級",
    inputSchema: z.object({
      time_range: z.string().default("24h").describe("評估時間範圍"),
      auto_promote: z.boolean().default(false).describe("是否自動提升合格記憶")
    }).strict()
  },
  {
    name: "sync_all_memories",
    description: "同步所有記憶層（pgvector、GitHub、本地）",
    inputSchema: z.object({
      direction: z.enum(["pull", "push", "bidirectional"]).default("bidirectional").describe("同步方向"),
      resolve_conflicts: z.enum(["newest", "highest_importance", "manual"]).default("newest").describe("衝突解決策略")
    }).strict()
  },
  {
    name: "generate_memory_report",
    description: "生成記憶系統報告",
    inputSchema: z.object({
      report_type: z.enum(["health", "insights", "patterns", "growth"]).describe("報告類型"),
      format: z.enum(["markdown", "json", "visual"]).default("markdown").describe("輸出格式")
    }).strict()
  }
];

// 註冊工具
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: TOOLS
}));

// 實現工具處理
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "store_memory": {
        const result = await memoryManager.storeMemory(
          args.content,
          args.metadata
        );
        
        if (args.trigger_reflection) {
          await reflectionEngine.reflect(result.memory_id);
        }
        
        return {
          content: [
            {
              type: "text",
              text: `✅ 記憶已儲存
- ID: ${result.memory_id}
- 層級: ${result.layer}
- 向量化: ${result.vectorized ? '完成' : '待處理'}
- 反思: ${args.trigger_reflection ? '已觸發' : '跳過'}`
            }
          ]
        };
      }

      case "search_memories": {
        const memories = await memoryManager.searchMemories(
          args.query,
          args.layers,
          args.limit,
          args.persona
        );
        
        return {
          content: [
            {
              type: "text",
              text: `🔍 找到 ${memories.length} 條相關記憶\n\n` +
                memories.map((m, i) => 
                  `${i + 1}. [${m.layer}] ${m.summary}\n` +
                  `   相關度: ${m.relevance.toFixed(2)} | ` +
                  `   時間: ${m.timestamp}\n` +
                  `   ${m.preview}`
                ).join('\n\n')
            }
          ]
        };
      }

      case "reflect_on_memory": {
        const reflection = await reflectionEngine.deepReflect({
          memory_id: args.memory_id,
          topic: args.topic,
          depth: args.depth
        });
        
        return {
          content: [
            {
              type: "text", 
              text: `🤔 反思完成\n\n` +
                `主題: ${reflection.topic}\n` +
                `深度: ${reflection.depth}\n\n` +
                `洞察:\n${reflection.insights.map(i => `- ${i}`).join('\n')}\n\n` +
                `行動建議:\n${reflection.actions.map(a => `- ${a}`).join('\n')}\n\n` +
                `記憶更新: ${reflection.memories_updated} 條`
            }
          ]
        };
      }

      case "collective_meditation": {
        const meditation = await meditationService.meditate({
          theme: args.theme,
          participants: args.participants,
          duration_minutes: args.duration_minutes
        });
        
        return {
          content: [
            {
              type: "text",
              text: `🧘 集體冥想完成\n\n` +
                `主題: ${meditation.theme}\n` +
                `參與者: ${meditation.participants.join(', ')}\n` +
                `共振頻率: ${meditation.resonance_frequency}Hz\n` +
                `相干度: ${meditation.coherence_level.toFixed(2)}\n\n` +
                `集體洞察:\n${meditation.collective_insights.join('\n')}\n\n` +
                `個體領悟:\n${Object.entries(meditation.individual_insights)
                  .map(([p, i]) => `${p}: ${i}`).join('\n')}`
            }
          ]
        };
      }

      case "memory_gradient_promotion": {
        const promotion = await memoryManager.evaluateAndPromote({
          time_range: args.time_range,
          auto_promote: args.auto_promote
        });
        
        return {
          content: [
            {
              type: "text",
              text: `📊 記憶層級評估完成\n\n` +
                `評估範圍: ${args.time_range}\n` +
                `評估記憶數: ${promotion.evaluated_count}\n\n` +
                `晉升建議:\n` +
                `- 主記憶 → 稀疏記憶: ${promotion.main_to_sparse.length} 條\n` +
                `- 稀疏記憶 → 元記憶: ${promotion.sparse_to_meta.length} 條\n\n` +
                `${args.auto_promote ? 
                  `✅ 已自動晉升 ${promotion.promoted_count} 條記憶` : 
                  `⏸️ 等待手動確認晉升`}`
            }
          ]
        };
      }

      case "sync_all_memories": {
        const sync = await memoryManager.syncAllLayers({
          direction: args.direction,
          resolve_conflicts: args.resolve_conflicts
        });
        
        return {
          content: [
            {
              type: "text",
              text: `🔄 記憶同步完成\n\n` +
                `同步方向: ${args.direction}\n` +
                `衝突解決: ${args.resolve_conflicts}\n\n` +
                `同步結果:\n` +
                `- pgvector: ${sync.pgvector.synced}/${sync.pgvector.total}\n` +
                `- GitHub: ${sync.github.synced}/${sync.github.total}\n` +
                `- 本地: ${sync.local.synced}/${sync.local.total}\n\n` +
                `衝突: ${sync.conflicts.length} 個${
                  sync.conflicts.length > 0 ? 
                  '\n' + sync.conflicts.map(c => `- ${c}`).join('\n') : ''
                }`
            }
          ]
        };
      }

      case "generate_memory_report": {
        const report = await memoryManager.generateReport({
          report_type: args.report_type,
          format: args.format
        });
        
        return {
          content: [
            {
              type: "text",
              text: report.content
            }
          ]
        };
      }

      default:
        throw new Error(`未知工具: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `❌ 錯誤: ${error.message}\n\n💡 這是真實的錯誤，不是表演。我們會從中學習。`
        }
      ]
    };
  }
});

// 啟動服務
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("🧠 MCP 記憶服務已啟動");
  
  // 初始化各層連接
  await memoryManager.initialize();
  console.error("✅ 記憶層已連接: pgvector + GitHub + 本地");
  
  // 啟動記憶守護進程
  memoryManager.startMemoryDaemon();
  console.error("👁️ 記憶守護進程已啟動");
}

main().catch((error) => {
  console.error("致命錯誤:", error);
  process.exit(1);
});