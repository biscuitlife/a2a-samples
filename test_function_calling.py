#!/usr/bin/env python3
"""测试 Ollama 通过 LiteLLM 的函数调用"""
import os
os.environ['OLLAMA_MODEL'] = 'ollama/qwen2.5:3b'

from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm

def list_agents():
    """列出可用的 Agent"""
    return [
        {"name": "Agent A", "description": "处理任务 A"},
        {"name": "Agent B", "description": "处理任务 B"}
    ]

# 创建测试 Agent
agent = Agent(
    model=LiteLlm(
        model='ollama/qwen2.5:3b',
        supports_function_calling=True,
    ),
    name='test_agent',
    description='测试 Agent',
    instruction='你是一个测试 Agent，当用户问你有什么 Agent 时，调用 list_agents 函数。',
    tools=[list_agents],
)

print("=" * 60)
print("测试 Ollama 函数调用")
print("=" * 60)

# 测试
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def test():
    runner = Runner(
        app_name='test',
        agent=agent,
        session_service=InMemorySessionService(),
    )
    
    session = await runner.session_service.create_session(
        app_name='test',
        user_id='test_user',
        state={},
        session_id='test_session',
    )
    
    content = types.Content(
        role='user',
        parts=[types.Part.from_text(text='你有哪些 Agent 可以使用？')]
    )
    
    print("\n发送消息: 你有哪些 Agent 可以使用？\n")
    
    async for event in runner.run_async(
        user_id='test_user',
        session_id=session.id,
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"响应: {part.text}")
                elif part.function_call:
                    print(f"函数调用: {part.function_call}")
                elif part.function_response:
                    print(f"函数响应: {part.function_response}")

asyncio.run(test())
