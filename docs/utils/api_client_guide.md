# API Client 集中化配置指南

## 概述

`api_client.py` 模块提供了一个集中化的OpenAI API客户端初始化方案，支持：

- ✅ 官方OpenAI API
- ✅ 自定义API基础URL（Azure OpenAI、国内服务等）
- ✅ 环境变量配置
- ✅ 显式参数传入
- ✅ 多个模块间共享同一初始化逻辑

## 快速开始

### 1. 基础使用（读取环境变量）

在 `.env` 文件中配置：

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_API_BASE=https://api.openai.com/v1    # 可选，默认为OpenAI官方服务
```

然后在代码中使用：

```python
from query import QueryTranslator

# 自动从环境变量读取配置
translator = QueryTranslator()
result = translator.translate_query("你好")
```

### 2. 使用自定义API Base

```python
from query import QueryTranslator

# 显式指定自定义API base
translator = QueryTranslator(
    api_base="https://your-custom-api/v1"
)
```

或在 `.env` 中配置：

```env
OPENAI_API_KEY=sk-your-key
OPENAI_API_BASE=https://your-custom-api/v1
```

### 3. 直接创建OpenAI客户端

如果你需要在其他地方创建OpenAI客户端，可以使用便利函数：

```python
from query import create_openai_client

# 自动从环境变量读取
client = create_openai_client()

# 或者显式指定
client = create_openai_client(
    api_key="sk-...",
    api_base="https://api.example.com/v1"
)
```

### 4. 使用APIClientConfig类

如果需要更多控制：

```python
from query import APIClientConfig

config = APIClientConfig(
    api_key="sk-...",
    api_base="https://api.example.com/v1"
)

# 检查配置
if config.is_configured():
    print(f"API Base: {config.get_api_base()}")
    client = config.create_client()
```

## 架构设计

### 模块结构

```
query/
├── api_client.py          ← 新增：集中化API客户端配置
├── translator.py          ← 已更新：使用api_client
├── intent_detector.py     ← 将来可以使用api_client
├── rewriter.py            ← 将来可以使用api_client
└── __init__.py            ← 已更新：导出api_client相关函数
```

### 初始化优先级

1. **显式参数** （最高）
   ```python
   QueryTranslator(api_key="sk-...", api_base="https://...")
   ```

2. **环境变量**
   ```env
   OPENAI_API_KEY=sk-...
   OPENAI_API_BASE=https://...
   ```

3. **默认值** （最低）
   - api_key: 无默认值（必须提供）
   - api_base: None（使用OpenAI官方API）

## 常见场景

### 场景1：使用官方OpenAI API

```env
OPENAI_API_KEY=sk-your-key
```

```python
translator = QueryTranslator()
```

### 场景2：使用Azure OpenAI

```env
OPENAI_API_KEY=your-azure-key
OPENAI_API_BASE=https://<your-resource>.openai.azure.com/v1
```

```python
translator = QueryTranslator()
```

### 场景3：使用本地服务（如Ollama兼容API）

```env
OPENAI_API_KEY=dummy-key
OPENAI_API_BASE=http://localhost:8000/v1
```

```python
translator = QueryTranslator()
```

### 场景4：开发环境与生产环境分离

```python
import os
from query import QueryTranslator

# 根据环境变量选择不同的配置
if os.getenv("ENVIRONMENT") == "production":
    translator = QueryTranslator(
        api_base="https://prod-api.example.com/v1"
    )
else:
    translator = QueryTranslator(
        api_base="http://localhost:8000/v1"
    )
```

## 其他模块集成

### 在QueryRewriter中使用

```python
from .api_client import create_openai_client

class QueryRewriter:
    def __init__(self, api_key=None, api_base=None):
        self.client = create_openai_client(api_key, api_base)
```

### 在IntentDetector中使用

```python
from .api_client import create_openai_client

class IntentDetector:
    def __init__(self, api_key=None, api_base=None):
        self.client = create_openai_client(api_key, api_base)
```

## 错误处理

```python
from query import QueryTranslator

try:
    translator = QueryTranslator()
except ValueError as e:
    print(f"配置错误: {e}")
    # 确保在 .env 中设置 OPENAI_API_KEY
```

## 最佳实践

1. **总是在.env中配置API密钥**
   ```env
   OPENAI_API_KEY=sk-...
   ```

2. **在requirements.txt中明确依赖版本**
   ```
   openai>=1.0.0
   ```

3. **为不同环境使用不同的.env文件**
   - `.env.development`
   - `.env.production`
   - `.env.example` （示例，不包含实际密钥）

4. **从不提交包含实际API密钥的.env文件**
   ```
   .env          # 在.gitignore中
   .env.example  # 可以提交，作为配置示例
   ```

5. **在初始化时验证配置**
   ```python
   config = APIClientConfig()
   if not config.is_configured():
       raise ValueError("API not properly configured")
   ```

## 总结

通过使用 `api_client.py` 模块：

- ✅ **DRY原则**：避免在多个模块中重复初始化逻辑
- ✅ **灵活性**：支持多种API配置方式
- ✅ **可维护性**：集中管理API配置，便于未来修改
- ✅ **可扩展性**：轻松添加新的API客户端功能

