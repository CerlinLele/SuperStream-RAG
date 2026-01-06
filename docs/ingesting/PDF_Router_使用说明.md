# PDF 路由器文档

## 概述

PDF 路由器 (`PDFRouter`) 是 SuperStream PDF 处理管道的核心组件,负责根据文档类型自动检测和路由 PDF 文件到相应的处理器。

## 快速开始

### 基本使用

```python
from ingest.processors import PDFRouter
from pathlib import Path

# 创建路由器实例
router = PDFRouter()

# 路由单个 PDF
pdf_path = Path("Schedule_2_Terms_and_Definitions_v2.1.pdf")
plan = router.route(pdf_path)

if plan:
    print(f"Schedule Type: {plan.schedule_type}")
    print(f"Processor: {plan.processor_type}")
    print(f"Extractors: {plan.extractors}")
else:
    print("Document type not recognized")
```

### 批量路由

```python
# 路由多个 PDF 文件
pdf_dir = Path("data/raw/official-documents/superstream-standard")
pdf_files = list(pdf_dir.glob("*.pdf"))

routes = router.route_batch(pdf_files)

for pdf_path, plan in routes.items():
    if plan:
        print(f"{pdf_path.name} -> {plan.schedule_type}")
```

## 路由规则详解

### 文档类型检测

路由器通过**文件名模式匹配**来检测文档类型。以下是所有支持的 Schedule 类型:

#### Schedule 2 - 术语定义
- **文件名模式**: `Schedule.*2.*Terms.*Definitions`
- **特点**:
  - 23 页
  - 简单的 2-3 列术语表
  - 包含 30+ 术语定义
- **处理器**: `table` (表格处理器)
- **提取器**: `terminology` (术语提取器)
- **用途**: 提取 SuperStream 标准术语和定义

**示例文件**:
```
Schedule_2_Terms_and_Definitions_v2.1.pdf
```

#### Schedule 3 - 支付方式
- **文件名模式**: `Schedule.*3.*Payment`
- **特点**:
  - 7 页
  - 文本和简单表格混合
  - 支付方式规范说明
- **处理器**: `text` (文本处理器)
- **提取器**: 无
- **用途**: 支付方式相关规范

**示例文件**:
```
Schedule_3_Payment_Methods_v2.0.pdf
```

#### Schedule 4a - 缴款指南
- **文件名模式**: `Schedule.*4a.*Contributions`
- **特点**:
  - 110 页 (最大)
  - 复杂的 15 列字段规范表
  - 包含 100+ 字段定义
  - XBRL 映射信息
- **处理器**: `table` (表格处理器)
- **提取器**: `field_spec` (字段规范提取器)
- **用途**: 提取成员缴款的字段规范和技术实现细节

**示例文件**:
```
Schedule_4a_ContributionsMIG_v2.0_Apr2017.pdf
```

**关键信息**:
这是最复杂的文档,包含:
- 字段名称和缩写
- M/O/C 要求指示符 (Mandatory/Optional/Conditional)
- 数据类型和长度
- 验证规则
- XBRL 事实映射

#### Schedule 4b - 滚动指南
- **文件名模式**: `Schedule.*4b.*Rollover`
- **特点**:
  - 57 页
  - 复杂的 15 列字段规范表
  - 包含 50+ 字段定义
  - 与 4a 类似的结构
- **处理器**: `table` (表格处理器)
- **提取器**: `field_spec` (字段规范提取器)
- **用途**: 提取滚动相关的字段规范

**示例文件**:
```
Schedule_4b_Rollover_MIG_v2.1_Nov17.pdf
```

#### Schedule 5 - 消息编排
- **文件名模式**: `Schedule.*5.*Message`
- **特点**:
  - 21 页
  - 消息流和编排规范
  - 多列规范表
- **处理器**: `table` (表格处理器)
- **提取器**: 无
- **用途**: 消息编排和配置文件规范

**示例文件**:
```
Schedule_5_Message_Orchestration_and_Profiles_v2.0_Apr2017.pdf
```

#### Schedule 6 - 错误代码管理
- **文件名模式**: `Schedule.*6.*Error`
- **特点**:
  - 26 页
  - 混合内容 (表格 + XML/XSD 代码块)
  - 错误代码定义表
  - XSD schema 定义
- **处理器**: `hybrid` (混合处理器)
- **提取器**: `error_code` (错误码提取器), `xml_schema` (XSD 提取器)
- **用途**: 提取错误代码和 XML schema 定义

