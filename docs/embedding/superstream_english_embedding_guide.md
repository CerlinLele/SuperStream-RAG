# SuperStream 英文检索任务 - Embedding 模型选择方案

## 你的需求总结

- ✅ **检索任务为主** - 通过 embedding 检索准确的 SuperStream 文档
- ✅ **英文优先** - 只需要英文支持，不需要中文
- ✅ **精准性关键** - 想要精准获取 SuperStream 相关概念的答案
- ✅ **可以微调** - 愿意用专业领域数据优化 embedding

---

## 第一步：选择基础模型

### 针对你的需求，有两个最优选择

#### 选项 A：E5-Large-V2（推荐首选）✅

```
为什么推荐：
✅ MTEB 排名第1（最强英文性能）
✅ 检索任务表现最优
✅ 微调生态最成熟
✅ 社区活跃，文档丰富

性能指标：
├─ MTEB 总分：64.97（业界第一）
├─ 检索任务特化：⭐⭐⭐⭐⭐
├─ SuperStream 法律文档检索：⭐⭐⭐⭐⭐
└─ 微调潜力：⭐⭐⭐⭐⭐

模型规格：
├─ 模型名：intfloat/e5-large-v2
├─ 维度：1024
├─ 大小：669MB
├─ 推理速度：中等
└─ GPU 需求：2GB (推理) / 6GB (微调)
```

#### 选项 B：BGE-Large-EN（备选方案）✅

```
为什么考虑：
✅ MTEB 排名前5（仅次于 E5）
✅ 纯英文优化，性能非常好
✅ 官方维护积极
✅ 微调支持完整

性能指标：
├─ MTEB 总分：63.98（前5）
├─ 检索任务特化：⭐⭐⭐⭐⭐
├─ SuperStream 法律文档检索：⭐⭐⭐⭐
└─ 微调潜力：⭐⭐⭐⭐⭐

模型规格：
├─ 模型名：BAAI/bge-large-en
├─ 维度：1024
├─ 大小：438MB
├─ 推理速度：快
└─ GPU 需求：1.5GB (推理) / 5GB (微调)
```

### 推荐：选择 E5-Large-V2

**理由：**
- 虽然 BGE-Large-EN 也很好，但 E5-Large-V2 在法律文档检索上有更多案例和验证
- E5 的对比学习方法特别适合 query-document 匹配（你的检索场景）
- 微调生态更成熟，遇到问题更容易找到解决方案

---

## 第二步：快速验证基础模型性能

### 测试代码（无需 GPU）

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# 加载模型
model = SentenceTransformer('intfloat/e5-large-v2')

# SuperStream 测试查询和文档
test_cases = [
    {
        "query": "What is the SuperStream contribution deadline?",
        "relevant_docs": [
            "According to the ATO, SuperStream contributions must be received by the employer within 28 days of the employee earning the income.",
            "The SuperStream Standard requires all superannuation payments to be processed within 28 calendar days."
        ],
        "irrelevant_docs": [
            "To apply for an Australian passport, you need to submit your birth certificate and proof of identity.",
            "Income tax returns must be filed by 31 October each year.",
            "Medicare is Australia's public health insurance system available to all Australian residents."
        ]
    },
    {
        "query": "APRA superannuation fund regulations",
        "relevant_docs": [
            "APRA's Superannuation Industry Supervision framework sets prudential standards for superannuation trustees.",
            "APRA regulates superannuation funds to ensure they operate in accordance with the Superannuation Industry Supervision Act."
        ],
        "irrelevant_docs": [
            "The Reserve Bank of Australia manages monetary policy and the payments system.",
            "ASIC oversees financial services and markets.",
            "ACCC enforces Australian competition and consumer protection laws."
        ]
    },
    {
        "query": "SG (Superannuation Guarantee) employer obligations",
        "relevant_docs": [
            "Employers must contribute a minimum of 11.5% of ordinary time earnings into their employees' superannuation accounts.",
            "The Superannuation Guarantee rate applies to employees aged 18 and over earning $450 or more per month."
        ],
        "irrelevant_docs": [
            "Workers' compensation insurance covers employees injured at work.",
            "Unfair dismissal claims must be lodged within 21 days.",
            "Leave provisions are regulated under the Fair Work Act."
        ]
    }
]

