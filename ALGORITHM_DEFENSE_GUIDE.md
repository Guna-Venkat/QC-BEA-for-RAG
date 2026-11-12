# Algorithm defense guide

These are operational explanations of unchanged source code, not hidden model reasoning or new experiments. Ask which cohort/status a number belongs to before comparing it.

## FIXED_SENTENCE

**What / why:** Strong simple policy that distributes a limited budget across query-relevant sentences.

**Input:** frozen query, source pool and exact units; required scores/predictor artifacts; tokenizer and evidence budget. **Output:** selected representations, exact evidence IDs/text, decisions and trace; answer generation is a separate reader stage.

**Main equation:** Sort exact source sentences by descending query cosine; tentatively add each sentence if serialized evidence tokens remain ≤B. There is no fixed top-k restriction (C2 is the separate top-eight control).

**Steps:**

1. Use the frozen SFR candidate pool and its exact sentences.
2. Rank by descending query-sentence similarity; ties use document order, start offset and stable ID.
3. Trial-serialize every candidate; skip non-fitting sentences and continue.
4. Serialize selected units into source ordered per-passage blocks, then supply their exact token IDs to Qwen.

**Main code:** [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py). **Functions:** choose, serialize, order.

**Component/line map:** [1_equations_to_code.md](5_qbgf/docs/1_equations_to_code.md).

**Complexity:** Cosine scoring O(Nd), sorting O(N log N), plus repeated tokenizer/serialization costs; not a knapsack solver.

**Hyperparameters:** Configured candidate width10; evidence budgets 256/1024; same frozen reader/decoder. No learned allocation threshold.

**Results:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv).

**Strength:** Simple, exact source text, budget-safe and chosen by the validation-time freeze.

**Biggest limitation / observed outcome:** Semantic similarity need not identify downstream usefulness; irrelevant/redundant evidence can remain.

**Scientific status:** W12 validation; frozen final policy; reserved confirmation separately reported.

**Must NOT claim:** Do not claim sentence evidence always beats passage evidence, or that the frozen choice is universally optimal.

## QBGF_FULL / QBGF_NO_QUERY

**What / why:** Choose how faithfully to expose each retrieved source jointly under a shared token budget.

**Input:** frozen query, source pool and exact units; required scores/predictor artifacts; tokenizer and evidence budget. **Output:** selected representations, exact evidence IDs/text, decisions and trace; answer generation is a separate reader stage.

**Main equation:** R_i=exp(5p_i)/Σ_l exp(5p_l); w_ij=exp(5s_ij)/Σ_t exp(5s_it); m_i(a)=Σ_selected w_ij; U_i(a)=R_i m_i(a). DROP has utility0; FULL has mass1. Maximize Σ_i U_i(a_i), one action per passage, subject to Σ_i c_i(a_i)≤B.

**Steps:**

1. Lab.prepare constructs the SFR-ranked pool, passage scores and sentence scores.
2. options creates DROP, SENT_1/2/4/8 and FULL, deduplicating identical short-source sentence states.
3. block computes exact token-ID costs including the trailing double newline.
4. solve runs multiple-choice dynamic programming over attainable integer costs.
5. choose serializes selected source representations and asserts additive cost consistency.
6. Reader.generate injects those evidence IDs into the frozen Qwen prompt.

**Main code:** [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py). **Functions:** softmax, options, block, serialize, solve, choose.

**Component/line map:** [1_equations_to_code.md](5_qbgf/docs/1_equations_to_code.md).

**Complexity:** DP transition count is bounded by O(P×B×A), with sparse attainable-cost states; Python tuple-path copying adds overhead. Exact only for this static surrogate and serializer.

**Hyperparameters:** SENT counts1,2,4,8; softmax multiplication factors5/5; budgets 256/1024; exact tie tolerances/order remain in solve.

**Results:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv).

**Strength:** Explicit global budget optimization and interpretable per-source fidelity choices.

**Biggest limitation / observed outcome:** The optimized relevance-mass surrogate is not answer utility; fusion did not establish robust universal superiority.

**Scientific status:** W12 validation and ablation; not the universally frozen final policy.

**Must NOT claim:** Do not say QBGF was the frozen final method, or that NO_QUERY removes query information from SFR retrieval.

## BEA_QBGF_V1

**What / why:** Reduce redundant exposure and add query-aspect coverage using recomputed context-dependent gains.