**示例文件**:
```
Schedule_6_Error_Code_Management_v2.0_Apr2017.pdf
```

**关键信息**:
这是唯一使用 `hybrid` 处理器的文档:
- 包含错误代码表 (E001, E002 等)
- 错误严重级别
- 解决方案信息
- XML/XSD 代码块

## 处理器类型

### table (表格处理器)
**适用于**: Schedule 2, 4a, 4b, 5

用途: 提取和结构化处理表格
- 支持简单 2-3 列表格 (Schedule 2)
- 支持复杂 15+ 列表格 (Schedule 4a/4b)
- 保留表格结构为 JSON/CSV

### text (文本处理器)
**适用于**: Schedule 3

用途: 处理文本和简单内容
- 提取段落和标题
- 处理叙述性内容
- 生成可搜索的文本

### hybrid (混合处理器)
**适用于**: Schedule 6

用途: 同时处理表格和代码块
- 分别提取表格和代码块
- 表格转换为结构化数据
- 代码块保留原始格式

## 提取器类型

### terminology (术语提取器)
- **应用场景**: Schedule 2
- **输出格式**: JSON 字典 `{term: definition}`
- **数据库位置**: `data/processed/terminology/`

### field_spec (字段规范提取器)
- **应用场景**: Schedule 4a, 4b
- **输出格式**: JSON 列表 `[{field_name, requirement, type, ...}]`
- **数据库位置**: `data/processed/field_specs/`

### error_code (错误码提取器)
- **应用场景**: Schedule 6
- **输出格式**: JSON 字典 `{code: {description, severity, resolution}}`
- **数据库位置**: `data/processed/error_codes/`

### xml_schema (XML Schema 提取器)
- **应用场景**: Schedule 6
- **输出格式**: JSON 数组包含代码块
- **数据库位置**: `data/processed/code/`

## 路由规则总表

| Schedule | 文件名模式 | 处理器 | 提取器 | 页数 | 复杂度 |
|----------|-----------|--------|--------|------|--------|
| Schedule 2 | `Schedule.*2.*Terms.*Definitions` | table | terminology | 23 | 低 |
| Schedule 3 | `Schedule.*3.*Payment` | text | 无 | 7 | 低-中 |
| Schedule 4a | `Schedule.*4a.*Contributions` | table | field_spec | 110 | 极高 |
| Schedule 4b | `Schedule.*4b.*Rollover` | table | field_spec | 57 | 极高 |
| Schedule 5 | `Schedule.*5.*Message` | table | 无 | 21 | 中 |
| Schedule 6 | `Schedule.*6.*Error` | hybrid | error_code,xml_schema | 26 | 中-高 |

## API 参考

### PDFRouter 类

#### `detect_schedule_type(pdf_path: Path) -> Optional[str]`

根据文件名检测 Schedule 类型。

**参数**:
- `pdf_path` (Path): PDF 文件路径

**返回值**:
- Schedule 类型字符串 (如 `'Schedule_2'`)
- 如果无法识别,返回 `None`

**示例**:
```python
router = PDFRouter()
schedule = router.detect_schedule_type(Path("Schedule_2_Terms_and_Definitions_v2.1.pdf"))
print(schedule)  # Output: 'Schedule_2'
```

#### `route(pdf_path: Path) -> Optional[ProcessingPlan]`

为 PDF 返回完整的处理计划。

**参数**:
- `pdf_path` (Path): PDF 文件路径

**返回值**:
- `ProcessingPlan` 对象,包含:
  - `schedule_type`: Schedule 类型
  - `processor_type`: 处理器类型
  - `extractors`: 提取器列表
  - `description`: 描述信息
- 如果无法识别,返回 `None`

**示例**:
```python
plan = router.route(Path("Schedule_4a_ContributionsMIG_v2.0_Apr2017.pdf"))
if plan:
    print(f"Processor: {plan.processor_type}")
    print(f"Extractors: {plan.extractors}")
```

#### `route_batch(pdf_paths: List[Path]) -> dict`

批量路由多个 PDF 文件。

**参数**:
- `pdf_paths` (List[Path]): PDF 文件路径列表

**返回值**:
- 字典,键为 Path,值为 ProcessingPlan (或 None 如果无法识别)

**示例**:
```python
pdf_files = list(Path("data/raw").glob("*.pdf"))
routes = router.route_batch(pdf_files)

for pdf_path, plan in routes.items():
    if plan:
        print(f"{pdf_path.name}: {plan.schedule_type}")
    else:
        print(f"{pdf_path.name}: NOT RECOGNIZED")
```

