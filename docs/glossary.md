# 术语表

[返回目录](../README.md)

| 术语 | 中文 / 含义 | 容易混淆的边界 | 章节 |
| --- | --- | --- | --- |
| Token | Tokenizer 使用的离散单位 | 不等于字符或单词 | [03](03-tokenization-and-embeddings.md) |
| Tokenizer | 文本与 Token ID 之间的映射组件 | 必须与模型匹配 | [03](03-tokenization-and-embeddings.md) |
| Vocabulary | 词表，可用 Token 集合 | 大小不等于上下文长度 | [03](03-tokenization-and-embeddings.md) |
| Embedding | 可学习的向量表示 | 内部 Token 表与检索模型用途不同 | [03](03-tokenization-and-embeddings.md) |
| Hidden state | 隐藏状态，网络中间表示 | 不是人类可直接读出的思想 | [04](04-transformer.md) |
| Parameter / Weight | 参数 / 权重，训练学习的数值 | 与请求中的激活不同 | [02](02-math-and-tensors.md) |
| Activation | 激活，某次输入产生的中间数值 | 不属于永久参数 | [02](02-math-and-tensors.md) |
| Logits | 未归一化输出分数 | 还不是概率 | [02](02-math-and-tensors.md) |
| Softmax | 将分数归一化为分布 | 不等于事实置信度校准 | [02](02-math-and-tensors.md) |
| Attention | 按关联权重汇总表示 | 不等于完整解释机制 | [04](04-transformer.md) |
| Q / K / V | 查询 / 键 / 值投影 | 不是数据库字段 | [05](05-attention-walkthrough.md) |
| Causal mask | 因果掩码，阻止读取未来 | 与损失掩码不同 | [04](04-transformer.md) |
| FFN / MLP | 前馈网络 / 多层感知器 | 典型实现逐位置计算 | [04](04-transformer.md) |
| Residual | 残差连接 | 不是模型剩余错误的专用模块 | [02](02-math-and-tensors.md) |
| Norm | 归一化 | 与输出概率归一化用途不同 | [02](02-math-and-tensors.md) |
| RoPE | 旋转位置编码 | 不保证任意长度外推 | [06](06-modern-architectures.md) |
| GQA / MQA | 分组查询 / 多查询注意力 | 查询头数不等于 K/V 头数 | [06](06-modern-architectures.md) |
| MoE | 混合专家，常见为稀疏路由 FFN | 总参数不等于激活参数 | [06](06-modern-architectures.md) |
| SSM | 状态空间模型 | 不代表所有任务都优于 Attention | [06](06-modern-architectures.md) |
| Pretraining | 预训练 | 基础目标不等于直接业务验收 | [07](07-pretraining.md) |
| SFT | 监督微调 | 是训练目标与数据形式，不是参数效率方法 | [08](08-post-training.md) |
| RLHF | 基于人类反馈的强化学习流程 | 不专指一个算法 | [08](08-post-training.md) |
| DPO | 直接偏好优化 | 通常无需独立奖励模型 | [08](08-post-training.md) |
| LoRA / QLoRA | 低秩适配 / 量化基础权重上的低秩适配 | 不意味着全部张量低比特 | [08](08-post-training.md) |
| Context window | 上下文窗口 | 可接收长度不等于有效利用能力 | [03](03-tokenization-and-embeddings.md) |
| KV Cache | 每层历史 Key/Value 缓存 | 不存储答案，不更新参数 | [09](09-inference-and-memory.md) |
| Prefill / Decode | 输入处理 / 增量生成阶段 | 与完整首字延迟、网络延迟不同 | [09](09-inference-and-memory.md) |
| Quantization | 量化，低比特表示与相关计算技术 | 权重与 KV 分别判断；降存储不必然降延迟 | [18](18-inference-engineering.md) |
| TTFT | 首 Token 延迟 | 先说明计时边界，再判断包含哪些链路开销 | [10](10-serving-and-distributed.md) |
| Throughput | 吞吐，单位时间的处理量 | 与单请求延迟不同 | [10](10-serving-and-distributed.md) |
| RAG | 检索增强生成 | 不只有向量数据库 | [11](11-rag-and-agents.md) |
| Reranker | 对检索候选再排序的组件 | 不能找回从未进入候选的文档 | [19](19-retrieval-engineering.md) |
| Tool calling | 模型提出结构化工具调用 | 提议与授权执行是两个环节 | [11](11-rag-and-agents.md) |
| Agent | 模型动态选择行动的系统范式 | 名称不说明具体自主范围 | [11](11-rag-and-agents.md) |
| Hallucination | 不正确或无依据的生成内容 | 低温度不能根除 | [12](12-evaluation.md) |
| Grounding | 将回答关联到可验证来源或环境 | 仅提供引用字符串还不够 | [12](12-evaluation.md) |
| Test-time compute | 测试时计算预算 | 更多计算不保证更准确 | [13](13-multimodal-and-reasoning.md) |

缩写的实际含义可能随论文或框架变化。阅读配置时应以对应实现为准。

## 基础、生成与系统资产

| 术语 | 含义与边界 | 正文 |
| --- | --- | --- |
| Generalization | 泛化，对未见输入的表现；训练拟合不等于泛化 | [23](23-machine-learning-foundations.md) |
| Self-supervised learning | 自监督，从数据构造目标；仍有学习信号 | [23](23-machine-learning-foundations.md) |
| Calibration | 校准，置信度与实际正确比例的关系 | [23](23-machine-learning-foundations.md) |
| Data lineage | 数据血缘，来源与派生处理关系 | [15](15-data-lifecycle.md) |
| VAE | 变分自编码器，学习可采样的潜在表示 | [24](24-generative-models.md) |
| GAN | 生成对抗网络，生成器与判别器共同训练 | [24](24-generative-models.md) |
| Diffusion | 扩散生成，训练与采样采用噪声相关机制 | [24](24-generative-models.md) |
| Flow Matching | 流匹配，学习分布路径上的向量场 | [24](24-generative-models.md) |
| Arithmetic intensity | 算术强度，每字节数据对应的运算量 | [27](27-compute-infrastructure.md) |
| RDMA | 远端内存访问；不自动替代应用协议 | [27](27-compute-infrastructure.md) |
| Prompt injection | 不可信内容改变模型指令处理 | [25](25-ai-security.md) |
| Model artifact | 模型资产，包含权重及匹配配置与处理器 | [26](26-model-lifecycle.md) |
| Checkpoint | 检查点，推理导出与训练恢复所需内容不同 | [17](17-training-engineering.md) |
| Idempotency | 幂等，同一业务意图重试不重复产生效果 | [20](20-agent-runtime.md) |
| MCP | 工具与资源连接协议；不是完整任务运行时 | [21](21-agent-planning-and-memory.md) |
