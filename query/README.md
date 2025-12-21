# Query 改写框架 (Query Rewriting Framework)

## 框架概览

这个框架提供了完整的 SuperStream RAG 系统的 Query 处理管道。通过对用户输入的查询进行多层次的转换和优化，显著提升检索质量和准确率。

## 目录结构

```
query/
├── __init__.py              # 模块初始化和导出
├── processor.py             # 主处理器 - 协调整个管道
├── normalizer.py            # 查询规范化 - 清理和术语映射
├── expander.py              # 查询扩展 - 生成多个变体
├── rewriter.py              # 查询重写 - 优化检索
├── translator.py            # 查询翻译 - 多语言支持
├── decomposer.py            # 查询分解 - 拆分复杂查询
├── intent_detector.py       # 意图检测 - 识别用户意图
└── README.md               # 本文档
```

## 模块说明

### 1. **processor.py** - QueryProcessor (主处理器)
**职责：** 协调整个 Query 处理管道

**关键函数：**
- `process_query()` - 执行完整的处理流程
- `detect_language()` - 语言检测
- `normalize()` - 调用规范化模块
- `expand()` - 调用扩展模块
- `rewrite()` - 调用重写模块
- `translate()` - 调用翻译模块
- `detect_intent()` - 调用意图检测模块
- `decompose_complex_query()` - 调用分解模块

**输出：** ProcessedQuery 数据类，包含所有处理结果

---

### 2. **normalizer.py** - QueryNormalizer (查询规范化)
**职责：** 标准化查询格式和映射专业术语

**关键函数：**
- `normalize()` - 执行完整规范化
- `clean_whitespace()` - 清理空白符
- `standardize_case()` - 统一大小写
- `normalize_punctuation()` - 处理标点符号
- `map_terminology()` - 术语映射（如"超级年金" → "Superannuation"）
- `build_terminology_map()` - 构建术语字典
- `load_terminology_map()` - 加载外部术语映射文件

**示例输入/输出：**
```
输入：  "什么是 SuperStream？？？"
输出：  "What is SuperStream?"
```

---

### 3. **expander.py** - QueryExpander (查询扩展)
**职责：** 生成多个语义变体，增加检索覆盖率

**关键函数：**
- `expand()` - 生成所有变体
- `generate_synonyms()` - 同义词替换
- `add_temporal_variations()` - 时间相关变体
- `add_requirement_variations()` - 需求相关变体
- `add_authority_variations()` - 权威来源变体
- `generate_paraphrases()` - 语义释义
- `add_domain_specific_variations()` - 领域特定变体

**示例输入/输出：**
```
输入：  "What is the SuperStream deadline?"
输出：  [
    "What is the SuperStream deadline?",
    "When must SuperStream be paid?",
    "What is the deadline for SuperStream contributions?",
    "ATO SuperStream submission deadline",
    "SuperStream payment timeframe"
]
```

---

### 4. **rewriter.py** - QueryRewriter (查询重写)
**职责：** 优化查询格式以提高嵌入模型的理解

**关键函数：**
- `rewrite()` - 执行完整重写
- `add_instruction_prefix()` - 添加语义指令前缀
- `add_context_clues()` - 添加上下文线索
- `expand_acronyms()` - 展开缩写词
- `remove_stopwords()` - 移除非关键词
- `highlight_key_entities()` - 突出关键实体
- `transform_for_embedding_model()` - 为特定模型优化

**示例输入/输出：**
```
输入：  "SuperStream deadline"
输出：  "Represent this legal query: SuperStream contribution payment deadline days ATO requirement"
```

---

### 5. **translator.py** - QueryTranslator (查询翻译)
**职责：** 多语言支持，主要用于中文→英文翻译

**关键函数：**
- `detect_language()` - 语言检测
- `translate_query()` - 通用翻译接口
- `translate_chinese_to_english()` - 中文→英文
- `translate_english_to_chinese()` - 英文→中文
- `handle_mixed_language_query()` - 处理中英混合
- `preserve_technical_terms()` - 保留技术术语
- `get_translation_confidence()` - 翻译置信度

**示例输入/输出：**
```
输入：  "超级年金的截止日期是什么？"
输出：  "What is the SuperStream contribution deadline?"

输入：  "What are APRA requirements for 超级年金?"
输出：  "What are APRA requirements for SuperStream?"
```

---

### 6. **decomposer.py** - QueryDecomposer (查询分解)
**职责：** 将复杂的多元素查询分解为简单的子查询

**关键函数：**
- `decompose()` - 执行完整分解
- `extract_entities()` - 提取所有实体
- `identify_query_complexity()` - 判断复杂度
- `extract_roles()` - 提取角色（谁）
- `extract_actions()` - 提取动作（做什么）
- `extract_objects()` - 提取对象（对什么）
- `extract_temporal_constraints()` - 提取时间约束
- `extract_conditions()` - 提取条件
- `build_sub_queries()` - 构建子查询

**示例输入/输出：**
```
输入：  "作为雇主，如果我在28天内没有支付超级年金，会怎样？"

输出：
实体：
- 角色：employer
- 动作：not pay (failure)
- 对象：SuperStream contribution
- 时间：28 days
- 条件：if not paid

子查询：
1. "SuperStream contribution deadline 28 days"
2. "Employer penalty for late SuperStream payment"
3. "ATO enforcement for SuperStream non-compliance"
4. "Consequences of missing SuperStream deadline"
```

---

### 7. **intent_detector.py** - IntentDetector (意图检测)
**职责：** 识别用户查询的意图类型，优化检索策略

