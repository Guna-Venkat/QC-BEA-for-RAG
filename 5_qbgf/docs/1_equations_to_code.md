# Equations and pipeline → exact code

Line numbers are extracted from the unchanged copied modules; use the named function if your editor does not support line anchors. Code views are internal symlinks, not rewritten implementations.

| Mathematical / pipeline component | Function and current source lines |
| --- | --- |
| Passage and sentence softmax; code multiplies by tau, it does not divide. | [softmax](../code/1_qbgf_and_sentence_allocator.py) (lines 11–15) |
| R_i, sentence weights, retained mass, NO_QUERY, SENTENCE_ONLY, PASSAGE_ONLY and options. | [options](../code/1_qbgf_and_sentence_allocator.py) (lines 43–66) |
| Exact cost of source ordered text plus trailing double newline. | [block](../code/1_qbgf_and_sentence_allocator.py) (lines 33–36) |
| Per-passage additive token-ID blocks; evidence text and IDs. | [serialize](../code/1_qbgf_and_sentence_allocator.py) (lines 37–42) |
| Sparse multiple-choice knapsack, cost feasibility and deterministic ties. | [solve](../code/1_qbgf_and_sentence_allocator.py) (lines 68–95) |
| Dispatch FIXED_SENTENCE/RAW_SKIP/H3/QBGF and assemble evidence. | [choose](../code/1_qbgf_and_sentence_allocator.py) (lines 97–124) |
| Corpus hierarchy → SFR pool and query-conditioned scores. | [Lab.prepare](../code/3_candidate_and_evidence_lab.py) (lines 51–71) |
| Allocator orchestration and saved selections. | [prepare](../code/2_validation_runner.py) (lines 36–82) |
| Frozen prompt IDs and Qwen answer generation. | [Reader.generate](../code/4_frozen_qwen_reader.py) (lines 32–40) |
