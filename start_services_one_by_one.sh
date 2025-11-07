#!/bin/bash

echo "🚀 Stopping existing services..."
pkill -f "uv run" 2>/dev/null
sleep 3

echo ""
echo "📌 Starting Reimbursement Agent (Port 10002)..."
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_expense_reimbursement
nohup uv run . > /tmp/reimbursement_agent.log 2>&1 &
REIMB_PID=$!
echo "   Started with PID: $REIMB_PID"
sleep 6

echo ""
echo "📌 Starting Facts Agent (Port 8001)..."
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_facts
GOOGLE_GENAI_USE_VERTEXAI=TRUE GOOGLE_CLOUD_PROJECT=sodium-atrium-331806 nohup uv run uvicorn agent:a2a_app --host localhost --port 8001 > /tmp/facts_agent.log 2>&1 &
FACTS_PID=$!
echo "   Started with PID: $FACTS_PID"
sleep 6

echo ""
echo "📌 Starting Analysis Bug Agent (Port 10003)..."
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/analysis_bug_agent
nohup uv run . > /tmp/analysis_bug_agent.log 2>&1 &
ANALYSIS_PID=$!
echo "   Started with PID: $ANALYSIS_PID"
sleep 6

# Host Agent is not needed - UI connects directly to agents

echo ""
echo "📌 Starting UI (Port 12000)..."
cd /Users/dirk/java/workspace/a2a-samples/demo/ui
nohup uv run main.py > /tmp/ui_server.log 2>&1 &
UI_PID=$!
echo "   Started with PID: $UI_PID"
sleep 8

echo ""
echo "✅ Checking service status..."
echo ""

if lsof -i :10002 > /dev/null 2>&1; then
    echo "✅ Reimbursement Agent - Running on port 10002"
else
    echo "❌ Reimbursement Agent - Failed to start"
    echo "   Log: tail -50 /tmp/reimbursement_agent.log"
fi

if lsof -i :8001 > /dev/null 2>&1; then
    echo "✅ Facts Agent - Running on port 8001"
else
    echo "❌ Facts Agent - Failed to start"
    echo "   Log: tail -50 /tmp/facts_agent.log"
fi

if lsof -i :10003 > /dev/null 2>&1; then
    echo "✅ Analysis Bug Agent - Running on port 10003"
else
    echo "❌ Analysis Bug Agent - Failed to start"
    echo "   Log: tail -50 /tmp/analysis_bug_agent.log"
fi

if lsof -i :12000 > /dev/null 2>&1; then
    echo "✅ UI - Running on port 12000"
else
    echo "❌ UI - Failed to start"
    echo "   Log: tail -50 /tmp/ui_server.log"
fi

echo ""
echo "🎉 Startup complete!"
echo ""
echo "📱 Access UI at: http://localhost:12000"
echo ""
echo "📋 Log files:"
echo "   - Reimbursement: /tmp/reimbursement_agent.log"
echo "   - Facts: /tmp/facts_agent.log"
echo "   - Analysis Bug: /tmp/analysis_bug_agent.log"
echo "   - UI: /tmp/ui_server.log"
echo ""
