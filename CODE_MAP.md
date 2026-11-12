# Code map — open these during the viva

Local numbered `.py` files are symlinks to byte-exact real modules. No artificial algorithm split or logic rewrite was performed. Follow the named function and extracted line range.

## FIXED_SENTENCE

**Open first:** [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py).

**Core functions:** [choose](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 97–124), [serialize](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 37–42), [order](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 20–20).

**Equation:** Sort exact source sentences by descending query cosine; tentatively add each sentence if serialized evidence tokens remain ≤B. There is no fixed top-k restriction (C2 is the separate top-eight control).

**Runner:** [run.py](11_shared_infrastructure/runtime/scripts/week12/run.py); **config:** [1_protocol.yaml](5_qbgf/configs/1_protocol.yaml); **notebook:** [3_qbgf_validation_surface.ipynb](5_qbgf/notebooks/3_qbgf_validation_surface.ipynb).

**Result:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); **statistics:** [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv).

**Component explanations:** [1_equations_to_code.md](5_qbgf/docs/1_equations_to_code.md). **Status:** W12 validation; frozen final policy; reserved confirmation separately reported.

## QBGF_FULL / QBGF_NO_QUERY

**Open first:** [1_qbgf_and_sentence_allocator.py](5_qbgf/code/1_qbgf_and_sentence_allocator.py).

**Core functions:** [softmax](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 11–15), [options](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 43–66), [block](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 33–36), [serialize](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 37–42), [solve](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 68–95), [choose](5_qbgf/code/1_qbgf_and_sentence_allocator.py) (lines 97–124).

**Equation:** R_i=exp(5p_i)/Σ_l exp(5p_l); w_ij=exp(5s_ij)/Σ_t exp(5s_it); m_i(a)=Σ_selected w_ij; U_i(a)=R_i m_i(a). DROP has utility0; FULL has mass1. Maximize Σ_i U_i(a_i), one action per passage, subject to Σ_i c_i(a_i)≤B.

**Runner:** [run.py](11_shared_infrastructure/runtime/scripts/week12/run.py); **config:** [1_protocol.yaml](5_qbgf/configs/1_protocol.yaml); **notebook:** [5_qbgf_query_and_fusion_ablations.ipynb](5_qbgf/notebooks/5_qbgf_query_and_fusion_ablations.ipynb).

**Result:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); **statistics:** [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv).

**Component explanations:** [1_equations_to_code.md](5_qbgf/docs/1_equations_to_code.md). **Status:** W12 validation and ablation; not the universally frozen final policy.

## BEA_QBGF_V1

**Open first:** [1_dynamic_marginal_allocator.py](7_bea_v1/code/1_dynamic_marginal_allocator.py).

**Core functions:** [aspects](7_bea_v1/code/1_dynamic_marginal_allocator.py) (lines 7–14), [signals](7_bea_v1/code/1_dynamic_marginal_allocator.py) (lines 21–25), [marginal](7_bea_v1/code/1_dynamic_marginal_allocator.py) (lines 27–32), [sequential_full](7_bea_v1/code/1_dynamic_marginal_allocator.py) (lines 34–42), [allocate](7_bea_v1/code/1_dynamic_marginal_allocator.py) (lines 44–122), [behavior](7_bea_v1/code/1_dynamic_marginal_allocator.py) (lines 124–142).

**Equation:** IG(s|E)=Rel(s,q)+0.5Σ_a max(0,cos(a,s)−coverage_a(E))−0.5 max_{e∈E}cos(s,e); coverage_a(E)=max(0,max_{e∈E}cos(a,e)). M=IG/Δserialized_tokens for positive cost.

**Runner:** [run.py](11_shared_infrastructure/runtime/W12-POST/run.py); **config:** [1_config.json](7_bea_v1/configs/1_config.json); **notebook:** [1_bea_v1_exploratory_pipeline.ipynb](7_bea_v1/notebooks/1_bea_v1_exploratory_pipeline.ipynb).

**Result:** [1_bea_v1_pilot_quality_results.csv](7_bea_v1/results/1_primary/1_bea_v1_pilot_quality_results.csv); **statistics:** [1_bea_v1_pilot_paired_tests.csv](7_bea_v1/results/3_statistics/1_bea_v1_pilot_paired_tests.csv).

**Component explanations:** [1_equations_to_code.md](7_bea_v1/docs/1_equations_to_code.md). **Status:** POST-W12 exploratory; pilot50/dataset and expansion150/dataset are distinct.

