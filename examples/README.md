# Curated Experimental Examples: CS787 RAG Project

**Project Title:** Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation  
**Directory Scope:** `FINAL_PROJECT_MAIN/examples/`  
**Integrity Guarantee:** 100% Traceable to Executed Experiments. Zero Synthetic Data. Zero Post-Hoc Falsification.

---

## 1. Master Example Directory & Use-Case Mapping

| # | Artifact / Example | Scientific Point Demonstrated | Dataset | Best Use Case | Survival Status | Primary Source Path |
| :-: | :--- | :--- | :---: | :---: | :---: | :--- |
| **01** | `01_datasets/hotpotqa_multihop_example.md` | Multi-hop reasoning requires chained evidence across documents; missing bridge causes hallucination. | HotpotQA | PPT / Viva | FULL | `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` |
| **02** | `01_datasets/qasper_sparsity_example.md` | Extreme evidence sparsity in long scientific papers; exact sentence selection preserves answers. | QASPER | Report / Demo | FULL | `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` |
| **03** | `01_datasets/scifact_verification_example.md` | Scientific verification requires single decisive assertions under strict 1-token output contracts. | SciFact | PPT / Report | FULL | `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` |
| **04** | `02_sara_context/1002_context_sensitivity.md` | Queries where adding context hurts accuracy ($k=0$ beats $k=10$ due to distractor dilution). | QASPER | PPT / Viva | FULL (Benchmark) | `results/post_w12/pilot_aspect_mechanism_audit/W12-POST/PILOT_ASPECT_MECHANISM_AUDIT.md` |
| **05** | `02_sara_context/1001_context_sensitivity.md` | Queries where context starvation causes catastrophic failure ($k=0$ fails; $k=6$ reaches 0.60 F1). | QASPER | PPT / Report | FULL (Benchmark) | `results/post_w12/pilot_aspect_mechanism_audit/W12-POST/PILOT_ASPECT_MECHANISM_AUDIT.md` |
| **06** | `03_qcca_context_prediction/asymmetric_payoff_example.md` | Asymmetric loss landscape: under-allocation drops 1.0 F1, while over-allocation drops only 0.05 F1. | QASPER | Report / Viva | FULL | `results/week3/evaluation/cost_aware_oracle_benchmark.json` |
| **07** | `04_passage_identity/917_fixed_k4_comparison.md` | Passage identity matters more than context volume; retrieving rank 8 gives F1=1.0 at fixed $k=4$. | QASPER | PPT / Viva | FULL | `results/week6/evaluation/oracle_selection_benchmark.json` |
| **08** | `05_intermediate_routing/learned_utility_vs_semantic_k8.md` | Pointwise learned utility routers suffer distribution shift and regress below static semantic $k=8$. | Hotpot/QASPER | Report / Viva | FULL | `results/week7/evaluation/pipeline_comparison.json` |
| **09** | `05_intermediate_routing/draft_promotion_example.md` | Adaptive controller stops confident queries at $k=2$ and promotes difficult queries to $k=6$. | QASPER | Demo / Report | FULL | `results/week8/evaluation/early_exit_benchmark.json` |
| **10** | `05_intermediate_routing/extraction_vs_exact_sentences.md` | Generative sentence extraction alters factual phrasing, losing quality compared to exact sentence spans. | QASPER | Viva / Report | FULL | `results/week9/evaluation/context_compression_benchmark.json` |
| **11** | `06_reader_retriever_confounds/retriever_candidate_recall_comparison.md` | Candidate recall ceiling: SFR bi-encoder achieves 0.727 recall@10 vs. 0.618 for BM25. | Cross-Dataset | Report / PPT | FULL | `results/week10/retrieval_benchmark.json` |
| **12** | `06_reader_retriever_confounds/scifact_reader_format_confound.md` | SciFact reader compliance: Mistral (1849/1850) and Llama (1826/1850) fail; Qwen produces 0 violations. | SciFact | Viva / Report | FULL | `results/week11/monitoring/memory_handoff_recovery.json` |
| **13** | `07_granularity/budget_granularity_tradeoff.md` | Budget $\times$ Granularity inversion: sentences win at 256 tokens, while passage blocks win at 1024 tokens. | HotpotQA | PPT / Report | FULL | `results/week11/granularity_pilot_results.csv` |
| **14** | `08_qbgf/7b4992e2d26577246a16ac0d1efc995ab4695d24_worked_example/` | Complete worked trace: QBGF knapsack solver achieves F1=0.8000 on baseline fact while baselines score 0. | QASPER | **DEMO / PPT** | FULL | `FINAL_PROJECT_MAIN/5_qbgf/code/1_qbgf_and_sentence_allocator.py` |
| **15** | `08_qbgf/query_conditioning_ablation.md` | Removing query-aspect conditioning drops performance by $-0.0460$ F1, proving query guidance is necessary. | HotpotQA | Report / Viva | FULL | `results/week12/qbgf/qbgf_ablation_study.csv` |
| **16** | `09_loo/loo_canonical_examples.md` | Empirical spectrum of Leave-One-Out unit utility: helpful ($\Delta=-0.91$), neutral ($\Delta=0$), harmful ($\Delta=+1.0$). | Hotpot/SciFact | PPT / Report | FULL | `results/week12/attribution/v1/analysis/unit_importance.csv` |
| **17** | `09_loo/loo_failure_mechanisms.md` | Taxonomy of LOO failure mechanisms: semantic redundancy, surface distractors, and context fragmentation. | Cross-Dataset | Viva / Report | FULL | `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` |
| **18** | `10_bea_v1/bea_v1_context_starvation.md` | Context starvation in BEA-V1: fixed threshold 0.01 strands 739 tokens at 1024 budget, dropping QA quality. | Hotpot/QASPER | **VIVA / PPT** | FULL | `FINAL_PROJECT_MAIN/7_bea_v1/code/1_bea_qbgf_allocator.py` |
| **19** | `11_bea_v2/bea_v2_learned_utility_rescue.md` | Learned utility ($P_{\text{help}}$) prioritizes multi-hop bridge $S_{005}$ in Step 1, restoring F1=1.0. | HotpotQA | PPT / Demo | FULL | `FINAL_PROJECT_MAIN/8_bea_v2/results/3_posthoc_reader_run/` |
| **20** | `11_bea_v2/calibration_tradeoff.md` | Stopping threshold calibration failure (`CALIBRATION_FAILED_TERMINATED`) and the starvation-stopping tradeoff. | Cross-Dataset | **VIVA / Report** | FULL | `FINAL_PROJECT_MAIN/8_bea_v2/results/2_calibration_failed/` |
| **21** | `12_minilm_crossencoder/minilm_vs_cosine_example.md` | Cross-encoder reranking dominates single-hop SciFact (+0.0566 F1) but underperforms multi-hop QA (-0.0257 F1). | SciFact/Hotpot | PPT / Viva | FULL | `FINAL_PROJECT_MAIN/9_minilm_reranker/results/1_primary/` |
| **22** | `13_final_comparisons/hotpotqa_matched_comparison.md` | 5-way matched comparison on multi-hop query: V1 starves; FIXED, QBGF, V2, and MiniLM retain bridge. | HotpotQA | Report / PPT | FULL | `FINAL_PROJECT_MAIN/10_final_method_comparison/results/` |
| **23** | `13_final_comparisons/qasper_matched_comparison.md` | 5-way matched comparison on QASPER: QBGF wins 0.8000 F1 by knapsack selection; all others trap on annotation. | QASPER | **DEMO / Report** | FULL | `FINAL_PROJECT_MAIN/10_final_method_comparison/results/` |
| **24** | `13_final_comparisons/scifact_matched_comparison.md` | 5-way matched comparison on SciFact: MiniLM, FIXED, and V2 retain decisive assertion; QBGF/V1 crowd out gold. | SciFact | Report / PPT | FULL | `FINAL_PROJECT_MAIN/10_final_method_comparison/results/` |

