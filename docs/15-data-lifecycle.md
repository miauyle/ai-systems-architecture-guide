# 15 · AI 数据生命周期与一致性

[知识地图](00-learning-roadmap.md) · [预训练](07-pretraining.md) · [检索工程](19-retrieval-engineering.md)

## 同一份数据可以进入不同路径

训练数据影响参数；RAG 数据影响在线证据；评估数据影响对系统的判断；工具与业务数据决定实际可执行操作。它们可能来自同一组织，但有不同的更新时间、权限和正确性要求。

把资料放入训练集，无法保证线上逐条追溯来源。把资料索引为向量，也不等于模型已经学会遵守其中的业务规则。数据进入哪条路径，应由所需能力决定，而不是由可用的存储产品决定。

| 数据路径 | 主要产物 | 更新影响 | 关键一致性要求 |
| --- | --- | --- | --- |
| 训练 | 数据快照与检查点 | 改变下一次训练或适配 | 可重复的数据顺序与处理版本 |
| 检索 | 文本块、索引、元数据 | 改变当前可见证据 | 内容、权限、版本同时有效 |
| 评估 | 案例、标签与结果 | 改变质量判定 | 固定快照、避免开发污染 |
| 业务工具 | 实体状态、事务与回执 | 改变外部系统 | 授权、事务、幂等与对账 |

## 原始层与派生层

原始文档应保存可追溯来源、获取时间和内容标识。解析文本、规范化数据、Token 序列、Embedding 和索引属于派生产物，需要记录处理代码、配置和依赖版本。

派生数据不适合成为唯一事实来源。Embedding 无法还原精确原文，摘要可能丢失例外，清洗可能删除关键条件。在线引用与重新处理需要回到可定位的原始或规范化资料。

可靠的数据血缘能回答某段证据来自哪份文档、经过哪次解析、用了哪个 Embedding 模型，以及哪个索引快照正在服务。血缘缺失时，排错常常只能猜模型是否“幻觉”。

## 数据质量是任务相关的

质量包括文本可读性、事实和标签可靠性、结构完整性、来源合法性、覆盖与分布。短且整洁不必然比长且复杂更适合训练；清洗掉全部低频结构可能损害真实任务的覆盖。

网页页眉、重复导航、乱码与代码截断会增加无效目标。文档解析丢失表头、单位或否定条件，会直接让检索证据失真。质量规则需要结合用途：训练强调学习分布，知识检索强调可回答性与可追溯性。

## 去重与划分顺序

精确去重识别相同内容，近重复去重识别转载、轻微改写与模板变体。按文件随机划分后再去重，可能把同一个内容家族分到训练与测试两侧，造成评估泄漏。

更合理的划分单位可以是文档家族、用户、时间或任务来源，取决于目标泛化。预测未来事件时按时间划分，不能使用未来资料补全过去样本。学习新用户行为时，同一用户跨集合也可能夸大效果。

