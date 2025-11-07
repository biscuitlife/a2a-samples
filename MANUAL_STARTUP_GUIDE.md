# 📚 A2A 多 Agent 系统手动启动指南

本指南详细说明如何手动启动 A2A 示例项目的各个组件。

---

## 📋 前置条件

### 1. 环境要求

- **Python**: 3.10 或更高版本
- **uv**: Python 包管理工具
- **Google Cloud**: 已启用计费的项目

### 2. 必需文件

确保以下配置文件存在：

```bash
# 检查配置文件
ls -l demo/ui/.env
ls -l samples/python/agents/adk_expense_reimbursement/.env
ls -l samples/python/agents/adk_facts/.env
ls -l /Users/dirk/Downloads/sodium-atrium-331806-1a322b6cfcb1.json
```

---

## 🚀 启动步骤

### 方法 1：使用后台启动（推荐）

#### 步骤 1：启动 Reimbursement Agent（费用报销）

```bash
# 进入 Agent 目录
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_expense_reimbursement

# 后台启动，日志输出到文件
nohup uv run . > /tmp/reimbursement_agent.log 2>&1 &

# 验证启动成功
sleep 5
lsof -i :10002
curl http://localhost:10002/.well-known/agent-card.json
```

**预期输出**：
```
COMMAND     PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python    xxxxx dirk    9u  IPv4 ...      TCP localhost:10002 (LISTEN)
```

---

#### 步骤 2：启动 Facts Agent（趣味事实）

```bash
# 进入 Agent 目录
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_facts

# 后台启动，日志输出到文件
nohup uv run uvicorn agent:a2a_app --host localhost --port 8001 > /tmp/facts_agent.log 2>&1 &

# 验证启动成功
sleep 5
lsof -i :8001
curl http://localhost:8001/.well-known/agent-card.json
```

**预期输出**：
```json
{
  "name": "facts_agent",
  "description": "Agent to give interesting facts about various topics.",
  ...
}
```

---

#### 步骤 3：启动 Demo UI（用户界面）

```bash
# 进入 UI 目录
cd /Users/dirk/java/workspace/a2a-samples/demo/ui

# 后台启动，日志输出到文件
nohup uv run main.py > /tmp/ui_server.log 2>&1 &

# 验证启动成功
sleep 8
lsof -i :12000
```

**预期输出**：
```
COMMAND     PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python    xxxxx dirk    7u  IPv4 ...      TCP *:12000 (LISTEN)
```

---

### 方法 2：使用前台启动（用于调试）

在 **3 个不同的终端窗口** 中分别执行：

#### 终端 1：Reimbursement Agent

```bash
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_expense_reimbursement
uv run .
```

#### 终端 2：Facts Agent

```bash
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_facts
uv run uvicorn agent:a2a_app --host localhost --port 8001
```

#### 终端 3：Demo UI

```bash
cd /Users/dirk/java/workspace/a2a-samples/demo/ui
uv run main.py
```

---

## ✅ 验证服务状态

### 1. 检查所有服务端口

```bash
# 检查所有服务是否监听
lsof -i :12000 -i :10002 -i :8001 | grep LISTEN
```

**预期输出**：
```
Python  xxxxx dirk  ... TCP localhost:10002 (LISTEN)
Python  xxxxx dirk  ... TCP localhost:8001 (LISTEN)
Python  xxxxx dirk  ... TCP *:12000 (LISTEN)
```

### 2. 检查进程状态

```bash
# 查看所有相关进程
ps aux | grep -E "main.py|uvicorn|adk_expense" | grep -v grep
```

### 3. 测试 Agent Card

```bash
# 测试 Reimbursement Agent
curl -s http://localhost:10002/.well-known/agent-card.json | python3 -m json.tool | head -20

# 测试 Facts Agent
curl -s http://localhost:8001/.well-known/agent-card.json | python3 -m json.tool | head -20
```

### 4. 访问 Web UI

打开浏览器访问：**http://localhost:12000**

---

## 📊 服务信息汇总

| 服务名称 | 端口 | 启动命令 | 日志文件 | Agent Card |
|---------|------|---------|---------|-----------|
| **Demo UI** | 12000 | `uv run main.py` | `/tmp/ui_server.log` | - |
| **Reimbursement Agent** | 10002 | `uv run .` | `/tmp/reimbursement_agent.log` | http://localhost:10002/.well-known/agent-card.json |
| **Facts Agent** | 8001 | `uv run uvicorn agent:a2a_app --host localhost --port 8001` | `/tmp/facts_agent.log` | http://localhost:8001/.well-known/agent-card.json |

---

## 🛑 停止服务

### 停止所有服务

```bash
# 方法 1：通过进程名停止
pkill -f "uv run"

# 方法 2：通过端口停止
lsof -ti :12000 | xargs kill
lsof -ti :10002 | xargs kill
lsof -ti :8001 | xargs kill
```

### 停止单个服务

```bash
# 查找进程 ID
ps aux | grep -E "main.py|uvicorn" | grep -v grep

# 停止特定进程
kill <PID>

# 强制停止
kill -9 <PID>
```

---

## 📝 查看日志

### 实时查看日志

```bash
# UI 服务日志
tail -f /tmp/ui_server.log

# Reimbursement Agent 日志
tail -f /tmp/reimbursement_agent.log

# Facts Agent 日志
tail -f /tmp/facts_agent.log
```

