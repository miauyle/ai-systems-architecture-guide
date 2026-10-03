# AI 系统知识库

**从数据与模型，到训练、推理服务和应用系统。**

本仓库用中文解释 AI 技术如何工作、为何这样设计、各组件怎样协同，以及能力与资源的边界。以大模型系统为深入主线，连接机器学习基础、生成模型、多模态、计算基础设施、RAG、Agent 与可靠性。

正文按知识关系组织，每章可以独立阅读。必要的定义公式和张量形状用于解释机制；内容不设置练习、答案、手算任务与实验课程。术语表只是查询入口，系统知识在正文中展开。

## 阅读入口

[完整专题目录](docs/README.md) · [知识关系地图](docs/00-learning-roadmap.md) · [系统全景](docs/01-system-map.md) · [术语表](docs/glossary.md) · [原始资料](docs/references.md)

| 分组 | 展开的关系 | 入口 |
| --- | --- | --- |
| 基础与全景 | 学习目标、表示、泛化，以及模型与系统的边界 | [机器学习](docs/23-machine-learning-foundations.md)、[数学与张量](docs/02-math-and-tensors.md)、[系统地图](docs/01-system-map.md) |
| 模型与生成 | 文本如何进入网络，注意力怎样传信息，各种架构与生成机制改变什么 | [Token 与表示](docs/03-tokenization-and-embeddings.md)、[Transformer](docs/04-transformer.md)、[生成模型](docs/24-generative-models.md) |
| 数据与训练 | 数据怎样形成学习信号，后训练怎样改变行为，分布式怎样管理状态 | [预训练](docs/07-pretraining.md)、[后训练](docs/08-post-training.md)、[数据生命周期](docs/15-data-lifecycle.md)、[训练系统](docs/17-training-engineering.md) |
| 推理与基础设施 | 从张量图与 Kernel 到集群路由、资源与 SLO | [编译与运行时](docs/28-ai-compiler-and-runtime.md)、[服务架构](docs/10-serving-and-distributed.md)、[引擎](docs/18-inference-engineering.md)、[计算基础设施](docs/27-compute-infrastructure.md)、[集群调度](docs/29-ai-platform-and-cluster-scheduling.md)、[性能模型](docs/30-ai-systems-performance.md) |
| 知识与行动 | 外部证据怎样进入回答，工具怎样变成可恢复的任务执行 | [RAG 与工具](docs/11-rag-and-agents.md)、[检索工程](docs/19-retrieval-engineering.md)、[Agent 运行时](docs/20-agent-runtime.md)、[规划与记忆](docs/21-agent-planning-and-memory.md) |
| 评估与生命周期 | 如何观测排障、判断质量、管理安全边界、升级和回退系统 | [评估](docs/12-evaluation.md)、[可观测性与排障](docs/31-ai-systems-observability-and-debugging.md)、[安全](docs/25-ai-security.md)、[模型生命周期](docs/26-model-lifecycle.md)、[生产评估](docs/22-evaluation-and-production.md) |

模型结构决定计算关系，训练决定参数怎样形成，执行系统决定计算怎样在资源中运行，应用决定知识、权限和动作怎样组织。理解这几层的连接，是本知识库的主线。

执行脉络贯穿 **Model Architecture → Tensor / Graph → Compiler / Runtime → Kernel → GPU / Network → Distributed Runtime → Training / Serving**。训练章连接 Device Mesh、现代并行组合与 checkpoint reshard；Serving 章连接 Gateway、KV-aware routing、P/D 池与执行所有权；平台和性能章将这些机制落到真实资源、SLO 和容量。

核心正文可沿具体对象跟踪：Token 经 Embedding、Attention、FFN 与 LM Head 成为下一个 Token；各层 K/V 在 Prefill 中写入、Decode 中读取；请求在服务中经历排队、分配、采样与流式输出。训练章连接监督信号、梯度与分片更新，应用章连接检索候选、可引用证据和持久动作状态。基础章讲完整逻辑，深入章展开实现与代价。

## 内容范围

当前包含 31 个专题正文与一份知识地图。数据版本与消费进度、Reasoning/RL 的采样—更新闭环、执行中间层及集群 Serving 连接为完整主线；Performance、Observability 与 Security 是贯穿训练、基础设施、应用和生产的横切能力。机器学习与生成家族提供通用脉络，不把全部 AI 等同于大语言模型。

本库负责请求、执行、并行、资源与生产关系；[AI Storage Notes](https://miauyle.github.io/ai-storage-notes/)深入 KV 层级、RDMA、GDS、对象存储与 GPU Data Path，避免复制底层存储专题。

本轮体系收口后进入维护、查漏补缺与技术演进更新阶段，停止主动横向新增专题；传统算法、完整视觉、推荐、强化学习理论与机器人不在当前扩充范围。本库不提供实时排行榜，不猜测未公开模型架构，也不把某篇论文的性能数字当作通用保证。

[系统整合章节](docs/14-end-to-end-case.md)展示数据、模型、服务与业务状态如何连接；[知识地图](docs/00-learning-roadmap.md)解释各专题的依赖，不要求按文件编号阅读。

## 文档与网页

可直接在 GitHub 阅读全部 Markdown。结构图使用 Mermaid，必要定义公式保留 GitHub 数学格式，章节采用相对链接。

文档站复用 `algorithm-notes`、`ai-storage-notes` 的 Jekyll + DocSteer 主题与 aqua 配色。首页以 AI Systems Knowledge Map 展示六个分组及核心专题入口，文档页提供侧栏、页内目录、全文搜索、深浅色模式、公式和 Mermaid。`docs/` 与 [navigation.json](navigation.json) 在构建时生成站点，不维护两份正文。

站点地址：[AI Systems Notes](https://miauyle.github.io/ai-systems-notes/)。实际发布状态以仓库 Pages 工作流为准，源码合并不等于部署成功。构建与发布方式见 [Pages 发布说明](maintenance/publishing.md)。

## 维护

正文在 `docs/`，仓库与发布说明在 `maintenance/`，可选工程记录在 `templates/`。文档检查：`python tools/check_docs.py`。

内容约定见 [CONTRIBUTING.md](CONTRIBUTING.md)，AI 协作规则见 [AGENTS.md](AGENTS.md)，修改记录见 [CHANGELOG.md](CHANGELOG.md)。仓库唯一长期主线为 `master`，通过临时分支与 PR 更新。
