# Cohort map

See DATASET_AND_EXPERIMENT_SETUP.md for exact W12 counts and grouping. The frozen split is [w12_split_freeze.json](5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json).

- W12 VAL: Hotpot7155, QASPER1005, SciFact177.
- Reserved confirmation: Hotpot200/200groups, SciFact50/43groups, QASPER0.
- LOO/V1 pilot/V2/MiniLM: same 50 queries per dataset from VAL; four-method post-hoc1200rows plus MiniLM300rows.
- V1 expansion:150 queries per dataset, includes pilot, still VAL.
- Qualitative cases: retrospective subset, not prevalence estimates.

Original TRAIN/VAL/CONFIRM IDs and group assignments were not regenerated. Full VAL, confirmation and matched pilot cannot be treated as paired cohorts.
