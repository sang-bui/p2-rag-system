"""Ablation variant of dense: the same chunks and cosine search, with potion-retrieval-32M in place of bge-small.

One thing changes, the embedder; chunking, query handling and scoring stay those of dense.py.
Run it only as an ablation: uv run p2 run --corpus own --system dense_potion --ablation
"""

from __future__ import annotations

from p2 import embed
from p2.retrievers.dense import Dense

NEEDS_CLAUDE = False
BASE = "dense"


def build(corpus, cfg):
    return Dense(corpus, cfg, model=embed.POTION)
