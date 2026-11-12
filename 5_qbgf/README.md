# Qbgf

## FIXED_SENTENCE

Strong simple policy that distributes a limited budget across query-relevant sentences.

**Status:** W12 validation; frozen final policy; reserved confirmation separately reported.

**Open first:** [1_qbgf_and_sentence_allocator.py](code/1_qbgf_and_sentence_allocator.py).

**Inputs:** frozen query, candidate passages and exact source units, required score/model identities, tokenizer and budget; V2 additionally uses group-cross-fitted predictors. **Output:** exact selected text/token IDs, decisions/trace, reader answer and task/cost records where the stage runs the reader.

**Equation:** Sort exact source sentences by descending query cosine; tentatively add each sentence if serialized evidence tokens remain ≤B. There is no fixed top-k restriction (C2 is the separate top-eight control).

1. Use the frozen SFR candidate pool and its exact sentences.
2. Rank by descending query-sentence similarity; ties use document order, start offset and stable ID.
3. Trial-serialize every candidate; skip non-fitting sentences and continue.
4. Serialize selected units into source ordered per-passage blocks, then supply their exact token IDs to Qwen.

**Entry:** [run.py](../11_shared_infrastructure/runtime/scripts/week12/run.py); **configuration:** [1_protocol.yaml](configs/1_protocol.yaml); **notebook:** [3_qbgf_validation_surface.ipynb](notebooks/3_qbgf_validation_surface.ipynb).

**Primary result:** [1_qbgf_validation_and_ablation_summary.csv](results/1_primary/1_qbgf_validation_and_ablation_summary.csv); **paired statistics:** [1_validation_and_query_conditioning_paired_tests.csv](results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv).

**Hyperparameters:** Configured candidate width10; evidence budgets 256/1024; same frozen reader/decoder. No learned allocation threshold.

**Key finding / limits:** Semantic similarity need not identify downstream usefulness; irrelevant/redundant evidence can remain.

**Do not claim:** Do not claim sentence evidence always beats passage evidence, or that the frozen choice is universally optimal.

## QBGF_FULL / QBGF_NO_QUERY

Choose how faithfully to expose each retrieved source jointly under a shared token budget.

**Status:** W12 validation and ablation; not the universally frozen final policy.

**Open first:** [1_qbgf_and_sentence_allocator.py](code/1_qbgf_and_sentence_allocator.py).

**Inputs:** frozen query, candidate passages and exact source units, required score/model identities, tokenizer and budget; V2 additionally uses group-cross-fitted predictors. **Output:** exact selected text/token IDs, decisions/trace, reader answer and task/cost records where the stage runs the reader.

**Equation:** R_i=exp(5p_i)/Σ_l exp(5p_l); w_ij=exp(5s_ij)/Σ_t exp(5s_it); m_i(a)=Σ_selected w_ij; U_i(a)=R_i m_i(a). DROP has utility0; FULL has mass1. Maximize Σ_i U_i(a_i), one action per passage, subject to Σ_i c_i(a_i)≤B.

1. Lab.prepare constructs the SFR-ranked pool, passage scores and sentence scores.
2. options creates DROP, SENT_1/2/4/8 and FULL, deduplicating identical short-source sentence states.
3. block computes exact token-ID costs including the trailing double newline.
4. solve runs multiple-choice dynamic programming over attainable integer costs.
5. choose serializes selected source representations and asserts additive cost consistency.
6. Reader.generate injects those evidence IDs into the frozen Qwen prompt.

**Entry:** [run.py](../11_shared_infrastructure/runtime/scripts/week12/run.py); **configuration:** [1_protocol.yaml](configs/1_protocol.yaml); **notebook:** [5_qbgf_query_and_fusion_ablations.ipynb](notebooks/5_qbgf_query_and_fusion_ablations.ipynb).

**Primary result:** [1_qbgf_validation_and_ablation_summary.csv](results/1_primary/1_qbgf_validation_and_ablation_summary.csv); **paired statistics:** [1_validation_and_query_conditioning_paired_tests.csv](results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv).

**Hyperparameters:** SENT counts1,2,4,8; softmax multiplication factors5/5; budgets 256/1024; exact tie tolerances/order remain in solve.

**Key finding / limits:** The optimized relevance-mass surrogate is not answer utility; fusion did not establish robust universal superiority.

**Do not claim:** Do not say QBGF was the frozen final method, or that NO_QUERY removes query information from SFR retrieval.

## How to inspect and reproduce

For defense, open the numbered code and saved tables; no execution is needed. Consult [equation-to-code map](docs/1_equations_to_code.md) and [notebook map](../NOTEBOOK_MAP.md). The original entry script and notebook show the historical run interface. They are not automatically executable in a fresh environment: external weights/data, original code revisions and frozen caches must be restored. No full run is authorized or necessary for this navigation task. Archived flags may already enable expensive work. V2 original calibration is terminal and must not be restarted.
