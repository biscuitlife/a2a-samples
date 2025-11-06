#!/bin/bash

# A2A 协议示例项目快速启动脚本
# 这个脚本会帮您启动一个完整的 A2A Demo 环境

echo "======================================"
echo "  A2A 协议示例项目快速启动"
echo "======================================"
echo ""

# 检查 uv 是否安装
if ! command -v uv &> /dev/null
then
    echo "❌ UV 未安装，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "✅ UV 安装完成"
else
    echo "✅ UV 已安装: $(uv --version)"
fi

echo ""
echo "请选择您想运行的示例："
echo "1) Demo Web 应用（推荐新手）- 可视化多 Agent 协作界面"
echo "2) Python CLI + LangGraph Agent（命令行）"
echo "3) Java Agent 示例（需要 Maven）"
echo ""
read -p "请输入选项 (1-3): " choice

case $choice in
  1)
    echo ""
    echo "======================================"
    echo "启动 Demo Web 应用"
    echo "======================================"
    echo ""
    echo "📝 步骤 1: 配置 API Key"
    echo "您需要 Google AI Studio API Key 或 Vertex AI 认证"
    echo ""
    
    cd demo/ui
    
    if [ ! -f .env ]; then
        echo "创建 .env 文件..."
        read -p "请输入您的 Google API Key（如果使用 Vertex AI 可以直接按回车跳过）: " api_key
        
        if [ -n "$api_key" ]; then
            echo "GOOGLE_API_KEY=$api_key" > .env
            echo "✅ API Key 已保存"
        else
            echo "⚠️  跳过 API Key 配置，您可以稍后在 UI 中输入"
        fi
    else
        echo "✅ .env 文件已存在"
    fi
    
    echo ""
    echo "📝 步骤 2: 启动 Demo 应用"
    echo "应用将在 http://localhost:12000 启动"
    echo ""
    
    uv run main.py
    ;;
    
  2)
    echo ""
    echo "======================================"
    echo "启动 Python CLI + LangGraph Agent"
    echo "======================================"
    echo ""
    
    # 先启动 Agent（后台）
    echo "📝 步骤 1: 启动 LangGraph Agent 服务器（端口 10001）"
    cd samples/python/agents/langgraph
    
    if [ ! -f .env ]; then
        read -p "请输入您的 Google API Key: " api_key
        echo "GOOGLE_API_KEY=$api_key" > .env
    fi
    
    uv run . &
    AGENT_PID=$!
    
    echo "✅ Agent 服务器已启动 (PID: $AGENT_PID)"
    echo "等待 5 秒让服务器完全启动..."
    sleep 5
    
    # 启动 CLI 客户端
    echo ""
    echo "📝 步骤 2: 启动 CLI 客户端"
    cd ../../hosts/cli
    
    echo "您现在可以通过命令行与 Agent 交互了！"
    echo "尝试问它：'Convert 100 USD to EUR'"
    echo ""
    
    uv run .
    
    # 清理
    echo ""
    echo "关闭 Agent 服务器..."
    kill $AGENT_PID
    ;;
    
  3)
    echo ""
    echo "======================================"
    echo "启动 Java Agent 示例"
    echo "======================================"
    echo ""
    
    cd samples/java/agents/weather_mcp
    
    if [ ! -f .env ]; then
        read -p "请输入您的 OpenWeatherMap API Key: " api_key
        echo "OPENWEATHER_API_KEY=$api_key" > .env
    fi
    
    echo "使用 Maven 构建并运行..."
    ./mvnw clean quarkus:dev
    ;;
    
  *)
    echo "❌ 无效的选项"
    exit 1
    ;;
esac
