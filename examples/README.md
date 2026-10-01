# 可运行教学示例

[返回知识库](../README.md)

示例用于检查机制，不使用预训练权重、不访问外部 API，也不操作真实业务系统。

在仓库根目录执行。模型示例需要 Python 和 NumPy，检索与 Agent 示例只使用 Python 标准库。本次验证环境为 Python 3.12.14、NumPy 2.3.5；需要安装 NumPy 时，可在自己的虚拟环境使用 `python -m pip install numpy`。

| 示例 | 命令 | 验证的知识 |
| --- | --- | --- |
| [可训练上下文注意力](context_attention_train.py) | `python examples/context_attention_train.py` | Q/K/V 反向传播、Adam、独立前缀、信息基线与输入干预 |
| [制度检索算例](rag_walkthrough.py) | `python examples/rag_walkthrough.py` | 生效区间、组织过滤、BM25 与可追溯证据 |
| [Transformer 前向](transformer_numpy.py) | `python examples/transformer_numpy.py` | 拆头、因果性、位置偏移、完整计算与 KV 缓存一致性 |
| [手写语言模型训练](bigram_train.py) | `python examples/bigram_train.py` | 交叉熵、解析梯度、重复索引累加、SGD 与训练不确定性 |
| [Agent 执行循环](agent_runtime.py) | `python examples/agent_runtime.py` | 结构/权限校验、预算、写操作结果未知、对账与幂等性 |

按[连续课程](../course/README.md)依次运行。每个程序包含针对机制的验证。小型 bigram 不具备 Transformer 的长上下文能力；注意力模型只训练固定长度的人工任务，未包含完整 Decoder 的 Norm/残差/FFN；随机 Transformer 没有语言能力；检索用手工词标注；Agent 的决策策略和后端是本地测试夹具。

与程序对应的解释见 [16](../docs/16-transformer-implementation.md)、[17](../docs/17-training-engineering.md) 和 [20](../docs/20-agent-runtime.md)。
