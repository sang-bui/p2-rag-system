"""Hybrid retrieval (stage 1): reciprocal rank fusion of bm25 and dense.

Ported from rrf() in the 13 lab's pipeline.py: each item scores the sum of 1 / (60 + rank) over the
rankings it appears in, with rank counted from 1. Full rankings are fused, not top-10 lists, so a
document that is 11th in both arms can still reach the fused top 10.
Settings, all optional, in a [hybrid] table of p2.toml:

    arms = ["bm25", "dense"]     the systems fused, any two or more in p2/retrievers/
    rrf_k = 60                   the constant in 1 / (k + rank)

search fuses document rankings; search_chunks fuses chunk rankings, which `p2 answer` and the
reranker's chunk search use.
"""

from __future__ import annotations

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False


def rrf(rankings, k):
    """Fused (id, score) pairs, best first; each id scores the sum of 1 / (k + rank) over the rankings."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, (item, _score) in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1 / (k + rank)
    return order(scores.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        settings = cfg.table("hybrid")
        self.arms = [retrievers.build(name, corpus, cfg) for name in settings.get("arms", ["bm25", "dense"])]
        self.rrf_k = settings.get("rrf_k", 60)
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text, k):
        return rrf([arm.search(text, self.n_docs) for arm in self.arms], self.rrf_k)[:k]

    def search_chunks(self, text, k):
        return rrf([arm.search_chunks(text, self.n_chunks) for arm in self.arms], self.rrf_k)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
