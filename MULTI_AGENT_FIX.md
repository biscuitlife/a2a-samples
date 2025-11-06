# 🐛 多 Agent 调用问题修复

## 问题描述

用户输入："帮我报销昨天和客户吃午饭的费用，花了 120 美元。另外再给我讲个趣事。"

**预期行为**：
1. 调用 Reimbursement Agent 处理报销 ✅
2. 调用 Facts Agent 讲趣事 ❌ (卡住)

**实际行为**：
- 第一步（报销）完成
- 第二步（讲趣事）卡在 "Working..." 状态

## 错误日志

```
Traceback (most recent call last):
  File ".../remote_agent_connection.py", line 37, in send_message
    async for event in self.agent_client.send_message(message):
  ...
a2a.client.errors.A2AClientJSONRPCError: JSON-RPC Error code=-32001 
message='Task 28f275ed-3b54-498f-9d75-eb8447084bc0 was specified but does not exist'
```

## 根本原因

### 问题分析

在 [`host_agent.py`](file:///Users/dirk/java/workspace/a2a-samples/samples/python/hosts/multiagent/host_agent.py) 的 `send_message` 方法中：

```python
# 从状态中获取 task_id（可能是上一个 Agent 的 task_id）
task_id = state.get('task_id', None)
context_id = state.get('context_id', None)

# 使用这个 task_id 发送消息
request_message = Message(
    role=Role.user,
    parts=[Part(root=TextPart(text=message))],
    message_id=message_id,
    context_id=context_id,
    task_id=task_id,  # ❌ 问题：使用了前一个 Agent 的 task_id
)
```

**执行流程**：

1. **第一步**：调用 Reimbursement Agent
   - 创建新 task：`task_id_1 = "request_id_9781363"`
   - 保存到状态：`state['task_id'] = task_id_1`
   - ✅ 处理成功

2. **第二步**：调用 Facts Agent
   - 从状态获取：`task_id = state.get('task_id')` → 获得 `task_id_1`
   - 发送消息给 Facts Agent，携带 `task_id_1`
   - ❌ Facts Agent 拒绝：不认识这个 task_id（这是 Reimbursement Agent 的 task）

### 核心问题

**会话状态管理错误**：不同的 Agent 之间共享了同一个 `task_id`，但每个 Agent 应该维护自己的 task 上下文。

## 解决方案

### 修复代码

在 [`host_agent.py`](file:///Users/dirk/java/workspace/a2a-samples/samples/python/hosts/multiagent/host_agent.py#L182-L198) 的 `send_message` 方法中添加逻辑：

```python
if agent_name not in self.remote_agent_connections:
    raise ValueError(f'Agent {agent_name} not found')
state = tool_context.state

# ✅ 新增：检测 Agent 切换
previous_agent = state.get('agent', None)
if previous_agent and previous_agent != agent_name:
    # 切换到不同的 Agent，清除前一个 Agent 的 task_id
    state['task_id'] = None

state['agent'] = agent_name
client = self.remote_agent_connections[agent_name]
if not client:
    raise ValueError(f'Client not available for {agent_name}')
task_id = state.get('task_id', None)  # ✅ 现在是 None，将创建新 task
context_id = state.get('context_id', None)
message_id = state.get('message_id', None)
```

### 修复逻辑

1. **检测 Agent 切换**：比较 `previous_agent` 和 `agent_name`
2. **清除旧状态**：如果切换到新 Agent，将 `task_id` 设为 `None`
3. **创建新 task**：新 Agent 收到 `task_id=None` 时会自动创建新 task

### 为什么保留 context_id？

`context_id` 是**整个对话会话的上下文**，应该在不同 Agent 之间保持一致，以维持对话连贯性。

`task_id` 是**特定 Agent 的任务标识**，每个 Agent 应该有独立的 task。

## 测试验证

### 测试步骤

1. 重启所有服务
2. 在 UI 中输入多步骤请求：
   ```
   帮我报销昨天和客户吃午饭的费用，花了 120 美元。另外再给我讲个趣事。
   ```

### 预期结果

1. ✅ Reimbursement Agent 返回报销表单
2. ✅ 填写并提交表单
3. ✅ Host Agent 自动调用 Facts Agent
4. ✅ Facts Agent 返回有趣的事实
5. ✅ 完整对话流程无阻塞

## 服务状态

### 当前运行的服务

| 服务 | 端口 | 状态 |
|------|------|------|
| Demo UI | 12000 | ✅ 运行中 |
| Reimbursement Agent | 10002 | ✅ 运行中 |
| Facts Agent | 8001 | ✅ 运行中 |

### 日志位置

- UI: `/tmp/ui_server.log`
- Reimbursement Agent: `/tmp/reimbursement_agent.log`
- Facts Agent: `/tmp/facts_agent.log`

## 后续改进建议

### 1. 每个 Agent 独立的状态管理

更好的方案是为每个 Agent 维护独立的状态字典：

```python
# 示例结构
state = {
    'agents': {
        'Reimbursement Agent': {
            'task_id': 'task_1',
            'context_id': 'ctx_1',
        },
        'facts_agent': {
            'task_id': 'task_2',
            'context_id': 'ctx_1',  # 共享对话上下文
        }
    }
}
```

### 2. 添加状态清理机制

在任务完成后清理状态，避免状态累积：

```python
if task.status.state in [TaskState.completed, TaskState.canceled, TaskState.failed]:
    # 清理该 Agent 的状态
    state['task_id'] = None
```

### 3. 增强日志

在切换 Agent 时记录日志：

```python
if previous_agent and previous_agent != agent_name:
    logger.info(f"Switching from {previous_agent} to {agent_name}, clearing task_id")
    state['task_id'] = None
```

## 相关文件

- [`host_agent.py`](file:///Users/dirk/java/workspace/a2a-samples/samples/python/hosts/multiagent/host_agent.py) - 修复的核心文件
- [`remote_agent_connection.py`](file:///Users/dirk/java/workspace/a2a-samples/samples/python/hosts/multiagent/remote_agent_connection.py) - Agent 连接管理
- [`state.py`](file:///Users/dirk/java/workspace/a2a-samples/demo/ui/state/state.py) - 状态管理

---

**修复时间**: 2025-11-06
**修复版本**: commit 后更新
**测试状态**: 待用户验证
