# Recovery Audit: Verbatim Frozen Evidence for Report Appendix

This document audits the verbatim recovery of all four missing empirical evidence cases for the CS787 Final Project Report and presentation appendices. All recovered items originated from immutable, frozen experiment files in the repository. No text was fabricated, paraphrased, or synthetically regenerated.

---

## 1. Audit Table of Recovered Evidence

| Case | Requested Artifact | Recovered? | Exact Source Path | Verbatim or Summarized? | Suitable for Direct Quotation? | Notes |
|:---|:---|:---:|:---|:---:|:---:|:---|
| **Case 1** | Decisive Rank-8 chunk text (`266_chunk_f28e546d...`) | **YES** | `results/week2/raw/dev_retrieval.jsonl` (line `question_id: "917"`) | Verbatim | **YES** | Explicitly defines ParCorFull English-German translation corpus for news and TED talks. |
| **Case 1** | Full Top-10 candidate pool (IDs, BM25 scores, text) | **YES** | `results/week2/raw/dev_retrieval.jsonl` | Verbatim | **YES** | All 10 chunks with exact float scores preserved. |
| **Case 1** | Route selections & reader predictions (R0, R1, R2 at $k=4$) | **YES** | `results/week6/passage_routing/routing_predictions/dev_routing_assignments.csv`<br>`results/week6/passage_routing/sara_generations/cache_R*.jsonl`<br>`results/week2/raw/dev_fixed_k_matrix.jsonl` | Verbatim | **YES** | R0 outputs `English` ($F_1=0.67$), R1 outputs `English, Spanish` ($F_1=0.50$), R2 outputs `English, German` ($F_1=1.00$). |
| **Case 1** | Structured Case Bundle | **YES** | `FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/01_q917_candidate_pool.json`<br>`FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/01_q917_passage_identity.md` | Verbatim | **YES** | Complete machine-readable and readable documentation. |
| **Case 2** | Harmful LOO unit sentence (`4074995272a575a0e24ff01a684d14f4`) | **YES** | `results/post_w12/bea_v2/v1/utility_model/training_units.csv` | Verbatim | **YES** | 40-token sentence from PMID `7873737` on GP IIb/IIIa receptor inhibition. |
| **Case 2** | Full Claim text and Gold Evidence metadata | **YES** | `data/week11/scifact/claims_dev.jsonl` (`id: 343`) | Verbatim | **YES** | Gold label `SUPPORT`, evidence in doc `5884524`. |
| **Case 2** | Full selected context pre-ablation (5 units) | **YES** | `results/week12/attribution/v1/analysis/unit_importance.csv`<br>`results/post_w12/bea_v2/v1/utility_model/training_units.csv` | Verbatim | **YES** | Units `7d0f...`, `f12f...`, `53cb...`, `4074...`, `75d6...` recovered with exact sentences and PMIDs. |
| **Case 2** | Reader outputs before/after ablation & flip confirmation | **YES** | `results/week12/attribution/v1/analysis/unit_importance.csv` (Row 2121) | Verbatim | **YES** | Pre-ablation: `NOT_ENOUGH_INFO` ($0.0$). Post-ablation: `SUPPORT` ($1.0$). $\Delta = +1.0000$. Category: `HARMFUL`. |
| **Case 2** | Structured Case Bundle | **YES** | `FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/02_scifact343_harmful_loo.json`<br>`FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/02_scifact343_harmful_loo.md` | Verbatim | **YES** | Detailed causal mechanism and clinical context. |
| **Case 3** | Exact query text & hash (`deb89bca...`, Paper 1904.04358) | **YES** | `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Anchor A04 / Case C12) | Verbatim | **YES** | Query ID `deb89bca0925657e0f91ab5daca78b9e548de2bd`. |
| **Case 3** | Decisive answer sentence S005 (`89dec5c880a37c7f44833d3ef0d0cfa0`) | **YES** | `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Sentence ledger) | Verbatim | **YES** | Enumerates presence/absence of consonants, phonemic nasal, bilabial, high-front vowels, and high-back vowels. |
| **Case 3** | Reader outputs (FIXED, QBGF, V1, V2 at budget 1024) | **YES** | `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` | Verbatim | **YES** | V1 hallucinates stimulus words ($F_1=0.0$). FIXED, QBGF, V2 get $F_1=0.7826$. |
| **Case 3** | BEA-V1 15-step transition ledger & stop diagnostic | **YES** | `FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_beav1_transition_trace.csv` | Verbatim | **YES** | Proves early termination at 245 tokens due to `LOW_MARGINAL_VALUE` ($\text{max marginal} = 0.009965 < 0.01$). |
| **Case 3** | Exact prompt contexts sent to reader | **YES** | `FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_beav1_selected_context.txt` (245 tokens)<br>`03_fixed_selected_context.txt` (1022 tokens)<br>`03_qbgf_selected_context.txt` (1018 tokens) | Verbatim | **YES** | Matches SHA-256 prompt and evidence hashes logged in study. |
| **Case 3** | Structured Case Report | **YES** | `FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_beav1_qasper_starvation.md` | Verbatim | **YES** | Explains context starvation and BEA-V2 calibration remedy. |
| **Case 4** | Question 1001 text & gold answer (Paper 293) | **YES** | `results/week2/raw/dev_retrieval.jsonl` (line `question_id: "1001"`) | Verbatim | **YES** | Lists Emotion Sensor Feature, Empath, POS, Punctuation, etc. |
| **Case 4** | Full Top-10 retrieval pool & BM25 scores | **YES** | `results/week2/raw/dev_retrieval.jsonl` | Verbatim | **YES** | All 10 chunks preserved verbatim. |
| **Case 4** | Decisive Rank-6 chunk text (`293_chunk_11813f79...`) | **YES** | `results/week2/raw/dev_retrieval.jsonl` (Rank 6) | Verbatim | **YES** | Verbatim text detailing Emotion Sensor Feature, Empath, punctuation, and POS tags. |
| **Case 4** | Reader outputs across budget sweep ($k=0, 2, 4, 5, 6, 8, 10$) | **YES** | `results/week2/raw/dev_fixed_k_matrix.jsonl` (`question_id: 1001`) | Verbatim | **YES** | Demonstrates plateau at $F_1=0.1429$ ($k \le 5$) followed by sharp leap to $F_1=0.6000$ at $k=6$. |
| **Case 4** | Structured Case Bundle | **YES** | `FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/04_q1001_top10.json`<br>`FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/04_q1001_rank6_evidence.md` | Verbatim | **YES** | Complete documentation of granular budget thresholding. |

