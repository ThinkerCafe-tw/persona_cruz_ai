"""
CRUZ AI SDK for Python
跨平台同步客戶端
"""
import asyncio
import json
import logging
from typing import Dict, Optional, Any, Callable, List
from datetime import datetime
import httpx
import websockets
from dataclasses import dataclass, asdict
from enum import Enum

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 人格類型
class PersonaType(Enum):
    CRUZ_DECISIVE = "cruz-decisive"
    SERENA_SUPPORTIVE = "serena-supportive"
    WOOD_CREATIVE = "wood-creative"
    FIRE_PASSIONATE = "fire-passionate"
    EARTH_STABLE = "earth-stable"
    METAL_PRECISE = "metal-precise"
    WATER_ADAPTIVE = "water-adaptive"

# 資料類別
@dataclass
class Message:
    platform: str
    user_id: str
    message: str
    persona: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Response:
    message_id: str
    platform: str
    user_id: str
    persona: str
    response: str
    emotion: Optional[str] = None
    memory_used: bool = False
    timestamp: str

@dataclass
class Session:
    current_persona: str
    memory_enabled: bool
    platforms: List[str]
    last_sync: Optional[str] = None

class CruzAISDK:
    """CRUZ AI Python SDK"""
    
    def __init__(
        self,
        api_key: str,
        platform: str,
        api_url: str = "http://localhost:8002",
        ws_url: str = "ws://localhost:8002",
        auto_reconnect: bool = True,
        reconnect_interval: int = 5
    ):
        self.api_key = api_key
        self.platform = platform
        self.api_url = api_url
        self.ws_url = ws_url
        self.auto_reconnect = auto_reconnect
        self.reconnect_interval = reconnect_interval
        
        self.user_id: Optional[str] = None
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.event_handlers: Dict[str, List[Callable]] = {}
        self._running = False
        self._reconnect_task: Optional[asyncio.Task] = None
        
    async def initialize(self, user_id: str) -> None:
        """初始化 SDK"""
        self.user_id = user_id
        await self._connect_websocket()
        
    async def _connect_websocket(self) -> None:
        """連接 WebSocket"""
        if not self.user_id:
            raise ValueError("User ID is required")
        
        try:
            self.ws = await websockets.connect(f"{self.ws_url}/ws/{self.user_id}")
            logger.info(f"🔌 WebSocket connected for user {self.user_id}")
            
            # 註冊平台
            await self._send({
                "type": "platform_register",
                "platform": self.platform
            })
            
            # 開始監聽
            self._running = True
            asyncio.create_task(self._listen())
            
        except Exception as e:
            logger.error(f"Failed to connect WebSocket: {e}")
            if self.auto_reconnect:
                await self._schedule_reconnect()
    
    async def _listen(self) -> None:
        """監聽 WebSocket 消息"""
        try:
            while self._running and self.ws:
                message = await self.ws.recv()
                data = json.loads(message)
                await self._handle_sync_event(data)
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed")
            if self.auto_reconnect:
                await self._schedule_reconnect()
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
    
    async def _handle_sync_event(self, event: Dict[str, Any]) -> None:
        """處理同步事件"""
        event_type = event.get("event_type", "")
        
        if event_type == "connection_established":
            session = Session(**event.get("session", {}))
            await self._emit("session_ready", session)
        elif event_type == "persona_changed":
            await self._emit("persona_changed", event)
        elif event_type == "memory_toggled":
            await self._emit("memory_toggled", event)
        elif event_type == "message_sync":
            await self._emit("message_sync", event)
        else:
            await self._emit(event_type, event)
    
    async def _schedule_reconnect(self) -> None:
        """安排重連"""
        if self._reconnect_task and not self._reconnect_task.done():
            return
        
        logger.info(f"🔄 Reconnecting in {self.reconnect_interval} seconds...")
        await asyncio.sleep(self.reconnect_interval)
        
        if self._running:
            await self._connect_websocket()
    
    async def send_message(
        self,
        message: str,
        persona: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Response:
        """發送消息"""
        if not self.user_id:
            raise RuntimeError("SDK not initialized")
        
        msg = Message(
            platform=self.platform,
            user_id=self.user_id,
            message=message,
            persona=persona,
            context=context,
            metadata=metadata
        )
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/message/unified",
                json=asdict(msg),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")
            
            data = response.json()
            return Response(**data)
    
    async def switch_persona(self, persona: PersonaType) -> None:
        """切換人格"""
        await self._send({
            "type": "persona_change",
            "persona": persona.value
        })
    
    async def toggle_memory(self, enabled: bool) -> None:
        """切換記憶功能"""
        await self._send({
            "type": "memory_toggle",
            "enabled": enabled
        })
    
    async def get_session(self) -> Session:
        """獲取會話狀態"""
        if not self.user_id:
            raise RuntimeError("SDK not initialized")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/user/{self.user_id}/session",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")
            
            data = response.json()
            return Session(**data["session"])
    
    async def _send(self, data: Dict[str, Any]) -> None:
        """發送 WebSocket 消息"""
        if self.ws and not self.ws.closed:
            await self.ws.send(json.dumps(data))
        else:
            logger.warning("WebSocket not connected")
    
    def on(self, event: str, handler: Callable) -> None:
        """註冊事件處理器"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def off(self, event: str, handler: Callable) -> None:
        """移除事件處理器"""
        if event in self.event_handlers:
            self.event_handlers[event].remove(handler)
    
    async def _emit(self, event: str, data: Any) -> None:
        """觸發事件"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    logger.error(f"Error in event handler for {event}: {e}")
    
    async def disconnect(self) -> None:
        """斷開連接"""
        self._running = False
        
        if self._reconnect_task:
            self._reconnect_task.cancel()
        
        if self.ws:
            await self.ws.close()
            self.ws = None

# 便利函數
def create_cruz_ai(api_key: str, platform: str, **kwargs) -> CruzAISDK:
    """創建 CRUZ AI SDK 實例"""
    return CruzAISDK(api_key, platform, **kwargs)

# 使用範例
async def example_usage():
    """SDK 使用範例"""
    # 創建 SDK
    sdk = create_cruz_ai(
        api_key="your-api-key",
        platform="python-client"
    )
    
    # 初始化
    await sdk.initialize("user123")
    
    # 註冊事件處理器
    def on_persona_changed(event):
        print(f"人格已切換: {event['persona']}")
    
    sdk.on("persona_changed", on_persona_changed)
    
    # 發送消息
    response = await sdk.send_message(
        message="我需要一些動力來完成我的專案",
        persona=PersonaType.CRUZ_DECISIVE.value
    )
    print(f"🎯 CRUZ: {response.response}")
    
    # 切換人格
    await sdk.switch_persona(PersonaType.SERENA_SUPPORTIVE)
    
    # 獲取會話狀態
    session = await sdk.get_session()
    print(f"當前人格: {session.current_persona}")
    print(f"記憶啟用: {session.memory_enabled}")
    
    # 保持連接一段時間
    await asyncio.sleep(10)
    
    # 斷開連接
    await sdk.disconnect()

if __name__ == "__main__":
    # 運行範例
    asyncio.run(example_usage())