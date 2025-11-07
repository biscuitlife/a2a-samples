# 🚀 A2A 快速启动参考

## 一键启动/停止

```bash
# 启动所有服务
./start_all.sh

# 停止所有服务
./stop_all.sh
```

---

## 手动启动命令

### 1️⃣ Reimbursement Agent（费用报销）

```bash
cd samples/python/agents/adk_expense_reimbursement
nohup uv run . > /tmp/reimbursement_agent.log 2>&1 &
```
**端口**: 10002

---

### 2️⃣ Facts Agent（趣味事实）

```bash
cd samples/python/agents/adk_facts
nohup uv run uvicorn agent:a2a_app --host localhost --port 8001 > /tmp/facts_agent.log 2>&1 &
```
**端口**: 8001

---

### 3️⃣ Demo UI（Web 界面）

```bash
cd demo/ui
nohup uv run main.py > /tmp/ui_server.log 2>&1 &
```
**端口**: 12000  
**访问**: http://localhost:12000

---

### 4️⃣ Analysis Bug Agent（代码错误分析）

```bash
cd samples/python/agents/analysis_bug_agent
nohup uv run . > /tmp/analysis_bug_agent.log 2>&1 &
```
**端口**: 10003

---

## 快速检查

```bash
# 检查所有服务
lsof -i :12000 -i :10002 -i :8001 -i :10003 | grep LISTEN

# 查看日志
tail -f /tmp/ui_server.log
tail -f /tmp/reimbursement_agent.log
tail -f /tmp/facts_agent.log
tail -f /tmp/analysis_bug_agent.log
```

---

## 添加 Agent 到 UI

1. 访问 http://localhost:12000
2. 点击 **"Agents"** 菜单
3. 点击 **"Add Agent"**
4. 添加以下地址：
   - `http://localhost:10002` (Reimbursement Agent)
   - `http://localhost:8001` (Facts Agent)
   - `http://localhost:10003` (Analysis Bug Agent)

---

## 测试对话

```
你有哪些远程 Agent 可以使用？
```

```
帮我报销昨天的午餐费 120 美元
```

```
给我讲一个关于人工智能的趣事
```

```
分析这个文件的错误：/path/to/test.py
错误：NameError: name 'x' is not defined at line 15
```

---

📖 **完整文档**: [MANUAL_STARTUP_GUIDE.md](MANUAL_STARTUP_GUIDE.md)