## BEA_V2

**Open first:** [1_usefulness_weighted_allocator.py](8_bea_v2/code/1_usefulness_weighted_allocator.py).

**Core functions:** [utility](8_bea_v2/code/1_usefulness_weighted_allocator.py) (lines 8–11), [sequence](8_bea_v2/code/1_usefulness_weighted_allocator.py) (lines 13–21), [allocate](8_bea_v2/code/1_usefulness_weighted_allocator.py) (lines 23–89).

**Equation:** P_help=σ(βᵀ StandardScaler(x)+b); U(s|E)=P_help(s)×max(0,IG(s|E)); transition value=Σ_hypothetical additions U; M=transition value/Δserialized_tokens.

**Runner:** [run_bea_v2.py](11_shared_infrastructure/runtime/W12-POST/run_bea_v2.py); **config:** [1_bea_v2_config.json](8_bea_v2/configs/1_bea_v2_config.json); **notebook:** [1_bea_v2_phelp_and_calibration.ipynb](8_bea_v2/notebooks/1_bea_v2_phelp_and_calibration.ipynb).

**Result:** [1_bea_v2_posthoc_quality_results.csv](8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv); **statistics:** [2_bea_v2_posthoc_paired_tests.csv](8_bea_v2/results/3_posthoc_reader_run/2_bea_v2_posthoc_paired_tests.csv).

**Component explanations:** [1_equations_to_code.md](8_bea_v2/docs/1_equations_to_code.md). **Status:** Official calibration failed; tau8e-5 reader study is a separate post-hoc exploratory branch.

## MINILM_CE_SENTENCE

**Open first:** [1_cross_encoder_sentence_reranker.py](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py).

**Core functions:** [Scorer](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py) (lines 7–54), [Scorer.score](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py) (lines 30–52), [rank_scores](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py) (lines 56–57), [pack](9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py) (lines 59–82).

**Equation:** r_j=CrossEncoder(q,s_j) raw logit; static descending ranking followed by exact serialize-and-skip packing under B. No softmax, P_help, aspect gain or gold-dependent selection.

**Runner:** [run_minilm_reranker.py](11_shared_infrastructure/runtime/W12-POST/run_minilm_reranker.py); **config:** [protocol.py](11_shared_infrastructure/runtime/W12-POST/reranker_baseline/protocol.py); **notebook:** [1_minilm_baseline_comparison.ipynb](9_minilm_reranker/notebooks/1_minilm_baseline_comparison.ipynb).

**Result:** [1_minilm_matched_quality_results.csv](9_minilm_reranker/results/1_primary/1_minilm_matched_quality_results.csv); **statistics:** [3_paired_statistical_comparisons.csv](10_final_method_comparison/results/3_paired_statistical_comparisons.csv).

**Component explanations:** [1_equations_to_code.md](9_minilm_reranker/docs/1_equations_to_code.md). **Status:** POST_W12_RERANKER_BASELINE_EXPLORATORY; shared 50 queries per dataset.

## Earlier methods and attribution

- [code views](1_problem_and_baselines/code) — [problem and baselines](1_problem_and_baselines/README.md)
- [code views](2_adaptive_evidence_quantity/code) — [adaptive evidence quantity](2_adaptive_evidence_quantity/README.md)
- [code views](3_evidence_identity_and_routing/code) — [evidence identity and routing](3_evidence_identity_and_routing/README.md)
- [code views](4_multigranular_evidence_study/code) — [multigranular evidence study](4_multigranular_evidence_study/README.md)
- [code views](6_downstream_utility_attribution/code) — [downstream utility attribution](6_downstream_utility_attribution/README.md)

The complete function/class line index is [code_symbol_index.csv](11_shared_infrastructure/audit/code_symbol_index.csv). Shared retrieval, segmentation, metrics, reader and serialization retain their original canonical package ownership under11_shared_infrastructure/runtime; they are not duplicated into divergent method implementations.

## Original baseline sources and project integrations

See the [baseline library](1_problem_and_baselines/baselines/README.md) for pinned SARA/RECOMP/LLMLingua source, original licenses/papers, project adapters and recorded results. Official source snapshots are reference artifacts, not substitutions for the evaluated project implementation.

## Source folders named by purpose

See [src/README.md](src/README.md) for the descriptive code layout and preserved historical import links.

## Numbered results and script navigation

See [results/README.md](results/README.md) and [scripts/README.md](scripts/README.md) for chronological names and preserved compatibility paths.
