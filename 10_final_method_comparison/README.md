# Final matched method comparison

**One canonical home** for FIXED_SENTENCE, QBGF_FULL, BEA_QBGF_V1, post-hoc BEA_V2 and MINILM_CE_SENTENCE on the shared 50 queries per dataset at 256/1024. This is exploratory developmental data, not the full W12 VAL surface or reserved confirmation.

1. [1_quality_comparison.csv](results/1_quality_comparison.csv) — recorded formatted point estimates.
2. [2_efficiency_comparison.csv](results/2_efficiency_comparison.csv) — recorded quality/cost summaries.
3. [3_paired_statistical_comparisons.csv](results/3_paired_statistical_comparisons.csv) — saved paired intervals, raw p-values and24-comparison Holm family.
4. [4_descriptive_point_winner_summary.json](results/4_descriptive_point_winner_summary.json) — descriptive only.

**Code:** comparison_table/analyze in [analysis.py](../11_shared_infrastructure/runtime/W12-POST/reranker_baseline/analysis.py). **Notebook:** [1_final_baseline_comparison.ipynb](notebooks/1_final_baseline_comparison.ipynb) (same canonical MiniLM notebook, not an independently generated comparison).

Hotpot’s strongest point estimates are post-hoc V2; QASPER FIXED/QBGF; SciFact MiniLM. No MiniLM contrast survives its registered Holm family. No universal winner or retrospective replacement of the frozen method follows. See docs/final_interpretation.md and the case-study evidence ledgers.
