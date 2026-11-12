# Equations and pipeline → exact code

Line numbers are extracted from the unchanged copied modules; use the named function if your editor does not support line anchors. Code views are internal symlinks, not rewritten implementations.

| Mathematical / pipeline component | Function and current source lines |
| --- | --- |
| Query-only aspects; at most six. | [aspects](../code/1_dynamic_marginal_allocator.py) (lines 7–14) |
| Normalized cosine relevance/aspect/pairwise matrices. | [signals](../code/1_dynamic_marginal_allocator.py) (lines 21–25) |
| Rel, ΔCoverage and redundancy, combined IG. | [marginal](../code/1_dynamic_marginal_allocator.py) (lines 27–32) |
| Source-order hypothetical FULL gain with updates. | [sequential_full](../code/1_dynamic_marginal_allocator.py) (lines 34–42) |
| Positive sentence actions, global competition, tau_stop/tau_expand and stop reasons. | [allocate](../code/1_dynamic_marginal_allocator.py) (lines 44–122) |
| Represented aspect threshold.5 and FULL constituent-sentence diagnostics. | [behavior](../code/1_dynamic_marginal_allocator.py) (lines 124–142) |
