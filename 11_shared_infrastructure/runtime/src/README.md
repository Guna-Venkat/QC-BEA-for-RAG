# Source code in chronological order

The physical folders below are numbered in week order and named by research purpose. Two-digit prefixes keep file-browser sorting correct. No research Python content was rewritten.

**Compatibility:** `week*`, `w7*`, `w5c`, and `post_w12` entries are relative links to the renamed folders. Keep them: frozen notebooks, source-hash registries, historical paths and Python imports still use those names. Use the descriptive folders for browsing; keep existing import statements when executing historical experiments. Do not mix descriptive and legacy import names in one process, since Python can create separate module objects.

| Folder | Responsibility | Compatibility name |
|---|---|---|
| [01_dataset_diagnostics](01_dataset_diagnostics) | Dataset adapters, evidence utilization and layer diagnostics | `week0` |
| [02_context_budget_surfaces](02_context_budget_surfaces) | Fixed-context response sweeps and query feature extraction | `week2` |
| [03_context_oracle_analysis](03_context_oracle_analysis) | Oracle ceilings, epsilon targets and context heterogeneity | `week3` |
| [04_query_context_allocation](04_query_context_allocation) | Query-conditioned context allocation models and feature ablations | `week4` |
| [05_content_aware_allocation](05_content_aware_allocation) | Passage-transformer allocation and regret prediction | `week5` |
| [06_passage_routing](06_passage_routing) | Semantic passage routing and learned passage importance | `week6` |
| [07_adaptive_routing_policies](07_adaptive_routing_policies) | Routing-aware budgets, continuation and fidelity policies | `week7` |
| [08_evidence_representation](08_evidence_representation) | Retrieval, sentence suppression and frozen execution support | `week9` |
| [09_reader_diagnostics](09_reader_diagnostics) | Reader and evidence-utilization root-cause diagnostics | `week10` |
| [10_granularity_study](10_granularity_study) | Matched retrieval, hierarchy, budgets, readers and granularity experiments | `week11` |
| [11_budgeted_evidence_fusion](11_budgeted_evidence_fusion) | QBGF, exact packing, controlled evaluation and frozen protocol | `week12` |
| [12_baseline_comparisons](12_baseline_comparisons) | Matched passage baselines and specialist SARA comparisons | `week12_extension` |
| [14_evidence_attribution](14_evidence_attribution) | No-refill evidence deletion and downstream-utility analysis | `week12_attribution` |
| [15_frozen_confirmation](15_frozen_confirmation) | Frozen final-method guards, execution and confirmation reporting | `week12_confirmation` |
| [13_final_method_review.py](13_final_method_review.py) | Final selection and method-review checks | `week12_final_review.py` |
| [16_exploratory_allocation](16_exploratory_allocation) | BEA-v1, learned-helpfulness BEA-v2 and qualitative case studies | `post_w12` |

## Core implementation entry points

- [QBGF and baseline evidence selection](11_budgeted_evidence_fusion/algorithm.py): exact serialization, sentence packing, fidelity options and multiple-choice knapsack.
- [Source segmentation and hierarchy](10_granularity_study/hierarchy.py): source-exact evidence units.
- [Frozen reader](11_budgeted_evidence_fusion/reader.py): prompt/token construction and generation.
- [BEA-v1](16_exploratory_allocation/bea_qbgf/allocator.py): bottom-up marginal allocation.
- [BEA-v2](16_exploratory_allocation/bea_v2/allocator.py): helpfulness-weighted transitions.
- [Canonical predictor features](16_exploratory_allocation/bea_v2/data.py): the outcome-free feature schema used in training.
- [Attribution](14_evidence_attribution/experiment.py) and [confirmation](15_frozen_confirmation/confirmation_runner.py) retain their distinct protocols.

## Adaptive routing subpackages

