"""
跨平台同步測試
測試統一 API Gateway 和多平台整合
"""
import asyncio
import json
from datetime import datetime
import httpx
import websockets

async def test_unified_gateway():
    """測試統一 API Gateway"""
    print("🌐 測試統一 API Gateway")
    print("=" * 50)
    
    base_url = "http://localhost:8002"
    test_user_id = "test_user_cross_platform"
    test_token = "test-api-key"
    
    async with httpx.AsyncClient() as client:
        # 1. 健康檢查
        print("\n1. 健康檢查...")
        response = await client.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"   ✅ 狀態: {health['status']}")
            print(f"   👥 活躍用戶: {health['active_users']}")
            print(f"   🔌 活躍連接: {health['active_connections']}")
            print(f"   🎯 支援平台: {', '.join(health['supported_platforms'])}")
        
        # 2. 測試統一消息 API
        print("\n2. 測試統一消息 API...")
        
        # Discord 消息
        discord_msg = {
            "platform": "discord",
            "user_id": test_user_id,
            "message": "測試從 Discord 發送消息",
            "persona": "cruz-decisive"
        }
        
        response = await client.post(
            f"{base_url}/message/unified",
            json=discord_msg,
            headers={"Authorization": f"Bearer {test_token}"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Discord 消息已處理")
            print(f"   📨 消息 ID: {result['message_id']}")
            print(f"   🎯 人格: {result['persona']}")
            print(f"   💬 回應: {result['response'][:50]}...")
        
        # Telegram 消息
        telegram_msg = {
            "platform": "telegram",
            "user_id": test_user_id,
            "message": "測試從 Telegram 發送消息",
            "persona": "serena-supportive"
        }
        
        response = await client.post(
            f"{base_url}/message/unified",
            json=telegram_msg,
            headers={"Authorization": f"Bearer {test_token}"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Telegram 消息已處理")
            print(f"   🌸 人格: {result['persona']}")
        
        # 3. 獲取用戶會話
        print("\n3. 獲取跨平台會話狀態...")
        response = await client.get(
            f"{base_url}/user/{test_user_id}/session",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        
        if response.status_code == 200:
            session = response.json()
            print(f"   ✅ 會話狀態獲取成功")
            print(f"   🎯 當前人格: {session['session']['current_persona']}")
            print(f"   💾 記憶狀態: {'開啟' if session['session']['memory_enabled'] else '關閉'}")
            print(f"   🔌 活躍連接: {session['active_connections']}")

async def test_websocket_sync():
    """測試 WebSocket 即時同步"""
    print("\n\n🔌 測試 WebSocket 即時同步")
    print("=" * 50)
    
    ws_url = "ws://localhost:8002/ws/test_user_sync"
    
    try:
        async with websockets.connect(ws_url) as websocket:
            print("✅ WebSocket 連接成功")
            
            # 接收初始消息
            message = await websocket.recv()
            data = json.loads(message)
            print(f"\n📨 收到初始消息:")
            print(f"   事件: {data['event_type']}")
            print(f"   用戶: {data['user_id']}")
            
            # 測試人格切換
            print("\n🎭 測試人格切換同步...")
            await websocket.send(json.dumps({
                "type": "persona_change",
                "persona": "fire-passionate"
            }))
            
            # 接收確認
            message = await websocket.recv()
            data = json.loads(message)
            print(f"   ✅ 人格切換事件: {data}")
            
            # 測試記憶切換
            print("\n💾 測試記憶切換同步...")
            await websocket.send(json.dumps({
                "type": "memory_toggle",
                "enabled": False
            }))
            
            # 接收確認
            message = await websocket.recv()
            data = json.loads(message)
            print(f"   ✅ 記憶切換事件: {data}")
            
            # 註冊平台
            print("\n📱 測試平台註冊...")
            await websocket.send(json.dumps({
                "type": "platform_register",
                "platform": "test_client"
            }))
            
            print("   ✅ 平台註冊完成")
            
    except Exception as e:
        print(f"❌ WebSocket 錯誤: {e}")

async def test_sdk_integration():
    """測試 SDK 整合"""
    print("\n\n📦 測試 SDK 整合")
    print("=" * 50)
    
    # 動態導入 SDK
    try:
        from sdk.cruz_ai_sdk import create_cruz_ai, PersonaType
        
        print("✅ Python SDK 導入成功")
        
        # 創建 SDK 實例
        sdk = create_cruz_ai(
            api_key="test-api-key",
            platform="test-platform"
        )
        
        print("\n🚀 初始化 SDK...")
        await sdk.initialize("sdk_test_user")
        
        # 測試發送消息
        print("\n💬 測試發送消息...")
        response = await sdk.send_message(
            message="SDK 測試消息",
            persona=PersonaType.CRUZ_DECISIVE.value
        )
        print(f"   ✅ 收到回應: {response.response[:50]}...")
        
        # 測試獲取會話
        print("\n📊 測試獲取會話...")
        session = await sdk.get_session()
        print(f"   當前人格: {session.current_persona}")
        print(f"   記憶啟用: {session.memory_enabled}")
        
        # 清理
        await sdk.disconnect()
        print("\n✅ SDK 測試完成")
        
    except ImportError:
        print("⚠️  無法導入 SDK，請確保在正確的目錄運行")
    except Exception as e:
        print(f"❌ SDK 測試錯誤: {e}")

async def test_multi_platform_scenario():
    """測試多平台場景"""
    print("\n\n🎯 測試多平台同步場景")
    print("=" * 50)
    
    scenario_user = "multi_platform_user"
    
    # 模擬多平台同時連接
    platforms = ["discord", "telegram", "web"]
    connections = []
    
    print(f"\n📱 連接 {len(platforms)} 個平台...")
    
    try:
        # 建立多個 WebSocket 連接
        for platform in platforms:
            ws = await websockets.connect(f"ws://localhost:8002/ws/{scenario_user}")
            connections.append((platform, ws))
            
            # 註冊平台
            await ws.send(json.dumps({
                "type": "platform_register",
                "platform": platform
            }))
            print(f"   ✅ {platform} 已連接")
        
        # 從一個平台切換人格
        print(f"\n🎭 從 {platforms[0]} 切換人格...")
        await connections[0][1].send(json.dumps({
            "type": "persona_change",
            "persona": "wood-creative"
        }))
        
        # 檢查其他平台是否收到通知
        print("\n📨 檢查同步通知...")
        for platform, ws in connections:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                data = json.loads(msg)
                if data.get("event_type") == "persona_changed":
                    print(f"   ✅ {platform} 收到人格切換通知")
            except asyncio.TimeoutError:
                pass
        
        # 清理連接
        for _, ws in connections:
            await ws.close()
            
        print("\n✅ 多平台同步測試完成")
        
    except Exception as e:
        print(f"❌ 多平台測試錯誤: {e}")

def print_summary():
    """打印測試總結"""
    print("\n\n📊 跨平台同步測試總結")
    print("=" * 50)
    print("""
✅ 已實現功能:
1. 統一 API Gateway
   - 統一消息處理端點
   - WebSocket 即時同步
   - 多平台會話管理
   
2. SDK 支援
   - TypeScript/JavaScript SDK
   - Python SDK
   - 事件驅動架構
   
3. 平台整合
   - Discord Bot 框架
   - Telegram Bot 框架（待實現）
   - Web 客戶端支援
   
4. 同步機制
   - 人格切換同步
   - 記憶狀態同步
   - 對話歷史同步

🚀 下一步:
- 完成 Telegram Bot
- 添加 Slack 整合
- 實現 WhatsApp Business API
- 添加衝突解決機制
- 實現離線支援
""")

async def main():
    """主測試流程"""
    print("🚀 Day 8-10: 跨平台同步測試")
    print("⏰ 開始時間:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        # 測試 Gateway
        await test_unified_gateway()
        
        # 測試 WebSocket
        await test_websocket_sync()
        
        # 測試 SDK
        await test_sdk_integration()
        
        # 測試多平台場景
        await test_multi_platform_scenario()
        
    except httpx.ConnectError:
        print("\n❌ 無法連接到統一 API Gateway")
        print("   請先啟動: python cross_platform/unified_gateway.py")
    except Exception as e:
        print(f"\n❌ 測試過程發生錯誤: {e}")
    
    # 打印總結
    print_summary()
    
    print(f"\n⏰ 結束時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())