**Input:** frozen query, source pool and exact units; required scores/predictor artifacts; tokenizer and evidence budget. **Output:** selected representations, exact evidence IDs/text, decisions and trace; answer generation is a separate reader stage.

**Main equation:** IG(s|E)=Rel(s,q)+0.5Σ_a max(0,cos(a,s)−coverage_a(E))−0.5 max_{e∈E}cos(s,e); coverage_a(E)=max(0,max_{e∈E}cos(a,e)). M=IG/Δserialized_tokens for positive cost.

**Steps:**

1. Derive up to six query-only rule-based aspects and normalized query/sentence/aspect similarities.
2. Recompute every unselected sentence’s relevance, positive coverage gain and maximum redundancy against current E.
3. Trial-serialize candidate additions to get exact incremental token cost.
4. Only after at least two positive source-sentence selections can FULL compete; evaluate its missing sentences sequentially in source order.
5. Choose the globally best admissible marginal gain/cost with the actual deterministic tie order.
6. Stop when no admissible action remains; record LOW_MARGINAL_VALUE, budget and other reasons.

**Main code:** [1_dynamic_marginal_allocator.py](7_bea_v1/code/1_dynamic_marginal_allocator.py). **Functions:** aspects, signals, marginal, sequential_full, allocate, behavior.

**Component/line map:** [1_equations_to_code.md](7_bea_v1/docs/1_equations_to_code.md).

**Complexity:** Dense pairwise cosine signals require O(N²) memory; each iteration rescans candidates and repeatedly serializes contexts. No exact global-optimum claim.

**Hyperparameters:** Effective frozen eta=.5, lambda=.5, tau_stop=.01, tau_expand=.01, tau_context=.05, min_parent_sentences2. The config file’s initial defaults are not the effective freeze.

**Results:** [1_bea_v1_pilot_quality_results.csv](7_bea_v1/results/1_primary/1_bea_v1_pilot_quality_results.csv); [1_bea_v1_pilot_paired_tests.csv](7_bea_v1/results/3_statistics/1_bea_v1_pilot_paired_tests.csv).

**Strength:** Context-dependent redundancy/coverage and auditable stop/upgrade traces.

**Biggest limitation / observed outcome:** Aspects can collapse to one; premature stopping, fragmentation and source escalation are task-dependent failure risks.

**Scientific status:** POST-W12 exploratory; pilot50/dataset and expansion150/dataset are distinct.

**Must NOT claim:** Do not call V1 a successful universal final system, or describe it as V2’s fixed1→2→4→8 state algorithm.

## BEA_V2

**What / why:** Weight semantic information gain by group-held-out predictions of historical LOO helpfulness.

**Input:** frozen query, source pool and exact units; required scores/predictor artifacts; tokenizer and evidence budget. **Output:** selected representations, exact evidence IDs/text, decisions and trace; answer generation is a separate reader stage.

**Main equation:** P_help=σ(βᵀ StandardScaler(x)+b); U(s|E)=P_help(s)×max(0,IG(s|E)); transition value=Σ_hypothetical additions U; M=transition value/Δserialized_tokens.

**Steps:**

1. data.audit/feature_rows map historical exact-sentence deletion labels to inference-time source/query features.
2. models.train uses deterministic five-fold GroupKFold, scaler fit only in training folds, separate logistic help/harm models.
3. models.predict routes each known query/group to its held-out model and verifies training exclusion.
4. sequence re-ranks after every hypothetical addition; allocate considers next cumulative1/2/4/8 states and eligible FULL transitions.
5. P_harm is persisted diagnostically but is not subtracted from P_help.
6. The original nine-query mechanical calibration and single resolution sweep failed unchanged eligibility; the reader branch at8e-5 is explicitly post-hoc.

**Main code:** [1_usefulness_weighted_allocator.py](8_bea_v2/code/1_usefulness_weighted_allocator.py). **Functions:** utility, sequence, allocate.

**Component/line map:** [1_equations_to_code.md](8_bea_v2/docs/1_equations_to_code.md).

**Complexity:** Training consists of fixed logistic fits over grouped historical unit rows. Allocation retains O(N²) pairwise signals plus repeated hypothetical re-ranking and serialization; not exact static MCKP.

**Hyperparameters:** 5folds; C1, L2, lbfgs, max_iter1000, no class weighting; eta=lambda=.5; states1,2,4,8; min parent2. No officially qualified tau. Post-hoc tau=.00008 only.

