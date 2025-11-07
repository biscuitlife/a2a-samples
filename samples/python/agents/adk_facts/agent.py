import os

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools import google_search

# Load environment variables
load_dotenv()

root_agent = Agent(
    name='facts_agent',
    model='gemini-2.0-flash-exp',  # 使用 Vertex AI 上的 Gemini 2.0
    description=('Agent to give interesting facts about various topics.'),
    instruction=('You are a helpful agent who can provide interesting and educational facts about any topic. Use web search when needed to find accurate information.'),
    tools=[google_search],
)

a2a_app = to_a2a(root_agent, port=int(os.getenv('PORT', '8001')))
