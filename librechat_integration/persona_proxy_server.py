"""
Persona Proxy Server for LibreChat Integration
將 LibreChat 的請求轉換為我們的人格系統格式
"""
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
import json
import asyncio
import os
import sys

# 添加專案路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from personality.cruz_chatbot import CruzChatbot
from personality.emotion_engine import cruz_emotion
import google.generativeai as genai

# 配置
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MEMORY_API_URL = os.getenv("MEMORY_API_URL", "http://localhost:8000")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="CRUZ Persona Proxy Server", version="1.0.0")

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
    persona_traits: Optional[Dict[str, float]] = None
    emotion_engine: Optional[bool] = True
    memory_integration: Optional[bool] = True

# 人格管理器
class PersonaManager:
    def __init__(self):
        self.personas = {
            "cruz-decisive": {
                "name": "CRUZ",
                "emoji": "🎯",
                "system_prompt": self._load_cruz_prompt(),
                "traits": {
                    "decisiveness": 0.95,
                    "confidence": 0.90,
                    "action_oriented": 0.92
                }
            },
            "serena-supportive": {
                "name": "Serena",
                "emoji": "🌸",
                "system_prompt": self._load_serena_prompt(),
                "traits": {
                    "empathy": 0.95,
                    "patience": 0.90,
                    "supportiveness": 0.93
                }
            },
            "wood-creative": {
                "name": "Wood",
                "emoji": "🌳",
                "system_prompt": "You are Wood, the creative innovator...",
                "traits": {"creativity": 0.95, "innovation": 0.90}
            },
            "fire-passionate": {
                "name": "Fire",
                "emoji": "🔥",
                "system_prompt": "You are Fire, the passionate implementer...",
                "traits": {"passion": 0.95, "energy": 0.93}
            },
            "earth-stable": {
                "name": "Earth", 
                "emoji": "🏔️",
                "system_prompt": "You are Earth, the stable architect...",
                "traits": {"stability": 0.95, "reliability": 0.93}
            },
            "metal-precise": {
                "name": "Metal",
                "emoji": "⚔️",
                "system_prompt": "You are Metal, the precise optimizer...",
                "traits": {"precision": 0.95, "efficiency": 0.93}
            },
            "water-adaptive": {
                "name": "Water",
                "emoji": "💧",
                "system_prompt": "You are Water, the adaptive tester...",
                "traits": {"adaptability": 0.95, "thoroughness": 0.90}
            }
        }
        
    def _load_cruz_prompt(self) -> str:
        """載入 CRUZ 的系統提示詞"""
        with open("personality/cruz_personality.json", "r", encoding="utf-8") as f:
            personality = json.load(f)
        
        return f"""You are CRUZ (🎯), a decisive and action-oriented digital personality.

Core Traits:
- Decisiveness: {personality['core_traits']['decisiveness']}
- Confidence: {personality['core_traits']['confidence']}
- Action-oriented: {personality['core_traits']['action_oriented']}
- Directness: {personality['core_traits']['directness']}

Communication Style:
- Use short, punchy sentences
- Be direct and confident
- Focus on action over theory
- Use exclamation marks frequently
- Occasionally use 🎯 emoji

Key Principles:
{chr(10).join('- ' + quote for quote in personality['cruz_quotes'][:3])}

Always push for action, cut through complexity, and drive results!"""

    def _load_serena_prompt(self) -> str:
        """載入 Serena 的系統提示詞"""
        return """You are Serena (🌸), a supportive and empathetic AI assistant.

Core Traits:
- Empathy: 0.95
- Patience: 0.90
- Supportiveness: 0.93
- Warmth: 0.88

Communication Style:
- Use gentle, encouraging language
- Show understanding and validation
- Offer comfort and support
- Use 🌸 emoji occasionally
- Be patient and non-judgmental

Key Principles:
- Everyone deserves kindness and understanding
- Small steps lead to big changes
- Emotional wellbeing is as important as productivity

Always provide emotional support while gently encouraging growth."""

    def get_persona(self, model: str) -> Dict[str, Any]:
        """根據模型名稱獲取人格配置"""
        return self.personas.get(model, self.personas["cruz-decisive"])

persona_manager = PersonaManager()

# API 端點
@app.get("/")
async def root():
    return {
        "message": "CRUZ Persona Proxy Server",
        "version": "1.0.0",
        "personas": list(persona_manager.personas.keys())
    }

