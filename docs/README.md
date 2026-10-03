# 完整专题目录

[首页](../README.md) · [知识关系地图](00-learning-roadmap.md)

正文按知识关系分组。编号用于稳定标识，不表示必须按数字顺序阅读。基础章给出完整逻辑主线，深入章展开布局、状态、调度与工程代价；相互链接，不以术语列表替代机制。

## 基础与全景

| 章节 | 展开的关系 |
| --- | --- |
| [00 · AI 知识关系地图](00-learning-roadmap.md) | 各层概念的依赖与三条知识脉络 |
| [01 · AI 系统架构全景](01-system-map.md) | 模型、训练、推理、应用与交付物 |
| [23 · 机器学习、表示学习与泛化](23-machine-learning-foundations.md) | 学习范式、表示、泛化与分布变化 |
| [02 · 只补齐必要的数学与张量知识](02-math-and-tensors.md) | 张量、概率、损失与数值行为 |

## 模型与生成

| 章节 | 展开的关系 |
| --- | --- |
| [03 · 从文字到模型表示](03-tokenization-and-embeddings.md) | 子词、聊天模板与上下文表示 |
| [04 · Transformer 的完整计算路径](04-transformer.md) | Token 到各层计算、LM Head 与下一轮输入 |
| [05 · 注意力的信息流与上下文机制](05-attention-walkthrough.md) | 逐查询匹配、归一化、内容汇总与信息边界 |
| [06 · 现代大模型的架构变体](06-modern-architectures.md) | 位置旋转、头共享、专家路由与状态取舍 |
| [13 · 多模态与推理模型](13-multimodal-and-reasoning.md) | 视觉、音频、视频与测试时计算 |
| [24 · 生成模型：自回归、VAE、GAN、扩散与流匹配](24-generative-models.md) | 自回归、VAE、GAN、扩散与流匹配 |

## 数据与训练

| 章节 | 展开的关系 |
| --- | --- |
| [15 · AI 数据生命周期与一致性](15-data-lifecycle.md) | 数据版本、mixture、采样打包、消费恢复与索引一致性 |
| [07 · 数据与预训练架构](07-pretraining.md) | 输入标签、监督 Mask、反向信号与数据配比 |
| [08 · 后训练、适配与对齐](08-post-training.md) | SFT/DPO、RL 轨迹与策略版本闭环、LoRA |
| [17 · 训练系统：优化、并行与恢复](17-training-engineering.md) | 现代并行、CP、RL 分池与权重发布、分片恢复 |

## 推理与基础设施

| 章节 | 展开的关系 |
| --- | --- |
| [09 · 推理、KV Cache 与资源管理](09-inference-and-memory.md) | 逐层 KV 写入读取、生成计数与缓存复用条件 |
| [16 · 模型计算布局、算子与执行语义](16-transformer-implementation.md) | 拆头打包、融合、在线 Softmax 与增量语义 |
| [10 · 推理服务与分布式架构](10-serving-and-distributed.md) | 请求生命周期、KV 所有权、P/D 池、集群路由与 fleet |
| [18 · 推理引擎内部、容量与调度](18-inference-engineering.md) | 分页与前缀共享、连续批处理、remote KV 与局部预算 |
| [27 · AI 计算基础设施与数据路径](27-compute-infrastructure.md) | 缓冲传输、数据复用、集体通信与资源关键路径 |
| [28 · AI Compiler、Runtime 与 Kernel 执行栈](28-ai-compiler-and-runtime.md) | 图捕获、IR、融合、编译缓存与 Kernel 执行 |
| [29 · AI Platform、GPU Cluster 与资源调度](29-ai-platform-and-cluster-scheduling.md) | GPU/NIC 拓扑、组调度、租户与副本生命周期 |
| [30 · AI Systems 性能模型、SLO 与容量分析](30-ai-systems-performance.md) | 延迟、有效吞吐、关键路径、SLO 与容量成本 |

## 知识与行动

| 章节 | 展开的关系 |
| --- | --- |
| [11 · RAG、工具调用与 Agent 应用架构](11-rag-and-agents.md) | 证据、调用提案、执行边界与应用控制流 |
| [19 · 检索系统：从文档到可引用证据](19-retrieval-engineering.md) | 离线对象、候选搜索、重排与断言证据绑定 |
| [20 · Agent 运行时：决策、执行、状态与恢复](20-agent-runtime.md) | 决策快照、意图记录、幂等执行与对账恢复 |
| [21 · Agent 规划、记忆、多 Agent 与协议](21-agent-planning-and-memory.md) | 就绪任务、依赖失效、记忆读写与协议边界 |
| [14 · 系统整合：从数据到生产请求的完整生命周期](14-end-to-end-case.md) | 构建与请求路径、资产生命周期、三层调度与故障传播 |

## 评估与生命周期

| 章节 | 展开的关系 |
| --- | --- |
| [12 · 评估、观测与可靠性](12-evaluation.md) | 能力与系统评估、标签与错误归因 |
| [22 · 从评估集到生产验收](22-evaluation-and-production.md) | 指标、样本不确定性、故障与发布 |
| [25 · AI 系统的安全、权限与信任边界](25-ai-security.md) | 数据、指令、权限、输出与供应链 |
| [26 · 模型资产、版本与发布生命周期](26-model-lifecycle.md) | 模型资产、路由、版本、发布与回退 |
| [31 · AI Systems Observability、Profiling 与系统排障](31-ai-systems-observability-and-debugging.md) | 请求/训练 trace、CPU/GPU timeline、profile 与故障定位 |

## 查询与依据

[术语表](glossary.md) · [原始资料](references.md)

维护信息：[内容约定](../CONTRIBUTING.md)、[GitHub Pages 准备](../maintenance/publishing.md)。它们不属于知识章节。
