# Minilm Reranker

## MINILM_CE_SENTENCE

Test a stronger query–sentence relevance scorer against embedding/cosine selection on the same source cohort.

**Status:** POST_W12_RERANKER_BASELINE_EXPLORATORY; shared 50 queries per dataset.

**Open first:** [1_cross_encoder_sentence_reranker.py](code/1_cross_encoder_sentence_reranker.py).

**Inputs:** frozen query, candidate passages and exact source units, required score/model identities, tokenizer and budget; V2 additionally uses group-cross-fitted predictors. **Output:** exact selected text/token IDs, decisions/trace, reader answer and task/cost records where the stage runs the reader.

**Equation:** r_j=CrossEncoder(q,s_j) raw logit; static descending ranking followed by exact serialize-and-skip packing under B. No softmax, P_help, aspect gain or gold-dependent selection.

1. Load the original frozen pool/sentences, without rerunning or changing upstream selection.
2. Score each query/sentence pair using the pinned MiniLM cross-encoder on FP32 CPU.
3. Sort by raw score, passage retrieval rank, source position and stable ID.
4. Trial-serialize sentences using the same Qwen token-ID block serializer; skip non-fitting candidates.
5. Restore source presentation order and use the unchanged Qwen answer reader.

**Entry:** [run_minilm_reranker.py](../11_shared_infrastructure/runtime/W12-POST/run_minilm_reranker.py); **configuration:** [protocol.py](../11_shared_infrastructure/runtime/W12-POST/reranker_baseline/protocol.py); **notebook:** [1_minilm_baseline_comparison.ipynb](notebooks/1_minilm_baseline_comparison.ipynb).

**Primary result:** [1_minilm_matched_quality_results.csv](results/1_primary/1_minilm_matched_quality_results.csv); **paired statistics:** [3_paired_statistical_comparisons.csv](../10_final_method_comparison/results/3_paired_statistical_comparisons.csv).

**Hyperparameters:** ms-marco-MiniLM-L6-v2 pinned revision; FP32 CPU; pair max512; raw identity logits; configured batch_size in protocol; evidence256/1024.

**Key finding / limits:** Static relevance still is not context-specific utility. It wins SciFact matched point estimates, but no comparison survives its recorded24-family Holm correction.

**Do not claim:** Do not call MiniLM a universally better allocator or fresh confirmation. Its tie rule differs from FIXED_SENTENCE even though the serializer/fit-skip packing are shared.

## How to inspect and reproduce

For defense, open the numbered code and saved tables; no execution is needed. Consult [equation-to-code map](docs/1_equations_to_code.md) and [notebook map](../NOTEBOOK_MAP.md). The original entry script and notebook show the historical run interface. They are not automatically executable in a fresh environment: external weights/data, original code revisions and frozen caches must be restored. No full run is authorized or necessary for this navigation task. Archived flags may already enable expensive work. V2 original calibration is terminal and must not be restarted.
