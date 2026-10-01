"""A local BM25 retrieval fixture with eligibility filters and evidence IDs.

Terms are manually annotated to isolate retrieval math. This is not a Chinese
tokenizer, an embedding model, or an LLM answer generator.
"""
import json
import math
from collections import Counter


DOCUMENTS = [
    {"id": "travel-2026#hotel", "org": "org-a", "from": "2026-01-01", "to": "2027-01-01",
     "source": "差旅制度", "version": "2026", "terms": ["上海", "住宿", "上限", "含税"],
     "text": "上海住宿报销上限为每人每晚800元，含税；超出部分需事前审批。"},
    {"id": "travel-2026#meal", "org": "org-a", "from": "2026-01-01", "to": "2027-01-01",
     "source": "差旅制度", "version": "2026", "terms": ["上海", "餐费", "上限"],
     "text": "上海餐费报销上限为每人每天120元。"},
    {"id": "travel-2025#hotel", "org": "org-a", "from": "2025-01-01", "to": "2026-01-01",
     "source": "差旅制度", "version": "2025", "terms": ["上海", "住宿", "上限"],
     "text": "上海住宿报销上限为每人每晚600元。"},
    {"id": "org-b#hotel", "org": "org-b", "from": "2026-01-01", "to": "2027-01-01",
     "source": "其他组织制度", "version": "2026", "terms": ["上海", "住宿", "上限", "上海", "住宿", "上限"],
     "text": "上海住宿上限为每人每晚1000元。"},
]


def eligible(documents, org, date):
    # Organization identity comes from authenticated application state.
    # ISO dates, and a half-open validity interval: from <= date < to.
    return [doc for doc in documents
            if doc["org"] == org and doc["from"] <= date < doc["to"]]


def bm25(documents, query, k1=1.2, b=.75):
    if not documents:
        return []
    counts = [Counter(doc["terms"]) for doc in documents]
    size = len(documents)
    average_length = sum(len(doc["terms"]) for doc in documents) / size
    results = []
    for doc, frequency in zip(documents, counts):
        score = 0.0
        for term in dict.fromkeys(query):
            df = sum(term in count for count in counts)
            idf = math.log(1 + (size - df + .5) / (df + .5))
            tf = frequency[term]
            denominator = tf + k1 * (1 - b + b * len(doc["terms"]) / average_length)
            score += idf * tf * (k1 + 1) / denominator
        results.append({"id": doc["id"], "score": score,
                        "text": doc["text"], "source": doc["source"], "version": doc["version"]})
    return sorted(results, key=lambda row: (-row["score"], row["id"]))


def main():
    query = ["上海", "住宿", "上限"]
    candidates = eligible(DOCUMENTS, "org-a", "2026-10-01")
    ranked = bm25(candidates, query)
    assert ranked[0]["id"] == "travel-2026#hotel"
    assert {row["id"] for row in ranked} == {"travel-2026#hotel", "travel-2026#meal"}
    assert eligible(DOCUMENTS, "unknown-org", "2026-10-01") == []
    assert {doc["id"] for doc in eligible(DOCUMENTS, "org-a", "2026-01-01")} == {
        "travel-2026#hotel", "travel-2026#meal"}
    print(json.dumps({"query_terms": query, "candidate_count": len(candidates),
                      "ranking": ranked, "unfiltered_top": bm25(DOCUMENTS, query)[0]["id"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
