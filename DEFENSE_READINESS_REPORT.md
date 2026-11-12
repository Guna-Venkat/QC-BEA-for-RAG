# Defense-readiness reorganization report

## A. Structure

```text
FINAL_PROJECT_MAIN/
├── CODE_MAP.md / NOTEBOOK_MAP.md / ALGORITHM_DEFENSE_GUIDE.md
├── RESULTS_INDEX.md / IMPORTANT_NUMBERS.md
├── DATASET_AND_EXPERIMENT_SETUP.md
├── 1_problem_and_baselines/
├── 2_adaptive_evidence_quantity/
├── 3_evidence_identity_and_routing/
├── 4_multigranular_evidence_study/
├── 5_qbgf/
├── 6_downstream_utility_attribution/
├── 7_bea_v1/
├── 8_bea_v2/
├── 9_minilm_reranker/
├── 10_final_method_comparison/
├── 11_shared_infrastructure/
└── 12_report_support/
```

Methods expose code/configs/notebooks/results/docs and figures where available. The source package layout is canonical under11_shared_infrastructure/runtime; local numbered code files are internal links to it, not invented algorithm splits.

## B–E. Major moves, code/results and notebooks

Motivation and SARA parent references were combined into1. Earlier week-first experiments map to2–4. QBGF validation/ablation/freeze/confirmation is in5. Attribution/V1/V2/MiniLM/final comparison are in6–10. Shared source/env/audit records and historical report support are11–12.

Examples of canonical code movement:

- shared/runtime/src/week12/algorithm.py →11_shared_infrastructure/runtime/src/week12/algorithm.py; defense view5_qbgf/code/1_qbgf_and_sentence_allocator.py.
- shared/runtime/src/post_w12/bea_qbgf/allocator.py →11_shared_infrastructure/runtime/src/post_w12/bea_qbgf/allocator.py; defense view7_bea_v1/code/1_dynamic_marginal_allocator.py.
- shared/runtime/src/post_w12/bea_v2/models.py →11_shared_infrastructure/runtime/src/post_w12/bea_v2/models.py; defense view8_bea_v2/code/2_group_crossfit_phelp_models.py.
- shared/runtime/W12-POST/reranker_baseline/minilm_reranker.py →11_shared_infrastructure/runtime/W12-POST/reranker_baseline/minilm_reranker.py; defense view9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py.

Key results were numbered in reading order: QBGF validation summary, query-conditioning/primary contrasts, sentence/passage fusion comparisons, frozen policy and reserved confirmation; V1 pilot/expansion/efficiency; V2 predictor metrics/calibration failure/post-hoc reader outcomes; MiniLM quality and final matched quality/efficiency/statistics/winner metadata.

The full actual old→new path and hash log is [defense_reorganization_actions.csv](11_shared_infrastructure/audit/defense_reorganization_actions.csv). It supplies the exact mapping for every moved artifact, including original report/notebook names. No scientific CSV was filtered/rebuilt to imitate a requested filename. Multi-method tables retain all original rows and precision.

Notebook locations and original paths are listed in [NOTEBOOK_MAP.md](NOTEBOOK_MAP.md) and its machine-readable inventory. All original notebook cells, flags, outputs and bytes are unchanged. The final comparison notebook is the same canonical MiniLM notebook, linked from10 for convenience.

## F. Restored missing evidence

Real V1 pilot/expanded query rows and exact150matched source pools were copied read-only from their original results/post_w12/bea_qbgf/v3 namespaces. Pilot/expanded rows live under7_bea_v1/results/5_query_level; matched source pools under11_shared_infrastructure/data/matched_source_pools. Every original/new path, reason and SHA is in [restored_defense_artifacts.csv](11_shared_infrastructure/audit/restored_defense_artifacts.csv). No model/retrieval/statistical result was regenerated.

## G–H. Open these first

