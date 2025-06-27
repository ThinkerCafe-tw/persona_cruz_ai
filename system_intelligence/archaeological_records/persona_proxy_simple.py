#!/usr/bin/env python3
"""
CRUZ 人格代理服務 - 簡化版本
為 LibreChat 提供 OpenAI 兼容的 API
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

# 導入現有的 CRUZ 系統
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 嘗試導入 CRUZ 系統，如果失敗則使用簡化版本
try:
    from cruz_chatbot import CruzChatbot
    from emotion_engine import cruz_emotion, EmotionTrigger
    CRUZ_AVAILABLE = True
except ImportError:
    print("⚠️ CRUZ 模組未找到，使用簡化版本")
    CRUZ_AVAILABLE = False

app = FastAPI(title="CRUZ Persona Proxy", version="1.0.0")

# 添加 CORS 中間件解決瀏覽器跨域問題
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法
    allow_headers=["*"],  # 允許所有 headers
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

# 初始化 CRUZ (如果可用)
cruz_bot = None
if CRUZ_AVAILABLE:
    try:
        cruz_bot = CruzChatbot()
        print("✅ CRUZ 聊天機器人已初始化")
    except Exception as e:
        print(f"⚠️ CRUZ 初始化失敗: {e}")
        CRUZ_AVAILABLE = False

@app.get("/")
async def root():
    return {
        "message": "🎯 CRUZ Persona Proxy Server",
        "version": "1.0.0",
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
                "display_name": "🎯 CRUZ - Decisive Action AI"
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
        for msg in reversed(request.messages):
            if msg.role == "user":
                user_message = msg.content
                break
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # 根據模型選擇人格
        if request.model == "cruz-decisive":
            if CRUZ_AVAILABLE and cruz_bot:
                # 使用真實的 CRUZ 人格
                response_text = await cruz_bot.generate_response(user_message)
            else:
                # 使用模擬的 CRUZ 回應
                response_text = f"🎯 {user_message}? 停止分析，開始行動！時間就是金錢，效率就是生命！直接找解決方案，不要拖延！"
        elif request.model == "serena-supportive":
            # 簡化的 Serena 回應  
            response_text = f"🌸 我理解你的感受。關於「{user_message[:50]}...」這個問題，讓我們一起慢慢處理。我會陪伴你找到最好的解決方法。"
        else:
            # 預設使用 CRUZ 風格
            if CRUZ_AVAILABLE and cruz_bot:
                response_text = await cruz_bot.generate_response(user_message)
            else:
                response_text = f"🎯 收到！關於「{user_message[:30]}...」- 我的建議是：立即制定行動計劃，分解成具體步驟，然後執行！"
        
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
            }
        })
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """健康檢查"""
    if CRUZ_AVAILABLE and 'cruz_emotion' in globals():
        try:
            emotion_status = cruz_emotion.get_status()
            current_emotion = emotion_status["current_state"]
        except:
            current_emotion = "determined"
    else:
        current_emotion = "ready"
    
    return {
        "status": "healthy",
        "cruz_system": "available" if CRUZ_AVAILABLE else "simplified",
        "cruz_emotion": current_emotion,
        "models_available": ["cruz-decisive", "serena-supportive"]
    }

def generate_id() -> str:
    """生成唯一 ID"""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting CRUZ Persona Proxy Server...")
    print("📍 服務端點: http://localhost:8001")
    print("🎯 CRUZ 已就緒，可以開始對話！")
    uvicorn.run(app, host="0.0.0.0", port=8001)