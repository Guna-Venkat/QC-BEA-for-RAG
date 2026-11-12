# CS787 Repository Artifact Map

This audit documents the location, completeness, and reconstruction status of experimental artifacts across the entire repository prior to example extraction.

---

## Stage 1: Problem Definition & SARA Motivation (Weeks 0–1)

- **Scientific stage:** Stage 1 — SARA Context Exploration & Evidence Sparsity
- **Repository path:** `results/week0/`, `FINAL_PROJECT_MAIN/1_problem_and_baselines/`
- **Available raw inputs:** Paper, question, and chunk statistics in `results/week0/tables/`; raw QASPER documents.
- **Available selected evidence:** Chunk-level attention and ablation passage scores in `results/week0/tables/ablation_passage_scores.csv`.
- **Available model outputs:** Historical reproduction logs and summary tables; individual answer strings summarized in tables.
- **Available metrics:** Answer F1, Exact Match, ROUGE-L, evidence recall in `results/week0/tables/dataset_summary.csv`.
- **Available token counts:** Context token counts and passage utilization distributions in `results/week0/tables/passage_utilization_summary.csv`.
- **Available per-query attribution:** Question-level layer similarities and attention passage scores in `results/week0/tables/question_level_statistics.csv`.
- **Cohort/split:** QASPER train/dev partitions.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Ground-truth evidence sparsity patterns and attention concentration over long documents are fully preserved.

---

## Stage 2: SARA Adaptive Context & Fixed-$k$ Matrix (Weeks 2–3)

- **Scientific stage:** Stage 2 — Static-$k$ Curves, Context Sensitivity & Retrospective Oracle
- **Repository path:** `results/week2/`, `results/week3/`, `FINAL_PROJECT_MAIN/2_adaptive_evidence_quantity/`
- **Available raw inputs:** `results/week2/raw/dev_retrieval.jsonl` (query text, gold answers, retrieved passage text, BM25 scores).
- **Available selected evidence:** `results/week2/raw/dev_fixed_k_matrix.jsonl` (`retrieved_passage_ids`, `k`, `n_compressed`).
- **Available model outputs:** Predictions verbatim for each $k \in \{0, 2, 4, 6, 8, 10\}$ in `dev_fixed_k_matrix.jsonl`.
- **Available metrics:** Per-query Token F1, Exact Match, ROUGE-L, and latency in `dev_fixed_k_matrix.jsonl` and `dev_per_query_k_matrix.csv`.
- **Available token counts:** `input_tokens`, `context_tokens`, `generated_tokens` recorded per query per $k$.
- **Available per-query attribution:** `results/week2/processed/per_query_best_k.csv` maps each query's individual oracle $k^*$.
- **Cohort/split:** QASPER DEV (231 queries).
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Full per-query inputs, outputs, and scores survive across all evaluated values of $k$.

---

## Stage 3: Context-Size Prediction & Payoff Asymmetry (Weeks 4–5)

- **Scientific stage:** Stage 3 — QCCA Feature Screening & Nonlinear Benchmark
- **Repository path:** `results/week4/`, `results/week5/`, `FINAL_PROJECT_MAIN/2_adaptive_evidence_quantity/`
- **Available raw inputs:** 64 extracted features across 6 families in `results/week4/feature_discovery/feature_matrix.csv`.
- **Available selected evidence:** Target optimal context decisions in `target_matrix.csv`; out-of-fold decisions in `oof_predictions.csv`.
- **Available model outputs:** Error classification in `results/week4/processed/qcca_error_cases.csv` (over-compression vs. over-expansion).
- **Available metrics:** Mean gain captured ($+0.3395$), distractor penalty ($-0.1345$ / $-0.4184$), headroom recovery in `results/week4/model_benchmark/error_analysis.csv`.
- **Available token counts:** Cumulative and prompt tokens recorded per model policy in `results/week4/model_benchmark/policy_comparison.csv`.
- **Available per-query attribution:** Question-by-question regret in `qcca_error_cases.csv`.
- **Cohort/split:** QASPER DEV (231 queries, 5-fold GroupKFold by paper ID).
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Real query examples illustrating catastrophic over-compression (loss of gold fact) versus mild over-expansion penalty are fully documented.

---

## Stage 4: Passage Identity at Fixed $k=4$ (Week 6)