---

## 2. Guide by Use Case

### A. Presentation Slides (PPT)
- **Slide on Motivation (Why Adaptive Context?):** Use `02_sara_context/1001_context_sensitivity.md` vs. `1002_context_sensitivity.md`. Contrast the query that peaks at $k=0$ with the query that requires $k=6$.
- **Slide on Passage Identity:** Use `04_passage_identity/917_fixed_k4_comparison.md`. Show that at fixed $k=4$, changing passage identity swings F1 from 0.0 to 1.0.
- **Slide on Budget $\times$ Granularity Tradeoff:** Use `07_granularity/budget_granularity_tradeoff.md`. Show the crossover diagram where sentence selection wins at 256 tokens and passage selection wins at 1024 tokens.
- **Slide on Algorithmic Failure (BEA-V1 Context Starvation):** Use `10_bea_v1/bea_v1_context_starvation.md`. Show how a hard stopping threshold $\tau = 0.01$ left 739 tokens unused.
- **Slide on Cross-Encoder Tradeoff:** Use `12_minilm_crossencoder/minilm_vs_cosine_example.md`. Show why MiniLM wins SciFact but loses HotpotQA.

### B. Viva Defense Preparation
- **Defense Topic 1: Why did you freeze Qwen2.5-7B as the reader?**  
  $\to$ Reference `06_reader_retriever_confounds/scifact_reader_format_confound.md`. Point to the 1,849 format violations from Mistral and 1,826 from Llama. Qwen was frozen to eliminate reader compliance confounds.