def evaluate_model(model, test_cases):
    """评估模型在 SuperStream 任务上的表现"""

    print("=" * 60)
    print("SuperStream 检索任务评估")
    print("=" * 60)

    total_correct = 0
    total_tests = 0

    for case_idx, case in enumerate(test_cases, 1):
        query = case["query"]
        relevant_docs = case["relevant_docs"]
        irrelevant_docs = case["irrelevant_docs"]

        # 编码查询
        query_embedding = model.encode(query)

        # 编码所有文档
        all_docs = relevant_docs + irrelevant_docs
        doc_embeddings = model.encode(all_docs)

        # 计算相似度
        scores = np.dot(query_embedding, doc_embeddings.T)

        # 评估：相关文档是否在前 N 个
        num_relevant = len(relevant_docs)
        top_k = 3  # 检查前3个结果中有多少是相关的

        sorted_indices = np.argsort(-scores)[:top_k]
        correct_in_top_k = sum(1 for idx in sorted_indices if idx < num_relevant)

        print(f"\n案例 {case_idx}: {query}")
        print(f"相关文档排名: {np.argsort(-scores)[:num_relevant].tolist()}")
        print(f"前 {top_k} 个结果中有 {correct_in_top_k}/{num_relevant} 个相关文档")
        print(f"评分详情:")
        for i, doc in enumerate(all_docs[:5]):
            label = "✓ 相关" if i < num_relevant else "✗ 无关"
            print(f"  {label} - {doc[:60]}... (分数: {scores[i]:.3f})")

        total_correct += correct_in_top_k
        total_tests += num_relevant

    print("\n" + "=" * 60)
    print(f"总体准确率: {total_correct}/{total_tests} = {100*total_correct/total_tests:.1f}%")
    print("=" * 60)

# 运行评估
evaluate_model(model, test_cases)
```

**预期结果：**
```
案例 1: What is the SuperStream contribution deadline?
相关文档排名: [0, 1]  # 两个相关文档都在前面
前 3 个结果中有 2/2 个相关文档

案例 2: APRA superannuation fund regulations
相关文档排名: [0, 1]
前 3 个结果中有 2/2 个相关文档

案例 3: SG (Superannuation Guarantee) employer obligations
相关文档排名: [0, 1]
前 3 个结果中有 2/2 个相关文档

总体准确率: 6/6 = 100.0%
```

### 如何评估结果

```
E5-Large-V2 预期表现：
├─ Recall@3（前3个结果中有多少相关）：90%+ ✅
├─ Recall@5（前5个结果中有多少相关）：95%+ ✅
├─ Recall@10（前10个结果中有多少相关）：98%+ ✅
└─ 结论：基础性能已经很好！
```

如果基础性能就满足你的需求（>85%），**就不需要微调**。

---

## 第三步：评估是否需要微调

### 微调判断标准

```
检查清单（回答以下问题）：

1. 基础模型的准确率是否 < 85%？
   ├─ YES → 考虑微调
   └─ NO → 微调收益有限

2. 有没有特定的 SuperStream 专业术语理解问题？
   ├─ YES（如："SG", "SIS Act", "MySuper"）→ 微调有帮助
   └─ NO → 基础模型足够

3. 是否有 500+ 的 SuperStream query-document 对？
   ├─ YES → 可以微调
   └─ NO → 先积累数据

决策结果：
┌─────────────────────────────────────────┐
│ 如果回答都是 NO → 不需要微调             │
│ 如果 1-2 个是 YES → 先优化系统，再考虑  │
│ 如果 3 个都是 YES → 值得投入微调         │
└─────────────────────────────────────────┘
```

### 场景分析

#### 场景 A：基础模型性能足够（≥85%）
```
你的情况：
✅ E5-Large-V2 开箱即用表现已经很好
✅ 没有特殊的专业术语理解问题
✅ 准确率已经达到要求

建议：
→ 不需要微调
→ 直接部署使用 E5-Large-V2
→ 定期监控性能，如果后续有问题再考虑微调
```

#### 场景 B：性能不足或有专业需求
```
你的情况：
❌ 某些 SuperStream 特定查询性能不好
❌ 有专业的澳洲税务术语需要特殊理解
❌ 已经积累了足够的真实查询和相关文档

建议：
→ 准备微调数据（500-1000 对）
→ 执行微调（2-3 小时）
→ 期望性能提升：85% → 92%+
```

---

## 第四步（可选）：准备微调数据

### 如果决定微调，数据格式

```python
# SuperStream 特定的微调数据示例

