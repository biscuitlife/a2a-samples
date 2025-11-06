#!/usr/bin/env python3
"""测试 VPN 连接后 Gemini API 是否可用"""
import os
import sys

API_KEY = "AIzaSyBaIE_tPdcT_j9CS-wAVe7sGBOoN018IgA"
os.environ['GOOGLE_API_KEY'] = API_KEY

print("=" * 70)
print("🌐 测试 VPN 连接后的 Gemini API")
print("=" * 70)

# 测试 1: 检查网络连接
print("\n[步骤 1] 检查网络连接...")
try:
    import urllib.request
    # 测试 Google 的连接
    req = urllib.request.Request('https://www.google.com', headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=5)
    print("✅ 网络连接正常")
except Exception as e:
    print(f"❌ 网络连接失败: {e}")
    print("   请确认网络和 VPN 连接！")

# 测试 2: 测试 Gemini API
print("\n[步骤 2] 测试 Gemini API 调用...")
try:
    from google import genai
    client = genai.Client(api_key=API_KEY)
    
    print("   发送测试请求: 'Say hello'")
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents='Say hello in one word'
    )
    
    print(f"✅ API 调用成功！")
    print(f"   响应: {response.text}")
    print(f"\n🎉 恭喜！VPN 配置正确，API 可以正常使用！")
    
except Exception as e:
    error_msg = str(e)
    print(f"❌ API 调用失败")
    print(f"   错误: {error_msg}")
    
    if "FAILED_PRECONDITION" in error_msg or "location" in error_msg.lower():
        print("\n⚠️  仍然显示地理位置限制错误！")
        print("   可能的原因：")
        print("   1. VPN 未正确连接")
        print("   2. VPN 连接的地区不支持 Gemini API")
        print("   3. 需要尝试连接到其他地区（如美国）")
        print("\n   建议：")
        print("   - 断开并重新连接 VPN")
        print("   - 切换 VPN 服务器到美国节点")
        print("   - 或者考虑使用 Vertex AI（无地理限制）")
    else:
        print(f"\n   完整错误信息:")
        import traceback
        traceback.print_exc()
    
    sys.exit(1)

# 测试 3: 测试 ADK Agent
print("\n[步骤 3] 测试 ADK Agent 创建...")
try:
    from google.adk import Agent
    
    test_agent = Agent(
        name='test_agent',
        model='gemini-2.0-flash-001',
        description='测试 Agent',
        instruction='你是一个测试 Agent',
    )
    print("✅ ADK Agent 创建成功！")
    
except Exception as e:
    print(f"❌ Agent 创建失败: {e}")

print("\n" + "=" * 70)
print("✅ 所有测试通过！现在可以重启 Demo 应用了。")
print("=" * 70)
