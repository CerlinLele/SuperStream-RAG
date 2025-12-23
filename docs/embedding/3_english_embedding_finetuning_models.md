# 英文 Embedding 模型微调方案

## 快速答案

**✅ 有很多英文 embedding 模型支持微调！**

推荐的英文微调模型（按推荐度排序）：

| 模型 | 维度 | 性能 | 微调 | 推荐度 |
|------|------|------|------|--------|
| **E5-Large-V2** | 1024 | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| **BGE-Large-EN** | 1024 | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| **EmbeddingGemma** | 768 | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| **Mistral Embed** | 1024 | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| **ONNX/Sentence-Transformers** | 可选 | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |

---

## 英文模型详解

### 1. E5 系列（推荐首选）✅

**模型：`intfloat/e5-large-v2`**

#### 特点
- **性能最强** - MTEB 排名第1
- **微调友好** - 使用对比学习，易于微调
- **中英混合** - 对中英文都支持（特别适合 SuperStream）
- **活跃社区** - 大量微调示例和工具
- **商业友好** - MIT 开源许可

#### 性能指标
```
MTEB Score: 64.97 (英文排名第1)
中文性能: 也很好
维度: 1024
大小: 669MB
```

#### 微调代码示例

```python
from sentence_transformers import SentenceTransformer, losses, models, InputExample
from torch.utils.data import DataLoader

# 加载 E5 模型
model = SentenceTransformer('intfloat/e5-large-v2')

# 准备训练数据（SuperStream 示例）
train_examples = [
    InputExample(
        texts=[
            "What is the SuperStream contribution deadline?",  # query
            "According to ATO, SuperStream contributions must be made within 28 days...",  # positive
            "How to apply for a mortgage in Australia..."  # negative
        ],
        label=1.0
    ),
    InputExample(
        texts=[
            "APRA superannuation regulations",
            "APRA provides guidance on superannuation fund regulation and compliance...",
            "Tax deductions for medical expenses..."
        ],
        label=1.0
    ),
    # ... 更多数据
]

# 创建数据加载器
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=32)

# 定义损失函数
train_loss = losses.MultipleNegativesRankingLoss(model)

# 执行微调
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1,
    warmup_steps=100,
    output_path="models/e5-superstream-en",
    show_progress_bar=True,
)

# 验证微调效果
test_query = "What is the SuperStream contribution deadline?"
test_embedding = model.encode(test_query)
print(f"Embedding shape: {test_embedding.shape}")  # (1024,)
```

#### 在 LlamaIndex 中使用

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 使用微调后的模型
embed_model = HuggingFaceEmbedding(
    model_name="models/e5-superstream-en",
    device="cuda",
)

# 创建索引
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex(
    nodes=documents,
    embed_model=embed_model,
)

# 使用
query_engine = index.as_query_engine()
response = query_engine.query("What is the SuperStream contribution deadline?")
```

### 2. BGE-Large-EN（备选方案）✅

**模型：`BAAI/bge-large-en`**

#### 特点
- **英文优化** - 专为英文优化
- **性能强** - MTEB 排名前5
- **多型号选择** - small / base / large / xl
- **对比学习** - 标准的对比学习框架
- **活跃维护** - BAAI（北京人工智能研究院）维护

#### 性能指标
```
MTEB Score: 63.98 (英文排名前5)
维度: 1024
大小: 438MB
```

#### 微调代码

```python
from sentence_transformers import SentenceTransformer, losses
from torch.utils.data import DataLoader

model = SentenceTransformer('BAAI/bge-large-en')

# 微调（与 E5 类似）
train_loss = losses.MultipleNegativesRankingLoss(model)

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1,
    warmup_steps=100,
    output_path="models/bge-superstream-en",
)
```

### 3. EmbeddingGemma（Google 新品）✅

**模型：`google/embedding-gemma-en-large`**

#### 特点
- **Google 出品** - 最新最先进
- **轻量高效** - 比 E5 更小但性能接近
- **参数高效微调** - 支持 LoRA 和 Adapter
- **易于微调** - 官方文档详细

#### 性能指标
```
MTEB Score: 62.5 (新品，持续改进)
维度: 768
大小: 200MB（比 E5 小）
```

#### 微调代码（LoRA 参数高效）

```python
from sentence_transformers import SentenceTransformer, losses
from peft import LoraConfig, get_peft_model

# 加载基础模型
model = SentenceTransformer('google/embedding-gemma-en-large')

# 使用 LoRA 参数高效微调（推荐！）
# LoRA 只需更新 10% 的参数，节省显存和时间
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM",
)

model.model = get_peft_model(model.model, peft_config)

