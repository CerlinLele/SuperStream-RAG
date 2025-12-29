# Vector Database 快速参考卡

## 🚀 一分钟快速选择

### 我应该用什么?

**问题 1: 现在还是未来?**
- 现在用: **FAISS** ✅
- 未来升级: 见下表

**问题 2: 用户/规模多大?**
```
< 100 用户       → FAISS
100-1000 用户    → FAISS 容器 / Chroma
1000+ 用户       → Pinecone / Qdrant
```

**问题 3: 预算是多少?**
```
$0        → FAISS
$50-100   → Chroma 自建
$100-300  → Pinecone 或 Qdrant
$300+     → 任意选择
```

---

## 📊 功能速查表

| 需求 | 解决方案 |
|------|--------|
| **我想快速部署** | Pinecone |
| **我想要最便宜** | FAISS |
| **我想要灵活性** | Chroma / Qdrant 自建 |
| **我想要高性能** | Pinecone / Milvus |
| **我想要完全控制** | Milvus / Weaviate 自建 |
| **我想要无运维** | Pinecone / Weaviate Cloud |

---

## ⏱️ 迁移成本速查

### FAISS → X 的工作量

| 目标 | 学习 | 编码 | 测试 | 总计 |
|------|------|------|------|------|
| Chroma | 2h | 3h | 2h | 7h |
| Qdrant | 3h | 4h | 2h | 9h |
| Pinecone | 2h | 2h | 1h | 5h |
| Milvus | 4h | 6h | 3h | 13h |

**结论**: Pinecone 迁移最快！

---

## 💰 价格速查表

### 你应该支付多少?

```
数据量   推荐方案        月费范围      何时买
─────────────────────────────────────────────────
<1GB     FAISS           $0           免费
1-10GB   Chroma/Qdrant   $50-100      自建
10-100GB Pinecone        $100-300     云托管
>100GB   Milvus          $300+        企业级
```

---

## 🎯 决策树 (超简化版)

```
        START
          │
          ↓
    "有钱吗?" ─── Yes ──→ Pinecone (最简单)
          │
         No
          ↓
    "想自建吗?" ─── Yes ──→ Chroma 或 Qdrant
          │
         No
          ↓
    FAISS (现在就用)
```

---

## 📝 记忆法

### FAQWM 对比法

| 字母 | 含义 | FAISS | Chroma | Pinecone | Weaviate | Milvus | Qdrant |
|------|------|-------|--------|----------|----------|--------|--------|
| **F** | Fast (速度) | ⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡ | ⚡⚡⚡ |
| **A** | Awesome (功能) | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Q** | Quiet (运维) | ⚠️ | ✅ | ✅✅ | ✅ | ⚠️ | ✅ |
| **W** | Wallet (成本) | $0 | $50 | $100 | $100 | $300 | $75 |
| **M** | Maturity (成熟度) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎬 快速开始代码片段

### FAISS (现在)

```python
from llama_index.vector_stores.faiss import FaissVectorStore
from ingest import PDFLoader, IndexBuilder

# 1. 加载文档
documents = PDFLoader().load_documents()

# 2. 构建索引
builder = IndexBuilder()
index = builder.build_index(documents)

# 3. 查询
from retrieval import SuperStreamQueryEngine
engine = SuperStreamQueryEngine()
response = engine.query("What is APRA?")
```

### Chroma (下一步)

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# 1. 创建 Chroma 向量存储
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection("superstream")
vector_store = ChromaVectorStore(chroma_collection=collection)

# 2. 构建索引
from ingest import PDFLoader
documents = PDFLoader().load_documents()
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)

# 3. 查询
query_engine = index.as_query_engine()
response = query_engine.query("What is APRA?")
```

### Pinecone (最简单)

```python
import pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore

# 1. 初始化 Pinecone
pinecone.init(api_key="your-key", environment="gcp-starter")
index = pinecone.Index("superstream")

# 2. 创建向量存储
vector_store = PineconeVectorStore(pinecone_index=index)

# 3. 构建索引
from ingest import PDFLoader
documents = PDFLoader().load_documents()
from llama_index.core import VectorStoreIndex
vector_index = VectorStoreIndex.from_documents(
    documents,
    vector_store=vector_store
)

