# AI 系统架构知识库

**大模型、推理服务、RAG 与 Agent**

从模型内部计算到训练、部署，再到检索、工具和行动系统，理解各个组件如何组成可验证的 AI 应用。

本知识库以大模型驱动的 AI 系统为当前主线，按知识依赖组织：AI 与机器学习的位置 → 数学与表示 → 模型结构 → 训练 → 推理与服务 → RAG、Agent 与评估。各章节从直觉讲到机制、公式和实践，形成统一的系统学习路径。详见[知识体系与学习路线](docs/00-learning-roadmap.md)。

## 你将学会什么

- 解释 Token、Embedding、Attention、Transformer、MoE 各自解决什么问题。
- 跟踪一句话如何变成张量，再变成下一个 Token 的概率。
- 区分预训练、SFT、偏好优化、强化学习，以及 Prompt、RAG、微调的作用。
- 估算参数、训练状态、KV Cache 的显存，理解长上下文和高并发为什么昂贵。
- 从质量、延迟、吞吐、成本出发，设计推理服务和知识库助手。
- 通过自测和小实验检查理解，而不只记住术语。
- 跟踪可运行 Transformer 的前向与缓存实现，手算训练梯度，设计 Agent 的执行与恢复状态机。

## 当前覆盖范围

| 系统组成 | 当前内容 |
| --- | --- |
| 模型与训练 | 数学、Token、Transformer、架构变体、预训练与后训练 |
| 推理与服务 | KV Cache、显存、量化、调度、缓存与分布式 |
| 知识与工具 | RAG、检索、引用、工具调用与权限 |
| Agent 与工作流 | 执行状态机、规划依赖、记忆、协作、幂等性、恢复、终止与预算 |
| 评估与扩展 | 质量和性能评估、多模态、推理模型与系统案例 |

Agent 属于应用系统层：模型提供理解与决策能力，工具负责外部执行，状态和控制流组织多步任务。入门见[第 11 章](docs/11-rag-and-agents.md)，执行机制见[第 20 章](docs/20-agent-runtime.md)，规划、记忆与多 Agent 协作见[第 21 章](docs/21-agent-planning-and-memory.md)。

传统机器学习、视觉、推荐与机器人等方向可在后续扩展，当前章节聚焦大模型驱动的系统。

## 先建立全景

```mermaid
flowchart TB
    D[数据采集、清洗与切分] --> T[预训练]
    T --> P[后训练：SFT、偏好优化与 RL]
    P --> W[模型权重与配置]
    W --> S[推理服务：调度、缓存、并行]
    U[用户请求] --> A[应用：Prompt、检索与工具]
    A --> S
    S --> A
    A --> O[答案或行动结果]
    E[评估、观测与反馈] -.-> D
    E -.-> P
    E -.-> S
    E -.-> A
```

模型架构决定一次前向计算怎样发生；训练架构决定参数怎样被学到；推理架构决定计算怎样被高效执行；应用架构决定模型怎样连接数据、权限和业务。这四层相互约束，但不能混为一谈。

## 文档导航

建议按顺序读；已有基础时可用最后一列跳转。

