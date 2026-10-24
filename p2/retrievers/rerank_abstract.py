"""Ablation variant of rerank: the same reranker, but each passage Claude sees is the paper's title
once plus its abstract, without the citation header (the repeated title, authors, journal, DOI and
license URL) that the own-corpus documents start with.

One thing changes, the text of each passage. The candidates (hybrid's top 20, in the same order),
the prompt, the model and the 600-character limit stay those of rerank.py. A document without a
citation header, such as a 30 CFR section, is passed through unchanged.
Run it only as an ablation:
    uv run p2 run --corpus own --system rerank_abstract --ablation
"""

from __future__ import annotations

import re

from p2.retrievers.rerank import Rerank

NEEDS_CLAUDE = True
BASE = "rerank"

HEADER_END = re.compile(r"^Published in .*License: \S+\s*$", re.M)


def without_header(title: str, text: str) -> str:
    """The title once, then the text after the citation header; the text unchanged if it has no header."""
    end = HEADER_END.search(text)
    if not end:
        return text
    body = re.sub(r"^Abstract\.?\s*", "", text[end.end() :].strip())
    return f"{title}\n\n{body}"


class RerankAbstract(Rerank):
    def search(self, text, k):
        ranked = self.first.search(text, max(k, self.candidates))
        docs = self.corpus.docs
        return self.rerank(text, ranked, lambda d: without_header(docs[d].title, docs[d].text))[:k]

    def search_chunks(self, text, k):
        ranked = self.first.search_chunks(text, max(k, self.candidates))
        docs = self.corpus.docs
        return self.rerank(text, ranked, lambda c: without_header(docs[c.rsplit("#", 1)[0]].title, self.chunk_text[c]))[:k]


def build(corpus, cfg):
    return RerankAbstract(corpus, cfg)
