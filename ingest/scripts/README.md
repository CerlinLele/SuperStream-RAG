# SuperStream 词汇表处理脚本

本目录包含两个主要脚本用于处理 SuperStream 词汇表：
1. **extract_glossary.py** - 从 HTML 文件中提取词汇表
2. **glossary_to_faiss.py** - 创建 FAISS 向量索引用于语义搜索

---

## 脚本 1: 提取词汇表 (extract_glossary.py)

从 SuperStream 官方 HTML 文档中提取词汇表术语，并保存为 JSON 格式。

### 快速开始

```bash
# 提取单个 HTML 文件
python -m ingest.scripts.extract_glossary single "data/raw/official-documents/2-role-based-guide/glossary.html"

# 批量提取目录中的所有 HTML 文件
python -m ingest.scripts.extract_glossary batch "data/raw/official-documents/2-role-based-guide/" --output-dir "data/glossaries"
```

### 使用方法

#### 单个文件提取

```bash
python -m ingest.scripts.extract_glossary single <html_file_path> [--output-name <name>] [--output-dir <dir>]
```

**参数说明：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `html_file` | Path | ✓ | 要提取的 HTML 文件路径 |
| `--output-name` | str | ✗ | 输出 JSON 文件的名称，不含 `.json` 扩展名（默认：`superstream_glossary`） |
| `--output-dir` | Path | ✗ | 输出目录的路径（默认：使用配置中的 `GLOSSARY_OUTPUT_DIR`） |

**示例：**
```bash
python -m ingest.scripts.extract_glossary single "data/raw/official-documents/2-role-based-guide/glossary.html" --output-name "role_guide_glossary"
```

#### 批量提取

```bash
python -m ingest.scripts.extract_glossary batch <source_dir> [--output-dir <dir>]
```

**参数说明：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `source_dir` | Path | ✓ | 包含 HTML 文件的目录 |
| `--output-dir` | Path | ✗ | 输出目录的路径（默认：使用配置中的 `GLOSSARY_OUTPUT_DIR`） |

**示例：**
```bash
# 递归处理目录下所有 HTML 文件
python -m ingest.scripts.extract_glossary batch "data/raw/official-documents/" --output-dir "data/glossaries"
```

### 脚本功能

1. **解析 HTML**：从 HTML 文件中提取词汇表条目
2. **保存 JSON**：将提取的词汇表以 JSON 格式保存
3. **统计信息**：显示提取的词汇数量、输出文件大小、示例词汇等
4. **批量处理**：支持递归查找目录中的所有 HTML 文件并逐个处理

### 输出格式

提取成功后会输出类似以下信息：

```
======================================================================
SuperStream Glossary Extraction - HTML to JSON
======================================================================

[Input]  HTML file: data/raw/official-documents/2-role-based-guide/glossary.html
[Output] JSON file: data/glossaries/superstream_glossary.json

[Step 1] Extracting glossary terms from HTML...
[SUCCESS] Found 150 glossary terms

[Step 2] Saving glossary as JSON...

======================================================================
[SUCCESS] Glossary extraction completed successfully!
======================================================================

Statistics:
  Total terms extracted: 150
  Output file: data/glossaries/superstream_glossary.json
  File size: 45.23 KB

First 5 terms:
  1. API Key
     -> Authentication credential used to access SuperStream...
  2. Dashboard
     -> Main interface for monitoring...
  ...
```

### 输出文件格式

JSON 文件格式如下：

```json
{
  "Term 1": "Definition of term 1",
  "Term 2": "Definition of term 2",
  "Term 3": "Definition of term 3",
  ...
}
```

---

## 脚本 2: 创建 FAISS 索引 (glossary_to_faiss.py)

这个脚本从 SuperStream JSON 或 PDF 文件中提取词汇表术语，并创建 FAISS 向量索引以进行语义搜索和检索。

### 快速开始

```bash
# 直接运行脚本
python ingest/scripts/glossary_to_faiss.py

# 输出：
# - 索引保存位置: data/indices/superstream_glossary_index
# - 数据源: data/glossaries/superstream_glossary.json
```

### 脚本功能

此脚本执行以下步骤：

