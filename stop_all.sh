#!/bin/bash

echo "🛑 停止 A2A 多 Agent 系统..."
echo ""

# 停止所有服务
pkill -f "uv run"

sleep 2

# 验证
echo "验证服务状态..."
echo ""

if lsof -i :12000 > /dev/null 2>&1; then
    echo "⚠️  UI 仍在运行 (端口 12000)"
    echo "   尝试强制停止: lsof -ti :12000 | xargs kill -9"
else
    echo "✅ UI 已停止"
fi

if lsof -i :10002 > /dev/null 2>&1; then
    echo "⚠️  Reimbursement Agent 仍在运行 (端口 10002)"
    echo "   尝试强制停止: lsof -ti :10002 | xargs kill -9"
else
    echo "✅ Reimbursement Agent 已停止"
fi

if lsof -i :8001 > /dev/null 2>&1; then
    echo "⚠️  Facts Agent 仍在运行 (端口 8001)"
    echo "   尝试强制停止: lsof -ti :8001 | xargs kill -9"
else
    echo "✅ Facts Agent 已停止"
fi

if lsof -i :10003 > /dev/null 2>&1; then
    echo "⚠️  Analysis Bug Agent 仍在运行 (端口 10003)"
    echo "   尝试强制停止: lsof -ti :10003 | xargs kill -9"
else
    echo "✅ Analysis Bug Agent 已停止"
fi

echo ""
echo "🎉 所有服务已停止"
echo ""
