"""
統一 API Gateway - 跨平台同步核心
支援多平台（Discord, Telegram, Slack, WhatsApp）的統一接入點
"""
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Union
import asyncio
import json
import uuid
from datetime import datetime
import httpx
from contextlib import asynccontextmanager

# WebSocket 連接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        
        # 初始化用戶會話
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "current_persona": "cruz-decisive",
                "memory_enabled": True,
                "platforms": [],
                "last_sync": datetime.now().isoformat()
            }
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)
    
    async def broadcast_to_user(self, data: dict, user_id: str):
        message = json.dumps(data)
        await self.send_personal_message(message, user_id)

# 應用初始化
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時
    print("🌐 統一 API Gateway 啟動中...")
    yield
    # 關閉時
    print("👋 統一 API Gateway 關閉中...")

app = FastAPI(
    title="CRUZ AI 統一 API Gateway",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 設置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 連接管理器
manager = ConnectionManager()

# 安全認證
security = HTTPBearer()

# 資料模型
class UnifiedMessage(BaseModel):
    platform: str  # discord, telegram, slack, whatsapp, librechat
    user_id: str
    message: str
    persona: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}

class UnifiedResponse(BaseModel):
    message_id: str
    platform: str
    user_id: str
    persona: str
    response: str
    emotion: Optional[str] = None
    memory_used: bool = False
    timestamp: str

class SyncEvent(BaseModel):
    event_type: str  # persona_change, memory_toggle, conversation_sync
    platform: str
    user_id: str
    data: Dict[str, Any]
    timestamp: str

class PlatformConfig(BaseModel):
    platform: str
    enabled: bool
    webhook_url: Optional[str] = None
    api_key: Optional[str] = None
    features: List[str] = []

# 平台適配器
class PlatformAdapter:
    """平台適配器基類"""
    def __init__(self, platform: str):
        self.platform = platform
        self.config = {}
    
    async def send_message(self, user_id: str, message: str, metadata: dict = None):
        """發送消息到特定平台"""
        raise NotImplementedError
    
    async def process_webhook(self, data: dict) -> UnifiedMessage:
        """處理平台 webhook"""
        raise NotImplementedError

# Discord 適配器
class DiscordAdapter(PlatformAdapter):
    def __init__(self):
        super().__init__("discord")
    
    async def send_message(self, user_id: str, message: str, metadata: dict = None):
        # TODO: 實現 Discord API 調用
        print(f"[Discord] 發送給 {user_id}: {message}")
        return {"status": "sent", "platform": "discord"}
    
    async def process_webhook(self, data: dict) -> UnifiedMessage:
        return UnifiedMessage(
            platform="discord",
            user_id=data.get("author", {}).get("id", ""),
            message=data.get("content", ""),
            metadata={"channel_id": data.get("channel_id")}
        )

# Telegram 適配器
class TelegramAdapter(PlatformAdapter):
    def __init__(self):
        super().__init__("telegram")
    
    async def send_message(self, user_id: str, message: str, metadata: dict = None):
        # TODO: 實現 Telegram API 調用
        print(f"[Telegram] 發送給 {user_id}: {message}")
        return {"status": "sent", "platform": "telegram"}
    
    async def process_webhook(self, data: dict) -> UnifiedMessage:
        message = data.get("message", {})
        return UnifiedMessage(
            platform="telegram",
            user_id=str(message.get("from", {}).get("id", "")),
            message=message.get("text", ""),
            metadata={"chat_id": message.get("chat", {}).get("id")}
        )

# 平台管理器
platform_adapters = {
    "discord": DiscordAdapter(),
    "telegram": TelegramAdapter(),
    # TODO: 添加 Slack, WhatsApp 適配器
}

# API 端點
@app.get("/")
async def root():
    return {
        "service": "CRUZ AI Unified Gateway",
        "version": "1.0.0",
        "status": "operational",
        "supported_platforms": list(platform_adapters.keys()),
        "features": [
            "unified_messaging",
            "cross_platform_sync",
            "real_time_updates",
            "persona_management",
            "memory_integration"
        ]
    }