#### Step 1: 从 JSON 或 PDF 提取词汇表
- **JSON 方式**（推荐）：从 `data/glossaries/superstream_glossary.json` 加载
- **PDF 方式**：使用 `pdfplumber` 从表格提取
- 将术语和定义转换为 Document 对象

### Step 2: 创建嵌入
- 使用 `intfloat/e5-large-v2` 模型（1024 维）
- 首次运行下载模型（~650 MB），后续使用缓存

### Step 3: 构建 FAISS 索引
- 创建向量索引用于快速相似性搜索
- 保存到 `data/indices/superstream_glossary_index/`

### 使用方法

#### Python 代码

```python
from ingest.scripts.glossary_to_faiss import create_glossary_faiss_index
from pathlib import Path

# 使用 JSON 文件（推荐）
index_path = create_glossary_faiss_index(
    json_path=Path("data/glossaries/superstream_glossary.json"),
    embedding_model="intfloat/e5-large-v2",
    index_name="superstream_glossary_index"
)

# 或使用 PDF 文件
index_path = create_glossary_faiss_index(
    pdf_path=Path("your_glossary.pdf"),
    embedding_model="intfloat/e5-large-v2",
    index_name="glossary_index"
)
```

### 查询索引

```python
from llama_index.core import StorageContext, load_index_from_storage

# 加载索引
storage_context = StorageContext.from_defaults(
    persist_dir="data/indices/superstream_glossary_index"
)
index = load_index_from_storage(storage_context)

# 创建查询引擎
query_engine = index.as_query_engine(similarity_top_k=5)

# 执行查询
response = query_engine.query("What is SMSF?")
print(response)
```

## 数据源格式（FAISS 索引脚本）

### JSON 格式（推荐）
文件位置: `data/glossaries/superstream_glossary.json`

```json
{
  "Term Name": "Definition of the term",
  "Another Term": "Its definition",
  ...
}
```

### PDF 格式
需要包含表格的 PDF，格式：
- 第一列：术语
- 第二列：定义

## 输出文件（FAISS 索引）

```
data/indices/superstream_glossary_index/
├── default__vector_store.json    # FAISS 向量存储
├── docstore.json                 # 文档存储
├── graph_store.json              # 图存储
├── image__vector_store.json      # 图像向量存储
└── index_store.json              # 索引元数据
```

## FAISS 索引脚本参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `json_path` | Path | 有* | JSON 文件路径 |
| `pdf_path` | Path | 有* | PDF 文件路径 |
| `output_dir` | Path | ✗ | 索引保存目录（默认：data/indices） |
| `embedding_model` | str | ✗ | 嵌入模型（默认：intfloat/e5-large-v2） |
| `index_name` | str | ✗ | 索引名称（默认：glossary_index） |

*注：`json_path` 和 `pdf_path` 至少需要提供一个

## 嵌入模型（FAISS 索引）

### intfloat/e5-large-v2（默认）
- 维度：1024
- 用途：语义搜索和检索
- 下载大小：~650 MB
- 本地运行，无需 API 密钥

### 其他可选模型
- `intfloat/e5-base`（512 维）
- `intfloat/e5-small`（384 维）
- OpenAI 嵌入模型（需要 API 密钥）

## 依赖安装

```bash
# 从 requirements.txt 安装所有依赖
pip install -r requirements.txt

# 或单独安装核心包
pip install llama-index llama-index-embeddings-huggingface llama-index-vector-stores-faiss sentence-transformers faiss-cpu
```

## 性能对比

### extract_glossary.py（HTML 提取）
| 操作 | 时间 |
|------|------|
| 解析 HTML 文件 | ~0.5-1 秒 |
| 保存 JSON 文件 | ~0.1 秒 |
| **总耗时** | ~1-2 秒 |

### glossary_to_faiss.py（FAISS 索引）

| 操作 | 时间 |
|------|------|
| JSON 加载（35 个术语） | ~0.1 秒 |
| 嵌入创建（35 个术语） | ~3 秒 |
| 索引保存 | ~1 秒 |
| **总耗时** | ~4 秒 |

首次运行会下载模型（~650 MB），后续运行使用缓存，速度更快。

## 使用工作流

### 完整工作流（推荐）

