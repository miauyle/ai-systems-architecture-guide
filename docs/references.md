# 原始资料与延伸阅读

[返回目录](../README.md)

本表提供稳定知识的原始资料入口，不是实时模型榜单。链接指向论文或官方项目；本版未逐一联网检查外链可访问性。仓库内相对文件链接已通过交付检查。

## 核心结构与表示

| 资料 | 年份 | 支持本仓库中的主题 | 建议先看 |
| --- | --- | --- | --- |
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | 2017 | Transformer、Attention、FFN、位置编码 | 架构图与第 3 节 |
| [BERT](https://arxiv.org/abs/1810.04805) | 2018 | Encoder-only 与双向表示 | 模型和预训练目标 |
| [T5](https://arxiv.org/abs/1910.10683) | 2019 | Encoder–Decoder 与统一文本任务 | 方法图与任务格式 |
| [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) | 2015 | 子词 BPE | 算法示例 |
| [SentencePiece](https://arxiv.org/abs/1808.06226) | 2018 | Tokenization 工具与表示 | 方法与使用方式 |
| [RMSNorm](https://arxiv.org/abs/1910.07467) | 2019 | 均方根归一化 | 归一化公式 |
| [GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) | 2020 | 门控 FFN 与 SwiGLU | 变体公式与成本比较 |
| [RoFormer / RoPE](https://arxiv.org/abs/2104.09864) | 2021 | 旋转位置编码 | 相对位置机制 |

## 现代架构与效率

| 资料 | 年份 | 主题 | 建议先看 |
| --- | --- | --- | --- |
| [Multi-Query Attention](https://arxiv.org/abs/1911.02150) | 2019 | MQA 与增量推理带宽 | 头共享机制 |
| [GQA](https://arxiv.org/abs/2305.13245) | 2023 | 分组查询注意力 | MHA/MQA/GQA 对照图 |
| [Switch Transformers](https://arxiv.org/abs/2101.03961) | 2021 | 稀疏 MoE 路由与负载 | 专家结构与稳定训练 |
| [Mixtral of Experts](https://arxiv.org/abs/2401.04088) | 2024 | MoE 的具体实例 | 总参数和激活参数 |
| [FlashAttention](https://arxiv.org/abs/2205.14135) | 2022 | IO-aware 精确注意力 | 分块与内存访问 |
| [Mamba](https://arxiv.org/abs/2312.00752) | 2023 | 选择性状态空间模型 | 状态选择与实现思路 |

## 训练与适配

| 资料 | 年份 | 主题 | 建议先看 |
| --- | --- | --- | --- |
| [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) | 2022 | 参数、数据与计算预算 | 计算最优的前提与实验 |
| [InstructGPT](https://arxiv.org/abs/2203.02155) | 2022 | SFT、偏好、奖励模型与 RLHF | 训练流程图 |
| [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) | 2023 | DPO | 偏好目标与参考模型 |
| [LoRA](https://arxiv.org/abs/2106.09685) | 2021 | 低秩适配 | 低秩更新图与公式 |
| [QLoRA](https://arxiv.org/abs/2305.14314) | 2023 | 量化基础模型上的微调 | 内存机制与实验设置 |
| [ZeRO](https://arxiv.org/abs/1910.02054) | 2019 | 分片训练状态 | 各阶段分片对象 |

## 服务、应用与多模态

| 资料 | 年份 | 主题 | 建议先看 |
| --- | --- | --- | --- |
| [PagedAttention / vLLM](https://arxiv.org/abs/2309.06180) | 2023 | KV 管理与服务 | 分页设计及负载假设 |
| [Speculative Decoding](https://arxiv.org/abs/2211.17192) | 2022 | 草稿与验证 | 采样正确性及加速条件 |
| [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | 2020 | 检索增强生成 | 原始方法与实验任务 |
| [ReAct](https://arxiv.org/abs/2210.03629) | 2022 | 推理与行动交织的 Agent 范式 | 工具反馈循环 |
| [Vision Transformer](https://arxiv.org/abs/2010.11929) | 2020 | 图像 patch 表示 | 图像到序列的结构图 |
| [LLaVA / Visual Instruction Tuning](https://arxiv.org/abs/2304.08485) | 2023 | 视觉与语言连接、指令训练 | 编码器与投影结构 |
| [DeepSeek-R1](https://arxiv.org/abs/2501.12948) | 2025 | 推理训练的公开实例 | 训练策略与评估限制 |

## 深入机制的资料

| 资料 | 年份 | 对应内容 |
| --- | --- | --- |
| [Adam](https://arxiv.org/abs/1412.6980) | 2014 | 一阶/二阶矩、偏差修正与优化更新 |
| [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101) | 2017 | AdamW 与权重衰减 |
| [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906) | 2020 | 稠密检索的训练与评估 |
| [Sentence-BERT](https://arxiv.org/abs/1908.10084) | 2019 | 句向量与相似度任务 |
| [BM25 综述](https://doi.org/10.1561/1500000019) | 2009 | 词频、逆文档频率与长度归一化 |
| [Reciprocal Rank Fusion](https://doi.org/10.1145/1571941.1572114) | 2009 | 基于名次的检索融合 |
| [HNSW](https://arxiv.org/abs/1603.09320) | 2016 | 近似最近邻与图索引 |
| [Tree of Thoughts](https://arxiv.org/abs/2305.10601) | 2023 | 多候选搜索与选择机制的实例 |
| [Reflexion](https://arxiv.org/abs/2303.11366) | 2023 | 反馈与记忆机制的研究实例 |
| [MemGPT](https://arxiv.org/abs/2310.08560) | 2023 | 上下文与外部记忆管理的实例 |

这些论文是具体方案，不能由某个实验结果推断所有 Agent 或业务任务都有效。仓库中的教学代码独立用于解释机制，不是上述项目的复现。

## 官方实现与学习工具

- [Hugging Face Transformers 文档](https://huggingface.co/docs/transformers/index)：模型配置、Tokenizer、生成与部署接口。
- [Hugging Face Tokenizers 文档](https://huggingface.co/docs/tokenizers/index)：实际切分、编码和训练流程。
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/index.html)：张量、自动微分、分布式与数值实现。
- [vLLM 文档](https://docs.vllm.ai/)：服务配置、支持的模型与运行条件。
- [SentencePiece 项目](https://github.com/google/sentencepiece)：Tokenization 工具。
- [GitHub Markdown 文档](https://docs.github.com/en/get-started/writing-on-github)：公式、Mermaid 与 Markdown 阅读方式。
- [MCP 规范](https://modelcontextprotocol.io/specification/latest)：工具与资源的协议约定；版本随规范演进。
- [LangGraph 文档](https://docs.langchain.com/oss/python/langgraph/overview)：状态、图编排和运行时机制的实现入口。

官方文档会更新，实验时应记录所用版本。论文年份按本表所链接预印本的首次发布年份，可能与会议发表年份不同。

## 怎样读论文更省力？

先看问题、架构图、输入输出和实验设置，再读公式。检查结论适用的模型规模、数据、硬件与负载，不把论文中的某个加速倍数当作所有环境的保证。

初学顺序建议：Transformer → GQA → LoRA → InstructGPT → FlashAttention / PagedAttention → RAG。算法方向再深入损失推导，工程方向优先跟踪形状、资源和测量条件。
