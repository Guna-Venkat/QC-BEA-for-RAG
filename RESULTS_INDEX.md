# Results defense index

Every primary/statistics entry below links to exact stored source bytes. No filtered scientific CSV was fabricated to imitate the suggested filenames. A single real table can contain several methods/contrasts; use the specified row selectors.

| Experiment / method | Datasets | Budget | Status | Primary results | Statistics | Figures | Code | Notebook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FIXED_SENTENCE | QASPER / HotpotQA / SciFact | 256/1024 | W12 validation; frozen final policy; reserved confirmation separately reported | [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv) | [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv) | [figures](5_qbgf/figures) | [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py) | [3_qbgf_validation_surface.ipynb](5_qbgf/notebooks/3_qbgf_validation_surface.ipynb) |
| QBGF_FULL / QBGF_NO_QUERY | QASPER / HotpotQA / SciFact | 256/1024 | W12 validation and ablation; not the universally frozen final policy | [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv) | [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv) | [figures](5_qbgf/figures) | [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py) | [5_qbgf_query_and_fusion_ablations.ipynb](5_qbgf/notebooks/5_qbgf_query_and_fusion_ablations.ipynb) |
| BEA_QBGF_V1 | QASPER / HotpotQA / SciFact | 256/1024 | POST-W12 exploratory; pilot50/dataset and expansion150/dataset are distinct | [1_bea_v1_pilot_quality_results.csv](7_bea_v1/results/1_primary/1_bea_v1_pilot_quality_results.csv) | [1_bea_v1_pilot_paired_tests.csv](7_bea_v1/results/3_statistics/1_bea_v1_pilot_paired_tests.csv) | No figure required; inspect source table | [1_dynamic_marginal_allocator.py](7_bea_v1/code/1_dynamic_marginal_allocator.py) | [1_bea_v1_exploratory_pipeline.ipynb](7_bea_v1/notebooks/1_bea_v1_exploratory_pipeline.ipynb) |
| BEA_V2 | QASPER / HotpotQA / SciFact | 256/1024 | Official calibration failed; tau8e-5 reader study is a separate post-hoc exploratory branch | [1_bea_v2_posthoc_quality_results.csv](8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv) | [2_bea_v2_posthoc_paired_tests.csv](8_bea_v2/results/3_posthoc_reader_run/2_bea_v2_posthoc_paired_tests.csv) | No figure required; inspect source table | [1_usefulness_weighted_allocator.py](8_bea_v2/code/1_usefulness_weighted_allocator.py) | [1_bea_v2_phelp_and_calibration.ipynb](8_bea_v2/notebooks/1_bea_v2_phelp_and_calibration.ipynb) |
| MINILM_CE_SENTENCE | QASPER / HotpotQA / SciFact | 256/1024 | POST_W12_RERANKER_BASELINE_EXPLORATORY; shared 50 queries per dataset | [1_minilm_matched_quality_results.csv](9_minilm_reranker/results/1_primary/1_minilm_matched_quality_results.csv) | [3_paired_statistical_comparisons.csv](10_final_method_comparison/results/3_paired_statistical_comparisons.csv) | No figure required; inspect source table | [1_cross_encoder_sentence_reranker.py](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py) | [1_minilm_baseline_comparison.ipynb](9_minilm_reranker/notebooks/1_minilm_baseline_comparison.ipynb) |
| QBGF sentence-only / passage-only fusion ablations | Three datasets | 256/1024 | W12 validation ablation | [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); filter method | [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv) | Source tables are canonical | [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py) → options | [5_qbgf_query_and_fusion_ablations.ipynb](5_qbgf/notebooks/5_qbgf_query_and_fusion_ablations.ipynb) |
| Reserved frozen confirmation | Hotpot200 / SciFact50 / QASPER0 | 256/1024 | Reserved confirmation; raw rows unavailable | [1_frozen_system_confirmation_results.csv](5_qbgf/results/5_reserved_confirmation/1_frozen_system_confirmation_results.csv) | [2_confirmation_paired_tests.csv](5_qbgf/results/5_reserved_confirmation/2_confirmation_paired_tests.csv) | See method figures | [confirmation_runner.py](11_shared_infrastructure/runtime/src/week12_confirmation/confirmation_runner.py) | [8_reserved_confirmation.ipynb](5_qbgf/notebooks/8_reserved_confirmation.ipynb) |
| BEA-V1 expansion | 150 queries per dataset, includes pilot | 256/1024 | Exploratory expansion, not new holdout | [1_bea_v1_expanded_quality_results.csv](7_bea_v1/results/2_expanded/1_bea_v1_expanded_quality_results.csv) | [paired_comparisons.csv](7_bea_v1/results/2_expanded/paired_comparisons.csv) | Source reports | [1_dynamic_marginal_allocator.py](7_bea_v1/code/1_dynamic_marginal_allocator.py) | [1_bea_v1_exploratory_pipeline.ipynb](7_bea_v1/notebooks/1_bea_v1_exploratory_pipeline.ipynb) |

