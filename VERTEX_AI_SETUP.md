# ✅ Vertex AI 配置完成

## 🎯 配置摘要

已成功将 A2A 示例项目从 Ollama 本地模型迁移到 **Google Vertex AI**，解决了之前函数调用不完整的问题。

---

## 📋 配置信息

- **项目 ID**: `sodium-atrium-331806`
- **服务账号**: `a2a-demo@sodium-atrium-331806.iam.gserviceaccount.com`
- **区域**: `us-central1`
- **模型**: `vertex_ai/gemini-2.0-flash-exp`
- **密钥文件**: `/Users/dirk/Downloads/sodium-atrium-331806-1a322b6cfcb1.json`

---

## 🚀 服务状态

### ✅ 正在运行的服务

1. **Demo UI**
   - 地址: http://localhost:12000
   - 进程: Python (PID 27688)
   - 状态: ✅ 运行中

2. **Reimbursement Agent**
   - 地址: http://localhost:10002
   - 进程: Python (PID 27330)
   - 状态: ✅ 运行中

---

## 🔧 配置文件更改

### 1. `/demo/ui/.env`
```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=sodium-atrium-331806
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/Users/dirk/Downloads/sodium-atrium-331806-1a322b6cfcb1.json
LITELLM_MODEL=vertex_ai/gemini-2.0-flash-exp
```

### 2. `/samples/python/agents/adk_expense_reimbursement/.env`
```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=sodium-atrium-331806
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/Users/dirk/Downloads/sodium-atrium-331806-1a322b6cfcb1.json
LITELLM_MODEL=vertex_ai/gemini-2.0-flash-exp
```

### 3. `/samples/python/hosts/multiagent/host_agent.py`
```python
def create_agent(self) -> Agent:
    model_name = os.getenv(
        'LITELLM_MODEL', 'vertex_ai/gemini-2.0-flash-exp'
    )
    return Agent(
        model=LiteLlm(
            model=model_name,
            supports_function_calling=True,
        ),
        # ...
    )
```

### 4. `/samples/python/agents/adk_expense_reimbursement/agent.py`
```python
def _build_agent(self) -> LlmAgent:
    model_name = os.getenv(
        'LITELLM_MODEL', 'vertex_ai/gemini-2.0-flash-exp'
    )
    return LlmAgent(
        model=LiteLlm(model=model_name),
        # ...
    )
```

---

## 🎯 使用方法

### 1. 访问 UI
打开浏览器访问: http://localhost:12000

### 2. 添加远程 Agent
1. 点击 "Agents" 选项卡
2. 点击 "Add Agent"
3. 输入地址: `http://localhost:10002`
4. 点击 "Add"

### 3. 测试对话
在对话框中输入:
```
你有哪些远程 Agent 可以使用？
```

应该会看到类似以下的回复:
```
我可以使用以下远程 Agent：
- Reimbursement Agent: 处理员工的费用报销请求
```

### 4. 测试费用报销功能
```
帮我报销昨天和客户吃午饭的费用，花了 120 美元
```

---

## ✨ Vertex AI 优势

相比之前的 Ollama 本地模型，Vertex AI 提供：

1. **✅ 无地理限制** - 全球可用，无需 VPN
2. **✅ 完整函数调用** - 原生支持工具调用，无需 workaround
3. **✅ 企业级稳定性** - Google Cloud 基础设施保障
4. **✅ 最新模型** - 可使用 Gemini 2.0 Flash 等最新模型
5. **✅ 高性能** - 云端推理速度更快

---

## 🛑 停止服务

如需停止所有服务:
```bash
pkill -f "uv run"
```

---

## 🔄 重启服务

使用快速启动脚本:
```bash
./demo/ui/start.sh
```

或手动启动:
```bash
# 启动 Reimbursement Agent
cd samples/python/agents/adk_expense_reimbursement
uv run . &

# 启动 UI
cd ../../demo/ui
uv run main.py &
```

---

## ⚠️ 注意事项

### 警告信息
启动时可能看到以下警告，这是正常的：
```
UserWarning: [GEMINI_VIA_LITELLM] vertex_ai/gemini-2.0-flash-exp: 
You are using Gemini via LiteLLM. For better performance, consider 
using Gemini directly through ADK's native Gemini integration.
```

**这不影响使用**，只是建议直接使用 ADK 的 Gemini 集成而非 LiteLLM 包装器。可以通过以下方式忽略:
```bash
export ADK_SUPPRESS_GEMINI_LITELLM_WARNINGS=true
```

### 成本考虑
- Vertex AI 按使用量计费
- Gemini 2.0 Flash 有免费额度
- 详见: https://cloud.google.com/vertex-ai/generative-ai/pricing

---

## 🎉 成功标志

配置成功的标志：
1. ✅ 服务启动无错误
2. ✅ UI 不再要求输入 API Key
3. ✅ 能够成功添加远程 Agent
4. ✅ 对话能正确调用函数并返回结果（不再只返回 JSON）
5. ✅ 费用报销功能完整可用

---

**配置完成时间**: 2025-11-06
**配置方式**: Vertex AI + Service Account
**状态**: ✅ 正常运行
