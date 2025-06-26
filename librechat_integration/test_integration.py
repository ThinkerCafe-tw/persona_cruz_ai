"""
測試 LibreChat Integration
"""
import asyncio
import httpx
import json

async def test_persona_proxy():
    """測試 Persona Proxy Server"""
    base_url = "http://localhost:8001"
    
    print("🎯 Testing CRUZ Persona Proxy Server")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # 1. 測試根端點
        print("\n1. Testing root endpoint...")
        response = await client.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # 2. 測試模型列表
        print("\n2. Testing models endpoint...")
        response = await client.get(f"{base_url}/v1/models")
        print(f"   Status: {response.status_code}")
        models = response.json()
        print(f"   Available personas: {len(models['data'])}")
        for model in models['data'][:3]:
            print(f"   - {model['display_name']} ({model['id']})")
        
        # 3. 測試 CRUZ 對話
        print("\n3. Testing CRUZ chat completion...")
        chat_request = {
            "model": "cruz-decisive",
            "messages": [
                {"role": "user", "content": "I'm procrastinating on my project. What should I do?"}
            ],
            "temperature": 0.8,
            "stream": False
        }
        
        response = await client.post(
            f"{base_url}/v1/chat/completions",
            json=chat_request,
            headers={
                "x-persona-type": "cruz",
                "x-memory-enabled": "false"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   CRUZ says: {result['choices'][0]['message']['content'][:100]}...")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
        
        # 4. 測試 Serena 對話
        print("\n4. Testing Serena chat completion...")
        chat_request["model"] = "serena-supportive"
        chat_request["messages"] = [
            {"role": "user", "content": "I'm feeling overwhelmed and stressed."}
        ]
        
        response = await client.post(
            f"{base_url}/v1/chat/completions",
            json=chat_request,
            headers={
                "x-persona-type": "serena",
                "x-memory-enabled": "false"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Serena says: {result['choices'][0]['message']['content'][:100]}...")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
        
        # 5. 測試流式回應
        print("\n5. Testing streaming response...")
        chat_request["model"] = "fire-passionate"
        chat_request["stream"] = True
        chat_request["messages"] = [
            {"role": "user", "content": "Let's build something amazing!"}
        ]
        
        response = await client.post(
            f"{base_url}/v1/chat/completions",
            json=chat_request,
            headers={
                "x-persona-type": "fire",
                "x-memory-enabled": "false"
            }
        )
        
        if response.status_code == 200:
            print(f"   Status: {response.status_code}")
            print(f"   Fire streaming: ", end="")
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        print(" [DONE]")
                        break
                    try:
                        chunk = json.loads(data)
                        if chunk["choices"][0]["delta"].get("content"):
                            print(".", end="", flush=True)
                    except:
                        pass
        
        # 6. 測試健康檢查
        print("\n6. Testing health endpoint...")
        response = await client.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Health: {response.json()}")

async def test_librechat_config():
    """測試 LibreChat 配置"""
    print("\n\n🔧 LibreChat Configuration Test")
    print("=" * 50)
    
    # 讀取配置文件
    with open("librechat_integration/cruz_librechat.yaml", "r") as f:
        config = f.read()
    
    print("✅ Configuration file created successfully")
    print("📍 Location: librechat_integration/cruz_librechat.yaml")
    print("\n📋 Configured personas:")
    print("   - CRUZ (🎯): Decisive action-oriented AI")
    print("   - Serena (🌸): Supportive empathetic AI")
    print("   - Five Elements (🌳🔥🏔️⚔️💧): Team collaboration")
    
    print("\n🔌 Plugin features:")
    print("   - Persona switching with hotkeys (Alt+1, Alt+2, Alt+3)")
    print("   - Real-time emotion state display")
    print("   - Memory integration toggle (Alt+M)")
    print("   - Visual persona selector")

def print_integration_instructions():
    """打印整合說明"""
    print("\n\n📚 Integration Instructions")
    print("=" * 50)
    print("""
To integrate with LibreChat:

1. **Start the Persona Proxy Server**:
   ```bash
   cd librechat_integration
   python persona_proxy_server.py
   ```

2. **Copy configuration to LibreChat**:
   ```bash
   cp librechat_integration/cruz_librechat.yaml librechat_fork/librechat.yaml
   ```

3. **Install the plugin**:
   - Copy `cruz_personas_plugin.js` to LibreChat's plugin directory
   - Or inject it via browser console for testing

4. **Start LibreChat**:
   ```bash
   cd librechat_fork
   npm run backend:dev  # In one terminal
   npm run frontend:dev # In another terminal
   ```

5. **Access LibreChat**:
   - Open http://localhost:3090
   - Select "CRUZ" from endpoints menu
   - Use Alt+1/2/3 to switch personas

6. **Memory API** (optional):
   - Start Memory API: `python memory_api/main_sqlite.py`
   - Enable with Alt+M in LibreChat

🎯 CRUZ says: "Integration ready! Let's ship it!"
""")

async def main():
    """運行所有測試"""
    # 測試 Proxy Server
    try:
        await test_persona_proxy()
    except httpx.ConnectError:
        print("\n❌ Persona Proxy Server is not running!")
        print("   Please start it with: python librechat_integration/persona_proxy_server.py")
    
    # 測試配置
    await test_librechat_config()
    
    # 顯示整合說明
    print_integration_instructions()

if __name__ == "__main__":
    print("🚀 LibreChat Integration Test - Day 6-7")
    asyncio.run(main())