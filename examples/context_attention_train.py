"""Train last-position causal attention on a controlled context-copy task.

Only NumPy is required. This is an attention-only conditional next-token
model, without Transformer normalization/FFN/residual blocks or a tokenizer.
It learns on synthetic IDs; it is not a pretrained language model.
"""
import itertools
import numpy as np


def softmax(x):
    exp = np.exp(x - x.max(axis=-1, keepdims=True))
    return exp / exp.sum(axis=-1, keepdims=True)


def data(seed=17):
    # Labels 0..3, nuisance tokens 4..7, and a shared query token 8.
    # Training and test contain disjoint prefixes and equal label counts.
    rng = np.random.default_rng(seed)
    nuisance = np.array(list(itertools.product(range(4, 8), repeat=3)))
    train_x, train_y, test_x, test_y = [], [], [], []
    for label in range(4):
        order = rng.permutation(len(nuisance))
        for number, row in enumerate(order):
            x = [label, *nuisance[row], 8]
            if number < 48:
                train_x.append(x)
                train_y.append(label)
            else:
                test_x.append(x)
                test_y.append(label)
    return tuple(np.asarray(v, dtype=np.int64) for v in
                 (train_x, train_y, test_x, test_y))


class AttentionModel:
    def __init__(self, seed=23, width=16):
        self.width = width
        rng = np.random.default_rng(seed)
        self.params = {
            "E": rng.normal(0, .2, (9, width)),
            "P": rng.normal(0, .2, (5, width)),
            "Wq": rng.normal(0, .2, (width, width)),
            "Wk": rng.normal(0, .2, (width, width)),
            "Wv": rng.normal(0, .2, (width, width)),
            "Wo": rng.normal(0, .2, (width, 9)),
        }

    def forward(self, ids):
        p = self.params
        x = p["E"][ids] + p["P"][None, :, :]
        q = x[:, -1] @ p["Wq"]
        k, v = x @ p["Wk"], x @ p["Wv"]
        scores = np.einsum("bd,btd->bt", q, k) / np.sqrt(self.width)
        weights = softmax(scores)
        z = np.einsum("bt,btd->bd", weights, v)
        logits = z @ p["Wo"]
        return logits, (x, q, k, v, weights, z)

    def loss_and_grad(self, ids, targets):
        logits, (x, q, k, v, weights, z) = self.forward(ids)
        # Compute loss from log-softmax, without log(0) or probability clipping.
        shifted = logits - logits.max(axis=-1, keepdims=True)
        log_probs = shifted - np.log(np.exp(shifted).sum(axis=-1, keepdims=True))
        count = len(ids)
        loss = -log_probs[np.arange(count), targets].mean()
        dl = np.exp(log_probs)
        dl[np.arange(count), targets] -= 1
        dl /= count
        p = self.params
        grad = {"Wo": z.T @ dl}
        dz = dl @ p["Wo"].T
        dv = weights[:, :, None] * dz[:, None, :]
        da = np.einsum("bd,btd->bt", dz, v)
        ds = weights * (da - (da * weights).sum(axis=-1, keepdims=True))
        scale = np.sqrt(self.width)
        dq = np.einsum("bt,btd->bd", ds, k) / scale
        dk = ds[:, :, None] * q[:, None, :] / scale
        flat_x = x.reshape(-1, self.width)
        grad["Wq"] = x[:, -1].T @ dq
        grad["Wk"] = flat_x.T @ dk.reshape(-1, self.width)
        grad["Wv"] = flat_x.T @ dv.reshape(-1, self.width)
        dx = dk @ p["Wk"].T + dv @ p["Wv"].T
        dx[:, -1] += dq @ p["Wq"].T
        grad["P"] = dx.sum(axis=0)
        grad["E"] = np.zeros_like(p["E"])
        np.add.at(grad["E"], ids, dx)
        return float(loss), grad


def gradient_check(model, ids, targets):
    """Check sampled coordinates in every parameter against central differences."""
    _, analytic = model.loss_and_grad(ids, targets)
    rng = np.random.default_rng(31)
    errors = []
    epsilon = 1e-5
    for name, parameter in model.params.items():
        for flat_index in rng.choice(parameter.size, size=6, replace=False):
            index = np.unravel_index(flat_index, parameter.shape)
            old = parameter[index]
            parameter[index] = old + epsilon
            plus, _ = model.loss_and_grad(ids, targets)
            parameter[index] = old - epsilon
            minus, _ = model.loss_and_grad(ids, targets)
            parameter[index] = old
            numeric = (plus - minus) / (2 * epsilon)
            errors.append(abs(numeric - analytic[name][index]))
    maximum = max(errors)
    assert maximum < 1e-7, maximum
    return maximum


def train(model, ids, targets, steps=350, learning_rate=.02):
    # Full-batch Adam: moments, bias correction, then parameter update.
    # No weight decay: this deliberately differs from AdamW.
    first = {name: np.zeros_like(p) for name, p in model.params.items()}
    second = {name: np.zeros_like(p) for name, p in model.params.items()}
    records = []
    for step in range(1, steps + 1):
        loss, gradients = model.loss_and_grad(ids, targets)
        if step in (1, 10, 50, 100, steps):
            records.append((step, loss))
        for name, parameter in model.params.items():
            gradient = gradients[name]
            first[name] = .9 * first[name] + .1 * gradient
            second[name] = .999 * second[name] + .001 * gradient ** 2
            m = first[name] / (1 - .9 ** step)
            v = second[name] / (1 - .999 ** step)
            parameter -= learning_rate * m / (np.sqrt(v) + 1e-8)
    return records


def main():
    train_x, train_y, test_x, test_y = data()
    assert not (set(map(tuple, train_x)) & set(map(tuple, test_x)))
    assert np.array_equal(np.bincount(train_y), np.full(4, 48))
    assert np.array_equal(np.bincount(test_y), np.full(4, 16))
    # Every prefix ends in 8, so any last-token-only predictor has this bound.
    print("bigram test ceiling: 0.250000; optimal loss: 1.386294")
    model = AttentionModel()
    error = gradient_check(model, train_x[[0, 49, 98, 147]], train_y[[0, 49, 98, 147]])
    print(f"gradient maximum absolute error: {error:.3e}")
    for step, loss in train(model, train_x, train_y):
        print(f"step {step:3d}, pre-update train loss {loss:.6f}")
    test_loss, _ = model.loss_and_grad(test_x, test_y)
    logits, cache = model.forward(test_x)
    accuracy = (logits.argmax(axis=-1) == test_y).mean()
    changed = test_x.copy()
    changed[:, 0] = (changed[:, 0] + 1) % 4
    changed_predictions = model.forward(changed)[0].argmax(axis=-1)
    prediction_change = np.mean(logits.argmax(axis=-1) != changed_predictions)
    print(f"held-out prefixes: {len(test_y)}; test loss: {test_loss:.6f}; accuracy: {accuracy:.6f}")
    print(f"mean attention on position 0: {cache[4][:, 0].mean():.6f}")
    print(f"prediction changes when remembered token changes: {prediction_change:.6f}")
    print(f"parameters: {sum(p.size for p in model.params.values())}")
    assert accuracy > .95
    assert prediction_change > .95
    assert np.mean(changed_predictions == changed[:, 0]) > .95


if __name__ == "__main__":
    main()
