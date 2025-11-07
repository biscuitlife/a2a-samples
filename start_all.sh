#!/bin/bash

echo "🚀 启动 A2A 多 Agent 系统..."

# 停止已有服务
echo "📌 停止旧服务..."
pkill -f "uv run" 2>/dev/null

sleep 2

# 启动 Reimbursement Agent
echo "📌 启动 Reimbursement Agent (端口 10002)..."
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_expense_reimbursement
nohup uv run . > /tmp/reimbursement_agent.log 2>&1 &
REIMB_PID=$!

sleep 5

# 启动 Facts Agent
echo "📌 启动 Facts Agent (端口 8001)..."
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_facts
nohup uv run uvicorn agent:a2a_app --host localhost --port 8001 > /tmp/facts_agent.log 2>&1 &
FACTS_PID=$!

sleep 5

# 启动 Analysis Bug Agent
echo "📌 启动 Analysis Bug Agent (端口 10003)..."
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/analysis_bug_agent
nohup uv run . > /tmp/analysis_bug_agent.log 2>&1 &
ANALYSIS_PID=$!

sleep 5

# 启动 UI
echo "📌 启动 Demo UI (端口 12000)..."
cd /Users/dirk/java/workspace/a2a-samples/demo/ui
# 直接使用 uv run 并依赖 main.py 中的 load_dotenv()
nohup uv run main.py > /tmp/ui_server.log 2>&1 &
UI_PID=$!

sleep 8

# 验证服务
echo ""
echo "✅ 验证服务状态..."
echo ""

if lsof -i :10002 > /dev/null 2>&1; then
    echo "✅ Reimbursement Agent 运行中 (PID: $REIMB_PID, 端口: 10002)"
else
    echo "❌ Reimbursement Agent 启动失败"
    echo "   查看日志: tail -50 /tmp/reimbursement_agent.log"
fi

if lsof -i :8001 > /dev/null 2>&1; then
    echo "✅ Facts Agent 运行中 (PID: $FACTS_PID, 端口: 8001)"
else
    echo "❌ Facts Agent 启动失败"
    echo "   查看日志: tail -50 /tmp/facts_agent.log"
fi

if lsof -i :10003 > /dev/null 2>&1; then
    echo "✅ Analysis Bug Agent 运行中 (PID: $ANALYSIS_PID, 端口: 10003)"
else
    echo "❌ Analysis Bug Agent 启动失败"
    echo "   查看日志: tail -50 /tmp/analysis_bug_agent.log"
fi

if lsof -i :12000 > /dev/null 2>&1; then
    echo "✅ Demo UI 运行中 (PID: $UI_PID, 端口: 12000)"
else
    echo "❌ Demo UI 启动失败"
    echo "   查看日志: tail -50 /tmp/ui_server.log"
fi

echo ""
echo "🎉 启动完成！"
echo ""
echo "📱 访问 UI: http://localhost:12000"
echo ""
echo "📋 日志文件："
echo "   - UI: /tmp/ui_server.log"
echo "   - Reimbursement Agent: /tmp/reimbursement_agent.log"
echo "   - Facts Agent: /tmp/facts_agent.log"
echo "   - Analysis Bug Agent: /tmp/analysis_bug_agent.log"
echo ""
echo "💡 使用 './stop_all.sh' 停止所有服务"
echo ""
