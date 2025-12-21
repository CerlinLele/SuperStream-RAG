# Query 框架 - 快速参考

## 文件清单

```
query/
├── __init__.py                  (495 bytes)  - 模块导出
├── processor.py                 (1.7 KB)    - 主处理器
├── normalizer.py                (1.6 KB)    - 规范化
├── expander.py                  (2.0 KB)    - 扩展
├── rewriter.py                  (2.2 KB)    - 重写
├── translator.py                (2.2 KB)    - 翻译
├── decomposer.py                (2.9 KB)    - 分解
├── intent_detector.py           (3.6 KB)    - 意图检测
└── README.md                   (11.0 KB)    - 完整文档
```

**总计：8个模块 + 1个文档 = 9个文件**

---

## 核心类和函数一览

### 1. QueryProcessor (处理器)
```python
processor = QueryProcessor()
result = processor.process_query("user query")
# 返回: ProcessedQuery 对象
```

### 2. QueryNormalizer (规范化)
```python
normalizer = QueryNormalizer()
result = normalizer.normalize("query text")
# 功能: 术语映射、大小写统一、空白符清理
```

### 3. QueryExpander (扩展)
```python
expander = QueryExpander()
variants = expander.expand("query")
# 返回: List[str] - 多个查询变体
```

### 4. QueryRewriter (重写)
```python
rewriter = QueryRewriter()
optimized = rewriter.rewrite("query")
# 功能: 添加指令前缀、展开缩写、提取关键词
```

### 5. QueryTranslator (翻译)
```python
translator = QueryTranslator()
translated = translator.translate_chinese_to_english("中文查询")
# 功能: 中英互译、语言检测、术语保留
```

### 6. QueryDecomposer (分解)
```python
decomposer = QueryDecomposer()
result = decomposer.decompose("complex query")
# 返回: DecomposedQuery - 包含实体和子查询
```

### 7. IntentDetector (意图检测)
```python
detector = IntentDetector()
intent = detector.detect_intent("query")
# 返回: IntentInfo - 意图类型和策略建议
```

---

## 数据类结构

### ProcessedQuery
完整的查询处理结果：
- `original_query` - 原始输入
- `normalized_query` - 规范化结果
- `expanded_queries` - 扩展变体
- `rewritten_query` - 优化版本
- `detected_language` - 语言检测
- `translated_query` - 翻译结果
- `detected_intent` - 用户意图
- `decomposed_queries` - 子查询列表
- `metadata` - 其他信息

### QueryEntity
实体抽取结果：
- `entity_type` - 实体类型 (role/action/object/time/condition)
- `value` - 实体值
- `confidence` - 置信度 (0.0-1.0)

### IntentInfo
意图检测结果：
- `primary_intent` - 主意图
- `secondary_intents` - 次要意图列表
- `intent_confidence` - 置信度
- `query_type` - 查询分类

---

## 意图类型速查表

| 意图类型 | 特征关键词 | 检索策略 |
|---------|----------|--------|
| **definition** | "What is", "Define", "Explain" | 找定义、概念解释 |
| **requirement** | "Must", "Should", "Required", "Obligation" | 找规则和要求 |
| **process** | "How to", "Steps", "Procedure", "Process" | 找步骤和流程 |
| **penalty** | "What if", "Consequence", "Penalty", "Fine" | 找后果和罚款 |
| **exception** | "Exception", "Except", "Unless", "Special case" | 找例外情况 |
| **comparison** | "vs", "Difference", "Compare", "vs" | 找对比信息 |

---

## 处理流程示例

```
用户: "What is the SuperStream deadline?"
    ↓
detect_language() → "en"
normalize() → "What is the SuperStream deadline?"
translate() → (skip, 已是英文)
detect_intent() → "definition" (置信度 0.95)
decompose() → (skip, 不是复杂查询)
expand() → [
    "What is the SuperStream deadline?",
    "When must SuperStream be paid?",
    "SuperStream contribution deadline",
    "ATO SuperStream requirement"
]
rewrite() → "Represent this legal query: SuperStream deadline contribution payment requirement ATO"
    ↓
ProcessedQuery 对象
    ↓
传递给 Retrieval 模块进行向量检索
```

---

## 当前状态

✅ **框架搭建完成**
- 所有7个核心模块已创建
- 所有关键函数已定义
- 完整文档已编写

⏳ **待实现**
- 各模块的具体实现逻辑
- 外部依赖集成 (翻译API、意图识别模型等)
- 单元测试
- 集成测试

---

## 开发指南

### 添加新的规范化规则
编辑 `normalizer.py`，在 `build_terminology_map()` 中添加新的术语对应关系

### 添加新的查询扩展策略
编辑 `expander.py`，实现新的 `add_*_variations()` 方法

### 添加新的意图类型
编辑 `intent_detector.py`，添加 `is_*_query()` 方法和关键词

### 集成翻译服务
编辑 `translator.py`，实现具体的翻译调用逻辑

---

## 集成点

该框架与以下模块协同工作：

```
用户查询输入
    ↓
[Query 框架] ← 你在这里
    ↓
改写后的查询 + 元数据
    ↓
[Retrieval 模块] (待实现)
    ├─ 向量检索 (E5-Large-V2)
    ├─ BM25 混合检索
    └─ 重排
        ↓
    检索结果
        ↓
[Generation 模块] (待实现)
    └─ LLM 生成回复
```

---

## 测试建议

### Unit 测试位置
建议创建: `tests/query/` 目录

```python
# tests/query/test_normalizer.py
def test_terminology_mapping():
    normalizer = QueryNormalizer()
    result = normalizer.map_terminology("超级年金")
    assert "Superannuation" in result or "SuperStream" in result

# tests/query/test_intent_detector.py
def test_definition_query():
    detector = IntentDetector()
    is_def, confidence = detector.is_definition_query("What is SuperStream?")
    assert is_def is True
    assert confidence > 0.8
```

---

生成时间: 2025-12-21
框架版本: v1.0 (MVP)