去重与 rare data 的覆盖可能冲突：模板相似不一定语义冗余，低资源语言、代码结构和少见任务可能被过度删除。保留去重簇、阈值和过滤原因，按领域/语言审计删除比例，必要时采用分层规则；保留稀有覆盖不等于放任测试泄漏。依据：[Deduplicating Training Data Makes Language Models Better](https://aclanthology.org/2022.acl-long.577/)，其特定实验结果不构成所有数据集的统一收益。

Contamination detection 还要查训练、validation 与 benchmark 的问题、答案、解释、译文/改写和同源材料。精确字符串未命中不证明无污染；近重复与语义检测有误报/漏报，应保留判定依据与人工抽查。验证集反复用于筛数据或调 mixture 也会形成开发适配，最终仍需独立留出集；公开评测内容要有明确保护与排除规则。改写污染的原始研究见[Rethinking Benchmark and Contamination](https://arxiv.org/abs/2311.04850)。

## 训练输入的供给链

Raw Data → Parse / Clean → Dedup / Filter → Dataset Version → Mixture → Shard → Sample / Pack → DataLoader → Host Buffer → GPU → Training Step。物理存储分片、样本分配和 Token 打包是不同责任，不能只用“数据已经分片”说明完整输入合同。

| 对象 | 谁产生、谁消费 | 必须固定的状态 |
| --- | --- | --- |
| Dataset manifest | 构建/整理流程产生，采样/恢复系统读取 | 内容标识/checksum、shard 清单、样本/Token 统计、split、解析/过滤/Tokenizer 版本 |
| Dataset version | 验证后发布的数据快照，mixture 引用 | 不可变内容与处理规则；可变 URL 或文件夹名不是充分版本身份 |
| Mixture | 训练策略指定，sampler 消费 | 数据源版本、权重、计数口径、耗尽/重采样策略和随进度变化的计划 |
| Sample / pack state | sampler/packer 产生，DataLoader 消费 | shuffle/RNG、样本与边界、未打包余项、监督位置与有效 Token |
| Host buffer | loader/CPU 准备，H2D 与训练消费 | 预取队列、传输依赖与可复用边界，见[物理路径](27-compute-infrastructure.md) |

Manifest 应指向可验证内容与处理血缘，而非只列若干地址。数据版本也是模型可复现性的一部分：相同代码与 weights 起点，换了清洗、Tokenizer、split 或 mixture 就可能训练出不同结果。

## Mixture、采样权重与 Token budget

Sampling weight 要说明是在“选择一个数据源/样本”还是“分配有效 Token 份额”。相同样本抽样概率在长度不同的数据源上不产生相同 Token 比例；token-based sampling 可以按目标 Token 配比组织采样，但应区分输入 Token、非 padding Token 与参与损失的监督 Token。

Epoch 表示对明确数据集合的一轮遍历；带重采样的 mixture 或无限 streaming dataset 不一定有自然的全局 epoch。Token budget 用消费口径定义训练进度和停止边界；数据源耗尽后是结束、重新采样还是重归一化，需要固定，否则实际配比会漂移。

Curriculum / mixture change 按进度改变来源或长度，应记录计划版本、生效更新点与实际消费份额。它是训练分布变化，不只是 DataLoader 的性能开关。数据加权的代表性研究见[DoReMi](https://arxiv.org/abs/2305.10429)，不能把某组权重当作任意模型/任务的最优配比。

## Packing 不应改变样本监督语义

Sample packing 可指按长度把样本分配到批次/槽位，sequence packing 则常指将多个样本放进同一执行序列；术语随实现变化，必须核对是否跨样本 Attention、怎样处理位置和 loss mask。

若训练目标要求样本独立，拼接后应保护样本边界、位置、因果/块级 Attention mask 与标签移位，不能让前一条回答成为后一条样本的未授权上下文。若有意训练连续文档，则是另一种目标。减少 padding 不意味着可以删除真实边界；SFT 的工具/用户段也不能因为 packing 就变成监督回答。

Packer 可能保留不足一个序列的余项。截断、丢弃、跨批次拼接和恢复该余项决定实际看到哪些 Token，须与预算、统计和 checkpoint 对齐，而不是只报告打包后 batch size。

## Shuffling、distributed sampler 与 worker ownership

Map-style 数据可先打乱索引再分配；streaming dataset 按需迭代，通常用 shard 顺序和有限 shuffle buffer 近似打乱，不等于对全量数据做均匀随机排列。buffer 大小、seed、epoch、数据源顺序和耗尽策略都影响看到的分布。

数据并行 rank 通常领取不同样本；TP/CP 等协同计算同一样本的成员不能各自随意抽一条新样本。再考虑每个 rank 内的 DataLoader workers：明确 rank × worker 的 shard/样本归属，否则复制一个 IterableDataset 对象可能导致多 worker 重复读取。分片数量也限制有效并行度。

DistributedSampler 的补齐或丢尾策略可能重复/遗漏部分样本，打乱也要按实现更新 epoch/seed。存储 shard 是 I/O 单位，不自动等于 sampling weight，也不保证数据源混合均匀。官方机制入口：[PyTorch Dataset / DataLoader / DistributedSampler](https://docs.pytorch.org/docs/stable/data.html)、[Hugging Face Dataset streaming](https://huggingface.co/docs/datasets/stream)。具体 worker 分配、可恢复接口与状态支持可能变化。

小文件的请求开销、大分片的更新粒度和预取造成的主机压力影响供给；GPU 等输入也可能是 CPU 解析或不均衡 shard。定位方法见[第 31 章](31-ai-systems-observability-and-debugging.md)，不在本章重复硬件与 I/O 深层机制。

## DataLoader resume 要恢复已经消费的进度

读到的位置、已预取的位置与训练更新实际消费的位置不同。Checkpoint 的数据进度应和一致更新点对齐；若直接从最远预取游标续读，会跳过从未用于更新的样本，退得过多则可能重复训练。

| 恢复对象 | 需要保存或可重建的语义 |
| --- | --- |
| Dataset / mixture version | 固定内容、比例、curriculum 生效点及耗尽策略 |
| Sampler / shard | 顺序、归属、偏移、epoch 和已提交消费位置 |
| RNG / shuffle | 各相关随机流与 buffer 的恢复/重建约定 |
| Packing / loader | 未完成余项、worker 状态及预取样本如何重放或丢弃 |
| Consumed token progress | 明确有效计数、对应更新点，避免将预取量当成训练量 |

不是所有 loader 都支持严格恢复这些状态。可以保存完整状态，也可以从可重建边界确定性重放并跳过已消费部分；必须说明代价与是否等价。拓扑/worker 数改变时，旧本地游标要映射为全局消费进度，不能逐 rank 机械接续。Weights/optimizer 的分片提交和 reshard 由[第 17 章](17-training-engineering.md)主责；数据消费合同由本章主责。

## 索引更新是多产物发布

一份文档改变后，文本块、Embedding、关键词索引、元数据和引用映射都可能改变。逐个原地更新会出现部分新部分旧的窗口。

可以采用版本化快照：完成新产物构建和验证后，切换线上读取指针，再逐步回收旧版本。增量更新则需要明确失败重试、删除传播和重建机制。两种方式都要保证在线结果能追溯到一个可解释的数据版本。

权限撤销不能只等下一次完整重建。检索前的授权过滤、来源打开时的访问校验、缓存失效和后台删除分别承担不同责任。索引里删除一条记录，也不会自动撤回已经输出的文本。

## Embedding 升级影响整个比较空间

新模型产生的向量通常不能直接与旧模型向量混合比较，即使维度相同。查询与文档端应使用兼容模型与预处理，必要时重建索引并同时切换查询配置。

迁移期间可以维护两套版本并比较结果，但不同空间的分数不能随意拼接。分块规则变化同样影响召回和引用 ID，需要将数据迁移与应用兼容性一起管理。

## 删除、纠正与知识更新

外部文档删除相对容易落实到检索索引和缓存，已经训练进参数的信息却不能由“删原文件”保证消失。模型遗忘属于独立研究与工程问题；在缺少验证时不能承诺删除一个样本等于删除其全部参数影响。

事实纠正也分层处理：来源错误应先修原始资料，索引错误修派生产物，生成错误修上下文或模型行为。把所有纠正都投入微调，会增加更新成本并掩盖数据链的缺陷。

## 数据反馈闭环

线上输出不是天然可靠的训练标签。用户点赞可能反映措辞偏好，人工改写可能含有新的错误，自动采集的模型输出可能放大旧模型偏差。

Training Output / Production Feedback → Validation → Data Curation → New Dataset Version，再由 mixture 选择进入下轮训练。评估集需要与调参反馈保持边界；否则系统“越来越高分”可能只是越来越熟悉测试题。

Synthetic / model-generated data 保留生成模型、模板、采样策略、seed（适用时）、来源/工具依据、筛选和 verifier 版本。过滤可用规则、程序检查、独立模型或人工，但生成与判分共用同一种偏差可能造成自证；来源合法、污染检查与独立验证不能因为它是“合成数据”而省略。

Data quality metrics 应按来源/语言/领域统计解析失败、过滤/去重比例、长度、重复簇、稀有覆盖、污染告警与有效监督 Token，并和留出任务质量联系。单一质量分、更多 Token 或更高 verifier 通过率不充分证明数据更好；采样策略也可能只留下容易案例。新版本需验证后发布，不能直接把生产输出追加成可信标签。

相关章节：[机器学习与泛化](23-machine-learning-foundations.md)、[模型生命周期](26-model-lifecycle.md)、[安全边界](25-ai-security.md)。