**Results:** [1_bea_v2_posthoc_quality_results.csv](8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv); [2_bea_v2_posthoc_paired_tests.csv](8_bea_v2/results/3_posthoc_reader_run/2_bea_v2_posthoc_paired_tests.csv).

**Strength:** Separates predictive usefulness from semantic relevance with group isolation and inspectable transition values.

**Biggest limitation / observed outcome:** Predictors are imbalanced historical context-specific surrogates; calibration failed. predict rejects unseen queries without a separately frozen all-development model.

**Scientific status:** Official calibration failed; tau8e-5 reader study is a separate post-hoc exploratory branch.

**Must NOT claim:** Do not call V2 calibrated, freshly confirmed, causal-help probability, universally superior or deployable on arbitrary unseen queries.

## MINILM_CE_SENTENCE

**What / why:** Test a stronger query–sentence relevance scorer against embedding/cosine selection on the same source cohort.

**Input:** frozen query, source pool and exact units; required scores/predictor artifacts; tokenizer and evidence budget. **Output:** selected representations, exact evidence IDs/text, decisions and trace; answer generation is a separate reader stage.

**Main equation:** r_j=CrossEncoder(q,s_j) raw logit; static descending ranking followed by exact serialize-and-skip packing under B. No softmax, P_help, aspect gain or gold-dependent selection.

**Steps:**

1. Load the original frozen pool/sentences, without rerunning or changing upstream selection.
2. Score each query/sentence pair using the pinned MiniLM cross-encoder on FP32 CPU.
3. Sort by raw score, passage retrieval rank, source position and stable ID.
4. Trial-serialize sentences using the same Qwen token-ID block serializer; skip non-fitting candidates.
5. Restore source presentation order and use the unchanged Qwen answer reader.

**Main code:** [1_cross_encoder_sentence_reranker.py](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py). **Functions:** Scorer, Scorer.score, rank_scores, pack.

**Component/line map:** [1_equations_to_code.md](9_minilm_reranker/docs/1_equations_to_code.md).

**Complexity:** One transformer pair per sentence, length capped512; sorting O(N log N); repeated exact packing costs remain. No serving-throughput claim.

**Hyperparameters:** ms-marco-MiniLM-L6-v2 pinned revision; FP32 CPU; pair max512; raw identity logits; configured batch_size in protocol; evidence256/1024.

**Results:** [1_minilm_matched_quality_results.csv](9_minilm_reranker/results/1_primary/1_minilm_matched_quality_results.csv); [3_paired_statistical_comparisons.csv](10_final_method_comparison/results/3_paired_statistical_comparisons.csv).

**Strength:** Simple strong relevance control; no trained utility/aspect/stopping machinery.

**Biggest limitation / observed outcome:** Static relevance still is not context-specific utility. It wins SciFact matched point estimates, but no comparison survives its recorded24-family Holm correction.

**Scientific status:** POST_W12_RERANKER_BASELINE_EXPLORATORY; shared 50 queries per dataset.

**Must NOT claim:** Do not call MiniLM a universally better allocator or fresh confirmation. Its tie rule differs from FIXED_SENTENCE even though the serializer/fit-skip packing are shared.

## Rapid professor-question routes

| Question | Open first | Then show |
| --- | --- | --- |
| Show QBGF / knapsack | [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py) → options/solve | [1_equations_to_code.md](5_qbgf/docs/1_equations_to_code.md) and [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv) |
| Show BEA-V2 / P_help | [1_usefulness_weighted_allocator.py](8_bea_v2/code/1_usefulness_weighted_allocator.py) → utility/sequence/allocate | [2_group_crossfit_phelp_models.py](8_bea_v2/code/2_group_crossfit_phelp_models.py) → train/predict, then failed calibration and separate post-hoc table |
| Why was semantic relevance insufficient? | [1_relevance_downstream_utility_correlations.csv](6_downstream_utility_attribution/results/3_statistics/1_relevance_downstream_utility_correlations.csv) | [2_helpful_neutral_harmful_summary.csv](6_downstream_utility_attribution/results/1_primary/2_helpful_neutral_harmful_summary.csv) and qualitative examples; say context-specific, not universal failure |
| Show reranker baseline | [1_cross_encoder_sentence_reranker.py](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py) → Scorer.score/rank_scores/pack | [1_quality_comparison.csv](10_final_method_comparison/results/1_quality_comparison.csv) and [3_paired_statistical_comparisons.csv](10_final_method_comparison/results/3_paired_statistical_comparisons.csv) |
