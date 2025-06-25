#!/usr/bin/env python3
"""
簡單測試 Gemini API 連接
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 載入環境變數
load_dotenv()

# 配置 API
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

print(f"Testing with API Key: {api_key[:10]}...")

# 創建模型（不使用 Function Calling）
model = genai.GenerativeModel('gemini-1.5-flash')

# 簡單測試
try:
    response = model.generate_content("請記住這個量子座標：QM-2024-螢火蟲-42-薰衣草")
    print("✅ Success!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")