- **Defense Topic 2: Why did BEA-V2 calibration fail?**  
  $\to$ Reference `11_bea_v2/calibration_tradeoff.md`. Defend that high $\tau$ starved context while low $\tau$ collapsed to budget exhaustion. No single scalar threshold satisfied both preregistered criteria. Emphasize that the failure was preserved as `CALIBRATION_FAILED_TERMINATED` rather than cosmetically modified.
- **Defense Topic 3: Does Leave-One-Out (LOO) measure intrinsic sentence quality?**  
  $\to$ Reference `09_loo/loo_failure_mechanisms.md`. Defend that LOO measures *contextual marginal utility*, which is confounded by semantic redundancy and reader distractors, not intrinsic factuality.
- **Defense Topic 4: Why did generative compression fail?**  
  $\to$ Reference `05_intermediate_routing/extraction_vs_exact_sentences.md`. Defend that LLMLingua-style extractive generation distorts factual entities, causing a $-0.0213$ F1 regression compared to exact sentence extraction.

### C. Live Interactive Demo
- **Primary Worked Example:** Open `08_qbgf/7b4992e2d26577246a16ac0d1efc995ab4695d24_worked_example/README.md`.
  1. Inspect `query.json` (*"What was the baseline used?"*).
  2. Inspect `candidate_passages.json` (retrieved paragraphs).
  3. Walk through `option_table.csv` showing how MCKP evaluates discrete candidate fidelities ($\text{SENT}_2, \text{SENT}_4, \text{SENT}_8, \text{FULL}$).
  4. Inspect `selected_evidence.txt` and verify that the 255-token budget was filled with the exact Rei (2016) sentence.
  5. Check `answer.txt` and verify the reader output `"Rei2016 model"`.

---

## 3. Repository Integrity Audit

- **Original Project Files:** ZERO files outside `FINAL_PROJECT_MAIN/examples/` were modified, moved, renamed, or deleted.
- **Machine-Readable Metadata:** All 24 examples are indexed with full 22-column metadata in [00_EXAMPLE_INDEX.csv](00_EXAMPLE_INDEX.csv).
- **Missing Artifact Disclosures:** All purged historical prompt caches and negative results are formally accounted for in [00_MISSING_EXAMPLES.md](00_MISSING_EXAMPLES.md).
- **Verification Audit:** Complete audit checklist is recorded in [FINAL_EXAMPLE_AUDIT.md](FINAL_EXAMPLE_AUDIT.md).