| Method | Primary implementation view | Primary stored result | Notebook |
| --- | --- | --- | --- |
| FIXED_SENTENCE | [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py) | [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv) | [3_qbgf_validation_surface.ipynb](5_qbgf/notebooks/3_qbgf_validation_surface.ipynb) |
| QBGF_FULL / QBGF_NO_QUERY | [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py) | [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv) | [5_qbgf_query_and_fusion_ablations.ipynb](5_qbgf/notebooks/5_qbgf_query_and_fusion_ablations.ipynb) |
| BEA_QBGF_V1 | [1_dynamic_marginal_allocator.py](7_bea_v1/code/1_dynamic_marginal_allocator.py) | [1_bea_v1_pilot_quality_results.csv](7_bea_v1/results/1_primary/1_bea_v1_pilot_quality_results.csv) | [1_bea_v1_exploratory_pipeline.ipynb](7_bea_v1/notebooks/1_bea_v1_exploratory_pipeline.ipynb) |
| BEA_V2 | [1_usefulness_weighted_allocator.py](8_bea_v2/code/1_usefulness_weighted_allocator.py) | [1_bea_v2_posthoc_quality_results.csv](8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv) | [1_bea_v2_phelp_and_calibration.ipynb](8_bea_v2/notebooks/1_bea_v2_phelp_and_calibration.ipynb) |
| MINILM_CE_SENTENCE | [1_cross_encoder_sentence_reranker.py](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py) | [1_minilm_matched_quality_results.csv](9_minilm_reranker/results/1_primary/1_minilm_matched_quality_results.csv) | [1_minilm_baseline_comparison.ipynb](9_minilm_reranker/notebooks/1_minilm_baseline_comparison.ipynb) |

Equation→function→line maps are under each central method’s docs/1_equations_to_code.md. CODE_MAP is the quick reference; ALGORITHM_DEFENSE_GUIDE explains equations, steps, complexity, hyperparameters, strengths, limits and forbidden claims. IMPORTANT_NUMBERS contains recorded source-linked defense tables.

## H2. Baseline references and cleanup

Official licensed SARA, RECOMP and LLMLingua source subsets are pinned under1_problem_and_baselines/baselines. Their source hashes/Git blob identities and repository/tree commits are verified separately. Project adaptations and result links are separate from published paper results. RECOMP was not a matched project evaluation; LLMLingua-2 qualification is not a full W12 quality result.

Obsolete generated navigation/audit copies were retired with pre-deletion hashes/reasons in cleanup_retirements.json. Research records, notebooks and fold predictors were not deleted. A local .gitignore excludes regenerable caches and large external checkpoints, not scientific result tables or query-level rows. The parent folder remains ignored by the outer repository until that outer rule is changed separately.

See [CLEANUP_AND_BASELINES_REPORT.md](CLEANUP_AND_BASELINES_REPORT.md) and the [baseline library](1_problem_and_baselines/baselines/README.md).

## I. Remaining problems

Full original W12 C/D validation row directories, reserved-confirmation answer rows and attribution perturbation/generation outputs are missing. Recorded aggregate tables, statistical outputs, original reconstruction/closeout receipts and checksum inventories remain. A code view cannot repair missing historical evidence; independent raw rescoring is blocked until a genuine backup is restored.

External corpora, pinned reader/retriever weights, adapted SARA checkpoint/projector and the historical environment/source revision are not a complete portable bundle. Guarded archived notebooks are not guaranteed fresh launchers; many saved full/install flags are alreadyTrue. Obsolete generated guides/audit generations were removed with explicit retirement receipts; retained source reports can embed historical paths. Current navigation and verifier supersede old instructions.

No central algorithm ownership was invented: method-local files reference their actual shared modules. Byte-identity deduplication is not a claim of statistical/experimental equivalence. No unresolved distinct-result duplicate was silently merged in this pass.

## J. Safety and verification

No files outside FINAL_PROJECT_MAIN were modified, renamed, moved or deleted. Algorithm equations, parameters, tie behavior, datasets, metrics, statistics, prompts, token budgets and result bytes were not changed. Notebooks were not edited or executed. No model, retrieval, calibration, training or statistical experiment ran.

Checks passed: **52/52**; notebook source hashes preserved: **50**; source Python files syntax checked: **398**; real numbered code views: **31**; function/class symbols indexed: **2269**; navigation links checked: **1460**. Detailed checks: [defense_verification_summary.json](11_shared_infrastructure/audit/defense_verification_summary.json).


## K. Assessment

**NO for unconditional readiness as the sole evidence repository for all four requested purposes**, because independent defense of missing historical raw outputs remains limited.

- Presentation navigation: ready, with scientific-status/cohort caveats.
- Code explanation: ready for inspected central algorithms; exact modules/functions/equations are mapped.
- Final report: ready to write a carefully scoped report from recorded sources, explicitly disclosing raw-output gaps.
- Results defense: recorded tables/statistics can be shown and matched exploratory rows verified; full original W12/confirmation row-level verification remains incomplete.

The navigation problem is addressed. Missing historical evidence was documented rather than fabricated.