- **Scientific stage:** Stage 4 — Evidence Identity & Semantic Cosine Routing
- **Repository path:** `results/week6/`, `FINAL_PROJECT_MAIN/3_evidence_identity_and_routing/`
- **Available raw inputs:** Same 231 QASPER DEV queries and candidate pools from Week 2 retrieval.
- **Available selected evidence:** Selected passage ranks for R0 (prefix), R1 (semantic cosine), and R2 (learned router) in `results/week6/passage_routing/routing_predictions/dev_routing_assignments.csv`.
- **Available model outputs:** Verbatim generation text for each router in `results/week6/passage_routing/sara_generations/dev_sara_generations.jsonl` and `cache_R1_semantic_topk_k4.jsonl`.
- **Available metrics:** Token F1, exact match, evidence recall, and latency in `w6_failure_analysis.csv` and `w6_main_results.csv`.
- **Available token counts:** `context_tokens` recorded per query per router.
- **Available per-query attribution:** Win/loss/tie classifications comparing R2 vs. R0 in `w6_failure_analysis.csv`.
- **Cohort/split:** QASPER DEV (231 queries).
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Questions 917 and 1000 provide complete, verbatim comparisons demonstrating the effect of passage identity at fixed $k=4$.

---

## Stage 5: Learned Ranking, Draft Promotion & Extraction (Weeks 7–9)

- **Scientific stage:** Stage 5 — Intermediate Routing, Learned Rankers & Extraction Interventions
- **Repository path:** `results/week7/`, `results/week8/`, `results/week9/`, `FINAL_PROJECT_MAIN/3_evidence_identity_and_routing/`
- **Available raw inputs:** Base draft generation, entropy, and margins in `results/week8/drafts/draft_diagnostics_internal_val_exact.jsonl`; extraction units in `results/week9/ke_surface/fit/w9b_ke_surface.jsonl`.
- **Available selected evidence:** Gate decisions (PROMOTE vs. STOP) in `results/week8/w8e_controller/E3_internal_val_decisions.csv`; exact sentence selections in `results/week9/w9e3_senttopk/v1/fit/`.
- **Available model outputs:** Base draft text, promoted answer text in `w8e_controller/` replay files; extraction text in `w9b_ke_surface.jsonl`.
- **Available metrics:** Base F1, promoted F1, delta F1 in `E3_internal_val_replay.csv`; macro-F1 / F1 comparisons across D0, D1, D2, D3, E3 in `w9e3_senttopk/v1/fit/summary.csv`.
- **Available token counts:** Prompt tokens, context tokens, and generated tokens per query.
- **Available per-query attribution:** Per-query gate probabilities and decision reasons in `E3_internal_val_decisions.csv`.
- **Cohort/split:** QASPER DEV / internal validation split.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Full provenance exists showing that generative extraction degraded performance (D2: 0.3687 vs. D0: 0.3856) while exact query-ranked sentences yielded a modest gain (E3-k3: 0.3900).

---

## Stage 6: Reader & Retriever Confounds (Week 10)

- **Scientific stage:** Stage 6 — Root-Cause Disentanglement & Reader Interface Study
- **Repository path:** `results/week10/`, `FINAL_PROJECT_MAIN/4_multigranular_evidence_study/`
- **Available raw inputs:** BM25, MiniLM, and SFR candidate pools over 231 QASPER diagnostic queries.
- **Available selected evidence:** Retrieved passages at depths 1 to 10 in `results/week10/root_cause/v1/retrieval_summary.csv`.
- **Available model outputs:** Panel reader responses for Mistral, Qwen, and Llama under `results/week10/root_cause/v1/full_reader_panel_summary.csv` and format audits in `results/week11/monitoring/memory_handoff_recovery.json`.
- **Available metrics:** Any-evidence recall (0.618 BM25, 0.636 MiniLM, 0.727 SFR at depth 10); strict-format invalid rates (Mistral: 1,849/1,850; Llama: 1,826/1,850; Qwen: 0/1,850).
- **Available token counts:** Prompt tokens, generated tokens, and execution times recorded per reader.
- **Available per-query attribution:** Recorded in `retrieval_summary.csv` and reader monitoring logs.
- **Cohort/split:** Diagnostic cohort (231 queries) and SciFact verification panel.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Illustrates the evaluation-contract confound that led to freezing Qwen3-8B as the controlled reader.

---

## Stage 7: Multi-Granularity Evidence Study (Week 11)

- **Scientific stage:** Stage 7 — Budget vs. Granularity Systematic Pilot
- **Repository path:** `results/week11/`, `FINAL_PROJECT_MAIN/4_multigranular_evidence_study/`
- **Available raw inputs:** 50 queries each from HotpotQA, QASPER, SciFact; SFR retrieval pool.
- **Available selected evidence:** Passages, sentences, and propositions selected under 256, 512, and 1024 token ceilings in `FINAL_PROJECT_MAIN/4_multigranular_evidence_study/results/1_primary/2_matched_reader_results.csv`.
- **Available model outputs:** Generation outputs recorded in `multigranular/v1/` summary frames; per-query answers summarized in `2_matched_reader_results.csv`.
- **Available metrics:** Answer F1, Exact Match, macro-F1, evidence recall across granularities and budgets.
- **Available token counts:** Exact serialized `actual_evidence_tokens` and `cumulative_prompt_tokens`.
- **Available per-query attribution:** Matched reader performance in `2_matched_reader_results.csv`.
- **Cohort/split:** 50-query development pilot per dataset.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Establishes why sentence granularity dominates at 256 tokens (HotpotQA: 0.4213 vs. 0.3375), whereas whole passages become competitive at 1024 tokens (0.4803 vs. 0.4721).

