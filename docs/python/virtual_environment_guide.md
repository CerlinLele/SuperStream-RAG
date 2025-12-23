# Python 虚拟环境使用指南

## 简介

本项目使用 Python 虚拟环境 (`venv`) 来隔离项目依赖。虚拟环境可以确保项目的依赖不会污染系统 Python，也不会与其他项目的依赖冲突。

## 项目结构

```
SuperStream-RAG/
├── .venv/              # 虚拟环境目录（已隔离）
├── requirements.txt    # 依赖列表
├── config.py          # 项目配置
├── main.py            # 应用入口
└── docs/
    └── python/
        └── virtual_environment_guide.md  # 本文件
```

## 快速开始

### 1. 激活虚拟环境

#### Windows (PowerShell / Git Bash)
```bash
# 使用 PowerShell
.venv\Scripts\Activate.ps1

# 或使用 Git Bash
source .venv/Scripts/activate
```

#### macOS / Linux
```bash
source .venv/bin/activate
```

激活成功后，命令行前面会显示 `(.venv)` 标识。

### 2. 验证虚拟环境

```bash
# 检查 Python 位置（应该在 .venv 目录中）
which python  # macOS/Linux
where python  # Windows

# 检查已安装的包
pip list

# 验证 LlamaIndex 安装
python -c "from llama_index.core import VectorStoreIndex; print('LlamaIndex is ready!')"
```

### 3. 运行项目

```bash
# 确保虚拟环境已激活
python main.py
```

### 4. 退出虚拟环境

```bash
deactivate
```

## 依赖管理

### 查看所有依赖

```bash
# 激活虚拟环境后
pip list
```

### 安装新依赖

```bash
# 激活虚拟环境
source .venv/Scripts/activate  # 或对应的激活命令

# 安装包
pip install package_name

# 更新 requirements.txt
pip freeze > requirements.txt
```

### 更新所有依赖

```bash
# 激活虚拟环境
source .venv/Scripts/activate

# 升级 pip
pip install --upgrade pip

# 更新 requirements.txt 中的所有包
pip install -r requirements.txt --upgrade
```

### 卸载依赖

```bash
# 激活虚拟环境
source .venv/Scripts/activate

# 卸载单个包
pip uninstall package_name

# 卸载 requirements.txt 中的所有包
pip uninstall -r requirements.txt -y
```

## 虚拟环境管理

### 重新创建虚拟环境

如果虚拟环境损坏或需要重新初始化：

```bash
# 删除旧的虚拟环境
rm -rf .venv  # macOS/Linux
rmdir /s /q .venv  # Windows

# 创建新的虚拟环境
python -m venv .venv

# 激活虚拟环境
source .venv/Scripts/activate  # Windows Git Bash
# 或
.venv\Scripts\Activate.ps1  # Windows PowerShell

# 安装依赖
pip install -r requirements.txt
```

### 导出依赖

将当前虚拟环境的所有依赖导出到 requirements.txt：

```bash
pip freeze > requirements.txt
```

### 从 requirements.txt 恢复环境

```bash
pip install -r requirements.txt
```

## 项目依赖说明

本项目的主要依赖包括：

| 包名 | 版本约束 | 用途 |
|------|--------|------|
| llama-index-core | >=0.10.0 | LlamaIndex 核心框架 |
| llama-index-embeddings-openai | >=0.1.0 | OpenAI 嵌入模型 |
| llama-index-llms-openai | >=0.1.0 | OpenAI LLM 接口 |
| llama-index-readers-file | >=0.1.0 | 文件读取功能 |
| llama-index-vector-stores-faiss | >=0.1.0 | FAISS 向量存储 |
| python-dotenv | >=1.0.0 | 环境变量管理 |
| pydantic | >=2.0 | 数据验证 |

## 常见问题

### Q: 虚拟环境在哪里？
**A:** 虚拟环境在项目根目录的 `.venv` 文件夹中。

### Q: 如何确认虚拟环境已激活？
**A:** 命令行前面会显示 `(.venv)` 标识，例如：
```
(.venv) user@machine:~/SuperStream-RAG $
```

### Q: 激活虚拟环境时出现权限错误（Windows PowerShell）
**A:** 在 PowerShell 中执行以下命令提升权限：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: 如何清理虚拟环境中的缓存？
**A:**
```bash
# 清理 pip 缓存
pip cache purge

# 或删除 __pycache__ 目录
find . -type d -name __pycache__ -exec rm -rf {} +  # macOS/Linux
```

### Q: 虚拟环境占用了多少空间？
**A:**
```bash
# 查看 .venv 目录大小
du -sh .venv  # macOS/Linux
```

### Q: 如何在 IDE 中使用虚拟环境？

#### VSCode
1. 打开命令面板 (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. 搜索 "Python: Select Interpreter"
3. 选择 `./.venv/bin/python` (macOS/Linux) 或 `.\.venv\Scripts\python.exe` (Windows)

#### PyCharm
1. File → Settings → Project → Python Interpreter
2. 点击齿轮图标 → Add
3. 选择 "Existing Environment"
4. 浏览到 `.venv/bin/python` (macOS/Linux) 或 `.venv\Scripts\python.exe` (Windows)

## 相关命令速查表

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（Windows Git Bash）
source .venv/Scripts/activate

# 激活虚拟环境（Windows PowerShell）
.venv\Scripts\Activate.ps1

# 激活虚拟环境（macOS/Linux）
source .venv/bin/activate

# 退出虚拟环境
deactivate

# 安装依赖
pip install -r requirements.txt

# 升级 pip
pip install --upgrade pip

# 查看已安装包
pip list

# 导出依赖
pip freeze > requirements.txt

# 安装新包
pip install package_name

# 卸载包
pip uninstall package_name

# 运行项目
python main.py
```

## 参考资源

- [Python venv 官方文档](https://docs.python.org/3/library/venv.html)
- [pip 官方文档](https://pip.pypa.io/)
- [LlamaIndex 官方文档](https://docs.llamaindex.ai/)

---

最后更新: 2025-12-20