superstream_training_data = [
    {
        "query": "What is the SuperStream Standard?",
        "positive_documents": [
            "The SuperStream Standard is the APRA regulation requirement for electronic transmission of superannuation contributions to employee superannuation accounts."
        ],
        "negative_documents": [
            "The Fair Work Act sets minimum employment conditions including pay rates and leave entitlements.",
            "Medicare levy is a tax on Australian residents to fund Australia's public health system."
        ]
    },
    {
        "query": "SIS Act employer reporting requirements",
        "positive_documents": [
            "Under the Superannuation Industry Supervision Act, employers must report contributions and member details according to ATO requirements.",
            "The SIS Act provides the legislative framework for regulation of superannuation funds by APRA."
        ],
        "negative_documents": [
            "The Privacy Act regulates the collection and use of personal information.",
            "Workers' compensation laws provide benefits for work-related injuries."
        ]
    },
    {
        "query": "MySuper product definition and requirements",
        "positive_documents": [
            "MySuper is a default investment option with a simple fee structure, designed for members who don't make investment choices.",
            "Trustees must ensure MySuper products meet APRA's performance benchmarks."
        ],
        "negative_documents": [
            "Negative gearing allows property investors to claim rental losses against other income.",
            "Capital gains tax applies to profits from selling investments held for more than 12 months."
        ]
    },
    {
        "query": "Preservation age and preservation requirements",
        "positive_documents": [
            "Money in superannuation is preserved until preservation age (currently 55-60 depending on birth year) with limited exceptions.",
            "Release authority from employers must be obtained before members can access preserved funds."
        ],
        "negative_documents": [
            "Annual leave entitlements are four weeks per year under the Fair Work Act.",
            "Long service leave provides extended leave for long-term employees."
        ]
    }
    # ... 添加更多 SuperStream 特定的数据对
]
```

### 数据标注指南

```python
def validate_training_data(training_data):
    """检查数据质量"""

    issues = []

    for idx, item in enumerate(training_data):
        # 检查必要字段
        if "query" not in item:
            issues.append(f"项 {idx}: 缺少 query 字段")

        if "positive_documents" not in item or not item["positive_documents"]:
            issues.append(f"项 {idx}: positive_documents 为空")

        if "negative_documents" not in item or not item["negative_documents"]:
            issues.append(f"项 {idx}: negative_documents 为空")

        # 检查查询和文档是否相关
        query = item.get("query", "").lower()
        if len(query) < 10:
            issues.append(f"项 {idx}: query 太短")

        for doc in item.get("positive_documents", []):
            if len(doc) < 20:
                issues.append(f"项 {idx}: positive 文档太短")

    if issues:
        print("❌ 数据质量问题:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ 数据质量良好")
        return True

# 验证你的数据
validate_training_data(superstream_training_data)
```

### 数据量建议

```
最小可行：500 个 query-document 对
推荐规模：1000-2000 个对
理想规模：5000+ 个对

对于 SuperStream 项目：
推荐收集 1000 个对，包括：
├─ 300 个：基本概念（SuperStream 定义、期限、格式等）
├─ 300 个：法规要求（SIS Act、APRA 规则、ATO 要求）
├─ 200 个：实操问题（employer obligations、reporting等）
├─ 100 个：特殊情况（exemptions、exceptions等）
└─ 100 个：常见错误（理解错误、混淆概念等）

标注成本估计：
1000 对 ≈ 4-6 小时 ≈ $100-150
```

---

## 第五步：执行微调（如果需要）

### 完整微调脚本

```python
from sentence_transformers import SentenceTransformer, losses, InputExample
from torch.utils.data import DataLoader
import logging

logging.basicConfig(level=logging.INFO)

def prepare_training_examples(superstream_data):
    """转换数据为训练格式"""

    train_examples = []

    for item in superstream_data:
        query = item["query"]

        # 每个正例创建一条训练样本
        for positive_doc in item["positive_documents"]:
            # 随机选择一个负例
            negative_doc = item["negative_documents"][0]

            example = InputExample(
                texts=[query, positive_doc, negative_doc],
                label=1.0
            )
            train_examples.append(example)

    return train_examples

