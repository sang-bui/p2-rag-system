"""How much bm25's and dense's top 10s overlap, per query and per class, on the shared and own corpora.

For each query: the intersection size of the two top-10 document lists and their Jaccard similarity
(intersection over union). No Claude calls. On sets with judgments, it also prints hybrid's MRR@10
minus the better of bm25 and dense, next to the overlap, as a comparison, not a cause.

    uv run python scripts/arm_overlap.py
"""

from __future__ import annotations

import statistics as st
from collections import defaultdict
from pathlib import Path

from p2 import config, corpus, retrievers, runfile

ROOT = Path(__file__).resolve().parents[1]


def rr(ranked, rel):
    return next((1 / i for i, d in enumerate(ranked[:10], 1) if d in rel), 0.0)


def main() -> None:
    cfg = config.load(ROOT)
    sets = [
        ("shared", "practice", ROOT / "eval/shared/practice.queries.tsv", ROOT / "eval/shared/practice.qrels.txt"),
        ("shared", "test", ROOT / "eval/shared/test.queries.tsv", None),
        ("own", "own", ROOT / "eval/own/queries.tsv", ROOT / "eval/own/qrels.txt"),
    ]
    for name, label, qpath, rpath in sets:
        c = corpus.load(ROOT, name)
        bm, de, hy = (retrievers.build(s, c, cfg) for s in ("bm25", "dense", "hybrid"))
        queries, _ = runfile.read_queries(qpath, require_origin=(name == "own"))
        rel = runfile.relevant(runfile.read_qrels(rpath)[0]) if rpath else None
        by = defaultdict(list)
        for q in queries:
            b = [d for d, _ in bm.search(q.text, 10)]
            d = [d for d, _ in de.search(q.text, 10)]
            inter = len(set(b) & set(d))
            jac = inter / len(set(b) | set(d))
            gap = None
            if rel is not None:
                r = rel.get(q.qid, set())
                h = [x for x, _ in hy.search(q.text, 10)]
                gap = rr(h, r) - max(rr(b, r), rr(d, r))
            for key in (q.cls, "all"):
                by[key].append((inter, jac, gap))
        print(f"\n{name} corpus, {label} queries ({len(queries)})")
        print("class        queries  mean shared in top 10  median  mean Jaccard" + ("  hybrid MRR minus better arm" if rel is not None else ""))
        for key in ("identifier", "paraphrase", "mixed", "all"):
            rows = by[key]
            line = f"{key:<12} {len(rows):>7}  {st.mean(x[0] for x in rows):>21.2f}  {st.median(x[0] for x in rows):>6}  {st.mean(x[1] for x in rows):>12.3f}"
            if rel is not None:
                line += f"  {st.mean(x[2] for x in rows):>+28.3f}"
            print(line)


if __name__ == "__main__":
    main()
