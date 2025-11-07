# Analysis Bug Agent 使用示例

## 📖 功能说明

Analysis Bug Agent 是一个专业的代码错误分析工具，能够：
- 读取本地代码文件
- 分析错误堆栈信息
- 精确定位错误行号
- 提供详细的修复建议
- 生成完整的错误报告

---

## 🚀 快速开始

### 1. 启动 Agent

```bash
cd /Users/dirk/java/workspace/a2a-samples/samples/python/agents/analysis_bug_agent
uv run .
```

### 2. 添加到 UI

1. 打开 http://localhost:12000
2. 点击 "Agents" → "Add Agent"
3. 输入：`http://localhost:10003`
4. 点击 "Add"

---

## 💡 使用示例

### 示例 1：分析 Python NameError

**问题代码** (`/tmp/test.py`):
```python
def main():
    print("Starting calculation...")
    result = calculate_sum(10, 20)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

**错误信息**:
```
Traceback (most recent call last):
  File "/tmp/test.py", line 7, in <module>
    main()
  File "/tmp/test.py", line 3, in main
    result = calculate_sum(10, 20)
NameError: name 'calculate_sum' is not defined
```

**输入到 UI**:
```
分析文件 /tmp/test.py 的错误
错误信息：NameError: name 'calculate_sum' is not defined at line 3
```

**Agent 输出** (示例):
```markdown
📋 错误摘要
- 错误类型: NameError
- 错误行号: 3
- 错误信息: 未定义的函数 'calculate_sum'

🔍 根本原因分析
在第3行调用了函数 `calculate_sum(10, 20)`，但该函数在整个代码文件中都未定义。
Python 无法找到该函数的定义，因此抛出 NameError 异常。

📍 受影响的代码行
   3 |     result = calculate_sum(10, 20)
问题：调用了未定义的函数

💡 修复建议
1. 优先级：高
   - 建议：定义 calculate_sum 函数
   - 原因：必须先定义函数才能调用

✅ 修改后的代码示例
```python
def calculate_sum(a, b):
    """计算两个数的和"""
    return a + b

def main():
    print("Starting calculation...")
    result = calculate_sum(10, 20)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

🛡️ 预防措施
- 使用 IDE 的代码检查功能（如 PyCharm, VSCode）
- 运行代码前使用 pylint 或 flake8 进行语法检查
- 确保所有调用的函数都已定义
```

---

### 示例 2：分析 IndexError

**问题代码** (`/tmp/list_error.py`):
```python
numbers = [1, 2, 3, 4, 5]
print(numbers[10])
```

**输入到 UI**:
```
帮我分析这个错误：
文件路径：/tmp/list_error.py
错误：IndexError: list index out of range at line 2
```

**Agent 输出** (示例):
```markdown
📋 错误摘要
- 错误类型: IndexError
- 错误行号: 2
- 错误信息: 列表索引超出范围

🔍 根本原因分析
列表 `numbers` 只有 5 个元素（索引 0-4），但代码尝试访问索引 10，
超出了列表的有效索引范围，导致 IndexError。

📍 受影响的代码行
   2 | print(numbers[10])
问题：索引值 10 超出列表范围（有效范围：0-4）

💡 修复建议
1. 优先级：高
   - 建议：检查索引是否在有效范围内
   - 原因：防止运行时错误

2. 优先级：中
   - 建议：使用 try-except 捕获异常
   - 原因：提高代码健壮性

✅ 修改后的代码示例
```python
numbers = [1, 2, 3, 4, 5]

# 方法 1：检查索引范围
index = 10
if index < len(numbers):
    print(numbers[index])
else:
    print(f"索引 {index} 超出范围（列表长度：{len(numbers)}）")

# 方法 2：使用 try-except
try:
    print(numbers[10])
except IndexError:
    print("索引超出范围")
```

🛡️ 预防措施
- 访问列表元素前检查索引是否有效
- 使用 `len(list)` 获取列表长度
- 考虑使用 `list.get()` 方法（对于字典）
- 添加边界检查逻辑
```

