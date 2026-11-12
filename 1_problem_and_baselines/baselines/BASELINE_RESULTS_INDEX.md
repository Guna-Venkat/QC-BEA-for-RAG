# Recorded project baseline results

Source: [merged_validation_summary.csv](../../5_qbgf/results/1_primary/w12_validation/baseline_extension/merged_validation_summary.csv). The selected fields below are stored results, not a new evaluation or calculated average. BM25/SFR plain RAG are RAW_SKIP under a shared evidence budget.

| Dataset | Method ID | Budget | n | Quality |
| --- | --- | --- | --- | --- |
| HotpotQA | BM25_PLAIN_RAG | 1024 | 7155 | 0.4353448244623784 |
| HotpotQA | BM25_PLAIN_RAG | 256 | 7155 | 0.37955346793283345 |
| HotpotQA | SFR_PLAIN_RAG | 1024 | 7155 | 0.4521325548200152 |
| HotpotQA | SFR_PLAIN_RAG | 256 | 7155 | 0.4069742752674127 |
| QASPER | BM25_PLAIN_RAG | 1024 | 1005 | 0.2559277905112202 |
| QASPER | BM25_PLAIN_RAG | 256 | 1005 | 0.15338809208287119 |
| QASPER | SFR_PLAIN_RAG | 1024 | 1005 | 0.2879568225586981 |
| QASPER | SFR_PLAIN_RAG | 256 | 1005 | 0.16928258980092695 |
| SciFact | BM25_PLAIN_RAG | 1024 | 177 | 0.7107163106819089 |
| SciFact | BM25_PLAIN_RAG | 256 | 177 | 0.4375109437429079 |
| SciFact | SFR_PLAIN_RAG | 1024 | 177 | 0.6989786840325967 |
| SciFact | SFR_PLAIN_RAG | 256 | 177 | 0.4563775340644733 |

SARA query-level k5/n10 results and scope: [specialist_references.csv](../../5_qbgf/results/1_primary/w12_validation/baseline_extension/specialist_references.csv) and [baseline_availability.csv](../../5_qbgf/results/1_primary/w12_validation/baseline_extension/baseline_availability.csv). These two1005-query QASPER specialist arms use adapted Mistral and are not budget-matched Qwen systems. No new aggregate statistic was computed.

RECOMP has no matched project result. LLMLingua-2 has a qualification receipt, not a full W12 quality score. Published-paper numbers are isolated in each baseline’s PAPER_RESULTS_REFERENCE.md and must not enter project validation/confirmation tables. Historical parent RAG/SARA results and early fixed-k/oracle results remain in the adaptive-quantity section.