# 4. 查询
query_engine = vector_index.as_query_engine()
response = query_engine.query("What is APRA?")
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: FAISS 无法扩展

**问题**: 单机承载不了 1M+ 向量
**解决**: 迁移到 Pinecone / Chroma

### 陷阱 2: 无法同时更新索引和查询

**问题**: FAISS 索引更新需要重建
**解决**: 使用支持实时更新的数据库 (Chroma, Pinecone, Qdrant)

### 陷阱 3: Pinecone 成本爆表

**问题**: 向量数过多，费用超预期
**解决**: 使用向量量化、删除冗余数据、或切换到 Chroma 自建

### 陷阱 4: 自建 Milvus 太复杂

**问题**: 运维成本高，性能调优困难
**解决**: 改用 Pinecone 或 Qdrant (更简单)

### 陷阱 5: 迁移数据丢失

**问题**: 新数据库的数据不完整
**解决**: 先验证数据完整性，再删除旧索引

---

## 📞 快速诊断

### "我的系统太慢了"

**症状**: 查询延迟 > 500ms

**诊断**:
```
FAISS + 大数据集?
  → 切换到 Pinecone 或优化索引参数

Chroma 过载?
  → 增加实例或切换到 Pinecone

网络延迟?
  → 检查网络配置或部署到同地域
```

### "我的成本太高了"

**症状**: 月费超预算

**诊断**:
```
Pinecone 超额?
  → 删除冗余向量或切换到自建 Chroma

自建 Milvus 昂贵?
  → 优化硬件配置或切换到 Pinecone

不知道什么原因?
  → 分析数据量、查询频率和操作成本
```

### "我需要高可用"

**症状**: 不能接受停机时间

**诊断**:
```
用 FAISS?
  → 立即迁移到 Pinecone / Chroma / Qdrant

自建单机?
  → 配置副本和故障转移

或者
  → 使用托管服务 (Pinecone, Weaviate Cloud)
```

---

## 📱 移动端速查卡

### 选择流程 (文本版)

```
Step 1: 成本限制?
  无→ 任意 | <$100→ 自建 | $100+→ 托管

Step 2: 用户量?
  <1K→ FAISS | 1K-10K→ Chroma | >10K→ Pinecone

Step 3: 运维能力?
  无→ Pinecone | 有→ 自建任意 | 中等→ Chroma/Qdrant

结果: 见本表
```

### 产品代号记忆

```
F = FAISS (快速、免费)
C = Chroma (轻量级、易用)
P = Pinecone (专业、托管)
W = Weaviate (完整、复杂)
M = Milvus (强大、昂贵)
Q = Qdrant (高性能、开源)
```

---

## 🎓 学习路径

### 如果你：

#### "第一次用向量数据库"
1. 学 FAISS (2 小时)
2. 学 LlamaIndex 集成 (1 小时)
3. 构建 demo (2 小时)
   → **总计 5 小时**

#### "准备上生产"
1. 学 Docker 部署 (3 小时)
2. 学 Chroma 或 Pinecone (2 小时)
3. 迁移数据和测试 (4 小时)
   → **总计 9 小时**

#### "需要企业级方案"
1. 学 Milvus 或 Weaviate (8 小时)
2. 集群部署 (6 小时)
3. 性能调优 (4 小时)
   → **总计 18 小时**

---

## 🔗 快速链接

### 官方网站
- FAISS: https://github.com/facebookresearch/faiss
- Chroma: https://trychroma.com
- Pinecone: https://www.pinecone.io
- Weaviate: https://weaviate.io
- Milvus: https://milvus.io
- Qdrant: https://qdrant.tech

### 文档
- 详细对比: [detailed_comparison.md](./detailed_comparison.md)
- 完整指南: [vector_database_selection_guide.md](./vector_database_selection_guide.md)
- 实施清单: [implementation_checklist.md](./implementation_checklist.md)

---

## 💡 最后的话

> **不要过度设计。用 FAISS，等业务需要时再升级。**

关键决策点：
- **日均查询 > 10,000** → 考虑升级
- **索引大小 > 10GB** → 考虑升级
- **需要多实例** → 立即升级
- **其他时候** → 继续用 FAISS

---

**最后更新**: 2025-12-24
**快速参考卡版本**: 1.0