### ProcessingPlan 数据类

```python
@dataclass
class ProcessingPlan:
    schedule_type: str      # 如 'Schedule_2'
    processor_type: str     # 'table', 'text', 或 'hybrid'
    extractors: List[str]   # 如 ['terminology', 'field_spec']
    description: str        # 人类可读的描述
```

## 实现细节

### 文件名匹配算法

路由器使用**正则表达式**进行文件名匹配:

```python
SCHEDULE_PATTERNS = {
    r"Schedule.*2.*Terms.*Definitions": "Schedule_2",
    r"Schedule.*3.*Payment": "Schedule_3",
    r"Schedule.*4a.*Contributions": "Schedule_4a",
    r"Schedule.*4b.*Rollover": "Schedule_4b",
    r"Schedule.*5.*Message": "Schedule_5",
    r"Schedule.*6.*Error": "Schedule_6",
}
```

**关键特点**:
- 大小写不敏感 (IGNORECASE 标志)
- 支持灵活的版本号和文件名变化
- 例如以下都能匹配 Schedule_2:
  - `Schedule_2_Terms_and_Definitions_v2.1.pdf`
  - `schedule 2 terms definitions.pdf`
  - `SCHEDULE_2_TERMS_AND_DEFINITIONS.pdf`

### 路由流程

```
输入 PDF 文件
    |
    V
检测 Schedule 类型 (文件名匹配)
    |
    +-- 匹配? --> 返回 ProcessingPlan
    |
    +-- 不匹配? --> 返回 None
```

## 常见问题

### Q: 如何添加新的 Schedule 类型?

在 `pdf_router.py` 中修改:

1. 在 `SCHEDULE_PATTERNS` 中添加新的正则表达式:
```python
r"Schedule.*7.*YourType": "Schedule_7",
```

2. 在 `PROCESSING_PLANS` 中添加处理计划:
```python
"Schedule_7": ProcessingPlan(
    schedule_type="Schedule_7",
    processor_type="table",  # 或 text/hybrid
    extractors=["your_extractor"],
    description="Your description",
),
```

### Q: 如果文件名不匹配怎么办?

路由器会返回 `None`。建议检查:
1. 文件名是否包含 "Schedule" 关键词
2. 文件名中是否有正确的 Schedule 编号 (2, 3, 4a, 4b, 5, 6)
3. 是否存在拼写错误

### Q: 能否基于文件内容而不是文件名进行路由?

可以,但需要修改 `detect_schedule_type()` 方法。当前实现基于文件名是为了性能和简单性。

如果需要基于内容的检测,可以:
1. 使用 pdfplumber 读取 PDF 的第一页
2. 分析页面标题或元数据
3. 返回 Schedule 类型

### Q: 处理器和提取器的关系是什么?

- **处理器** (`processor_type`) 定义如何读取 PDF 内容
- **提取器** (`extractors`) 定义从处理后的内容中提取什么数据

例如:
- 处理器: `table` - 使用 pdfplumber 提取所有表格
- 提取器: `terminology` - 从表格中提取术语-定义对

## 集成示例

将路由器集成到完整的处理管道:

```python
from pathlib import Path
from ingest.processors import PDFRouter

def process_pdf_directory(pdf_dir: Path):
    """Process all PDFs in a directory."""

    router = PDFRouter()
    pdf_files = list(pdf_dir.glob("*.pdf"))

    # 批量路由
    routes = router.route_batch(pdf_files)

    # 按处理器类型分组
    table_docs = []
    text_docs = []
    hybrid_docs = []

    for pdf_path, plan in routes.items():
        if plan is None:
            print(f"Warning: {pdf_path.name} not recognized")
            continue

        if plan.processor_type == 'table':
            table_docs.append((pdf_path, plan))
        elif plan.processor_type == 'text':
            text_docs.append((pdf_path, plan))
        elif plan.processor_type == 'hybrid':
            hybrid_docs.append((pdf_path, plan))

    # 现在可以为每个组提供适当的处理器
    print(f"Table documents: {len(table_docs)}")
    print(f"Text documents: {len(text_docs)}")
    print(f"Hybrid documents: {len(hybrid_docs)}")
```

## 相关文档

- [PDF 处理管道架构](SuperStream-PDF-解析系统实现计划.md)
- [表格处理器文档](../README.md) (待实现)
- [文本处理器文档](../README.md) (待实现)
- [混合处理器文档](../README.md) (待实现)