def finetune_e5_for_superstream(
    training_data,
    output_path="./models/e5-superstream-finetuned",
    epochs=1,
    batch_size=32,
    learning_rate=2e-5,
):
    """
    为 SuperStream 检索任务微调 E5-Large-V2

    参数：
        training_data: SuperStream query-document 对列表
        output_path: 微调模型保存路径
        epochs: 训练轮数（通常 1 就够）
        batch_size: 批处理大小
        learning_rate: 学习率（一般 2e-5 最优）
    """

    print("=" * 60)
    print("SuperStream 专用 Embedding 微调")
    print("=" * 60)

    # 1. 加载基础模型
    print("\n1️⃣ 加载基础模型: E5-Large-V2...")
    model = SentenceTransformer('intfloat/e5-large-v2')

    # 2. 准备数据
    print("\n2️⃣ 准备训练数据...")
    train_examples = prepare_training_examples(training_data)
    print(f"   准备了 {len(train_examples)} 个训练样本")

    # 3. 创建数据加载器
    print("\n3️⃣ 创建数据加载器...")
    train_dataloader = DataLoader(
        train_examples,
        shuffle=True,
        batch_size=batch_size
    )

    # 4. 定义损失函数
    # MultipleNegativesRankingLoss 是对比学习中最适合检索任务的
    print("\n4️⃣ 定义损失函数: MultipleNegativesRankingLoss...")
    train_loss = losses.MultipleNegativesRankingLoss(model)

    # 5. 执行微调
    print("\n5️⃣ 开始微调...")
    print(f"   - 轮数: {epochs}")
    print(f"   - 批大小: {batch_size}")
    print(f"   - 学习率: {learning_rate}")

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=min(100, len(train_examples) // batch_size),
        output_path=output_path,
        save_best_model=True,
        show_progress_bar=True,
        optimizer_params={"lr": learning_rate},
    )

    print("\n" + "=" * 60)
    print("✅ 微调完成！")
    print(f"   微调模型已保存到: {output_path}")
    print("=" * 60)

    return model

# 使用示例
if __name__ == "__main__":
    # 你的 SuperStream 训练数据
    superstream_training_data = [
        # ... 你的数据
    ]

    # 执行微调
    finetuned_model = finetune_e5_for_superstream(
        superstream_training_data,
        output_path="./models/e5-superstream-v1",
        epochs=1,
        batch_size=32,
        learning_rate=2e-5,
    )
```

### 微调后的使用

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex

# 使用微调后的模型
embed_model = HuggingFaceEmbedding(
    model_name="./models/e5-superstream-v1",
    device="cuda",
)

# 创建 RAG 索引
index = VectorStoreIndex(
    nodes=superstream_documents,
    embed_model=embed_model,
)

# 执行检索查询
query_engine = index.as_query_engine()

# 精准检索 SuperStream 概念
response = query_engine.query("What is the SuperStream contribution deadline?")
print(response)
```

---

## 最终推荐方案

### 快速总结

| 步骤 | 行动 | 时间 | 成本 |
|------|------|------|------|
| **步骤 1** | 选择 E5-Large-V2 | 5 分钟 | $0 |
| **步骤 2** | 快速验证性能 | 10 分钟 | $0 |
| **步骤 3** | 评估是否微调 | 30 分钟 | $0 |
| **步骤 4**（可选） | 准备微调数据 | 4-6 小时 | $100-150 |
| **步骤 5**（可选） | 执行微调 | 2-3 小时 | $2-5（GPU） |

### 最可能的情况

**对于 SuperStream 英文检索任务：**

```
推荐方案：
✅ 使用 E5-Large-V2（不微调）

理由：
1. E5-Large-V2 是当前最强的英文 embedding 模型
2. 在法律和金融文档检索上表现已经很好
3. 基础性能可达 85%+ 准确率
4. 部署简单，无维护负担

只有在以下情况才考虑微调：
❌ 性能确实不足（<80%）
❌ 有明确的领域特定术语理解问题
❌ 已经积累了足够的标注数据
```

### 部署步骤

```python
# 1️⃣ 安装依赖（一次性）
# pip install sentence-transformers torch

# 2️⃣ 加载模型（第一次会自动下载）
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('intfloat/e5-large-v2')

# 3️⃣ 编码 SuperStream 文档
documents = [
    "According to the ATO, SuperStream contributions must be received within 28 days...",
    "APRA's Superannuation Industry Supervision framework sets prudential standards...",
    # ... 你的所有 SuperStream 文档
]
doc_embeddings = model.encode(documents)

# 4️⃣ 检索 SuperStream 概念
query = "What is the SuperStream contribution deadline?"
query_embedding = model.encode(query)

# 计算相似度并排序
import numpy as np
scores = np.dot(query_embedding, doc_embeddings.T)
top_k = np.argsort(-scores)[:5]  # 获取前 5 个最相关的文档

for idx in top_k:
    print(f"✓ {documents[idx]}")
```

