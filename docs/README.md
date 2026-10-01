# 完整专题目录

[首页](../README.md) · [知识关系地图](00-learning-roadmap.md)

正文按知识关系分组。编号用于稳定标识，不表示必须按数字顺序阅读。基础章解释对象与边界，深入章解释执行、状态和组件协同。

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
| [04 · Transformer 的完整计算路径](04-transformer.md) | 注意力、FFN、残差与输出 |
| [05 · 注意力的信息流与上下文机制](05-attention-walkthrough.md) | 信息选择、Mask、位置与长上下文 |
| [06 · 现代大模型的架构变体](06-modern-architectures.md) | RoPE、GQA、MoE 与状态结构取舍 |
| [13 · 多模态与推理模型](13-multimodal-and-reasoning.md) | 视觉、音频、视频与测试时计算 |
| [24 · 生成模型：自回归、VAE、GAN、扩散与流匹配](24-generative-models.md) | 自回归、VAE、GAN、扩散与流匹配 |

## 数据与训练

| 章节 | 展开的关系 |
| --- | --- |
| [15 · AI 数据生命周期与一致性](15-data-lifecycle.md) | 数据血缘、划分、更新与索引一致性 |
| [07 · 数据与预训练架构](07-pretraining.md) | 预训练目标、数据配比与计算预算 |
| [08 · 后训练、适配与对齐](08-post-training.md) | SFT、偏好、奖励与参数适配 |
| [17 · 训练系统：优化、并行与恢复](17-training-engineering.md) | 梯度聚合、优化状态、分片与恢复 |

## 推理与基础设施

| 章节 | 展开的关系 |
| --- | --- |
| [09 · 推理、KV Cache 与资源管理](09-inference-and-memory.md) | 生成阶段、KV、资源增长与解码 |
| [16 · 模型计算布局、算子与执行语义](16-transformer-implementation.md) | 张量布局、融合、精度与缓存语义 |
| [10 · 推理服务与分布式架构](10-serving-and-distributed.md) | 准入、调度、副本、并行与服务指标 |
| [18 · 推理引擎内部、容量与调度](18-inference-engineering.md) | 块缓存、抢占、量化与推测解码 |
| [27 · AI 计算基础设施与数据路径](27-compute-infrastructure.md) | 主机、HBM、通信、存储与集群 |

## 知识与行动

| 章节 | 展开的关系 |
| --- | --- |
| [11 · RAG、工具调用与 Agent 应用架构](11-rag-and-agents.md) | Prompt、外部证据、工具与控制流 |
| [19 · 检索系统：从文档到可引用证据](19-retrieval-engineering.md) | 召回、融合、ANN、重排与证据 |
| [20 · Agent 运行时：决策、执行、状态与恢复](20-agent-runtime.md) | 授权、持久状态、幂等与恢复 |
| [21 · Agent 规划、记忆、多 Agent 与协议](21-agent-planning-and-memory.md) | 依赖、重规划、记忆与协作接口 |
| [14 · 系统整合：知识助手怎样成为可靠应用](14-end-to-end-case.md) | 知识助手的组件、版本与业务状态 |

## 评估与生命周期

| 章节 | 展开的关系 |
| --- | --- |
| [12 · 评估、观测与可靠性](12-evaluation.md) | 能力与系统评估、标签与错误归因 |
| [22 · 从评估集到生产验收](22-evaluation-and-production.md) | 指标、样本不确定性、故障与发布 |
| [25 · AI 系统的安全、权限与信任边界](25-ai-security.md) | 数据、指令、权限、输出与供应链 |
| [26 · 模型资产、版本与发布生命周期](26-model-lifecycle.md) | 模型资产、路由、版本、发布与回退 |

## 查询与依据

[术语表](glossary.md) · [原始资料](references.md)

维护信息：[内容约定](../CONTRIBUTING.md)、[GitHub Pages 准备](../maintenance/publishing.md)。它们不属于知识章节。
