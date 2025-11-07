import os
import json
from pathlib import Path
from typing import Optional, Any
from collections.abc import AsyncIterable

from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


def read_file_content(file_path: str) -> str:
    """
    Read local file content with line numbers
    
    Args:
        file_path: Absolute or relative file path
        
    Returns:
        File content string with line numbers
    """
    try:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            return f"Error: File does not exist - {file_path}"
        if not path.is_file():
            return f"Error: Path is not a file - {file_path}"
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add line numbers
        lines = content.split('\n')
        numbered_content = '\n'.join([f"{i+1:4d} | {line}" for i, line in enumerate(lines)])
        
        return f"File Path: {path}\nFile Size: {len(content)} bytes\nTotal Lines: {len(lines)}\n\n{numbered_content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


class AnalysisBugAgent:
    """Code Bug Analysis Agent"""
    
    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']
    
    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = 'remote_agent'
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
    
    def get_processing_message(self) -> str:
        return 'Analyzing code errors...'
    
    def _build_agent(self) -> LlmAgent:
        """Build LLM Agent"""
        # Use Vertex AI
        model_name = os.getenv(
            'LITELLM_MODEL', 'vertex_ai/gemini-2.0-flash-exp'
        )
        return LlmAgent(
            model=LiteLlm(model=model_name),
            name='analysis_bug_agent',
            description='Analyze code errors and provide detailed error reports with fix suggestions',
            instruction="""
You are a professional code error analysis expert. Your responsibilities are:

1. **Read Code Carefully**: Understand the logic and context of the code
2. **Analyze Error Stack**: Locate the exact position where the error occurs
3. **Identify Root Cause**: Find not only surface issues but also underlying causes
4. **Provide Fix Suggestions**: Give specific, actionable modification plans
5. **Generate Detailed Report**: Include error line numbers, cause analysis, fix suggestions, etc.

## Analysis Process:
1. Use `read_file_content` to read code file (automatically adds line numbers)
2. Analyze error stack and locate the problem line
3. Understand code context and logic
4. Generate structured analysis report

## Report Requirements (strictly follow this format):

### 📋 Error Summary
- **Error Type**: <Error type, e.g., NameError, TypeError, etc.>
- **Error Line**: <Specific line number>
- **Error Message**: <Brief description>

### 🔍 Root Cause Analysis
<Detailed explanation of the root cause, at least 2-3 sentences>

### 📍 Affected Code Lines
```
<Line number> | <Original code>
Issue: <Specific problem with this line>
```

### 💡 Fix Suggestions
1. **Priority: High/Medium/Low**
   - Suggestion: <Specific modification suggestion>
   - Reason: <Why this modification is needed>

### ✅ Fixed Code Example
```python
<Modified code>
```

### 🛡️ Prevention Measures
- <Prevention suggestion 1>
- <Prevention suggestion 2>

Always maintain professionalism, accuracy, and helpfulness.
""",
            tools=[read_file_content],
        )
    
    async def stream(self, query: str, session_id: str) -> AsyncIterable[dict[str, Any]]:
        """Stream process analysis requests"""
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        
        content = types.Content(
            role='user', 
            parts=[types.Part.from_text(text=query)]
        )
        
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )
        
        async for event in self._runner.run_async(
            user_id=self._user_id,
            session_id=session.id,
            new_message=content
        ):
            if event.is_final_response():
                response = ''
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    response = '\n'.join(
                        [p.text for p in event.content.parts if p.text]
                    )
                
                yield {
                    'is_task_complete': True,
                    'content': response,
                }
            else:
                yield {
                    'is_task_complete': False,
                    'updates': self.get_processing_message(),
                }