---

## Stage 8: QBGF Formulation, Validation & Ablation (Week 12)

- **Scientific stage:** Stage 8 — Multiple-Choice Knapsack Evidence Allocation
- **Repository path:** `results/week12/`, `FINAL_PROJECT_MAIN/5_qbgf/`
- **Available raw inputs:** SFR top-10 candidate passages, serialized sentences, and query embeddings.
- **Available selected evidence:** Per-passage choice ($\texttt{DROP}, \texttt{SENT\_1}, \texttt{SENT\_2}, \texttt{SENT\_4}, \texttt{SENT\_8}, \texttt{FULL}$) in `1_qbgf_validation_and_ablation_summary.csv`.
- **Available model outputs:** Validation answers and ablation summaries; reserved confirmation receipts in `results/week12/final_confirmation/v1/`.
- **Available metrics:** Answer F1 for QA; macro-F1 for SciFact; paired bootstrap tests in `1_validation_and_query_conditioning_paired_tests.csv`.
- **Available token counts:** Serialized token counts per option and total utilized budget.
- **Available per-query attribution:** Complete worked allocations reconstructable from frozen candidate pools using `5_qbgf/code/1_qbgf_and_sentence_allocator.py`.
- **Cohort/split:** Week-12 validation surface (50 queries/dataset) and reserved confirmation (Hotpot: 200, SciFact: 50).
- **Can a complete human-readable example be reconstructed?** YES (Reconstructed from frozen deterministic inputs and code for intermediate knapsack tables; exact outputs preserved in qualitative reports).
- **Notes:** Full DP table, option utilities, token costs, and query-conditioning ablation are traceable.

---

## Stage 9: Leave-One-Out (LOO) Attribution & Qualitative Taxonomy (Week 12 Attribution)

- **Scientific stage:** Stage 9 — Downstream Evidence Utility Attribution
- **Repository path:** `results/week12/attribution/v1/`, `FINAL_PROJECT_MAIN/6_downstream_utility_attribution/`
- **Available raw inputs:** Evaluated evidence units, candidate pools, and gold spans in `results/week12/attribution/v1/analysis/qualitative_candidates.json`.
- **Available selected evidence:** Selected unit IDs, relevance scores, and parent retrieval ranks in `unit_importance.csv`.
- **Available model outputs:** Verbatim original answers, ablated answers, and label transitions for every unit deletion in `unit_importance.csv` (9,607 evaluated perturbations).
- **Available metrics:** $\Delta_i = \text{Score}(E \setminus \{u_i\}) - \text{Score}(E)$, importance, full score, ablated score, correctness flips.
- **Available token counts:** Unit token lengths recorded.
- **Available per-query attribution:** Categorized per-unit classifications: HELPFUL, NEUTRAL, HARMFUL in `unit_importance.csv`.
- **Cohort/split:** Attribution cohort across HotpotQA, QASPER, SciFact.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Real, verified examples for Helpful, Neutral, and Harmful units, plus qualitative failure modes (redundancy, high-similarity distractor, context fragmentation) exist in full detail.

---

## Stage 10: BEA-V1 Dynamic Marginal Allocation (Post-Week 12)