## Exact row selectors

- W12 validation summary: dataset, budget, method, reader. Filter QBGF_FULL, QBGF_NO_QUERY, QBGF_SENTENCE_ONLY or QBGF_PASSAGE_ONLY; do not substitute a matched-pilot score.
- Query-conditioning contrasts: left=QBGF_FULL, right=QBGF_NO_QUERY in [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv). The same file contains other registered primary contrasts.
- Fusion: QBGF_FULL−QBGF_SENTENCE_ONLY and −QBGF_PASSAGE_ONLY in [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv). Keep stored joint-family corrections.
- Confirmation: five frozen systems, two budgets and two datasets in [1_frozen_system_confirmation_results.csv](5_qbgf/results/5_reserved_confirmation/1_frozen_system_confirmation_results.csv).
- Matched comparison: same 50 queries per dataset for all five methods in [1_quality_comparison.csv](10_final_method_comparison/results/1_quality_comparison.csv); exact precision in [1_minilm_matched_quality_results.csv](9_minilm_reranker/results/1_primary/1_minilm_matched_quality_results.csv) and [1_bea_v2_posthoc_quality_results.csv](8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv). Display CSV retains recorded markdown emphasis/four-decimal formatting.
- Query-level controls/V2 answers are under8_bea_v2/results/3_posthoc_reader_run/rows; MiniLM rows under9_minilm_reranker/results/4_diagnostics/rows; V1 original pilot/expanded rows under7_bea_v1/results/5_query_level.

## Final comparison

| Dataset | Budget | FIXED_SENTENCE | QBGF_FULL | BEA-V1 | BEA-V2 post-hoc | MiniLM | Descriptive point winner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HotpotQA | 256 | 0.3661 | 0.4042 | 0.2976 | **0.4352** | 0.3404 | BEA-V2 |
| HotpotQA | 1024 | 0.3893 | 0.4020 | 0.3441 | **0.4234** | 0.3618 | BEA-V2 |
| QASPER | 256 | **0.2668** | 0.2641 | 0.1868 | 0.2618 | 0.2641 | FIXED |
| QASPER | 1024 | 0.2896 | **0.2964** | 0.2084 | 0.2904 | 0.2827 | QBGF |
| SciFact | 256 | 0.6289 | 0.5310 | 0.6127 | 0.5522 | **0.6855** | MiniLM Reranker |
| SciFact | 1024 | 0.5533 | 0.5881 | 0.6432 | 0.5772 | **0.6479** | MiniLM Reranker |

Every MiniLM Holm-adjusted p-value in [3_paired_statistical_comparisons.csv](10_final_method_comparison/results/3_paired_statistical_comparisons.csv) exceeds.05. Do not treat descriptive winners as significance. See IMPORTANT_NUMBERS.md for source-linked defense tables, PROVENANCE_MANIFEST.csv for source paths/SHA, and UNRESOLVED_PROVENANCE.md for missing historical raw outputs.

## Original baselines and recorded baseline outcomes

[Baseline results index](1_problem_and_baselines/baselines/BASELINE_RESULTS_INDEX.md) links actual matched RAG and specialist SARA records. Published-paper outcomes are isolated in per-baseline PAPER_RESULTS_REFERENCE.md files; RECOMP and qualified-only LLMLingua do not receive invented project scores.

## Numbered results and script navigation

See [results/README.md](results/README.md) and [scripts/README.md](scripts/README.md) for chronological names and preserved compatibility paths.
