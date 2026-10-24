"""Ablation variant of rerank: the same Claude reranker over 20 candidates, but the 20 come from
alternating bm25's and dense's rankings (p2/retrievers/_interleave.py) instead of hybrid's RRF fusion.

One thing changes, how the candidates are chosen; the prompt, model, passage length and candidate
count stay those of rerank.py. Run it only as an ablation:
    uv run p2 run --corpus own --system rerank_interleave --ablation
"""

from __future__ import annotations

from p2.retrievers._interleave import Interleave
from p2.retrievers.rerank import Rerank

NEEDS_CLAUDE = True
BASE = "rerank"


def build(corpus, cfg):
    return Rerank(corpus, cfg, first=Interleave(corpus, cfg))
