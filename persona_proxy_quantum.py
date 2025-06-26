#!/usr/bin/env python3
"""
CRUZ 人格代理服務 - 量子記憶增強版
整合量子記憶系統，提供智能化回應
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
import os
import sys
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加專案路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Railway 環境檢測
RAILWAY_ENV = os.getenv("RAILWAY_ENVIRONMENT")

# 導入量子記憶系統
try:
    # 設定資料庫連接（Railway 共用資料庫）
    if RAILWAY_ENV:
        # Railway 環境使用內部 URL
        os.environ['DATABASE_URL'] = os.getenv('DATABASE_PRIVATE_URL', os.getenv('DATABASE_URL', ''))
        logger.info(f"🚂 Railway 環境偵測：使用共用量子記憶資料庫")
    
    from quantum_integration import QuantumIntegration
    quantum_integration = QuantumIntegration()
    QUANTUM_AVAILABLE = True
    logger.info("✅ 量子記憶系統已載入")
except Exception as e:
    logger.warning(f"⚠️ 量子記憶系統載入失敗: {e}")
    QUANTUM_AVAILABLE = False

# 嘗試導入 CRUZ 系統
try:
    from cruz_chatbot import CruzChatbot
    from emotion_engine import cruz_emotion, EmotionTrigger
    CRUZ_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ CRUZ 模組未找到，使用增強版本")
    CRUZ_AVAILABLE = False

app = FastAPI(title="CRUZ Quantum Persona Proxy", version="2.0.0")

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 請求模型
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.8
    max_tokens: Optional[int] = 4096
    stream: Optional[bool] = False
    user: Optional[str] = "default_user"

# CRUZ 決策回應系統
class CruzDecisionEngine:
    """增強版 CRUZ 決策引擎"""
    
    def __init__(self):
        self.patterns = {
            "學習": {
                "keywords": ["學習", "學", "教", "不知道", "不懂", "怎麼"],
                "responses": [
                    "🎯 學習？別想太多！先動手做！\n1. 選一個專案\n2. 寫第一行程式碼\n3. 遇到問題再查！\n行動勝過完美計劃！",
                    "🎯 學新技能？簡單！\n1. 今天就開始\n2. 每天30分鐘\n3. 實作大於理論！\n停止規劃，開始執行！"
                ]
            },
            "專案": {
                "keywords": ["專案", "項目", "計劃", "計畫", "30天", "完成"],
                "responses": [
                    "🎯 30天完成專案？沒問題！\n第1週：MVP原型\n第2週：核心功能\n第3週：優化調整\n第4週：上線發布！\n現在就開始！",
                    "🎯 專案管理秘訣：\n1. 定義最小可行產品\n2. 每日衝刺目標\n3. 週檢討月發布！\n別等完美，先出貨！"
                ]
            },
            "效率": {
                "keywords": ["效率", "生產力", "時間", "拖延", "管理"],
                "responses": [
                    "🎯 提高效率？立即執行！\n1. 番茄工作法25分鐘\n2. 關閉所有通知\n3. 一次只做一件事！\n效率就是專注！",
                    "🎯 時間管理金律：\n1. 早上處理最難的事\n2. 批次處理瑣事\n3. 說不的藝術！\n時間就是生命！"
                ]
            },
            "決策": {
                "keywords": ["選擇", "決定", "猶豫", "不確定", "該"],
                "responses": [
                    "🎯 猶豫？停！\n1. 列出選項\n2. 設定期限\n3. 相信直覺！\n錯誤決定勝過不決定！",
                    "🎯 決策框架：\n1. 這能帶來行動嗎？\n2. 失敗成本多高？\n3. 現在就選！\n分析癱瘓是進步的敵人！"
                ]
            }
        }
        
    def get_response(self, user_input: str) -> str:
        """根據用戶輸入生成 CRUZ 風格回應"""
        # 檢查關鍵詞匹配
        for category, data in self.patterns.items():
            for keyword in data["keywords"]:
                if keyword in user_input:
                    import random
                    return random.choice(data["responses"])
        
        # 預設回應
        return f"🎯 {user_input[:20]}...？別想了！\n1. 定義目標\n2. 制定計劃\n3. 立即行動！\n思考是行動的敵人！現在就開始！"

# 初始化決策引擎
cruz_engine = CruzDecisionEngine()

# 初始化 CRUZ (如果可用)
cruz_bot = None
if CRUZ_AVAILABLE:
    try:
        cruz_bot = CruzChatbot()
        logger.info("✅ CRUZ 聊天機器人已初始化")
    except Exception as e:
        logger.warning(f"⚠️ CRUZ 初始化失敗: {e}")
        CRUZ_AVAILABLE = False

@app.get("/")
async def root():
    return {
        "message": "🎯 CRUZ Quantum Persona Proxy",
        "version": "2.0.0",
        "quantum_memory": "enabled" if QUANTUM_AVAILABLE else "disabled",
        "status": "ready"
    }

@app.get("/v1/models")
async def list_models():
    """列出可用的人格模型"""
    return {
        "object": "list",
        "data": [
            {
                "id": "cruz-decisive",
                "object": "model",
                "created": 1677610602,
                "owned_by": "cruz-ai",
                "display_name": "🎯 CRUZ - Quantum Enhanced"
            },
            {
                "id": "serena-supportive", 
                "object": "model",
                "created": 1677610602,
                "owned_by": "cruz-ai",
                "display_name": "🌸 Serena - Supportive AI"
            }
        ]
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """處理聊天完成請求"""
    try:
        # 提取最後的用戶訊息
        user_message = ""
        conversation_history = []
        
        for msg in request.messages:
            if msg.role == "user":
                user_message = msg.content
            conversation_history.append({"role": msg.role, "content": msg.content})
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # 量子記憶搜尋（如果可用）
        memory_context = ""
        if QUANTUM_AVAILABLE:
            try:
                # 搜尋相關記憶
                memories = quantum_integration.bridge.search_memories(
                    query=user_message,
                    limit=3,
                    persona="CRUZ"
                )
                
                if memories:
                    memory_context = "\n[量子記憶]:\n"
                    for mem in memories:
                        memory_context += f"- {mem.content[:100]}...\n"
                    logger.info(f"找到 {len(memories)} 個相關記憶")
                    
            except Exception as e:
                logger.warning(f"量子記憶搜尋失敗: {e}")
        
        # 根據模型選擇人格
        if request.model == "cruz-decisive":
            if CRUZ_AVAILABLE and cruz_bot:
                # 使用真實的 CRUZ 人格
                response_text = await cruz_bot.generate_response(user_message)
            else:
                # 使用增強版 CRUZ 回應
                base_response = cruz_engine.get_response(user_message)
                
                # 如果有量子記憶，增強回應
                if memory_context:
                    response_text = f"{base_response}\n\n💡 基於過往經驗：{memory_context}"
                else:
                    response_text = base_response
                    
        elif request.model == "serena-supportive":
            # Serena 回應  
            response_text = f"🌸 我理解你的感受。關於「{user_message[:50]}...」\n讓我們一起慢慢探索這個問題。記住，每一步前進都是進步。我會一直陪伴你。"
        else:
            # 預設使用 CRUZ 風格
            response_text = cruz_engine.get_response(user_message)
        
        # 儲存到量子記憶（如果可用）
        if QUANTUM_AVAILABLE:
            try:
                quantum_integration.process_conversation(
                    user_id=request.user or "web_user",
                    message=user_message,
                    response=response_text,
                    current_role=request.model.split("-")[0],
                    emotion="determined"
                )
                logger.info("對話已同步到量子記憶")
            except Exception as e:
                logger.warning(f"量子記憶儲存失敗: {e}")
        
        # 回傳 OpenAI 格式的回應
        return JSONResponse(content={
            "id": f"chatcmpl-{generate_id()}",
            "object": "chat.completion", 
            "created": int(asyncio.get_event_loop().time()),
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(user_message.split()) + len(response_text.split())
            },
            "quantum_memory": QUANTUM_AVAILABLE
        })
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """健康檢查"""
    health_data = {
        "status": "healthy",
        "cruz_system": "available" if CRUZ_AVAILABLE else "enhanced",
        "quantum_memory": "enabled" if QUANTUM_AVAILABLE else "disabled",
        "models_available": ["cruz-decisive", "serena-supportive"]
    }
    
    # 檢查量子記憶狀態
    if QUANTUM_AVAILABLE:
        try:
            status = quantum_integration.monitor.get_status()
            health_data["quantum_status"] = {
                "total_memories": status.get("total_memories", 0),
                "active_personas": status.get("active_personas", [])
            }
        except:
            health_data["quantum_status"] = "error"
    
    if CRUZ_AVAILABLE and 'cruz_emotion' in globals():
        try:
            emotion_status = cruz_emotion.get_status()
            health_data["cruz_emotion"] = emotion_status["current_state"]
        except:
            health_data["cruz_emotion"] = "determined"
    else:
        health_data["cruz_emotion"] = "ready"
    
    return health_data

def generate_id() -> str:
    """生成唯一 ID"""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

if __name__ == "__main__":
    import uvicorn
    
    # Railway 環境檢測
    PORT = int(os.getenv("PORT", 8001))
    RAILWAY_ENV = os.getenv("RAILWAY_ENVIRONMENT")
    
    print("🚀 Starting CRUZ Quantum Persona Proxy Server...")
    print(f"🌍 環境: {'Railway - ' + RAILWAY_ENV if RAILWAY_ENV else '本地開發'}")
    print("🧠 量子記憶系統：" + ("已啟用" if QUANTUM_AVAILABLE else "未啟用"))
    print(f"📍 服務端點: http://0.0.0.0:{PORT}")
    print("🎯 CRUZ 準備就緒，開始量子增強對話！")
    
    # 使用 Railway 提供的 PORT
    uvicorn.run(app, host="0.0.0.0", port=PORT)