- **Scientific stage:** Stage 10 — Coverage- & Redundancy-Aware Sequential Greedy Allocation
- **Repository path:** `results/post_w12/bea_qbgf/`, `FINAL_PROJECT_MAIN/7_bea_v1/`, `W12-POST/`
- **Available raw inputs:** 150 problem caches, aspect lists, candidate pools in `FINAL_PROJECT_MAIN/7_bea_v1/results/5_query_level/pilot/`.
- **Available selected evidence:** Step-by-step selected units, stop reasons (`LOW_MARGINAL_VALUE` vs. `BUDGET_EXHAUSTED`) in `PILOT_ASPECT_MECHANISM_AUDIT.md` and `outcome_mechanisms.csv`.
- **Available model outputs:** Verbatim generation envelopes in `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Anchors A01–A08, Cases C01–C21).
- **Available metrics:** Per-query answer F1 and SciFact accuracy across 50 pilot and 150 expanded queries.
- **Available token counts:** Actual utilized evidence tokens and unused tokens recorded per query.
- **Available per-query attribution:** Win/loss/tie ledgers against `FIXED_SENTENCE` and `QBGF_FULL`.
- **Cohort/split:** 50-query pilot and 150-query expanded exploratory cohorts.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Directly demonstrates the context-starvation failure mode (e.g., HotpotQA@1024 utilizing only ~284 evidence tokens and dropping answer-bearing facts).

---

## Stage 11: BEA-V2 Utility Weighting & Calibration Failure (Post-Week 12)

- **Scientific stage:** Stage 11 — Cross-Fitted $P_{\text{help}}$ Prediction & Stopping Threshold Study
- **Repository path:** `results/post_w12/bea_v2/`, `FINAL_PROJECT_MAIN/8_bea_v2/`, `W12-POST/`
- **Available raw inputs:** Out-of-fold feature matrices, cross-fitted $L_2$ logistic regression models, candidate sentence pools.
- **Available selected evidence:** Selected transitions ($1 \to 2 \to 4 \to 8 \to \text{FULL}$) with patched help-only objective $U = P_{\text{help}} \cdot \max(0, \text{Rel} + 0.5 \Delta\text{Coverage} - 0.5 \text{Redundancy})$ in `posthoc_selection_changes.csv`.
- **Available model outputs:** Verbatim generated answers for post-hoc reader run ($\tau_{\text{stop}} = 0.00008$) in `FINAL_PROJECT_MAIN/8_bea_v2/results/3_posthoc_reader_run/rows/`.
- **Available metrics:** Quality results in `1_bea_v2_posthoc_quality_results.csv`; stopping threshold sweep in `BEA_QBGF_V2.ipynb`.
- **Available token counts:** Evidence token totals per query.
- **Available per-query attribution:** Individual query rescue cases (e.g., Anchor A05 recovering the Javier Gullón award fact).
- **Cohort/split:** Matched 50-query pilot.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Full documentation of the calibration failure (`CALIBRATION_FAILED_TERMINATED`) and the post-hoc exploratory operating point.

---

## Stage 12: MiniLM Cross-Encoder Reranker Control (Post-Week 12)

- **Scientific stage:** Stage 12 — Sentence Cross-Encoder Comparison
- **Repository path:** `FINAL_PROJECT_MAIN/9_minilm_reranker/`, `W12-POST/reranker_baseline/`
- **Available raw inputs:** Sentence pools scored by `cross-encoder/ms-marco-MiniLM-L-6-v2`.
- **Available selected evidence:** Reranked sentences and packing order in `FINAL_PROJECT_MAIN/9_minilm_reranker/results/4_diagnostics/rows/`.
- **Available model outputs:** Verbatim Qwen3-8B answers in `rows/`.
- **Available metrics:** Answer F1 for QA, macro-F1 for SciFact in `1_minilm_matched_quality_results.csv`.
- **Available token counts:** Serialized evidence tokens recorded per query.
- **Available per-query attribution:** Stored in per-query diagnostic JSON files.
- **Cohort/split:** Matched 50-query pilot across HotpotQA, QASPER, SciFact.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Demonstrates why MiniLM reranking succeeds on single decisive sentence retrieval (SciFact: 0.6855) but falters on multi-hop reasoning (HotpotQA: 0.3404 vs. 0.4042 for QBGF).

---

## Stage 13: Final Matched Method Comparison (Post-Week 12 Synthesis)

- **Scientific stage:** Stage 13 — 5-Method Matched Cohort Comparison
- **Repository path:** `FINAL_PROJECT_MAIN/10_final_method_comparison/`, `results/post_w12/final_case_study/`
- **Available raw inputs:** Exactly aligned 50 development queries per dataset across all five methods (`FIXED_SENTENCE`, `QBGF_FULL`, `BEA_QBGF_V1`, `BEA_V2_POSTHOC`, `MINILM_CE_SENTENCE`).
- **Available selected evidence:** Aligned evidence ledgers in `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Anchors A01–A08, Cases C01–C21).
- **Available model outputs:** Verbatim answers for all 5 methods side by side.
- **Available metrics:** Primary quality summary in `1_quality_comparison.csv`; paired bootstrap tests in `3_paired_statistical_comparisons.csv`.
- **Available token counts:** Evidence tokens per method per query.
- **Available per-query attribution:** Complete ledger of evidence overlap, gold coverage, and error types.
- **Cohort/split:** Matched 50 development queries per dataset at 256 and 1024 token budgets.
- **Can a complete human-readable example be reconstructed?** YES
- **Notes:** Gold-standard presentation examples ready for slides, report, and viva defense.

