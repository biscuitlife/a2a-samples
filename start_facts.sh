#!/bin/bash
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_facts
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=sodium-atrium-331806
uv run uvicorn agent:a2a_app --host localhost --port 8001
