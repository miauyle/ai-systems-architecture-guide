"""A small, untrained Pre-Norm decoder: full attention and KV-cached decoding.

Run from the repository root: python examples/transformer_numpy.py
Requires NumPy. Uses float64, learned absolute positions, and no padding.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Config:
    vocab: int = 32
    width: int = 16
    heads: int = 4
    layers: int = 2
    ff_width: int = 32
    max_length: int = 64


def softmax(x):
    z = x - x.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def layer_norm(x, eps=1e-5):
    mean = x.mean(axis=-1, keepdims=True)
    variance = ((x - mean) ** 2).mean(axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(variance + eps)


def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))


class TinyDecoder:
    def __init__(self, config=Config(), seed=7):
        if config.width % config.heads:
            raise ValueError("width must be divisible by heads")
        self.c = config
        rng = np.random.default_rng(seed)

        def weight(a, b):
            return rng.normal(0, 0.12, size=(a, b))

        self.embedding = weight(config.vocab, config.width)
        self.position = weight(config.max_length, config.width)
        self.output = weight(config.width, config.vocab)
        self.blocks = []
        for _ in range(config.layers):
            self.blocks.append({
                "q": weight(config.width, config.width),
                "k": weight(config.width, config.width),
                "v": weight(config.width, config.width),
                "o": weight(config.width, config.width),
                "up": weight(config.width, config.ff_width),
                "down": weight(config.ff_width, config.width),
            })

    def forward(self, ids, cache=None):
        ids = np.asarray(ids)
        if ids.ndim != 2 or ids.shape[1] == 0:
            raise ValueError("ids must have shape [batch, nonzero_length]")
        if not np.issubdtype(ids.dtype, np.integer):
            raise ValueError("ids must be integers")
        if ids.min() < 0 or ids.max() >= self.c.vocab:
            raise ValueError("token ID is outside the vocabulary")
        batch, length = ids.shape
        if cache is not None and len(cache) != self.c.layers:
            raise ValueError("cache must contain one K/V pair per layer")
        past = 0 if cache is None else cache[0][0].shape[2]
        if past + length > self.c.max_length:
            raise ValueError("sequence exceeds maximum length")
        if cache is not None:
            expected = (batch, self.c.heads, past, self.c.width // self.c.heads)
            if any(k.shape != expected or v.shape != expected for k, v in cache):
                raise ValueError("cache dimensions do not match this batch")

        x = self.embedding[ids] + self.position[past:past + length][None, :, :]
        new_cache = []
        head_width = self.c.width // self.c.heads

        def split_heads(a):
            return a.reshape(batch, length, self.c.heads, head_width).transpose(0, 2, 1, 3)

        for index, block in enumerate(self.blocks):
            normed = layer_norm(x)
            q = split_heads(normed @ block["q"])
            k = split_heads(normed @ block["k"])
            v = split_heads(normed @ block["v"])
            if cache is not None:
                k = np.concatenate([cache[index][0], k], axis=2)
                v = np.concatenate([cache[index][1], v], axis=2)
            scores = (q @ k.transpose(0, 1, 3, 2)) / np.sqrt(head_width)
            query_positions = past + np.arange(length)
            key_positions = np.arange(past + length)
            allowed = key_positions[None, :] <= query_positions[:, None]
            scores = np.where(allowed[None, None, :, :], scores, -np.inf)
            attended = softmax(scores) @ v
            joined = attended.transpose(0, 2, 1, 3).reshape(batch, length, self.c.width)
            x = x + joined @ block["o"]
            x = x + gelu(layer_norm(x) @ block["up"]) @ block["down"]
            new_cache.append((k, v))
        return layer_norm(x) @ self.output, new_cache

    def parameter_count(self):
        return (self.embedding.size + self.position.size + self.output.size
                + sum(w.size for block in self.blocks for w in block.values()))


def main():
    model = TinyDecoder()
    ids = np.array([[1, 4, 8, 3, 7]])
    full, _ = model.forward(ids)
    cache = None
    chunks = []
    for t in range(ids.shape[1]):
        logits, cache = model.forward(ids[:, t:t + 1], cache)
        chunks.append(logits)
    incremental = np.concatenate(chunks, axis=1)
    cache_error = float(np.max(np.abs(full - incremental)))

    changed = ids.copy()
    changed[:, 3:] = [2, 9]
    changed_logits, _ = model.forward(changed)
    future_error = float(np.max(np.abs(full[:, :3] - changed_logits[:, :3])))

    _, prompt_cache = model.forward(ids[:, :3])
    continuation, _ = model.forward(ids[:, 3:], prompt_cache)
    chunk_error = float(np.max(np.abs(full[:, 3:] - continuation)))
    assert cache_error < 1e-10, "cached decoding differs from full forward"
    assert future_error < 1e-10, "future tokens leaked through the causal mask"
    assert chunk_error < 1e-10, "chunked continuation used incorrect positions"
    print("parameter_count:", model.parameter_count())
    print("logits_shape:", full.shape)
    print("cache_vs_full_max_error:", cache_error)
    print("future_token_leak_max_error:", future_error)
    print("chunked_continuation_max_error:", chunk_error)
    print("cache_bytes_float64:", sum(k.nbytes + v.nbytes for k, v in cache))


if __name__ == "__main__":
    main()
