# Ablation and exact-cost details

QBGF_NO_QUERY keeps the same query-dependent SFR-retrieved pool. In options(), R_i is uniform 1/P; sentence scores are all0, so sentence weights are uniform 1/n_i and tied ranking follows canonical source order. Retained mass is selected_count/n_i. FULL mass1 and DROP0 remain. This removes allocation/fidelity query conditioning, not upstream retrieval.

QBGF_SENTENCE_ONLY removes FULL; QBGF_PASSAGE_ONLY removes sentence options. All use the original optimizer, budgets and tie rules. The stored fusion CSV contains both contrast types; it was not split into invented result tables.

Exact cost is len(tokenizer.encode(source_ordered_block + double_newline, add_special_tokens=False)); serialize sums these per-parent block token-ID costs and preserves those exact IDs for the prompt. It is not simply the length of retokenizing the whole displayed concatenated string. The optimizer is exact for this additive block-cost/relevance surrogate, not downstream F1.

solve compares utilities with1e-12 tolerance, uses lexicographic option-path ties within a cost state, and final ordering by rounded utility, lower cost and path. FIXED_SENTENCE ties by canonical source position; MiniLM ties by passage retrieval rank then source position/ID. No tie behavior was normalized in this reorganization.

See [1_equations_to_code.md](1_equations_to_code.md).
