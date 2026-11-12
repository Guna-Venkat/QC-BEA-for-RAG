# Bea V1

## BEA_QBGF_V1

Reduce redundant exposure and add query-aspect coverage using recomputed context-dependent gains.

**Status:** POST-W12 exploratory; pilot50/dataset and expansion150/dataset are distinct.

**Open first:** [1_dynamic_marginal_allocator.py](code/1_dynamic_marginal_allocator.py).

**Inputs:** frozen query, candidate passages and exact source units, required score/model identities, tokenizer and budget; V2 additionally uses group-cross-fitted predictors. **Output:** exact selected text/token IDs, decisions/trace, reader answer and task/cost records where the stage runs the reader.

**Equation:** IG(s|E)=Rel(s,q)+0.5Σ_a max(0,cos(a,s)−coverage_a(E))−0.5 max_{e∈E}cos(s,e); coverage_a(E)=max(0,max_{e∈E}cos(a,e)). M=IG/Δserialized_tokens for positive cost.

1. Derive up to six query-only rule-based aspects and normalized query/sentence/aspect similarities.
2. Recompute every unselected sentence’s relevance, positive coverage gain and maximum redundancy against current E.
3. Trial-serialize candidate additions to get exact incremental token cost.
4. Only after at least two positive source-sentence selections can FULL compete; evaluate its missing sentences sequentially in source order.
5. Choose the globally best admissible marginal gain/cost with the actual deterministic tie order.
6. Stop when no admissible action remains; record LOW_MARGINAL_VALUE, budget and other reasons.

**Entry:** [run.py](../11_shared_infrastructure/runtime/W12-POST/run.py); **configuration:** [1_config.json](configs/1_config.json); **notebook:** [1_bea_v1_exploratory_pipeline.ipynb](notebooks/1_bea_v1_exploratory_pipeline.ipynb).

**Primary result:** [1_bea_v1_pilot_quality_results.csv](results/1_primary/1_bea_v1_pilot_quality_results.csv); **paired statistics:** [1_bea_v1_pilot_paired_tests.csv](results/3_statistics/1_bea_v1_pilot_paired_tests.csv).

**Hyperparameters:** Effective frozen eta=.5, lambda=.5, tau_stop=.01, tau_expand=.01, tau_context=.05, min_parent_sentences2. The config file’s initial defaults are not the effective freeze.

**Key finding / limits:** Aspects can collapse to one; premature stopping, fragmentation and source escalation are task-dependent failure risks.

**Do not claim:** Do not call V1 a successful universal final system, or describe it as V2’s fixed1→2→4→8 state algorithm.

## How to inspect and reproduce

For defense, open the numbered code and saved tables; no execution is needed. Consult [equation-to-code map](docs/1_equations_to_code.md) and [notebook map](../NOTEBOOK_MAP.md). The original entry script and notebook show the historical run interface. They are not automatically executable in a fresh environment: external weights/data, original code revisions and frozen caches must be restored. No full run is authorized or necessary for this navigation task. Archived flags may already enable expensive work. V2 original calibration is terminal and must not be restarted.