| Folder | Purpose | Legacy name |
|---|---|---|
| [07_adaptive_routing_policies/01_modular_routing](07_adaptive_routing_policies/01_modular_routing) | Compose budget allocation with semantic routing | `adaptive_routing_policies/w7a` |
| [07_adaptive_routing_policies/02_routing_budget_surfaces](07_adaptive_routing_policies/02_routing_budget_surfaces) | Routing-aware context response surfaces | `adaptive_routing_policies/w7b` |
| [07_adaptive_routing_policies/03_semantic_sufficiency](07_adaptive_routing_policies/03_semantic_sufficiency) | Retrieval-aware sufficiency prediction | `adaptive_routing_policies/w7c` |
| [07_adaptive_routing_policies/04_utility_continuation](07_adaptive_routing_policies/04_utility_continuation) | Utility-aware ranking and continuation | `adaptive_routing_policies/w7c2` |
| [07_adaptive_routing_policies/05_anchor_deviation](07_adaptive_routing_policies/05_anchor_deviation) | Anchor-and-deviate budget policies | `adaptive_routing_policies/w7c3` |
| [07_adaptive_routing_policies/06_generator_aligned_routing](07_adaptive_routing_policies/06_generator_aligned_routing) | Generator-aligned cross-encoder fidelity routing | `adaptive_routing_policies/w7d` |
| [07_adaptive_routing_policies/07_multifidelity_representation](07_adaptive_routing_policies/07_multifidelity_representation) | Multi-fidelity source representation and allocation | `adaptive_routing_policies/w7e` |
| [05_content_aware_allocation/01_representation_adaptation](05_content_aware_allocation/01_representation_adaptation) | Representation adaptation and content-aware training diagnostics | `content_aware_allocation/w5c` |

## What was deliberately preserved

No function, class, model, parameter, algorithm, prompt, split, result, notebook, scoring rule or dependency architecture was changed. The existing `17_shared_utilities`, `metrics`, `model` and baseline bindings retain their roles. Method-specific evidence folders elsewhere in this archive still point to the same files through compatibility links. This is a naming and navigation migration, not a claim that every historical experiment can be rerun from this archive alone.

Migration hashes: [source_name_migration.json](../../audit/source_name_migration.json).

## Numbered reading order

| Order / path | Original phase |
|---|---|
| [01_dataset_diagnostics](01_dataset_diagnostics) | W0 |
| [02_context_budget_surfaces](02_context_budget_surfaces) | W2 |
| [03_context_oracle_analysis](03_context_oracle_analysis) | W3 |
| [04_query_context_allocation](04_query_context_allocation) | W4 |
| [05_content_aware_allocation](05_content_aware_allocation) | W5 |
| [06_passage_routing](06_passage_routing) | W6 |
| [07_adaptive_routing_policies](07_adaptive_routing_policies) | W7 |
| [08_evidence_representation](08_evidence_representation) | W9 |
| [09_reader_diagnostics](09_reader_diagnostics) | W10 |
| [10_granularity_study](10_granularity_study) | W11 |
| [11_budgeted_evidence_fusion](11_budgeted_evidence_fusion) | W12 core / C-D |
| [12_baseline_comparisons](12_baseline_comparisons) | W12 C-EXT |
| [13_final_method_review.py](13_final_method_review.py) | W12 H-I freeze |
| [14_evidence_attribution](14_evidence_attribution) | W12 J-K-L |
| [15_frozen_confirmation](15_frozen_confirmation) | W12 M |
| [16_exploratory_allocation](16_exploratory_allocation) | POST-W12 |
| [17_shared_utilities](17_shared_utilities) | Shared support; not a new week |

Week 1 baseline code remains in the archive’s Baselines binding and baseline library; absent week packages were not invented. Numbering is a reading order, not a change to the experiment protocol. The W12 freeze review precedes attribution and final confirmation. Old descriptive names and week names are import/navigation aliases; keep them. Numbered paths are intended for browsing, while historical Python imports stay unchanged.
