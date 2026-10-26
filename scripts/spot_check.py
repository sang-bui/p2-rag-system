"""Gold-set spot check: draw the 20 query-document pairs that eval/own/spot-check.tsv records.

It reads the candidate pool (eval/own/spot-check-pool.tsv) and the labels (eval/own/qrels.txt), draws 10 pairs
labeled relevant and 10 not, with seed 20261026, and shuffles them together. The verdicts in spot-check.tsv were
made by hand from each document's complete abstract with these labels hidden. No Claude calls.

    uv run python scripts/spot_check.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

from p2 import runfile

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261026


def main() -> None:
    with open(ROOT / "eval/own/spot-check-pool.tsv", encoding="utf-8") as f:
        pool = [(r["qid"], r["docid"]) for r in csv.DictReader((line for line in f if not line.startswith("#")), delimiter="\t")]
    qrels, _ = runfile.read_qrels(ROOT / "eval/own/qrels.txt")
    rel = runfile.relevant(qrels)
    pos = [p for p in pool if p[1] in rel.get(p[0], ())]
    neg = [p for p in pool if p[1] not in rel.get(p[0], ())]
    rng = random.Random(SEED)
    pick = rng.sample(pos, 10) + rng.sample(neg, 10)
    rng.shuffle(pick)
    print(f"# {len(pos)} relevant and {len(neg)} other pairs in the pool")
    print("n\tqid\tdocid\toriginal_label")
    for n, (qid, docid) in enumerate(pick, 1):
        print(f"{n}\t{qid}\t{docid}\t{int(docid in rel.get(qid, ()))}")


if __name__ == "__main__":
    main()
