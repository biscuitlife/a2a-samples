# 🔧 A2A Demo 常见问题排查指南

## 问题 1: Conversation 中显示 "working" 后无响应

### 症状
- 在 Conversation 页面输入消息后
- 界面显示 "working..." 或加载状态
- 长时间没有任何响应
- 后台日志没有错误信息

### 可能原因及解决方案

#### ✅ 原因 1: API Key 配置不正确

**检查方法：**
```bash
# 查看 .env 文件
cat demo/ui/.env
```

**正确配置应包含：**
```bash
GOOGLE_API_KEY=你的API密钥
GEMINI_API_KEY=你的API密钥  # LiteLLM 需要
```

**解决方案：**
```bash
cd demo/ui
echo "GOOGLE_API_KEY=你的密钥" > .env
echo "GEMINI_API_KEY=你的密钥" >> .env
```

---

#### ⚠️ 原因 2: Host Agent LLM 调用失败

**检查方法：**
在 Demo UI 终端中查找错误日志，关键字：
- `Error`
- `Failed`
- `API key`
- `Rate limit`

**解决方案 A - 切换到原生 Gemini（推荐）：**

编辑 `/samples/python/hosts/multiagent/host_agent.py`:

```python
# 原来（使用 LiteLLM）
from google.genai.types import LiteLlm
model=LiteLlm(model=LITELLM_MODEL)

# 改为（使用原生 Gemini）
from google.genai.types import Gemini
model=Gemini(model='gemini-2.0-flash-001')
```

**解决方案 B - 设置环境变量抑制警告：**
```bash
export ADK_SUPPRESS_GEMINI_LITELLM_WARNINGS=true
```

---

#### ⚠️ 原因 3: 没有正确添加 Remote Agent

**检查方法：**
1. 访问 "Remote Agents" 标签
2. 确认是否看到已添加的 Agent
3. 检查 Agent 状态是否正常

**解决方案：**
```bash
# 1. 确认 Remote Agent 正在运行
curl http://localhost:10002/.well-known/agent-card.json

# 2. 如果返回 JSON，说明 Agent 正常运行
# 3. 在 Web UI 中重新添加 Agent 地址: localhost:10002
```

---

#### ⚠️ 原因 4: Remote Agent 未启动或端口冲突

**检查方法：**
```bash
# 检查端口占用
lsof -i :10002
lsof -i :12000

# 检查进程
ps aux | grep "adk_expense"
```

**解决方案：**
```bash
# 重启 Remote Agent
cd samples/python/agents/adk_expense_reimbursement
uv run .
```

---

#### ⚠️ 原因 5: 网络连接问题（Host → Remote Agent）

**检查方法：**
```bash
# 测试 Host 能否访问 Remote Agent
curl -v http://localhost:10002/.well-known/agent-card.json
```

**解决方案：**
- 确认防火墙设置
- 检查 localhost 解析
- 尝试使用 `127.0.0.1` 替代 `localhost`

---

#### ⚠️ 原因 6: 浏览器缓存或会话问题

**解决方案：**
1. **清空浏览器缓存**
2. **刷新页面** (Cmd+Shift+R 或 Ctrl+Shift+R)
3. **创建新的 Conversation**
4. **尝试使用隐私模式/无痕模式**

---

## 问题 2: Agent 添加成功但不可用

### 症状
- Remote Agents 列表中显示 Agent
- 但对话时 Host 无法调用

### 解决方案

```bash
# 1. 检查 Host Agent 日志
# 在 demo/ui 终端中查看是否有连接错误

# 2. 重新添加 Agent
# 在 Web UI 的 Remote Agents 页面：
# - 删除现有 Agent
# - 重新添加: localhost:10002

# 3. 测试对话
# 发送: "What remote agents do you have?"
```

---

## 问题 3: API 配额或限流

### 症状
- 初次请求正常
- 后续请求失败或超时
- 日志显示 "Rate limit" 或 "Quota exceeded"

### 解决方案

```bash
# 检查 API 配额
# 访问: https://aistudio.google.com/app/apikey

# 临时解决：添加重试间隔
export LITELLM_REQUEST_TIMEOUT=120
export LITELLM_MAX_RETRIES=3
```

---

## 实用调试命令

### 查看所有运行的 A2A 服务
```bash
ps aux | grep -E "uv run|python.*agent"
```

### 查看端口占用情况
```bash
netstat -an | grep -E "10002|12000"
# 或
lsof -i -P | grep -E "10002|12000"
```

### 重启所有服务
```bash
# 停止所有服务
pkill -f "uv run"

# 启动 Demo UI
cd demo/ui && uv run main.py &

# 启动 Remote Agent
cd samples/python/agents/adk_expense_reimbursement
uv run . &
```

### 查看实时日志
```bash
# Demo UI 日志
tail -f demo/ui/logs/*.log  # 如果有日志文件

# 直接查看终端输出
# 在运行 uv run 的终端中查看
```

---

## 最佳实践

### ✅ 启动顺序
1. **先启动** Remote Agent(s)
2. **后启动** Demo UI / Host
3. **在 UI 中** 添加 Remote Agent
4. **测试** 基础对话

### ✅ 环境配置检查清单
- [ ] `GOOGLE_API_KEY` 已设置
- [ ] `GEMINI_API_KEY` 已设置（如使用 LiteLLM）
- [ ] Remote Agent 的 `.env` 配置正确
- [ ] 所有 Agent 使用不同端口

### ✅ 调试技巧
1. **使用 curl 测试 API**
   ```bash
   curl http://localhost:10002/.well-known/agent-card.json
   ```

2. **启用详细日志**
   ```bash
   export LOG_LEVEL=DEBUG
   ```

3. **检查 Events 和 Tasks 标签**
   - 查看消息流
   - 查看任务状态
   - 定位问题环节

---

## 联系与反馈

遇到无法解决的问题？

1. 检查 [GitHub Issues](https://github.com/a2aproject/a2a-samples/issues)
2. 查看 [A2A 文档](https://goo.gle/a2a)
3. 使用 [a2a-inspector](https://github.com/a2aproject/a2a-inspector) 调试工具