# 微调
train_loss = losses.MultipleNegativesRankingLoss(model)

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1,
    warmup_steps=100,
    output_path="models/gemma-superstream-en",
)
```

### 4. Mistral Embed（备选）✅

**模型：`mistral-embed`**

#### 特点
- **Mistral AI 出品** - 新兴强劲团队
- **高效快速** - 推理速度快
- **现代架构** - 基于最新 Transformer

#### 局限
- 闭源提供（通过 API），但有开源替代

---

## 中英混合场景（SuperStream 最佳选择）

如果你的项目既需要英文支持，又要保留中文能力，有两个策略：

### 策略 1：使用支持中英混合的模型

**推荐：E5-Mistral 或 M3E-Large**

```python
# E5-Mistral（中英混合最优）
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('intfloat/e5-mistral-7b-instruct')

# 同时支持中英
en_query = "What is the SuperStream deadline?"
zh_query = "超级年金报送截止日期是什么？"

en_embedding = model.encode(en_query)
zh_embedding = model.encode(zh_query)

# 计算相似度（会很高）
import numpy as np
similarity = np.dot(en_embedding, zh_embedding) / (
    np.linalg.norm(en_embedding) * np.linalg.norm(zh_embedding)
)
print(f"Cross-lingual similarity: {similarity:.4f}")
```

### 策略 2：使用纯英文模型，但优化查询处理

```python
from sentence_transformers import SentenceTransformer
from googletrans import Translator  # 或用 LLM 翻译

model = SentenceTransformer('intfloat/e5-large-v2')
translator = Translator()

def search_superstream(query, documents):
    """支持中英混合查询"""

    # 如果是中文，翻译为英文
    if contains_chinese(query):
        query = translator.translate(query, src_language='zh-CN', dest_language='en')['text']

    # 用英文模型编码
    query_embedding = model.encode(query)

    # 进行检索
    return retrieve(query_embedding, documents)
```

---

## 微调数据准备指南

### 数据格式

对于 SuperStream RAG，你需要准备：

```python
training_pairs = [
    {
        "query": "What is the SuperStream contribution deadline?",
        "positive_passages": [
            "According to the ATO, SuperStream contributions must be received within 28 days...",
            "The ATO requires employers to process SuperStream payments..."
        ],
        "negative_passages": [
            "How to apply for Australian citizenship",
            "Tax deductions for home office expenses"
        ]
    },
    {
        "query": "APRA superannuation fund regulations",
        "positive_passages": [
            "APRA provides guidance on superannuation regulation...",
            "Superannuation fund compliance requirements..."
        ],
        "negative_passages": [
            "Stock market investment strategies",
            "Real estate property valuation"
        ]
    },
    # ... 更多数据
]

# 转换为 InputExample 格式
from sentence_transformers import InputExample

train_examples = []
for pair in training_pairs:
    for positive in pair["positive_passages"]:
        train_examples.append(InputExample(
            texts=[pair["query"], positive],
            label=1.0
        ))
    for negative in pair["negative_passages"]:
        train_examples.append(InputExample(
            texts=[pair["query"], negative],
            label=0.0
        ))
```

### 数据量建议

```
最少：500 个 query-document 对
推荐：1000-5000 个对
理想：10000+ 个对

成本估计：
- 500 对：2-4 小时标注，$50-100
- 1000 对：4-8 小时标注，$100-200
- 5000 对：1-2 周标注，$500-1000
```

---

## 性能对比

### 微调前后的改进

```
假设：SuperStream 文档检索任务

E5-Large-V2：
未微调：Recall@10 = 82%
微调后：Recall@10 = 91%
提升：+9%

BGE-Large-EN：
未微调：Recall@10 = 80%
微调后：Recall@10 = 90%
提升：+10%

EmbeddingGemma：
未微调：Recall@10 = 78%
微调后：Recall@10 = 88%
提升：+10%
```

---

## 完整实施方案（E5 + SuperStream）

```python
# 1. 安装依赖
# pip install sentence-transformers torch

from sentence_transformers import SentenceTransformer, losses, InputExample
from torch.utils.data import DataLoader
import torch

def finetune_e5_for_superstream():
    """为 SuperStream 微调 E5 模型"""

    # 加载预训练模型
    model = SentenceTransformer('intfloat/e5-large-v2')

    # 准备训练数据（你的 SuperStream 数据）
    train_examples = [
        InputExample(
            texts=[
                "What is the SuperStream contribution deadline?",
                "According to ATO SuperStream Employer Guide, contributions must be paid within 28 days of the employee earning the income.",
                "How to get a driver's license in Australia"
            ],
            label=1.0
        ),
        # ... 更多示例
    ]

    # 配置训练参数
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    train_loss = losses.MultipleNegativesRankingLoss(model)

    # 执行微调
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        warmup_steps=100,
        output_path="models/e5-superstream-finetuned",
        save_best_model=True,
        show_progress_bar=True,
        optimizer_params={"lr": 2e-5},  # 学习率
    )

    # 保存模型
    model.save("models/e5-superstream-final")
    print("✅ 微调完成！")

