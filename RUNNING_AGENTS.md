# 🎉 A2A 多 Agent 系统运行状态

## ✅ 当前运行的服务

| 服务名称 | 端口 | 地址 | 状态 | 功能描述 |
|---------|------|------|------|----------|
| **Demo UI** | 12000 | http://localhost:12000 | ✅ 运行中 | Web 界面，用于与多个 Agent 交互 |
| **Reimbursement Agent** | 10002 | http://localhost:10002 | ✅ 运行中 | 费用报销处理 Agent |
| **Facts Agent** | 8001 | http://localhost:8001 | ✅ 运行中 | 趣味事实生成 Agent（支持网络搜索） |

---

## 🔧 配置信息

### 通用配置
- **LLM 服务**: Google Vertex AI
- **项目 ID**: `sodium-atrium-331806`
- **区域**: `us-central1`
- **模型**: `gemini-2.0-flash-exp`

### 日志文件
- UI 服务: `/tmp/ui_server.log`
- Reimbursement Agent: `/tmp/reimbursement_agent.log`
- Facts Agent: `/tmp/facts_agent.log`

---

## 📝 如何添加 Agent 到 UI

### 方法 1: 通过 Web UI 添加

1. 打开浏览器访问: http://localhost:12000
2. 点击左侧菜单的 **"Agents"**
3. 点击 **"Add Agent"** 按钮
4. 输入 Agent 地址并添加：

   **Reimbursement Agent (已添加)**
   ```
   http://localhost:10002
   ```

   **Facts Agent (新)**
   ```
   http://localhost:8001
   ```

5. 点击 **"Add"**

### 方法 2: 验证 Agent 是否可访问

测试 Agent Card:
```bash
# Reimbursement Agent
curl http://localhost:10002/.well-known/agent-card.json

# Facts Agent
curl http://localhost:8001/.well-known/agent-card.json
```

---

## 💬 测试对话示例

添加 Agent 后，在对话界面尝试以下问题：

### 测试列出所有 Agent
```
你有哪些远程 Agent 可以使用？
```

**预期回复**:
```
我可以使用以下远程 Agent：
1. Reimbursement Agent - 处理员工的费用报销请求
2. facts_agent - 提供关于各种主题的有趣事实
```

### 测试 Reimbursement Agent
```
帮我报销昨天的午餐费用 150 元
```

### 测试 Facts Agent
```
告诉我一些关于人工智能的有趣事实
```

或者：
```
给我介绍一下量子计算的有趣知识
```

---

## 🚀 启动更多 Agent

项目中还有许多其他有趣的 Agent 可以启动：

### 可用的 Agent 列表

1. **dice_agent_rest** - 骰子游戏 Agent
2. **helloworld** - 简单的 Hello World Agent
3. **travel_planner_agent** - 旅行规划 Agent
4. **content_planner** - 内容规划 Agent
5. **analytics** - 数据分析 Agent
6. **github-agent** - GitHub 集成 Agent

### 启动新 Agent 的步骤

1. **选择 Agent 目录**
   ```bash
   cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/<agent_name>
   ```

2. **创建 .env 配置文件**
   ```bash
   cat > .env << EOF
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=sodium-atrium-331806
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_APPLICATION_CREDENTIALS=/Users/dirk/Downloads/sodium-atrium-331806-1a322b6cfcb1.json
   PORT=<选择一个未使用的端口>
   EOF
   ```

3. **启动 Agent**
   ```bash
   # 根据 Agent 类型选择启动方式
   
   # 方式 1: 使用 uv run .
   nohup uv run . > /tmp/<agent_name>.log 2>&1 &
   
   # 方式 2: 使用 uvicorn
   nohup uv run uvicorn agent:a2a_app --host localhost --port <PORT> > /tmp/<agent_name>.log 2>&1 &
   ```

4. **验证启动**
   ```bash
   lsof -i :<PORT>
   curl http://localhost:<PORT>/.well-known/agent-card.json
   ```

---

## 🛑 停止所有服务

```bash
# 停止所有 uv run 进程
pkill -f "uv run"

# 或者停止特定服务
kill <PID>
```

---

## 📊 查看实时日志

```bash
# UI 服务
tail -f /tmp/ui_server.log

# Reimbursement Agent
tail -f /tmp/reimbursement_agent.log

# Facts Agent
tail -f /tmp/facts_agent.log
```

---

## 🎯 当前系统架构

```
┌─────────────────────────────────────────┐
│         Demo UI (Port 12000)            │
│      http://localhost:12000             │
└──────────────┬──────────────────────────┘
               │
               │ A2A Protocol
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│Reimbursement│  │   Facts     │
│   Agent     │  │   Agent     │
│ Port 10002  │  │  Port 8001  │
└─────────────┘  └─────────────┘
       │                │
       └────────┬───────┘
                │
                ▼
      ┌──────────────────┐
      │   Vertex AI      │
      │  Gemini 2.0 Flash│
      └──────────────────┘
```

---

**更新时间**: 2025-11-06
**状态**: ✅ 所有服务正常运行
