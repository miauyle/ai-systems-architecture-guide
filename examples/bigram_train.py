"""Manual next-token learning, with an explicit softmax/CE gradient.

This is a bigram model, not a Transformer. Requires NumPy; no network or GPU.
"""
import numpy as np


def prepare():
    corpus = ["春天花开。", "春天雨落。", "夏天花开。", "夏天雨落。"]
    vocab = ["<BOS>", "<EOS>"] + sorted(set("".join(corpus)))
    mapping = {token: i for i, token in enumerate(vocab)}
    pairs = []
    for sentence in corpus:
        ids = [mapping["<BOS>"]] + [mapping[c] for c in sentence] + [mapping["<EOS>"]]
        pairs.extend(zip(ids[:-1], ids[1:]))
    inputs, labels = np.array(pairs).T
    return vocab, inputs, labels


def loss_and_gradient(table, inputs, labels):
    scores = table[inputs]
    shifted = scores - scores.max(axis=1, keepdims=True)
    log_probs = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
    loss = -log_probs[np.arange(len(labels)), labels].mean()
    gradient_rows = np.exp(log_probs)
    gradient_rows[np.arange(len(labels)), labels] -= 1
    gradient_rows /= len(labels)
    gradient_table = np.zeros_like(table)
    np.add.at(gradient_table, inputs, gradient_rows)
    return float(loss), gradient_table


def main():
    vocab, inputs, labels = prepare()
    table = np.zeros((len(vocab), len(vocab)))
    initial, gradient = loss_and_gradient(table, inputs, labels)
    # A finite-difference check validates the manually derived gradient.
    index = (int(inputs[0]), int(labels[0]))
    eps = 1e-5
    plus, minus = table.copy(), table.copy()
    plus[index] += eps
    minus[index] -= eps
    numeric = (loss_and_gradient(plus, inputs, labels)[0]
               - loss_and_gradient(minus, inputs, labels)[0]) / (2 * eps)
    gradient_error = abs(numeric - gradient[index])
    assert gradient_error < 1e-7
    for _ in range(400):
        _, gradient = loss_and_gradient(table, inputs, labels)
        table -= 3.0 * gradient
    final, _ = loss_and_gradient(table, inputs, labels)
    assert final < initial * 0.4
    print("vocab_size:", len(vocab))
    print("training_pairs:", len(labels))
    print("initial_loss:", initial)
    print("final_loss:", final)
    print("finite_difference_gradient_error:", gradient_error)
    token_id = vocab.index("天")
    scores = table[token_id] - table[token_id].max()
    probabilities = np.exp(scores) / np.exp(scores).sum()
    top = np.argsort(-probabilities)[:3]
    print("after_天:", [(vocab[i], round(float(probabilities[i]), 4)) for i in top])


if __name__ == "__main__":
    main()
