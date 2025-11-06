#!/usr/bin/env python3
"""Test Gemini API directly"""
import os
import sys

# Set API key
API_KEY = "AIzaSyBaIE_tPdcT_j9CS-wAVe7sGBOoN018IgA"
os.environ['GOOGLE_API_KEY'] = API_KEY

print("=" * 60)
print("Testing Gemini API...")
print("=" * 60)

# Test 1: Using google-genai (ADK's client)
print("\n[Test 1] Testing with google.genai (ADK)")
try:
    from google import genai
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents='Say hello in one word'
    )
    print(f"✅ SUCCESS: {response.text}")
except Exception as e:
    print(f"❌ FAILED: {type(e).__name__}: {str(e)[:200]}")
    import traceback
    traceback.print_exc()

# Test 2: Check if API key is valid by listing models
print("\n[Test 2] Listing available models...")
try:
    from google import genai
    client = genai.Client(api_key=API_KEY)
    models = list(client.models.list(page_size=5))
    print(f"✅ Found {len(models)} models:")
    for m in models[:3]:
        print(f"   - {m.name}")
except Exception as e:
    print(f"❌ FAILED: {type(e).__name__}: {str(e)[:200]}")

# Test 3: Test with ADK Agent directly
print("\n[Test 3] Testing ADK Agent...")
try:
    from google.adk import Agent
    
    test_agent = Agent(
        name='test_agent',
        model='gemini-2.0-flash-001',
        description='Test agent',
        instruction='You are a test agent. Respond briefly.',
    )
    print("✅ Agent created successfully")
    print(f"   Model: {test_agent._model}")
except Exception as e:
    print(f"❌ FAILED: {type(e).__name__}: {str(e)[:200]}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test complete")
print("=" * 60)
