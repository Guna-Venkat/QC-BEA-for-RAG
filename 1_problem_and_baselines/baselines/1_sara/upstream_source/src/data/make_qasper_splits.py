"""Create a leakage-safe, document-level QASPER train/dev split (release plan §6).

QASPER has many questions per paper, so a question-level random split would put the same paper in both
train and dev. We split by paper (``example_id``) deterministically and carve a dev set out of the
official train file. The official test file (``QASPER_test.jsonl``) is left untouched.

Outputs (under ``data/``):
- ``data/reformatted/QASPER_train_split.jsonl``  (train minus dev papers)
- ``data/reformatted/QASPER_dev.jsonl``          (held-out dev papers)
- ``data/manifests/qasper_split.json``           (paper-id manifest + zero-overlap assertion record)

Run: ``python -m src.data.make_qasper_splits --dev-frac 0.1 --seed 42``
"""

from __future__ import annotations

import argparse
import json
import os
import random
from collections import defaultdict

TRAIN = "data/reformatted/QASPER_train.jsonl"
TEST = "data/reformatted/QASPER_test.jsonl"
TRAIN_OUT = "data/reformatted/QASPER_train_split.jsonl"
DEV_OUT = "data/reformatted/QASPER_dev.jsonl"
MANIFEST = "data/manifests/qasper_split.json"


def _read(path):
    return [json.loads(l) for l in open(path)]


def _write(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-frac", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rows = _read(TRAIN)
    by_paper = defaultdict(list)
    for r in rows:
        by_paper[str(r["example_id"])].append(r)
    papers = sorted(by_paper.keys(), key=lambda x: int(x) if x.isdigit() else x)

    rng = random.Random(args.seed)
    shuffled = papers[:]
    rng.shuffle(shuffled)
    n_dev = max(1, int(round(len(shuffled) * args.dev_frac)))
    dev_papers = set(shuffled[:n_dev])
    train_papers = set(shuffled[n_dev:])

    # Document-level disjointness (release plan §6).
    assert train_papers.isdisjoint(dev_papers), "train/dev paper overlap!"

    train_rows = [r for p in train_papers for r in by_paper[p]]
    dev_rows = [r for p in dev_papers for r in by_paper[p]]
    _write(train_rows, TRAIN_OUT)
    _write(dev_rows, DEV_OUT)

    manifest = {
        "seed": args.seed, "dev_frac": args.dev_frac,
        "n_papers_total": len(papers), "n_papers_train": len(train_papers),
        "n_papers_dev": len(dev_papers),
        "n_rows_train": len(train_rows), "n_rows_dev": len(dev_rows),
        "n_rows_test": len(_read(TEST)),
        "train_paper_ids": sorted(train_papers, key=lambda x: int(x) if x.isdigit() else x),
        "dev_paper_ids": sorted(dev_papers, key=lambda x: int(x) if x.isdigit() else x),
        "overlap_train_dev": sorted(train_papers & dev_papers),
        "note": "Document-level split by example_id (paper). Test file is the official QASPER test split.",
    }
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"train: {len(train_papers)} papers / {len(train_rows)} rows -> {TRAIN_OUT}")
    print(f"dev:   {len(dev_papers)} papers / {len(dev_rows)} rows -> {DEV_OUT}")
    print(f"manifest -> {MANIFEST}; overlap = {len(train_papers & dev_papers)}")


if __name__ == "__main__":
    main()