# 2. 在 LlamaIndex 中使用
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex

def setup_superstream_rag():
    """设置 SuperStream RAG 系统"""

    # 使用微调模型
    embed_model = HuggingFaceEmbedding(
        model_name="models/e5-superstream-final",
        device="cuda",
    )

    # 创建索引
    from llama_index.vector_stores.chroma import ChromaVectorStore
    import chromadb

    chroma_client = chromadb.PersistentClient(path="./chroma_data")
    collection = chroma_client.get_or_create_collection(
        name="superstream-docs",
        metadata={"hnsw:space": "cosine"}
    )

    vector_store = ChromaVectorStore(chroma_collection=collection)

    from llama_index.core import StorageContext
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    index = VectorStoreIndex(
        nodes=[],
        storage_context=storage_context,
        embed_model=embed_model,
    )

    # 创建查询引擎
    query_engine = index.as_query_engine()

    # 查询
    response = query_engine.query(
        "What is the SuperStream contribution deadline?"
    )

    print(response)

if __name__ == "__main__":
    # 第一次运行：微调模型
    # finetune_e5_for_superstream()

    # 之后运行：使用微调模型
    setup_superstream_rag()
```

---

## 推荐方案总结

### 对于 SuperStream 项目：最佳方案

**第一阶段（快速验证）：**
```
使用：E5-Large-V2（未微调）
成本：$0（开源）+ 部署成本
准确率：82%（足够初期使用）
时间：立即可用
```

**第二阶段（性能优化，6个月后）：**
```
如果需要微调：
使用：E5-Large-V2（微调版本）
数据：1000-5000 SuperStream query-doc 对
微调时间：2-3 天（GPU）
预期准确率：91%+
维护：定期更新微调数据
```

**第三阶段（大规模部署）：**
```
可选选择：
- EmbeddingGemma（更轻量，LoRA 参数高效微调）
- 自部署 GPU 计算资源
- 完全本地化，隐私和性能都优化
```

---

## 快速对比表

| 维度 | OpenAI text-embedding-3 | E5-Large-V2 | BGE-Large-EN | EmbeddingGemma |
|------|---|---|---|---|
| **支持微调** | ❌ | ✅ | ✅ | ✅ |
| **英文性能** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **中文性能** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **开箱即用** | ✅ | ✅ | ✅ | ✅ |
| **微调难度** | N/A | 简单 | 简单 | 简单 |
| **模型大小** | API | 669MB | 438MB | 200MB |
| **推理速度** | API | 中等 | 中等 | 快 |
| **成本** | $2/月 | 自部署 | 自部署 | 自部署 |

---

## 常见问题

### Q: E5-Large 和 BGE-Large-EN 哪个更好？
**A:** 对于英文任务，都很好。选择建议：
- E5：更强的中英混合能力（如果需要）
- BGE-EN：纯英文优化，稍快一点

### Q: 微调一定比预训练好吗？
**A:** 不一定。只有在：
- 你有充足的领域数据（>500 对）
- 预训练模型在你的任务上性能不足（<80%）
- 微调数据与你的实际应用高度相关

才值得微调。否则优化其他方面（混合搜索、重排）更划算。

### Q: GPU 要求是什么？
**A:**
```
微调需求：
- 最少：GPU 显存 6GB（如 RTX 3060）
- 推荐：GPU 显存 12GB+（如 RTX 3060 Ti）
- 理想：24GB+（如 A100）

推理需求：
- 最少：2GB
- 推荐：4GB
```

### Q: 能在 CPU 上微调吗？
**A:** 可以，但很慢。建议至少用 GPU。云服务选项：
- Lambda Labs：$0.25/小时（V100）
- Vast.ai：$0.1-0.3/小时（各种 GPU）
- AWS SageMaker：按需计费

### Q: 微调多久才能看到效果？
**A:**
```
数据量 | 微调时间 | 成本 |
500对 | 1-2小时 | <$1
1000对 | 2-4小时 | $1-2
5000对 | 1天 | $5-10
```

---

## 总结

**有很多英文 embedding 模型支持微调！**

最推荐：**E5-Large-V2**
- 性能最强（MTEB 第1）
- 中英混合也不错
- 微调生态最成熟
- 社区最活跃

次选：**BGE-Large-EN**
- 纯英文性能也很强
- 官方维护好

新选：**EmbeddingGemma**
- Google 最新产品
- 轻量级（200MB）
- 参数高效微调（LoRA）

**建议路径：**
1. 先用 E5-Large-V2（未微调）快速验证
2. 如果需要，6个月后用真实数据微调
3. 预期提升：82% → 91%+

---

**更新时间：** 2025-12-19