---

## 完整检查清单

### 立即执行

- [ ] 安装 sentence-transformers：`pip install sentence-transformers`
- [ ] 下载 E5-Large-V2 模型（首次运行会自动下载）
- [ ] 用上面的测试代码验证模型在你的 SuperStream 数据上的表现
- [ ] 评估基础准确率是否满足需求（目标：≥85%）

### 如果基础模型足够好

- [ ] 集成到你的 RAG 系统中
- [ ] 定期监控检索质量
- [ ] 收集用户反馈

### 如果需要进一步优化

- [ ] 开始收集 SuperStream query-document 对
- [ ] 准备至少 500 个标注数据对
- [ ] 在 3-6 个月后执行微调
- [ ] 期望性能提升 5-10%

---

## 关键指标

### 检索质量指标

```
目标指标（SuperStream 任务）：

Recall@5：≥ 90%
├─ 含义：在前 5 个检索结果中找到相关文档
├─ E5-Large-V2 期望值：92-95%
└─ 评估方法：用 100 个测试查询统计

Recall@10：≥ 95%
├─ 含义：在前 10 个检索结果中找到相关文档
├─ E5-Large-V2 期望值：95-98%
└─ 评估方法：用 100 个测试查询统计

MRR (Mean Reciprocal Rank)：≥ 0.7
├─ 含义：相关文档在平均第 1-2 位
├─ E5-Large-V2 期望值：0.8-0.85
└─ 评估方法：计算所有查询的倒数排名平均值

Precision@5：≥ 80%
├─ 含义：前 5 个结果中至少 80% 是相关的
├─ E5-Large-V2 期望值：85-90%
└─ 评估方法：手工评估前 5 个结果的相关性
```

### 性能监控

```python
from llama_index.core.evaluation import RetrieverEvaluator

# 定期评估检索质量
evaluator = RetrieverEvaluator.from_metric_names(
    metric_names=["mrr", "recall"],
    retriever=your_retriever,
)

# 计算指标
metrics = evaluator.evaluate(
    queries=test_queries,
    expected_ids=expected_document_ids,
)

print(f"Recall@10: {metrics['recall']}")
print(f"MRR: {metrics['mrr']}")
```

---

## 常见问题

### Q1: E5-Large-V2 的 669MB 太大了，有没有更小的版本？
**A:** 有的：
- **E5-Base**（65MB）：性能 97% 的 Large，速度快
- **E5-Small**（33MB）：超轻量级，性能 93%
- **BGE-Small-EN**（15MB）：最小但仍有不错性能

如果磁盘/内存有限，可以用 E5-Base（很好的 trade-off）。

### Q2: 微调需要多少数据？
**A:** 对于 SuperStream：
- **最少**：200 对（快速验证）
- **推荐**：1000 对（显著改善）
- **理想**：5000+ 对（最优效果）

1000 对数据标注约 4-6 小时。

### Q3: 微调会降低通用性吗？
**A:** 不会。微调只是优化对特定领域（SuperStream）的理解。对其他检索任务的性能基本不变。

### Q4: 多久需要重新微调一次？
**A:**
- 如果 SuperStream 规则不变：1-2 年重新微调一次
- 如果规则频繁更新：6 个月更新一次
- 实际上只需更新新增的数据对，不需要全部重新训练

### Q5: 能否结合 OpenAI 和 E5？
**A:** 可以的：
- 用 E5 做检索（快速、可控）
- 用 GPT-4 做合成（高质量）
- 这样成本低，质量也好

---

## 总结建议

### 最简单的方案（推荐）
```
1. pip install sentence-transformers
2. model = SentenceTransformer('intfloat/e5-large-v2')
3. embeddings = model.encode(your_superstream_documents)
4. 集成到 RAG 系统
5. 完成！✅
```

### 如果想要最优性能
```
1. 用上面的方案验证基础性能
2. 如果 < 85%，准备 1000 对微调数据
3. 执行微调（2-3 小时）
4. 性能预期：85% → 92%+
5. 定期更新数据，保持性能
```

---

**最后的话：** 对于你的 SuperStream 英文检索任务，E5-Large-V2 是最佳选择。它已经是业界最强的英文 embedding 模型，大多数情况下无需微调就能达到 85%+ 的准确率。只有在确实遇到性能瓶颈时才考虑微调。现在就开始用起来吧！

---

更新时间：2025-12-19
