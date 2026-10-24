"""Candidate recall: the share of each own-corpus query's relevant papers that reach the reranker's top 20.

It splits misses into candidate-generation failures (a relevant paper never reaches the 20 the reranker
sees) and leaves ranking failures to the scored runs. It compares hybrid's top 20 (what rerank sees)
with the interleaved top 20 (what rerank_interleave sees). No Claude calls.
It reads eval/own/qrels.txt, so it scores the own corpus: run it only after DECISIONS.md prompt 1 is committed.

    uv run python scripts/candidate_recall.py
"""

from __future__ import annotations

from pathlib import Path

from p2 import config, corpus, retrievers, runfile
from p2.retrievers._interleave import Interleave

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    cfg = config.load(ROOT)
    own = corpus.load(ROOT, "own")
    queries, _ = runfile.read_queries(ROOT / "eval/own/queries.tsv", require_origin=True)
    qrels, _ = runfile.read_qrels(ROOT / "eval/own/qrels.txt")
    rel = runfile.relevant(qrels)
    pools = {"hybrid top 20": retrievers.build("hybrid", own, cfg), "interleave top 20": Interleave(own, cfg)}
    print("qid\tclass\trelevant\t" + "\t".join(pools))
    totals = {name: [0, 0] for name in pools}
    for q in queries:
        r = rel.get(q.qid, set())
        row = []
        for name, system in pools.items():
            got = len(r & {d for d, _ in system.search(q.text, 20)})
            totals[name][0] += got
            totals[name][1] += len(r)
            row.append(f"{got}/{len(r)}")
        print(f"{q.qid}\t{q.cls}\t{len(r)}\t" + "\t".join(row))
    for name, (got, n) in totals.items():
        print(f"{name}: {got} of {n} relevant papers reach the reranker ({got / n:.1%})")


if __name__ == "__main__":
    main()
