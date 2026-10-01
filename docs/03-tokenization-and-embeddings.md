# 03 · 从文字到模型表示

[返回目录](../README.md) · [下一章](04-transformer.md)

## Tokenizer：模型自己的切分方式

Tokenizer 把文本映射为 Token ID；每个 ID 对应词表中的一个单位。单位可能是完整词、子词、单字符或字节片段。常见方法包括 BPE、WordPiece 和 Unigram，具体规则依模型而定。

例如「大模型架构」可能被切成不同片段；没有指定 Tokenizer 时，不能给出真实切分结果。中文字符数、英文单词数和 Token 数也没有固定换算比例。

Token 数直接影响上下文占用、计算量和 API 计费。应使用目标模型的 Tokenizer 或服务返回的用量统计。

## 特殊 Token 与聊天模板

对话消息一般会被序列化成带角色边界的序列，例如系统、用户、助手的标记。真实模板因模型而异；手写一个看起来像聊天的字符串不一定符合它的训练格式。

上下文预算通常包含系统指令、历史消息、检索资料、工具描述和输出预留；服务商对内部 Token 的记账方式需要看其文档。

## Embedding：ID 查表得到向量

设词表大小 $V=32,000$，隐藏维度 $d=512$，Embedding 权重为 $E\in\mathbb{R}^{V\times d}$。Token ID 为 17 时，取第 17 行向量作为初始表示。该表由训练学习，不是人工逐项填写。

```mermaid
flowchart LR
    A[文本] --> B[Tokenizer]
    B --> C[Token IDs：B × T]
    C --> D[Embedding 查表]
    D --> E[初始向量：B × T × d]
    E --> F[位置机制与 Transformer]
    F --> G[上下文表示]
```

同一个 Token 在同一个 Embedding 表中的初始向量相同，但进入网络后会随上下文变化。例如「苹果」在水果描述和公司财报中的后续表示不同。

## 位置：顺序必须进入计算

Attention 本身不会自动理解自然语言中的先后顺序。需要位置机制，如绝对位置 Embedding、正弦位置编码、RoPE 或相对位置偏置。

有些机制将位置向量加到输入中；RoPE 主要作用于注意力的 Q/K。不能把所有位置机制都画成「Embedding 加一个位置向量」。详见[现代架构](06-modern-architectures.md)。

## 两种不同用途的 Embedding

| 类型 | 作用 | 输出形态 |
| --- | --- | --- |
| 模型内部 Token Embedding | 将 Token ID 映射成网络输入 | 每个 Token 一个向量 |
| 检索 Embedding 模型 | 将查询或文档映射为可比较的语义表示 | 常见为每段一个向量，也有多向量方法 |

二者都使用向量，但训练目标和使用方法可能不同。不能默认生成模型某个隐藏向量直接就是优质检索向量。

## Tokenization 的实际影响

- 生僻字、代码符号和混合语言可能需要更多 Token。
- 数字可能被切成多个片段；语言模型不天然执行精确整数运算。
- 输入格式变化可能改变 Token 数和模型行为。
- 上下文窗口大，表示能接收更多 Token；不保证对所有位置都同样有效。

## 自测

1. 为什么「1 万字的文档」不足以判断是否能放进上下文？
2. 内部 Token Embedding 和向量检索 Embedding 能直接互换吗？

[答案](misconceptions-and-answers.md)
