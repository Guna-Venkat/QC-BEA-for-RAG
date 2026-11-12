# Downstream utility attribution

**Purpose:** inspect whether cosine relevance is a useful proxy for the reader’s context-specific unit utility. This is post-freeze VAL diagnosis, not fresh confirmation or universal causal necessity.

**Inputs:** saved source units, original predictions, exact deletion interventions and source/group identities. **Output:** unit importance = original task score minus score after deletion; positive/exact-zero/negative categories follow the preserved sign rule. QA uses answer F1; SciFact inference uses its registered correctness/label behavior, not per-example macro-F1.

**Open first:** [experiment.py](../11_shared_infrastructure/runtime/src/week12_attribution/experiment.py). Core functions are perturb, prepare and execute.

**Main results:** [2_helpful_neutral_harmful_summary.csv](results/1_primary/2_helpful_neutral_harmful_summary.csv); **relevance statistics:** [1_relevance_downstream_utility_correlations.csv](results/3_statistics/1_relevance_downstream_utility_correlations.csv). See the local equation/code map and J/K/L notebooks.

**Finding:** many units are neutral and many associations weak/uncertain, with condition-specific positive exceptions. Neutral deletion does not prove unused evidence, and a harmful deletion effect is conditional on the rest of the context. Original perturbation output shards are missing; preserved tables cannot substitute for those receipts. Do not claim all semantic relevance failed.
