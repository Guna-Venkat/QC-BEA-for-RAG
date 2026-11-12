# Equations and pipeline → exact code

Line numbers are extracted from the unchanged copied modules; use the named function if your editor does not support line anchors. Code views are internal symlinks, not rewritten implementations.

| Mathematical / pipeline component | Function and current source lines |
| --- | --- |
| Query/source-only pair scoring; raw logits, CPU, max512. | [Scorer.score](../code/1_cross_encoder_sentence_reranker.py) (lines 30–52) |
| Static ranking and deterministic tie order. | [rank_scores](../code/1_cross_encoder_sentence_reranker.py) (lines 56–57) |
| Exact serialize-and-skip packing, source validation and source order restoration. | [pack](../code/1_cross_encoder_sentence_reranker.py) (lines 59–82) |
| Pool/source/group identity checks. | [check_frozen_identity](../code/2_reranker_experiment_runner.py) (lines 7–17) |
| Matched comparison and registered statistics output. | [analyze](../../10_final_method_comparison/code/1_final_comparison_analysis.py) (lines 44–103) |