---

## 2. Integration Guidance for Report Appendix (`CS787_Final_Project_Report.tex`)

These recovered records resolve the missing evidence descriptions in the LaTeX report appendix:

1. **Section on Passage Identity (Appendix B):**
   - Direct quote from Rank-8 passage:
     > *"we derive data from ParCorFull, an English-German corpus annotated with full coreference chains... we select a portion of English news texts and TED talks from ParCorFull"*
   - Cite [01_q917_passage_identity.md](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/01_q917_passage_identity.md) and [01_q917_candidate_pool.json](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/01_q917_candidate_pool.json).
   - This formally proves why R0 ($[1,2,3,4]$) and R1 ($[2,3,4,5]$) hallucinate or omit German, while R2 ($[1,2,6,8]$) achieves $F_1 = 1.0$.

2. **Section on LOO Attribution & Harmful Units (Appendix C):**
   - Quote harmful unit `4074995272a575a0e24ff01a684d14f4`:
     > *"Because this disease may be associated with increased platelet aggregation, we investigated whether diabetic patients with ACS derive particular benefit from platelet glycoprotein (GP) IIb/IIIa receptor inhibition."*
   - Contrast with the unblocked decisive support unit `75d64b9c3614c0b8cce8471b3f72b41c`:
     > *"patients with diabetes mellitus (DM) have high platelet reactivity and are at increased risk of ischaemic events and bleeding post-acute coronary syndromes (ACS)."*
   - This proves that high semantic relevance ($r=0.7882$) can actively degrade reader performance by introducing clinical hypothesis distractors.

3. **Section on Context Starvation & Stopping Thresholds (Appendix D):**
   - Quote decisive task-list sentence S005 (`89dec5c880a37c7f44833d3ef0d0cfa0`):
     > *"In order to explore the problem space, we thus specifically target five binary classification problems addressed in [17] , [18] , i.e presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels."*
   - Cite the early stopping diagnostic from [03_beav1_transition_trace.csv](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_beav1_transition_trace.csv) showing BEA-V1 leaving 779 tokens (76.1% of budget) unused due to threshold $\tau = 0.01$.

4. **Section on Granular Context Scaling (Appendix E):**
   - Quote Rank-6 chunk `293_chunk_11813f79-19af-44f4-9d2f-3ae82f54ba73` and contrast with Ranks 1 and 2.
   - Quote the reader progression where $F_1$ stays at 0.1429 until $k=6$ abruptly unlocks 0.6000 F1.

---

## 3. Preservation and Integrity Check
All files created in `FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/` are standalone, read-only references that do not modify or overwrite any historical result or original experiment directory.

