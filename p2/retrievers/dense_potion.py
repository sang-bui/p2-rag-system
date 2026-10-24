"""Ablation variant of dense: the same chunks and cosine search, with potion-retrieval-32M in place of bge-small.

One thing changes, the embedder; chunking, query handling and scoring stay those of dense.py.
Run it only as an ablation: uv run p2 run --corpus own --system dense_potion --ablation
"""

from __future__ import annotations

from p2 import embed
from p2.retrievers.dense import Dense

NEEDS_CLAUDE = False
BASE = "dense"


class DensePotion(Dense):
    def __init__(self, corpus, cfg):
        super(Dense, self).__init__(corpus, cfg)
        self.model = embed.POTION
        self.query_prefix = cfg.table("dense").get("query_prefix", "")
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)


def build(corpus, cfg):
    return DensePotion(corpus, cfg)
