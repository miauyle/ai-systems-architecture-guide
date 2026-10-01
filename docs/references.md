# 原始资料与延伸阅读

[返回目录](../README.md)

本表提供稳定知识的原始资料入口，不是实时模型榜单。关键原理在对应章节解释，资料用于追溯依据。2026-10-01 核对了核心计算、训练、缓存、并行、检索与运行时的部分论文和官方机制文档，并补充对应入口；未对所有历史外链逐一确认。官方接口和支持条件以所用版本为准。

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
| [Megatron-LM](https://arxiv.org/abs/1909.08053) | 2019 | TP 矩阵切分与层内通信 | FFN 与 Attention 划分图 |
| [PyTorch Distributed](https://arxiv.org/abs/2006.15704) | 2020 | DDP 梯度桶、通信重叠与跳过同步 | 反向就绪与归约顺序 |

## 服务、应用与多模态

| 资料 | 年份 | 主题 | 建议先看 |
| --- | --- | --- | --- |
| [PagedAttention / vLLM](https://arxiv.org/abs/2309.06180) | 2023 | KV 管理与服务 | 分页设计及负载假设 |
| [Orca](https://www.usenix.org/conference/osdi22/presentation/yu) | 2022 | 迭代级服务调度 | 请求加入与完成的调度边界 |
| [DistServe](https://arxiv.org/abs/2401.09670) | 2024 | Prefill / Decode 分离 | 阶段隔离、KV 传输与服务目标 |
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
| [Reciprocal Rank Fusion 作者版](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) | 2009 | 基于名次的检索融合；[DOI](https://doi.org/10.1145/1571941.1572114) |
| [HNSW](https://arxiv.org/abs/1603.09320) | 2016 | 近似最近邻与图索引 |
| [Tree of Thoughts](https://arxiv.org/abs/2305.10601) | 2023 | 多候选搜索与选择机制的实例 |
| [Reflexion](https://arxiv.org/abs/2303.11366) | 2023 | 反馈与记忆机制的研究实例 |
| [MemGPT](https://arxiv.org/abs/2310.08560) | 2023 | 上下文与外部记忆管理的实例 |

这些论文是具体方案，不能由某个实验结果推断所有 Agent 或业务任务都有效。正文描述机制与适用边界，不宣称复现上述项目。

## 官方实现与文档

- [Hugging Face Transformers 文档](https://huggingface.co/docs/transformers/index)：模型配置、Tokenizer、生成与部署接口。
- [Hugging Face Tokenizers 文档](https://huggingface.co/docs/tokenizers/index)：实际切分、编码和训练流程。
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/index.html)：张量、自动微分、分布式与数值实现。
- [vLLM 文档](https://docs.vllm.ai/)：服务配置、支持的模型与运行条件。
- [Hugging Face Cache Explanation](https://huggingface.co/docs/transformers/cache_explanation)：逐层 KV、增量位置与有效历史。
- [vLLM Prefix Caching 设计](https://docs.vllm.ai/en/latest/design/prefix_caching/)：前缀块标识、引用与分配流程；属于具体引擎实现。
- [PyTorch FSDP 教程](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)：参数取回、梯度分发、分片更新与预取。
- [NCCL 集体操作](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html)：归约、拼接、分发与 rank 对应关系。
- [CUDA 异步执行](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html)：stream、事件、传输与执行依赖。
- [SentencePiece 项目](https://github.com/google/sentencepiece)：Tokenization 工具。
- [GitHub Markdown 文档](https://docs.github.com/en/get-started/writing-on-github)：公式、Mermaid 与 Markdown 阅读方式。
- [MCP 规范](https://modelcontextprotocol.io/specification/latest)：工具与资源的协议约定；版本随规范演进。
- [LangGraph 文档](https://docs.langchain.com/oss/python/langgraph/overview)：状态、图编排和运行时机制的实现入口。
- [LangGraph 持久化](https://docs.langchain.com/oss/python/langgraph/persistence)：检查点与恢复的实现参考，不等于外部副作用的 exactly-once 保证。

官方文档会更新，使用具体接口时记录版本。论文年份按本表所链接预印本的首次发布年份，可能与会议发表年份不同。

## 怎样读论文更省力？

先看问题、架构图、输入输出和实验设置，再读公式。检查结论适用的模型规模、数据、硬件与负载，不把论文中的某个加速倍数当作所有环境的保证。

资料按专题使用，阅读关系见[知识地图](00-learning-roadmap.md)。不要求按论文列表逐篇完成。

## 通用学习与生成家族

| 资料 | 年份 | 对应主题 |
| --- | --- | --- |
| [Deep Learning](https://www.deeplearningbook.org/) | 2016 | 学习目标、表示、泛化与优化基础 |
| [scikit-learn 模型选择](https://scikit-learn.org/stable/model_selection.html) | 持续更新 | 数据划分、模型选择与评估 |
| [scikit-learn 常见问题](https://scikit-learn.org/stable/common_pitfalls.html) | 持续更新 | 预处理与数据泄漏 |
| [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) | 2013 | VAE 的编码、潜在分布与解码 |
| [Generative Adversarial Networks](https://arxiv.org/abs/1406.2661) | 2014 | 生成器与判别器的对抗学习 |
| [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) | 2020 | 扩散训练与采样 |
| [Latent Diffusion Models](https://arxiv.org/abs/2112.10752) | 2021 | 潜在空间中的生成与条件 |
| [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) | 2022 | 概率路径与向量场学习 |
| [CLIP](https://arxiv.org/abs/2103.00020) | 2021 | 图文表示与对比学习 |

对应正文：[机器学习基础](23-machine-learning-foundations.md)、[生成模型](24-generative-models.md)、[多模态](13-multimodal-and-reasoning.md)。

## 资产、基础设施与安全

| 官方资料 | 支持的知识关系 |
| --- | --- |
| [Hugging Face 模型配置](https://huggingface.co/docs/transformers/main_classes/configuration) | 配置与模型资产 |
| [Hugging Face 聊天模板](https://huggingface.co/docs/transformers/chat_templating) | 消息序列与训练格式 |
| [CUDA 编程指南](https://docs.nvidia.com/cuda/cuda-programming-guide/) | 加速器执行与内存层级 |
| [NCCL](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/) | 集体通信与设备拓扑 |
| [GPUDirect RDMA](https://docs.nvidia.com/cuda/gpudirect-rdma/) | 网卡与 GPU 的直接路径及支持条件 |
| [GPUDirect Storage](https://docs.nvidia.com/gpudirect-storage/overview-guide/index.html) | 存储与 GPU 数据路径 |
| [Faiss](https://github.com/facebookresearch/faiss/wiki) | 向量索引、近似与压缩 |
| [MCP 2025-06-18 架构](https://modelcontextprotocol.io/specification/2025-06-18/architecture) | host、client、server 与连接能力 |
| [OWASP GenAI](https://genai.owasp.org/) | 提示注入、权限与应用安全 |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | 系统风险与治理关系 |

对应正文：[模型生命周期](26-model-lifecycle.md)、[计算基础设施](27-compute-infrastructure.md)、[安全边界](25-ai-security.md)。这些入口的存在不代表所有平台组合都受支持，部署时仍须核对实际版本。
