"""A first stage for rerank_interleave: alternate between two systems' rankings instead of fusing them.

Take bm25's #1, then dense's #1, then bm25's #2, dense's #2, and so on, skipping anything already taken.
Unlike reciprocal rank fusion, an item that only one arm ranks highly keeps its place near the top, so
each arm's best candidates reach the reranker's top 20. The candidate count stays the same as hybrid's.
Scores are 1 / (position + 1), so the interleaved order is the ranking order.
"""

from __future__ import annotations

from p2 import retrievers


def interleave(rankings):
    """One ranking from several: their items taken in turn, best first, each item once."""
    out, seen = [], set()
    for row in zip(*rankings):
        for item, _score in row:
            if item not in seen:
                seen.add(item)
                out.append(item)
    for ranking in rankings:  # the tails of any longer rankings
        for item, _score in ranking:
            if item not in seen:
                seen.add(item)
                out.append(item)
    return [(item, 1 / (i + 1)) for i, item in enumerate(out)]


class Interleave:
    def __init__(self, corpus, cfg, arms=("bm25", "dense")):
        self.arms = [retrievers.build(name, corpus, cfg) for name in arms]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text, k):
        return interleave([arm.search(text, self.n_docs) for arm in self.arms])[:k]

    def search_chunks(self, text, k):
        return interleave([arm.search_chunks(text, self.n_chunks) for arm in self.arms])[:k]