---

### 示例 3：分析 TypeError

**问题代码** (`/tmp/type_error.py`):
```python
age = "25"
next_year_age = age + 1
print(next_year_age)
```

**输入到 UI**:
```
分析代码错误：
文件：/tmp/type_error.py
错误栈：TypeError: can only concatenate str (not "int") to str at line 2
```

**Agent 输出** (示例):
```markdown
📋 错误摘要
- 错误类型: TypeError
- 错误行号: 2
- 错误信息: 字符串与整数无法直接相加

🔍 根本原因分析
变量 `age` 是字符串类型 "25"，而 `1` 是整数类型。
Python 不支持字符串和整数直接使用 + 运算符，
因为 + 对字符串是拼接操作，对数字是加法操作，两者语义不同。

📍 受影响的代码行
   2 | next_year_age = age + 1
问题：尝试将字符串 "25" 与整数 1 相加

💡 修复建议
1. 优先级：高
   - 建议：将字符串转换为整数后再相加
   - 原因：确保数据类型一致

✅ 修改后的代码示例
```python
age = "25"
next_year_age = int(age) + 1  # 先转换为整数
print(next_year_age)  # 输出: 26

# 或者直接使用整数
age = 25
next_year_age = age + 1
print(next_year_age)
```

🛡️ 预防措施
- 使用类型注解明确变量类型
- 在函数输入处进行类型检查和转换
- 使用 mypy 等工具进行静态类型检查
- 确保数据类型一致性
```

---

## 🎯 最佳实践

### 1. 提供准确的文件路径

```
✅ 正确：
分析文件 /Users/dirk/code/test.py 的错误...

❌ 错误：
分析 test.py 的错误...  （相对路径可能找不到文件）
```

### 2. 包含完整的错误堆栈

```
✅ 正确：
错误信息：
Traceback (most recent call last):
  File "test.py", line 10, in <module>
    result = divide(10, 0)
ZeroDivisionError: division by zero

❌ 错误：
有个错误  （信息不足）
```

### 3. 描述上下文

```
✅ 正确：
这是一个数据处理脚本，在处理 CSV 文件时出错
文件：/path/to/process.py
错误：...

❌ 仅限：
文件有错误
```

---

## 🔧 高级用法

### 多文件分析

如果错误涉及多个文件，可以分别分析：

```
请帮我分析主文件的错误：
/path/to/main.py
错误：ImportError: cannot import name 'helper' from 'utils'
```

然后：

```
再分析依赖文件：
/path/to/utils.py
看看是否有 helper 函数的定义问题
```

### 批量错误分析

对于有多个错误的文件：

```
请先分析第一个错误：
文件：/path/to/complex.py
错误1：NameError at line 15
```

修复后：

```
现在分析第二个错误：
同一个文件，错误2：TypeError at line 28
```

---

## 📞 支持的错误类型

- ✅ **SyntaxError** - 语法错误
- ✅ **NameError** - 未定义的变量/函数
- ✅ **TypeError** - 类型错误
- ✅ **ValueError** - 值错误
- ✅ **IndexError** - 索引错误
- ✅ **KeyError** - 键错误
- ✅ **AttributeError** - 属性错误
- ✅ **ImportError** - 导入错误
- ✅ **ZeroDivisionError** - 除零错误
- ✅ 其他 Python 运行时错误

---

## 🚨 注意事项

1. **文件权限**：确保 Agent 有权限读取指定的文件
2. **路径格式**：建议使用绝对路径
3. **文件大小**：建议分析的文件不超过 1MB
4. **隐私安全**：不要分析包含敏感信息（密码、密钥等）的文件

---

## 📖 相关文档

- [README.md](README.md) - Agent 详细说明
- [快速启动指南](../../../../QUICK_START.md)
- [手动启动指南](../../../../MANUAL_STARTUP_GUIDE.md)
