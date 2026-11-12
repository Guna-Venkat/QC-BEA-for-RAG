# V1 actions and stopping

Open code/1_dynamic_marginal_allocator.py, functions marginal, sequential_full and allocate. V1 adds one sentence at a time; it is not V2’s discrete 1→2→4→8 state controller.

After each real selection, gains and exact incremental token costs are recomputed against current evidence. FULL can compete only after two positive source-sentence selections. Its missing sentences are hypothetically considered in source order; gains above tau_context are accumulated while updating the hypothetical context. The cost is the entire exact full-source replacement, including source sentences that did not contribute positive hypothetical gain. This is not an LM paraphrase/extraction.

Sentence candidates use tau_stop; FULL uses max(tau_stop,tau_expand). Among admissible actions the original deterministic order is descending ratio, descending gain, lower cost, canonical source position, then kind. A nonpositive incremental cost receives the original sentinel treatment; no new tie/zero-cost rule was introduced.

The effective frozen tau_stop/tau_expand are both 0.01, not the initial config defaults. Stop reasons distinguish marginal threshold, budget exhaustion, all-evidence-exposed and no-positive-marginal cases. These signals are diagnostics, not proof of reasoning failure or causal necessity.
