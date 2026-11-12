# Bea V2

## BEA_V2

Weight semantic information gain by group-held-out predictions of historical LOO helpfulness.

**Status:** Official calibration failed; tau8e-5 reader study is a separate post-hoc exploratory branch.

**Open first:** [1_usefulness_weighted_allocator.py](code/1_usefulness_weighted_allocator.py).

**Inputs:** frozen query, candidate passages and exact source units, required score/model identities, tokenizer and budget; V2 additionally uses group-cross-fitted predictors. **Output:** exact selected text/token IDs, decisions/trace, reader answer and task/cost records where the stage runs the reader.

**Equation:** P_help=σ(βᵀ StandardScaler(x)+b); U(s|E)=P_help(s)×max(0,IG(s|E)); transition value=Σ_hypothetical additions U; M=transition value/Δserialized_tokens.

1. data.audit/feature_rows map historical exact-sentence deletion labels to inference-time source/query features.
2. models.train uses deterministic five-fold GroupKFold, scaler fit only in training folds, separate logistic help/harm models.
3. models.predict routes each known query/group to its held-out model and verifies training exclusion.
4. sequence re-ranks after every hypothetical addition; allocate considers next cumulative1/2/4/8 states and eligible FULL transitions.
5. P_harm is persisted diagnostically but is not subtracted from P_help.
6. The original nine-query mechanical calibration and single resolution sweep failed unchanged eligibility; the reader branch at8e-5 is explicitly post-hoc.

**Entry:** [run_bea_v2.py](../11_shared_infrastructure/runtime/W12-POST/run_bea_v2.py); **configuration:** [1_bea_v2_config.json](configs/1_bea_v2_config.json); **notebook:** [1_bea_v2_phelp_and_calibration.ipynb](notebooks/1_bea_v2_phelp_and_calibration.ipynb).

**Primary result:** [1_bea_v2_posthoc_quality_results.csv](results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv); **paired statistics:** [2_bea_v2_posthoc_paired_tests.csv](results/3_posthoc_reader_run/2_bea_v2_posthoc_paired_tests.csv).

**Hyperparameters:** 5folds; C1, L2, lbfgs, max_iter1000, no class weighting; eta=lambda=.5; states1,2,4,8; min parent2. No officially qualified tau. Post-hoc tau=.00008 only.

**Key finding / limits:** Predictors are imbalanced historical context-specific surrogates; calibration failed. predict rejects unseen queries without a separately frozen all-development model.

**Do not claim:** Do not call V2 calibrated, freshly confirmed, causal-help probability, universally superior or deployable on arbitrary unseen queries.

## How to inspect and reproduce

For defense, open the numbered code and saved tables; no execution is needed. Consult [equation-to-code map](docs/1_equations_to_code.md) and [notebook map](../NOTEBOOK_MAP.md). The original entry script and notebook show the historical run interface. They are not automatically executable in a fresh environment: external weights/data, original code revisions and frozen caches must be restored. No full run is authorized or necessary for this navigation task. Archived flags may already enable expensive work. V2 original calibration is terminal and must not be restarted.