**意图类型：**
- **definition** - 要求定义或解释
- **requirement** - 询问规则和要求
- **process** - 询问步骤或程序
- **penalty** - 询问后果或罚款
- **exception** - 询问例外情况
- **comparison** - 比较两个概念
- **calculation** - 要求数值计算
- **clarification** - 澄清矛盾信息

**关键函数：**
- `detect_intent()` - 检测主要意图
- `is_definition_query()` - 检测定义查询
- `is_requirement_query()` - 检测需求查询
- `is_process_query()` - 检测流程查询
- `is_penalty_query()` - 检测罚款查询
- `is_exception_query()` - 检测例外查询
- `get_intent_keywords()` - 获取意图关键词
- `get_optimal_retrieval_strategy()` - 获取检索策略

**示例输入/输出：**
```
输入：  "What is SuperStream?"
检测结果：
- 主意图：definition (置信度 0.95)
- 查询类型：concept_explanation
- 推荐检索策略：{ top_k: 5, rerank: true, focus: "definition" }

输入：  "What happens if I don't pay SuperStream?"
检测结果：
- 主意图：penalty (置信度 0.92)
- 次要意图：requirement (置信度 0.65)
- 查询类型：consequence_inquiry
- 推荐检索策略：{ top_k: 10, rerank: true, focus: "penalty, enforcement" }
```

---

## 处理流程图

```
用户查询输入
    ↓
[QueryProcessor.process_query()]
    ├→ [语言检测] detect_language()
    │   ↓
    ├→ [规范化] QueryNormalizer.normalize()
    │   - 清理空白
    │   - 统一大小写
    │   - 术语映射
    │   ↓
    ├→ [翻译] QueryTranslator.translate_query()
    │   （如果非英文）
    │   ↓
    ├→ [意图检测] IntentDetector.detect_intent()
    │   ↓
    ├→ [分解] QueryDecomposer.decompose()
    │   （如果是复杂查询）
    │   ↓
    ├→ [扩展] QueryExpander.expand()
    │   - 同义词
    │   - 时间变体
    │   - 需求变体
    │   ↓
    ├→ [重写] QueryRewriter.rewrite()
    │   - 添加指令前缀
    │   - 扩展缩写词
    │   ↓
ProcessedQuery 对象
    ├─ original_query
    ├─ normalized_query
    ├─ expanded_queries
    ├─ rewritten_query
    ├─ detected_language
    ├─ translated_query
    ├─ detected_intent
    ├─ decomposed_queries
    └─ metadata
        ↓
    [传递给 Retrieval 模块进行检索]
```

---

## 数据类定义

### ProcessedQuery
```python
@dataclass
class ProcessedQuery:
    original_query: str              # 原始用户输入
    normalized_query: str            # 规范化后的查询
    expanded_queries: List[str]      # 扩展生成的多个变体
    rewritten_query: str             # 优化后的查询
    detected_language: str           # 检测到的语言 ("en", "zh", "mixed")
    translated_query: Optional[str]  # 翻译后的查询（如果需要）
    detected_intent: str             # 检测到的用户意图
    decomposed_queries: List[str]    # 分解后的子查询（如果是复杂查询）
    metadata: Dict[str, Any]         # 其他元数据
```

### QueryEntity
```python
@dataclass
class QueryEntity:
    entity_type: str      # "role", "action", "object", "time", "condition"
    value: str           # 实体值
    confidence: float    # 抽取置信度 (0.0-1.0)
```

### IntentInfo
```python
@dataclass
class IntentInfo:
    primary_intent: str           # 主意图类型
    secondary_intents: List[str]  # 次要意图类型列表
    intent_confidence: float      # 置信度 (0.0-1.0)
    query_type: str              # 具体查询分类
```

---

## 使用示例（待实现）

```python
from query import QueryProcessor

# 初始化处理器
processor = QueryProcessor()

# 处理用户查询
user_query = "What is the SuperStream contribution deadline?"
processed = processor.process_query(user_query)

# 使用处理结果进行检索
print(f"原始查询: {processed.original_query}")
print(f"规范化: {processed.normalized_query}")
print(f"检测意图: {processed.detected_intent}")
print(f"扩展查询: {processed.expanded_queries}")

# 传递给检索模块
for expanded_query in processed.expanded_queries:
    retrieval_results = retriever.search(expanded_query, top_k=5)
    # ... 处理检索结果
```

---

## 配置和外部资源

该框架使用以下外部资源（待集成）：

1. **术语映射文件** - `query/data/terminology_map.json`
  - 用户术语 → 官方术语映射
  - SuperStream 专业术语词典

2. **意图关键词列表** - `query/data/intent_keywords.json`
  - 各种意图类型的关键词集合
  - 用于意图识别

3. **翻译模型** - (待选择)
  - OpenAI API
  - Google Translate
  - 本地模型 (如 Helsinki-NLP)

4. **嵌入模型** - (从 config.py 读取)
  - E5-Large-V2 (推荐)
  - Multilingual-E5 (多语言)

---

## 优先级和实现计划

### Phase 1 (MVP) - 核心功能
- [ ] QueryNormalizer - 术语映射
- [ ] QueryExpander - 基础扩展
- [ ] QueryTranslator - 中英翻译
- [ ] QueryProcessor - 流程编排

### Phase 2 - 高级功能
- [ ] QueryDecomposer - 复杂查询分解
- [ ] QueryRewriter - 优化改写
- [ ] IntentDetector - 意图识别

### Phase 3 - 优化和扩展
- [ ] 性能优化
- [ ] 额外语言支持
- [ ] 反馈学习机制

---

## 备注

- 所有函数当前仅有签名，**没有实现**
- 函数名清晰反映功能，便于后续实现
- 每个模块高度独立，支持灵活组合
- 遵循单一职责原则 (SRP)
- 易于测试和维护

---

更新时间: 2025-12-21
