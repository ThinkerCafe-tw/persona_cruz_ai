#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import pg from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const { Pool } = pg;

// 資料庫連接
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://localhost/cruz_memory'
});

// 創建 MCP 服務器
const server = new Server(
  {
    name: "mcp-cruz",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

// 列出可用工具
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "remember_conversation",
        description: "記住一段對話內容",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string", description: "用戶ID" },
            user_message: { type: "string", description: "用戶說的話" },
            ai_response: { type: "string", description: "AI的回應" },
            context: { type: "object", description: "額外的上下文" }
          },
          required: ["user_id", "user_message", "ai_response"]
        }
      },
      {
        name: "search_memory",
        description: "搜尋相關記憶",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "搜尋關鍵字" },
            user_id: { type: "string", description: "限定用戶ID（可選）" },
            limit: { type: "number", description: "返回數量限制", default: 5 }
          },
          required: ["query"]
        }
      },
      {
        name: "analyze_understanding",
        description: "分析AI理解與用戶意圖的差距",
        inputSchema: {
          type: "object",
          properties: {
            conversation_id: { type: "string", description: "對話ID" },
            user_feedback: { type: "string", description: "用戶反饋" }
          },
          required: ["conversation_id"]
        }
      },
      {
        name: "get_user_context",
        description: "獲取用戶的完整上下文",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string", description: "用戶ID" }
          },
          required: ["user_id"]
        }
      }
    ]
  };
});

// 處理工具調用
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "remember_conversation": {
      try {
        const { user_id, user_message, ai_response, context = {} } = args;
        
        // 儲存到資料庫
        const result = await pool.query(
          `INSERT INTO conversations 
           (user_id, user_message, ai_response, context, created_at) 
           VALUES ($1, $2, $3, $4, NOW()) 
           RETURNING id`,
          [user_id, user_message, ai_response, JSON.stringify(context)]
        );
        
        return {
          content: [{
            type: "text",
            text: `✅ 記憶已儲存！對話ID: ${result.rows[0].id}`
          }]
        };
      } catch (error) {
        return {
          content: [{
            type: "text",
            text: `❌ 儲存失敗: ${error}`
          }]
        };
      }
    }

    case "search_memory": {
      try {
        const { query, user_id, limit = 5 } = args;
        
        let queryText = `
          SELECT * FROM conversations 
          WHERE (user_message ILIKE $1 OR ai_response ILIKE $1)
        `;
        const params: any[] = [`%${query}%`];
        
        if (user_id) {
          queryText += ` AND user_id = $2`;
          params.push(user_id);
        }
        
        queryText += ` ORDER BY created_at DESC LIMIT ${limit}`;
        
        const result = await pool.query(queryText, params);
        
        const memories = result.rows.map(row => ({
          id: row.id,
          user: row.user_message,
          ai: row.ai_response,
          time: row.created_at
        }));
        
        return {
          content: [{
            type: "text",
            text: `🔍 找到 ${memories.length} 個相關記憶:\n${JSON.stringify(memories, null, 2)}`
          }]
        };
      } catch (error) {
        return {
          content: [{
            type: "text",
            text: `❌ 搜尋失敗: ${error}`
          }]
        };
      }
    }

    case "analyze_understanding": {
      const { conversation_id, user_feedback } = args;
      
      // 簡單的理解分析
      const analysis = {
        conversation_id,
        feedback: user_feedback,
        gap_detected: user_feedback?.includes("不是") || user_feedback?.includes("錯"),
        suggestions: [
          "需要更多上下文",
          "確認用戶真實意圖",
          "提供具體範例"
        ]
      };
      
      return {
        content: [{
          type: "text",
          text: `📊 理解分析:\n${JSON.stringify(analysis, null, 2)}`
        }]
      };
    }

    case "get_user_context": {
      try {
        const { user_id } = args;
        
        // 獲取用戶最近的對話
        const result = await pool.query(
          `SELECT * FROM conversations 
           WHERE user_id = $1 
           ORDER BY created_at DESC 
           LIMIT 10`,
          [user_id]
        );
        
        const context = {
          user_id,
          conversation_count: result.rows.length,
          recent_topics: result.rows.map(r => r.user_message.substring(0, 50)),
          last_interaction: result.rows[0]?.created_at
        };
        
        return {
          content: [{
            type: "text",
            text: `👤 用戶上下文:\n${JSON.stringify(context, null, 2)}`
          }]
        };
      } catch (error) {
        return {
          content: [{
            type: "text",
            text: `❌ 獲取失敗: ${error}`
          }]
        };
      }
    }

    default:
      return {
        content: [{
          type: "text",
          text: `❌ 未知工具: ${name}`
        }]
      };
  }
});

// 列出資源
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "cruz://memory/stats",
        name: "記憶統計",
        description: "查看記憶系統的統計資訊",
        mimeType: "application/json"
      }
    ]
  };
});

// 讀取資源
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  
  if (uri === "cruz://memory/stats") {
    try {
      const stats = await pool.query(`
        SELECT 
          COUNT(DISTINCT user_id) as total_users,
          COUNT(*) as total_conversations,
          MAX(created_at) as last_update
        FROM conversations
      `);
      
      return {
        contents: [{
          uri,
          mimeType: "application/json",
          text: JSON.stringify(stats.rows[0], null, 2)
        }]
      };
    } catch (error) {
      return {
        contents: [{
          uri,
          mimeType: "text/plain",
          text: `Error: ${error}`
        }]
      };
    }
  }
  
  throw new Error(`Unknown resource: ${uri}`);
});

// 初始化資料庫表
async function initDatabase() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        user_message TEXT NOT NULL,
        ai_response TEXT NOT NULL,
        context JSONB DEFAULT '{}',
        created_at TIMESTAMP DEFAULT NOW(),
        INDEX idx_user_id (user_id),
        INDEX idx_created_at (created_at)
      )
    `);
    console.error("✅ 資料庫初始化完成");
  } catch (error) {
    console.error("⚠️ 資料庫初始化失敗:", error);
  }
}

// 啟動服務
async function main() {
  await initDatabase();
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("🎯 CRUZ MCP Server 已啟動");
}

main().catch((error) => {
  console.error("❌ 服務啟動失敗:", error);
  process.exit(1);
});