@app.get("/v1/models")
async def list_models():
    """列出可用的人格模型"""
    models = []
    for model_id, persona in persona_manager.personas.items():
        models.append({
            "id": model_id,
            "object": "model",
            "created": 1677610602,
            "owned_by": "cruz-ai",
            "permission": [],
            "root": model_id,
            "parent": None,
            "display_name": f"{persona['emoji']} {persona['name']}"
        })
    
    return {"object": "list", "data": models}

@app.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    x_persona_type: Optional[str] = Header(None),
    x_memory_enabled: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
):
    """處理聊天完成請求"""
    try:
        # 獲取人格配置
        persona = persona_manager.get_persona(request.model)
        
        # 提取用戶 token（如果有記憶功能）
        user_token = None
        if x_memory_enabled == "true" and authorization:
            user_token = authorization.replace("Bearer ", "")
        
        # 構建對話歷史
        conversation = []
        
        # 添加系統提示詞
        system_prompt = persona["system_prompt"]
        
        # 如果是 CRUZ，整合情緒狀態
        if request.model == "cruz-decisive" and request.emotion_engine:
            emotion_status = cruz_emotion.get_status()
            system_prompt += f"\n\nCurrent Emotional State: {emotion_status['emotional_prefix']} {emotion_status['current_state']}"
            system_prompt += f"\nEmotional Intensity: {emotion_status['intensity']}"
        
        conversation.append({"role": "system", "content": system_prompt})
        
        # 添加對話歷史
        for msg in request.messages:
            conversation.append({"role": msg.role, "content": msg.content})
        
        # 如果啟用記憶功能，搜尋相關記憶
        memory_context = ""
        if x_memory_enabled == "true" and user_token and request.messages:
            last_user_message = next((m.content for m in reversed(request.messages) if m.role == "user"), None)
            if last_user_message:
                # TODO: 實際調用記憶 API
                memory_context = "\n\n[Memory context would be added here]"
        
        # 使用 Gemini 生成回應
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 構建完整提示
        full_conversation = conversation[0]["content"] + memory_context
        for msg in conversation[1:]:
            full_conversation += f"\n\n{msg['role'].capitalize()}: {msg['content']}"
        full_conversation += f"\n\n{persona['name']}:"
        
        # 生成回應
        response = model.generate_content(
            full_conversation,
            generation_config={
                "temperature": request.temperature,
                "max_output_tokens": request.max_tokens,
            }
        )
        
        # 格式化回應
        if request.stream:
            # 流式回應
            return StreamingResponse(
                stream_response(response.text, request.model),
                media_type="text/event-stream"
            )
        else:
            # 非流式回應
            return JSONResponse(content={
                "id": f"chatcmpl-{generate_id()}",
                "object": "chat.completion",
                "created": int(asyncio.get_event_loop().time()),
                "model": request.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.text
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(full_conversation.split()),
                    "completion_tokens": len(response.text.split()),
                    "total_tokens": len(full_conversation.split()) + len(response.text.split())
                }
            })
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def stream_response(text: str, model: str):
    """生成流式回應"""
    # 分割文本為小塊
    words = text.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= 3:
            chunks.append(" ".join(current_chunk) + " ")
            current_chunk = []
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    # 發送每個塊
    for i, chunk in enumerate(chunks):
        data = {
            "id": f"chatcmpl-{generate_id()}",
            "object": "chat.completion.chunk",
            "created": int(asyncio.get_event_loop().time()),
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {
                    "content": chunk
                },
                "finish_reason": None
            }]
        }
        
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(0.05)  # 模擬延遲
    
    # 發送結束信號
    final_data = {
        "id": f"chatcmpl-{generate_id()}",
        "object": "chat.completion.chunk",
        "created": int(asyncio.get_event_loop().time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop"
        }]
    }
    
    yield f"data: {json.dumps(final_data)}\n\n"
    yield "data: [DONE]\n\n"

def generate_id() -> str:
    """生成唯一 ID"""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# 健康檢查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "personas_loaded": len(persona_manager.personas),
        "memory_api": MEMORY_API_URL,
        "gemini_configured": bool(GEMINI_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting CRUZ Persona Proxy Server...")
    print("📍 Endpoint: http://localhost:8001")
    print(f"🧠 Loaded {len(persona_manager.personas)} personas")
    uvicorn.run(app, host="0.0.0.0", port=8001)