@app.post("/message/unified", response_model=UnifiedResponse)
async def unified_message(
    message: UnifiedMessage,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """統一消息處理端點"""
    try:
        # 生成消息 ID
        message_id = str(uuid.uuid4())
        
        # 獲取或設置人格
        user_session = manager.user_sessions.get(message.user_id, {})
        current_persona = message.persona or user_session.get("current_persona", "cruz-decisive")
        
        # 調用人格 API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8001/v1/chat/completions",
                json={
                    "model": current_persona,
                    "messages": [{"role": "user", "content": message.message}],
                    "stream": False
                },
                headers={
                    "x-persona-type": current_persona.split("-")[0],
                    "x-memory-enabled": str(user_session.get("memory_enabled", True)),
                    "Authorization": f"Bearer {credentials.credentials}"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                
                # 廣播同步事件
                sync_event = {
                    "event_type": "message_sync",
                    "platform": message.platform,
                    "user_id": message.user_id,
                    "data": {
                        "message_id": message_id,
                        "user_message": message.message,
                        "ai_response": ai_response,
                        "persona": current_persona
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
                await manager.broadcast_to_user(sync_event, message.user_id)
                
                return UnifiedResponse(
                    message_id=message_id,
                    platform=message.platform,
                    user_id=message.user_id,
                    persona=current_persona,
                    response=ai_response,
                    emotion="determined",  # TODO: 從情緒引擎獲取
                    memory_used=user_session.get("memory_enabled", True),
                    timestamp=datetime.now().isoformat()
                )
            else:
                raise HTTPException(status_code=response.status_code, detail="AI service error")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket 端點用於即時同步"""
    await manager.connect(websocket, user_id)
    
    try:
        # 發送初始狀態
        await manager.send_personal_message(
            json.dumps({
                "event_type": "connection_established",
                "user_id": user_id,
                "session": manager.user_sessions.get(user_id, {}),
                "timestamp": datetime.now().isoformat()
            }),
            user_id
        )
        
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 處理不同類型的事件
            if message["type"] == "persona_change":
                manager.user_sessions[user_id]["current_persona"] = message["persona"]
                # 廣播到所有連接的平台
                await manager.broadcast_to_user({
                    "event_type": "persona_changed",
                    "persona": message["persona"],
                    "timestamp": datetime.now().isoformat()
                }, user_id)
                
            elif message["type"] == "memory_toggle":
                manager.user_sessions[user_id]["memory_enabled"] = message["enabled"]
                await manager.broadcast_to_user({
                    "event_type": "memory_toggled",
                    "enabled": message["enabled"],
                    "timestamp": datetime.now().isoformat()
                }, user_id)
                
            elif message["type"] == "platform_register":
                if "platforms" not in manager.user_sessions[user_id]:
                    manager.user_sessions[user_id]["platforms"] = []
                if message["platform"] not in manager.user_sessions[user_id]["platforms"]:
                    manager.user_sessions[user_id]["platforms"].append(message["platform"])
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast_to_user({
            "event_type": "client_disconnected",
            "timestamp": datetime.now().isoformat()
        }, user_id)

@app.post("/sync/event")
async def sync_event(
    event: SyncEvent,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """處理跨平台同步事件"""
    # 廣播事件到用戶的所有連接
    await manager.broadcast_to_user(event.dict(), event.user_id)
    
    # 更新用戶會話
    if event.user_id in manager.user_sessions:
        manager.user_sessions[event.user_id]["last_sync"] = event.timestamp
    
    return {"status": "synced", "event_id": str(uuid.uuid4())}

@app.get("/user/{user_id}/session")
async def get_user_session(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """獲取用戶跨平台會話狀態"""
    session = manager.user_sessions.get(user_id, {
        "current_persona": "cruz-decisive",
        "memory_enabled": True,
        "platforms": [],
        "last_sync": None
    })
    
    return {
        "user_id": user_id,
        "session": session,
        "active_connections": len(manager.active_connections.get(user_id, [])),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/webhook/{platform}")
async def platform_webhook(platform: str, data: dict):
    """平台 Webhook 處理"""
    if platform not in platform_adapters:
        raise HTTPException(status_code=404, detail=f"Platform {platform} not supported")
    
    # 使用適配器處理 webhook
    adapter = platform_adapters[platform]
    unified_msg = await adapter.process_webhook(data)
    
    # 處理統一消息
    # TODO: 添加認證 token 處理
    fake_token = "platform_webhook_token"
    
    return {"status": "received", "platform": platform}

@app.get("/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "active_users": len(manager.user_sessions),
        "active_connections": sum(len(conns) for conns in manager.active_connections.values()),
        "supported_platforms": list(platform_adapters.keys()),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🌐 啟動 CRUZ AI 統一 API Gateway...")
    print("📍 端點: http://localhost:8002")
    print("🔌 WebSocket: ws://localhost:8002/ws/{user_id}")
    print("🎯 支援平台: Discord, Telegram, Slack, WhatsApp")
    uvicorn.run(app, host="0.0.0.0", port=8002)