这是处理 SuperStream 词汇表的完整工作流：

1. **第一步：从 HTML 提取词汇表**
   ```bash
   python -m ingest.scripts.extract_glossary single "data/raw/official-documents/2-role-based-guide/glossary.html"
   ```
   输出：`data/glossaries/superstream_glossary.json`

2. **第二步：创建 FAISS 向量索引**
   ```bash
   python ingest/scripts/glossary_to_faiss.py
   ```
   输出：`data/indices/superstream_glossary_index/`

3. **第三步：使用索引进行语义搜索**
   ```python
   from llama_index.core import StorageContext, load_index_from_storage

   storage_context = StorageContext.from_defaults(
       persist_dir="data/indices/superstream_glossary_index"
   )
   index = load_index_from_storage(storage_context)
   query_engine = index.as_query_engine(similarity_top_k=5)
   response = query_engine.query("What is SMSF?")
   print(response)
   ```

### 快速更新工作流

当有新的 HTML 文档时：

1. 提取新的 HTML 文件：
   ```bash
   python -m ingest.scripts.extract_glossary batch "data/raw/official-documents/" --output-dir "data/glossaries"
   ```

2. 重建索引：
   ```bash
   python ingest/scripts/glossary_to_faiss.py
   ```

## 高级用法

### 添加新术语

1. **编辑 `data/glossaries/superstream_glossary.json`**
   ```json
   {
     "Existing Term": "Definition",
     "New Term": "Definition of new term",
     ...
   }
   ```

2. **重新运行 FAISS 脚本以重建索引**
   ```bash
   python ingest/scripts/glossary_to_faiss.py
   ```

### 使用检索器

```python
# 获取最相关的 5 个术语
retriever = index.as_retriever(similarity_top_k=5)
results = retriever.retrieve("superannuation")

for result in results:
    print(f"Score: {result.score}")
    print(f"Term: {result.metadata['term']}")
    print(f"Definition: {result.metadata['definition']}")
```

### 与其他索引结合

```python
# 可以与其他文档索引组合使用
# 创建混合搜索系统
```

## 故障排除

### 内存不足
- 使用较小的模型：`intfloat/e5-small`
- 或安装 GPU 版本：`pip install faiss-gpu`

### 编码问题
- 确保 JSON 文件使用 UTF-8 编码
- 脚本会自动处理 UTF-8 BOM

### PDF 提取失败
- 检查 PDF 是否包含表格
- 表格应至少有 2 列（术语、定义）
- 推荐改用 JSON 文件作为数据源

## 示例输出

```
Found pre-existing glossary JSON file, using that...

============================================================
SuperStream Glossary to FAISS Index
============================================================

[Step 1] Extracting glossary from source...
JSON File: data/glossaries/superstream_glossary.json
[OK] Successfully extracted 35 glossary terms
[OK] Created 35 Document objects

[Step 2] Building FAISS vector index...
Embedding Model: intfloat/e5-large-v2
Model Type: huggingface
Generating embeddings: 100%|##########| 35/35 [00:03<00:00, 10.82it/s]
Index built successfully with 35 documents
[OK] FAISS index built and saved successfully
[OK] Index location: data/indices/superstream_glossary_index

============================================================
SUMMARY
============================================================
Total Terms Extracted: 35
Total Documents: 35
Embedding Model: intfloat/e5-large-v2
Index Name: superstream_glossary_index
Index Path: data/indices/superstream_glossary_index
============================================================

[OK] Script completed successfully!
Index saved at: data/indices/superstream_glossary_index
```

## 常见问题

**Q: 第一次运行很慢，为什么？**
A: 首次运行会下载嵌入模型（~650 MB），后续运行会使用缓存并快得多。

**Q: 可以离线使用吗？**
A: 是的，模型下载一次后可以离线使用。

**Q: 如何更新索引中的术语？**
A: 编辑 JSON 文件并重新运行脚本。

**Q: 索引文件有多大？**
A: 大约 20-50 MB（取决于术语数量）。

**Q: 支持 GPU 加速吗？**
A: 是的，安装 `faiss-gpu` 和 CUDA 支持即可。

## 许可证

这个脚本是 SuperStream RAG 项目的一部分。
