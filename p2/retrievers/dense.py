"""Dense retrieval (stage 1): embed every chunk once, embed the query, and rank chunks by cosine similarity.

Ported from the 12 lab's dense_rankings (retrieve.py). The embedder is bge-small-en-v1.5 by default,
the model whose fusion with bm25 measured best in the 13 lab (rrf_bge MRR 0.83 against rrf_potion 0.76).
Settings, all optional, in a [dense] table of p2.toml:

    model = "BAAI/bge-small-en-v1.5"     any name p2.embed.load() accepts
    query_prefix = ""                    text put before every query, such as bge's search instruction

Chunk vectors are cached in .cache/vectors/ by p2.embed.doc_vectors, and every vector has length 1,
so one matrix-vector product gives the cosine similarity of the query with every chunk.
"""

from __future__ import annotations

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        settings = cfg.table("dense")
        self.model = settings.get("model", embed.BGE)
        self.query_prefix = settings.get("query_prefix", "")
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text):
        if not self.chunks:
            return []
        query = self.embedder.encode([self.query_prefix + text])[0]
        return self.vectors @ query


def build(corpus, cfg):
    return Dense(corpus, cfg)
