#!/usr/bin/env python3
"""
测试 Vertex AI 配置是否正确
"""
import os
import sys

# 设置环境变量
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/dirk/Downloads/sodium-atrium-331806-1a322b6cfcb1.json'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'sodium-atrium-331806'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'

print("=" * 60)
print("🔍 测试 Vertex AI 配置")
print("=" * 60)

print(f"\n✓ 项目 ID: {os.environ['GOOGLE_CLOUD_PROJECT']}")
print(f"✓ 区域: {os.environ['GOOGLE_CLOUD_LOCATION']}")
print(f"✓ 凭证文件: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")

# 测试 1: 检查凭证文件
print("\n📋 测试 1: 检查服务账号凭证文件...")
try:
    import json
    with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as f:
        creds = json.load(f)
    print(f"  ✅ 凭证文件存在")
    print(f"  ✅ 服务账号: {creds.get('client_email', 'N/A')}")
except Exception as e:
    print(f"  ❌ 错误: {e}")
    sys.exit(1)

# 测试 2: 测试 LiteLLM 调用 Vertex AI
print("\n📋 测试 2: 通过 LiteLLM 调用 Vertex AI...")
try:
    from litellm import completion
    
    print("  🔄 发送测试请求...")
    response = completion(
        model="vertex_ai/gemini-2.0-flash-exp",
        messages=[{"role": "user", "content": "Say 'Hello' in one word"}],
        vertex_project=os.environ['GOOGLE_CLOUD_PROJECT'],
        vertex_location=os.environ['GOOGLE_CLOUD_LOCATION'],
    )
    
    result = response.choices[0].message.content
    print(f"  ✅ 成功! 响应: {result}")
    
except Exception as e:
    print(f"  ❌ 错误: {type(e).__name__}: {e}")
    print("\n可能的原因:")
    print("  1. Vertex AI API 未启用")
    print("  2. 服务账号权限不足")
    print("  3. 网络连接问题")
    print("  4. 模型名称不正确")
    print("\n请访问以下链接启用 Vertex AI API:")
    print(f"  https://console.cloud.google.com/apis/library/aiplatform.googleapis.com?project={os.environ['GOOGLE_CLOUD_PROJECT']}")
    sys.exit(1)

# 测试 3: 测试 ADK 的 LiteLlm 模型
print("\n📋 测试 3: 通过 ADK 的 LiteLlm 调用 Vertex AI...")
try:
    from google.adk.models.lite_llm import LiteLlm
    
    model = LiteLlm(model="vertex_ai/gemini-2.0-flash-exp")
    print(f"  ✅ LiteLlm 模型创建成功")
    print(f"  ✅ 模型: {model.model}")
    
except Exception as e:
    print(f"  ❌ 错误: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 所有测试通过! Vertex AI 配置正确!")
print("=" * 60)
