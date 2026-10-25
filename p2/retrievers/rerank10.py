"""Cheaper variant of rerank for stretch option 3: the same reranker over hybrid's top 10 instead of 20.

Half the candidates per Claude call. In the measured practice run that saved only about 20% of the input
tokens (6,211 against 7,740 per query), because the fixed prompt overhead stays the same. Everything else
is rerank.py's.
Run it on the shared practice queries:
    uv run p2 run --corpus shared --queries practice --system rerank10
"""

from __future__ import annotations

from p2.retrievers.rerank import Rerank

NEEDS_CLAUDE = True
BASE = "rerank"


def build(corpus, cfg):
    return Rerank(corpus, cfg, candidates=10)
