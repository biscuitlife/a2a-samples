# Analysis Bug Agent

专业的代码错误分析 Agent，能够读取本地代码文件、分析错误堆栈、定位错误行号，并提供详细的修复建议。

## 功能特性

- ✅ **读取本地文件**：支持读取任意本地代码文件
- ✅ **错误栈分析**：智能解析错误堆栈信息
- ✅ **精确定位**：准确标注错误发生的行号
- ✅ **根因分析**：深入分析错误的根本原因
- ✅ **修复建议**：提供具体可行的修改方案
- ✅ **代码示例**：给出修改后的代码示例
- ✅ **预防措施**：提供避免类似错误的建议

## 启动服务

### 方法 1：使用 uv（推荐）

```bash
cd samples/python/agents/analysis_bug_agent
uv run .
```

### 方法 2：后台启动

```bash
cd samples/python/agents/analysis_bug_agent
nohup uv run . > /tmp/analysis_bug_agent.log 2>&1 &
```

### 验证服务

```bash
# 检查端口
lsof -i :10003

# 获取 Agent Card
curl http://localhost:10003/.well-known/agent-card.json
```

## 使用示例

### 示例 1：分析 Python 错误

**输入**：
```
分析文件 /Users/dirk/code/test.py 的错误，错误信息是：
NameError: name 'calculate_sum' is not defined
```

**输出**：
```json
{
    "error_summary": {
        "error_type": "NameError",
        "error_line": "15",
        "error_message": "未定义的函数名 'calculate_sum'"
    },
    "root_cause": "在第15行调用了函数 'calculate_sum'，但该函数在代码中未定义",
    "affected_lines": [
        {
            "line_number": 15,
            "original_code": "result = calculate_sum(a, b)",
            "issue": "调用了未定义的函数"
        }
    ],
    "fix_suggestions": [
        {
            "priority": "high",
            "suggestion": "定义 calculate_sum 函数",
            "reason": "必须先定义函数才能调用"
        }
    ],
    "fixed_code_example": "def calculate_sum(a, b):\n    return a + b\n\nresult = calculate_sum(a, b)",
    "prevention_tips": [
        "使用 IDE 的代码检查功能",
        "运行代码前进行语法检查"
    ]
}
```

### 示例 2：分析索引错误

**输入**：
```
帮我看看这个文件：/path/to/main.py
错误：IndexError: list index out of range at line 42
```

## 工具函数

### 1. read_file_content(file_path: str)

读取本地文件内容，自动添加行号。

**参数**：
- `file_path`: 文件路径（支持绝对路径和相对路径）

**返回**：
- 带行号的文件内容

### 2. analyze_error_stack(file_path: str, error_stack: str)

分析代码错误，生成详细报告。

**参数**：
- `file_path`: 代码文件路径
- `error_stack`: 错误堆栈信息

**返回**：
- 结构化的错误分析报告

### 3. generate_bug_report(file_path: str, error_stack: str)

快速生成 Bug 分析报告。

**参数**：
- `file_path`: 代码文件路径
- `error_stack`: 错误堆栈信息

**返回**：
- 格式化的分析报告

## 添加到 UI

1. 启动 Analysis Bug Agent (端口 10003)
2. 访问 http://localhost:12000
3. 点击 "Agents" 菜单
4. 点击 "Add Agent"
5. 输入: `http://localhost:10003`
6. 点击 "Add"

## 测试对话

```
分析这个文件的错误：/Users/dirk/test.py
错误信息是：TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

## 配置

Agent 使用 Vertex AI 的 Gemini 2.0 Flash 模型，配置在 `.env` 文件中：

```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=sodium-atrium-331806
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
PORT=10003
```

## 技术栈

- **框架**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.0 Flash (via Vertex AI)
- **协议**: A2A (Agent-to-Agent)
- **语言**: Python 3.10+

## 注意事项

1. **文件权限**：确保 Agent 有权限读取指定的文件
2. **路径格式**：支持绝对路径和相对路径（相对于 Agent 运行目录）
3. **文件大小**：建议分析的文件不超过 1MB
4. **安全性**：不要分析包含敏感信息的文件

## 日志查看

```bash
# 实时查看日志
tail -f /tmp/analysis_bug_agent.log

# 查看最近 50 行
tail -50 /tmp/analysis_bug_agent.log
```

## 故障排查

### 问题 1：无法读取文件

**原因**：文件路径错误或权限不足

**解决**：
- 检查文件路径是否正确
- 确认文件存在且可读

### 问题 2：分析超时

**原因**：文件太大或网络问题

**解决**：
- 减小文件大小
- 检查 Vertex AI 连接

## 许可证

Apache License 2.0