| 章节 | 核心问题 | 阅读目的 |
| --- | --- | --- |
| [00 知识体系与学习路线](docs/00-learning-roadmap.md) | 知识之间有什么依赖关系？ | 建立完整学习顺序与验收标准 |
| [01 AI 系统架构全景](docs/01-system-map.md) | 模型、训练、推理与应用怎样组成系统？ | 建立边界和整体地图 |
| [02 数学与张量基础](docs/02-math-and-tensors.md) | 公式中的矩阵在做什么？ | 补齐必要数学 |
| [03 Token 与表示](docs/03-tokenization-and-embeddings.md) | 文字如何进入模型？ | 理解表示与上下文 |
| [04 Transformer](docs/04-transformer.md) | 模型内部怎样流动？ | 掌握核心计算 |
| [05 Attention 数值例子](docs/05-attention-walkthrough.md) | Q、K、V 和 Mask 到底是什么？ | 手算一次注意力 |
| [06 现代架构变体](docs/06-modern-architectures.md) | RoPE、GQA、MoE、SSM 改了什么？ | 理解设计取舍 |
| [07 数据与预训练](docs/07-pretraining.md) | 模型怎样从语料中学习？ | 理解训练流程 |
| [08 后训练与适配](docs/08-post-training.md) | 模型怎样变得会回答、符合偏好？ | 比较 SFT、DPO、RL、LoRA |
| [09 推理与显存](docs/09-inference-and-memory.md) | 为什么首字慢、长对话贵？ | 估算资源和性能 |
| [10 服务与分布式](docs/10-serving-and-distributed.md) | 怎样服务多人并发？ | 理解调度与并行 |
| [11 RAG 与 Agent](docs/11-rag-and-agents.md) | 怎样连接私有知识和工具？ | 构建业务应用 |
| [12 评估与可靠性](docs/12-evaluation.md) | 怎样知道系统真的有用？ | 设计评估与排错 |
| [13 多模态与推理模型](docs/13-multimodal-and-reasoning.md) | 图像、语音和推理如何进入架构？ | 扩展知识边界 |
| [14 贯穿案例](docs/14-end-to-end-case.md) | 怎样设计一个企业知识助手？ | 串联全部知识 |
| [15 动手实验](docs/15-experiments.md) | 怎样以低成本验证理解？ | 从知识走向实践 |
| [16 Transformer 可运行实现](docs/16-transformer-implementation.md) | 公式如何变成程序，缓存怎样保持等价？ | 张量、Mask、位置与数值验证 |
| [17 训练系统详解](docs/17-training-engineering.md) | 梯度、批次、优化器和分布式如何协同？ | 手写训练、AdamW、分片、DPO 与排错 |
| [18 推理引擎详解](docs/18-inference-engineering.md) | 缓存、带宽、调度和量化实际怎么工作？ | 容量、计算、通信与性能实验 |
| [19 检索系统详解](docs/19-retrieval-engineering.md) | 怎样从原文找到完整且可引用的证据？ | 分块、BM25、向量、RRF、ANN 与重排 |
| [20 Agent 运行时](docs/20-agent-runtime.md) | 决策如何变成可靠的业务执行？ | 状态机、工具校验、预算、对账与幂等性 |
| [21 Agent 规划与记忆](docs/21-agent-planning-and-memory.md) | 怎样规划、保留状态和组织角色协作？ | 依赖图、重规划、记忆、MCP 与协作 |
| [22 评估与生产验收](docs/22-evaluation-and-production.md) | 怎样证明改动有效且能稳定交付？ | 指标定义、统计、故障注入与验收 |
| [可运行教学示例](examples/README.md) | 怎样执行并检查具体机制？ | Transformer、手写训练与 Agent 循环 |
| [术语表](docs/glossary.md) | 缩写和概念怎么对应？ | 随时查阅 |
| [常见误区与自测答案](docs/misconceptions-and-answers.md) | 哪些概念最容易混淆？ | 检查理解 |
| [原始资料与延伸阅读](docs/references.md) | 依据是什么？下一步读什么？ | 阅读论文和官方文档 |
| [云端 Codex 与 GitHub 连接](docs/github-connection.md) | 授权、Token、远程仓库与 Pages 怎么区分？ | 配置仓库访问与发布链路 |

## 怎么读

**只有 30 分钟：**读 01 的全景、04 的计算流程、09 的资源例子、11 的方法选择表。

**希望系统学习：**按照 00 的八周安排，先建立基础，再进入机制与实现。每章先读直觉，再看计算和状态变化，最后做自测与验证。

**希望做工程：**完成 14 的设计笔记和 15 的实验，再用 12 的评估表检查结果。

**希望深入具体机制：**先读相应基础章，再进入 16–22。重点练习完整与缓存计算对照、训练梯度、检索错误定位，以及 Agent 的超时恢复。运行示例时请注意各程序明确标注的教学简化。

本仓库侧重稳定原理，不提供实时模型排行榜，也不推测未公开模型的内部结构。数字均标明假设；同名技术在不同实现中的细节可能不同。资料入口见[参考资料](docs/references.md)。

## 仓库结构与维护

```text
ai-systems-architecture-guide/
├── README.md
├── docs/                 # 中文教程、图解、练习和资料
├── templates/            # 学习检查清单、架构决策与评估记录
├── examples/             # 三个可运行教学示例
├── tools/                # 文档与公式源代码检查
├── AGENTS.md             # AI 助手协作与验证规则
├── CONTRIBUTING.md       # 文档修改约定
├── CHANGELOG.md
└── .gitignore
```

全部正文使用 Markdown，独立公式使用 GitHub 支持的 `math` 代码块，结构图使用 Mermaid；表格中的张量形状和算式使用代码或普通文本。不需要安装依赖，可直接在 GitHub 中阅读。

文档源检查可运行 `python tools/check_docs.py`。公式修改还需实际浏览器排版检查，Markdown 接口识别出数学节点不等于公式已经排版成功。

后续可将这些 Markdown 接入 GitHub Pages 文档主题。选定主题后再配置站点导航、数学公式、Mermaid 和部署流程；当前交付尚未包含网站主题或 Pages 部署。

远程仓库：[miauyle/ai-systems-architecture-guide](https://github.com/miauyle/ai-systems-architecture-guide)，文档分支为 `main`。仓库提交与 GitHub Pages 网站部署是两个状态，当前尚未配置 Pages。后续发布方式参见[GitHub 发布说明](docs/publishing.md)。
