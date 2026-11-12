# Project map

| Research question | Folder | Open during defense |
| --- | --- | --- |
| How does simple sentence selection work? | [README.md](5_qbgf/README.md) | [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py) → [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv) |
| Where is QBGF / MCKP / NO_QUERY? | [README.md](5_qbgf/README.md) | [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py) → [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv) |
| Where are coverage, redundancy and stopping? | [README.md](7_bea_v1/README.md) | [1_dynamic_marginal_allocator.py](7_bea_v1/code/1_dynamic_marginal_allocator.py) → [1_bea_v1_pilot_quality_results.csv](7_bea_v1/results/1_primary/1_bea_v1_pilot_quality_results.csv) |
| Where is P_help, calibration failure and post-hoc V2? | [README.md](8_bea_v2/README.md) | [1_usefulness_weighted_allocator.py](8_bea_v2/code/1_usefulness_weighted_allocator.py) → [1_bea_v2_posthoc_quality_results.csv](8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv) |
| Where is static cross-encoder scoring and packing? | [README.md](9_minilm_reranker/README.md) | [1_cross_encoder_sentence_reranker.py](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py) → [1_minilm_matched_quality_results.csv](9_minilm_reranker/results/1_primary/1_minilm_matched_quality_results.csv) |

Early problem/SARA, adaptive quantity and identity/routing history are in1–3; systematic granularity in4; downstream utility diagnosis in6; one canonical final comparison in10. Shared imports/data/tokenization/reader/evaluation remain in11; provenance reports and retained historical prose in12.

The exact equation-to-function maps are local docs/1_equations_to_code.md. CODE_MAP.md is the complete shortcut list; NOTEBOOK_MAP.md inventories unchanged execution switches. No universal winner is implied by this organization.
