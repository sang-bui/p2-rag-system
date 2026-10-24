"""Listwise reranking (stage 1): Claude reorders the first stage's top 20.

Ported from rerank_one() in the 13 lab's pipeline.py. The top 20 of the first stage (hybrid by
default) go to Claude as numbered passages cut to 600 characters, the schema forces the reply into
{"order": [20 numbers, each 1 to 20]}, and a reply that is not each number once keeps the first-stage
order. Documents below the 20 keep their first-stage order underneath. Every call goes through
p2.claude.call, which caches replies in .cache/claude/ and records tokens in the run's trace.
Settings, all optional, in a [rerank] table of p2.toml:

    first_stage = "hybrid"
    candidates = 20
    passage_chars = 600

Scores are written so the reranked order is the run order: the item at position i (from 0) scores
1 / (i + 1), the same scale the lab's run files used.
"""

from __future__ import annotations

import sys

from p2 import claude, retrievers

NEEDS_CLAUDE = True

PROMPT = """Below are {n} passages from a document collection, numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def schema(n):
    return {
        "type": "object",
        "properties": {"order": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": n}, "minItems": n, "maxItems": n}},
        "required": ["order"],
    }


class Rerank:
    def __init__(self, corpus, cfg):
        settings = cfg.table("rerank")
        self.corpus = corpus
        self.cfg = cfg
        self.first = retrievers.build(settings.get("first_stage", "hybrid"), corpus, cfg)
        self.candidates = settings.get("candidates", 20)
        self.passage_chars = settings.get("passage_chars", 600)
        self.model = cfg.model
        self.chunk_text = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)

    def rerank(self, text, ranked, passage):
        """ranked: (id, score) pairs best first; passage(id) gives the text Claude sees for an id."""
        top, rest = ranked[: self.candidates], ranked[self.candidates :]
        ids = [item for item, _ in top]
        if len(ids) > 1:
            passages = "\n\n".join(f"[{i}] {passage(item)[: self.passage_chars]}" for i, item in enumerate(ids, 1))
            prompt = PROMPT.format(n=len(ids), query=text, passages=passages)
            reply = claude.call(prompt, schema(len(ids)), model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg))
            got = (reply.output or {}).get("order")
            if isinstance(got, list) and sorted(got) == list(range(1, len(ids) + 1)):
                ids = [ids[i - 1] for i in got]
            else:
                print(f"Note: rerank kept the first-stage order for {text[:60]!r}: {reply.error or got}", file=sys.stderr)
        order = ids + [item for item, _ in rest]
        return [(item, 1 / (i + 1)) for i, item in enumerate(order)]

    def search(self, text, k):
        ranked = self.first.search(text, max(k, self.candidates))
        return self.rerank(text, ranked, lambda d: self.corpus.docs[d].text)[:k]

    def search_chunks(self, text, k):
        ranked = self.first.search_chunks(text, max(k, self.candidates))
        return self.rerank(text, ranked, lambda c: self.chunk_text[c])[:k]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
