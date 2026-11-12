# Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation

**Defense working folder: FINAL_PROJECT_MAIN/**. All changes in this pass are confined here. No algorithm logic or notebook cells were changed and no experiments ran.

**Start with:** [ALGORITHM_DEFENSE_GUIDE.md](ALGORITHM_DEFENSE_GUIDE.md), [CODE_MAP.md](CODE_MAP.md), [NOTEBOOK_MAP.md](NOTEBOOK_MAP.md), [RESULTS_INDEX.md](RESULTS_INDEX.md), and [IMPORTANT_NUMBERS.md](IMPORTANT_NUMBERS.md). Dataset/metric details: [DATASET_AND_EXPERIMENT_SETUP.md](DATASET_AND_EXPERIMENT_SETUP.md).

The research story is quantity → identity → granularity → relevance → downstream utility. Final frozen W12 policy: **SFR top-10 → FIXED_SENTENCE → Qwen3-8B BASE_FP16**, evidence budgets 256/1024, no LoRA. QBGF was not promoted universally. BEA/MiniLM are later exploratory work; V2 calibration failed and its tau8e-5 reader branch is post-hoc.

1. [problem and baselines](1_problem_and_baselines/README.md)
2. [adaptive evidence quantity](2_adaptive_evidence_quantity/README.md)
3. [evidence identity and routing](3_evidence_identity_and_routing/README.md)
4. [multigranular evidence study](4_multigranular_evidence_study/README.md)
5. [qbgf](5_qbgf/README.md)
6. [downstream utility attribution](6_downstream_utility_attribution/README.md)
7. [bea v1](7_bea_v1/README.md)
8. [bea v2](8_bea_v2/README.md)
9. [minilm reranker](9_minilm_reranker/README.md)
10. [final method comparison](10_final_method_comparison/README.md)
11. [shared infrastructure](11_shared_infrastructure/README.md)
12. [report support](12_report_support/README.md)

Each method has local numbered code views, configs, untouched notebooks, results and docs where applicable. Code views are internal symlinks to exact canonical modules; no artificial module split or duplicate algorithm implementation was created. Raw/query-level results are retained when available. Top-level src/scripts/results aliases serve compatibility, not primary navigation.

Scientific-status/chronology/cohort documents distinguish validation, freeze, confirmation, post-freeze attribution and post-hoc exploration. The [provenance manifest](PROVENANCE_MANIFEST.csv) records exact source identities and every curated rename.

**Readiness limit:** missing original W12 full validation/confirmation raw shards and attribution perturbation receipts still prevent full independent historical verification. [UNRESOLVED_PROVENANCE.md](UNRESOLVED_PROVENANCE.md) states this explicitly. This pass improves defense navigation; it does not manufacture missing evidence or turn archived notebooks into safe run launchers. Many saved flags already enable full generation/install work; do not Run All for a viva. See DEFENSE_READINESS_REPORT.md.

Baseline references, project adapters/results and local ignore policy are documented in [CLEANUP_AND_BASELINES_REPORT.md](CLEANUP_AND_BASELINES_REPORT.md) and the [baseline library](1_problem_and_baselines/baselines/README.md).

## Source folders named by purpose

See [src/README.md](src/README.md) for the descriptive code layout and preserved historical import links.

## Numbered results and script navigation

See [results/README.md](results/README.md) and [scripts/README.md](scripts/README.md) for chronological names and preserved compatibility paths.
