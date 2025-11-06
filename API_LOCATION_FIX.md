# 🚨 API 地理位置限制问题 - 解决方案

## 问题诊断

您遇到的问题是：

```
400 FAILED_PRECONDITION
User location is not supported for the API use.
```

**这意味着 Google AI Studio API Key 在您的地理位置被限制使用。**

---

## 解决方案选择

### ✅ **方案 1：使用 Vertex AI（推荐，无地理限制）**

#### 步骤 1：设置 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 记下项目 ID（例如：`my-project-12345`）

#### 步骤 2：启用 Vertex AI API

```bash
# 安装 gcloud CLI（如果还没有）
# macOS:
brew install google-cloud-sdk

# 认证
gcloud auth login
gcloud auth application-default login

# 设置项目
gcloud config set project 你的项目ID

# 启用 Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

#### 步骤 3：配置 `.env` 文件

```bash
cd /Users/dirk/java/workspace/a2a-samples/demo/ui

cat > .env << 'EOF'
# 使用 Vertex AI（推荐）
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=你的项目ID
GOOGLE_CLOUD_LOCATION=us-central1

# 不使用 AI Studio API Key
# GOOGLE_API_KEY=...
EOF
```

#### 步骤 4：对 Remote Agent 做同样配置

```bash
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_expense_reimbursement

cat > .env << 'EOF'
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=你的项目ID
GOOGLE_CLOUD_LOCATION=us-central1
EOF
```

#### 步骤 5：重启服务

```bash
# 停止所有服务
pkill -f "uv run"

# 启动 Demo UI
cd /Users/dirk/java/workspace/a2a-samples/demo/ui
uv run main.py &

# 启动 Remote Agent
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/adk_expense_reimbursement
uv run . &
```

---

### 🌐 **方案 2：使用 VPN 或代理**

如果您有 VPN 可以连接到支持的地区（如美国）：

1. **连接 VPN** 到支持的地区
2. **保持原有 `.env` 配置**：
   ```bash
   GOOGLE_API_KEY=AIzaSyBaIE_tPdcT_j9CS-wAVe7sGBOoN018IgA
   GEMINI_API_KEY=AIzaSyBaIE_tPdcT_j9CS-wAVe7sGBOoN018IgA
   ```
3. **重启服务**

---

### 🔄 **方案 3：切换到其他 LLM 提供商**

使用支持您地区的其他 LLM：

#### 选项 A：OpenAI

```bash
# 在 .env 中
OPENAI_API_KEY=sk-your-openai-key

# 修改 host_agent.py 中的模型
model='gpt-4o-mini'  # 或 'gpt-4'
```

#### 选项 B：Anthropic Claude

```bash
# 在 .env 中
ANTHROPIC_API_KEY=sk-ant-your-key

# 使用 LiteLLM
from google.adk.models.lite_llm import LiteLlm
model=LiteLlm(model='claude-3-5-sonnet-20241022')
```

---

### 🧪 **方案 4：使用本地模型（Ollama）**

完全本地运行，无网络限制：

```bash
# 安装 Ollama
brew install ollama

# 启动 Ollama 服务
ollama serve &

# 下载模型
ollama pull gemma2

# 在 host_agent.py 中使用
from google.adk.models.lite_llm import LiteLlm
model=LiteLlm(model='ollama/gemma2')
```

---

## 快速测试方案 1（Vertex AI）

运行以下命令测试 Vertex AI 是否配置正确：

```bash
cd /Users/dirk/java/workspace/a2a-samples

cat > test_vertex_ai.py << 'PYTHONEOF'
import os
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'TRUE'
os.environ['GOOGLE_CLOUD_PROJECT'] = '你的项目ID'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'

from google.adk import Agent

agent = Agent(
    name='test',
    model='gemini-2.0-flash-001',
    description='Test',
    instruction='Say hello',
)

print("✅ Vertex AI configuration successful!")
PYTHONEOF

/Users/dirk/java/workspace/a2a-samples/.venv/bin/python test_vertex_ai.py
```

---

## 推荐路径

根据您的情况，我建议：

1. **如果有 GCP 项目** → 使用方案 1（Vertex AI）
2. **如果有 VPN** → 使用方案 2（VPN）
3. **如果都没有** → 使用方案 4（Ollama 本地模型）

---

## 需要帮助？

告诉我您想使用哪个方案，我会帮您完成配置！

- **方案 1**：我需要您的 GCP 项目 ID
- **方案 2**：您连接 VPN 后告诉我
- **方案 4**：我帮您配置 Ollama

现在请选择一个方案，我们立即解决！🚀