### 查看最近的日志

```bash
# 查看最后 50 行
tail -50 /tmp/ui_server.log

# 查看最后 100 行
tail -100 /tmp/reimbursement_agent.log

# 搜索错误
grep -i error /tmp/facts_agent.log
grep -i exception /tmp/ui_server.log
```

---

## 🔧 常见问题排查

### 问题 1：端口已被占用

**错误信息**：
```
Address already in use
```

**解决方案**：
```bash
# 查找占用端口的进程
lsof -i :12000
lsof -i :10002
lsof -i :8001

# 停止占用的进程
kill <PID>
```

---

### 问题 2：服务启动后立即退出

**检查方法**：
```bash
# 查看日志
tail -50 /tmp/ui_server.log
tail -50 /tmp/reimbursement_agent.log
tail -50 /tmp/facts_agent.log
```

**常见原因**：
1. 配置文件缺失或错误
2. Vertex AI 认证失败
3. 依赖包未安装

**解决方案**：
```bash
# 检查配置文件
cat demo/ui/.env

# 测试 Vertex AI 连接
cd /Users/dirk/java/workspace/a2a-samples
uv run python test_vertex_ai.py

# 重新安装依赖
cd samples/python/agents/adk_expense_reimbursement
uv sync
```

---

### 问题 3：UI 无法连接到 Agent

**检查步骤**：

1. **确认 Agent 已启动**：
   ```bash
   lsof -i :10002
   lsof -i :8001
   ```

2. **测试 Agent 可访问性**：
   ```bash
   curl http://localhost:10002/.well-known/agent-card.json
   curl http://localhost:8001/.well-known/agent-card.json
   ```

3. **在 UI 中注册 Agent**：
   - 访问 http://localhost:12000
   - 点击 "Agents" 菜单
   - 点击 "Add Agent"
   - 输入 `http://localhost:10002` 和 `http://localhost:8001`

---

### 问题 4：Vertex AI 认证失败

**错误信息**：
```
PERMISSION_DENIED
或
BILLING_DISABLED
```

**解决方案**：

1. **检查环境变量**：
   ```bash
   echo $GOOGLE_APPLICATION_CREDENTIALS
   echo $GOOGLE_CLOUD_PROJECT
   ```

2. **验证服务账号密钥**：
   ```bash
   cat /Users/dirk/Downloads/sodium-atrium-331806-1a322b6cfcb1.json | python3 -m json.tool
   ```

3. **测试 Vertex AI**：
   ```bash
   cd /Users/dirk/java/workspace/a2a-samples
   uv run python test_vertex_ai.py
   ```

4. **确认计费已启用**：
   访问：https://console.cloud.google.com/billing?project=sodium-atrium-331806

---

## 🎯 快速启动脚本（一键启动）

创建启动脚本 `start_all.sh`：

```bash
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

# 启动 UI
echo "📌 启动 Demo UI (端口 12000)..."
cd /Users/dirk/java/workspace/a2a-samples/demo/ui
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
fi

if lsof -i :8001 > /dev/null 2>&1; then
    echo "✅ Facts Agent 运行中 (PID: $FACTS_PID, 端口: 8001)"
else
    echo "❌ Facts Agent 启动失败"
fi

if lsof -i :12000 > /dev/null 2>&1; then
    echo "✅ Demo UI 运行中 (PID: $UI_PID, 端口: 12000)"
else
    echo "❌ Demo UI 启动失败"
fi

echo ""
echo "🎉 启动完成！"
echo ""
echo "访问 UI: http://localhost:12000"
echo ""
echo "日志文件："
echo "  - UI: /tmp/ui_server.log"
echo "  - Reimbursement Agent: /tmp/reimbursement_agent.log"
echo "  - Facts Agent: /tmp/facts_agent.log"
echo ""
```

**使用方法**：

```bash
# 赋予执行权限
chmod +x start_all.sh

# 运行脚本
./start_all.sh
```

---

## 🛑 快速停止脚本

创建停止脚本 `stop_all.sh`：

```bash
#!/bin/bash

echo "🛑 停止 A2A 多 Agent 系统..."

# 停止所有服务
pkill -f "uv run"

sleep 2

# 验证
if lsof -i :12000 > /dev/null 2>&1; then
    echo "⚠️  UI 仍在运行"
else
    echo "✅ UI 已停止"
fi

if lsof -i :10002 > /dev/null 2>&1; then
    echo "⚠️  Reimbursement Agent 仍在运行"
else
    echo "✅ Reimbursement Agent 已停止"
fi

if lsof -i :8001 > /dev/null 2>&1; then
    echo "⚠️  Facts Agent 仍在运行"
else
    echo "✅ Facts Agent 已停止"
fi

echo ""
echo "🎉 所有服务已停止"
```

**使用方法**：

```bash
chmod +x stop_all.sh
./stop_all.sh
```

---

## 📚 相关文档

- [Vertex AI 配置指南](VERTEX_AI_SETUP.md)
- [多 Agent 运行状态](RUNNING_AGENTS.md)
- [多 Agent 任务状态管理修复](MULTI_AGENT_FIX.md)
- [快速启动指南](快速启动指南.md)

---

**最后更新**: 2025-11-06  
**维护者**: A2A 示例项目团队
