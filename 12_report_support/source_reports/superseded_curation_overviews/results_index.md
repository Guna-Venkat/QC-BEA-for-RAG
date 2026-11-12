# Results Index and Claim-to-Artifact Provenance Map: `FINAL_PROJECT_MAIN`

**Project Title:** Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation  
**Document Purpose:** Direct mapping from every scientific claim to its machine-readable artifact, source code, and validation status  
**Integrity Principle:** Every numerical value in this document is read directly from existing repository artifacts. No metrics were invented, estimated, or fabricated.

---

## 1. Early Motivation & Problem Formulation / Week 0

- **Claim:** Adding raw uncompressed context scales prompt tokens linearly and introduces distracting, low-density text; latent representations or selective extraction offer potential savings.
- **Metric:** Compression ratio, evidence token density, answer F1.
- **Dataset / Cohort:** QASPER pilot split (40 questions).
- **Exact Stored Values:**
  - Raw uncompressed passage prompt tokens: 1,758.5 tokens
  - Evidence density: < 22% of tokens in retrieved passages contain answer-bearing spans.
- **Source Artifact:** [`results/early_key_results/week0/tables/`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/early_key_results/week0/tables/), [`results/early_key_results/week0/scientific_audit.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/early_key_results/week0/scientific_audit.md)
- **Source Code / Config:** `src/week0/evidence_density.py`, `src/week0/sara_motivation.py`
- **Scientific Status:** Retrospective pilot / exploratory motivation.

---

## 2. Fixed-k and Oracle Evidence Allocation / Week 2

- **Claim:** A fixed context size ($k$) is suboptimal across queries. A retrospective oracle choosing the best $k \in \{0, 2, 4, 5, 6, 8\}$ per query substantially outperforms the best static baseline ($k=8$), demonstrating large theoretical headroom for adaptive context allocation.
- **Metric:** Answer F1 (token overlap), Oracle headroom gain.
- **Dataset / Cohort:** QASPER DEV (231 questions).
- **Exact Stored Values:**
  - Pure compression ($k=0$): F1 = **0.1388**
  - Parent SARA baseline ($k=5$): F1 = **0.3629**
  - Best static SARA ($k=8$): F1 = **0.3950**
  - Vanilla RAG ($k=10$): F1 = **0.4090**
  - Retrospective Oracle SARA: F1 = **0.5008** (+0.1058 gain, +26.78% over static $k=8$)
  - Retrospective Overall Oracle: F1 = **0.5264** (+0.1174 gain, +28.69% over static $k=10$)
  - Percentage of queries where $k=0$ is equal or superior to $k=8$: **46.32%**
- **Source Artifact:** [`results/early_key_results/week2/processed/oracle_vs_static_summary.json`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/early_key_results/week2/processed/oracle_vs_static_summary.json), [`dev_fixed_k_summary.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/early_key_results/week2/processed/dev_fixed_k_summary.csv)
- **Source Code / Config:** `src/week2/sweep_runner.py`, `experiments/W0_W7_key/verify_week2.py`
- **Scientific Status:** Retrospective oracle ceiling (non-deployable upper bound).

---

## 3. Query-Conditioned Controller / Weeks 4–5

- **Claim:** Lightweight query-conditioned controllers (QCCA: logistic regression, decision trees) can predict context size from question semantics and achieve substantial token savings, but fall short of the quality achieved by static baselines.
- **Metric:** Answer F1, mean $k$, context reduction percentage.
- **Dataset / Cohort:** QASPER DEV (231 questions, 5-fold cross-validation).
- **Exact Stored Values:**
  - Static $k=8$: F1 = **0.3950**, mean $k = 8.00$, mean context = 1,758.5 tokens
  - QCCA-Rule: F1 = **0.3286**, mean $k = 3.56$, mean context = 854.4 tokens (51.41% token reduction)
  - QCCA-LogReg: F1 = **0.3034**, mean $k = 2.03$, mean context = 539.8 tokens (69.30% token reduction)
  - Epsilon Oracle ($\varepsilon=0.01$): F1 = **0.4894**, mean $k = 3.49$, mean context = 841.3 tokens (52.16% reduction, recovering 99.88% of oracle headroom)
- **Source Artifact:** [`results/early_key_results/week4/processed/model_comparison.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/early_key_results/week4/processed/model_comparison.csv), [`week4_summary.json`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/early_key_results/week4/processed/week4_summary.json)
- **Source Code / Config:** `src/week4/qcca_model.py`, `experiments/W0_W7_key/generate_week4_notebook.py`
- **Scientific Status:** Exploratory / Negative finding (controllers save compute but sacrifice quality relative to fixed-k).

---

## 4. Passage Identity & Routing / Week 6

- **Claim:** Selecting *which* passages are included (passage identity) has a greater impact than varying context size ($k$). Simple semantic similarity routing matches or exceeds learned routing models.
- **Metric:** Answer F1, context tokens.
- **Dataset / Cohort:** QASPER DEV (231 questions).
- **Exact Stored Values:**
  - BM25 prefix ($k=6$): F1 = **0.3857**, mean context = 1,351.1 tokens
  - Semantic top-$k$ ($k=6$): F1 = **0.3953**, mean context = 1,325.1 tokens
  - Learned router ($k=6$): F1 = **0.3694**, mean context = 1,422.2 tokens
- **Source Artifact:** [`results/early_key_results/week6/passage_routing/tables/w6_main_results.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/early_key_results/week6/passage_routing/tables/w6_main_results.csv)
- **Source Code / Config:** `src/week6/routing.py`, `src/week6/oracle.py`
- **Scientific Status:** Exploratory validation.

---

## 5. Learned Utility & Evidence Ranking / Week 7

- **Claim:** Ranking passages by semantic embedding similarity does not guarantee downstream reader utility; however, cross-encoder routers trained on proxy objectives struggle to beat dense retrieval baselines.
- **Metric:** Answer F1, rank correlation.
- **Dataset / Cohort:** QASPER DEV.
- **Source Artifact:** [`results/early_key_results/week7/w7b_semantic_budget/tables/w7b_oracle_shift_summary.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/early_key_results/week7/w7b_semantic_budget/tables/w7b_oracle_shift_summary.csv), [`docs/weekly_key_summaries/week_07/WeeklySummaryAnalysis.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/docs/weekly_key_summaries/week_07/WeeklySummaryAnalysis.md)
- **Source Code / Config:** `src/week7/w7d/cross_encoder.py`
- **Scientific Status:** Exploratory pivot (prompted transition to multi-granularity evidence study).

---

## 6. Multi-Granularity Evidence Study / Week 11

- **Claim:** Under strict token budgets (256 tokens), sentence-level evidence representations pack substantially more answer-bearing context and outperform whole passages. At larger budgets (1024 tokens), whole passages become competitive.
- **Metric:** Answer F1 (HotpotQA, QASPER), Macro-F1 (SciFact).
- **Dataset / Cohort:** Multi-dataset pilot (50 queries per dataset: HotpotQA, QASPER, SciFact).
- **Exact Stored Values (HotpotQA @ 256 tokens):**
  - Passage representation (semantic): F1 = **0.3375** (mean tokens: 165.9)
  - Proposition representation (semantic): F1 = **0.4079** (mean tokens: 198.3)
  - Sentence representation (semantic): F1 = **0.4213** (mean tokens: 201.2)
  - No evidence control (`NONE`): F1 = **0.1502**
- **Source Artifact:** [`results/W11/final_report/main_granularity_summary_df.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W11/final_report/main_granularity_summary_df.csv), [`master_summary_df.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W11/final_report/master_summary_df.csv)
- **Source Code / Config:** `src/week11/hierarchy.py`, `src/week11/readers.py`, `configs/week11/`
- **Scientific Status:** Validation pilot (foundation for QBGF formulation).

---

## 7. Controlled Final Study: Validation & Baselines / Week 12

- **Claim:** Across extensive validation splits (7,155 HotpotQA, 1,005 QASPER, 177 SciFact), simple sentence selection (`FIXED_SENTENCE`) provides a strong, cost-effective baseline. Adaptive multi-granularity fusion (`QBGF_FULL`) offers cell-specific gains but fails to establish a consistent, statistically superior advantage across all datasets and budgets.
- **Metric:** Answer F1 (HotpotQA, QASPER), 3-class Macro-F1 (SciFact).
- **Model & Retrieval:** Salesforce `SFR-Embedding-Mistral` top-10 retrieval $\to$ `Qwen/Qwen2.5-7B-Instruct` BASE_FP16.
- **Exact Stored Values (from `results/W12/validation_and_ablations/summary.csv`):**
  - **HotpotQA (7,155 queries):**
    - 256 budget: `NONE` = 0.1653 | `RAW_SKIP` = 0.4070 | `FIXED_SENTENCE` = **0.4082** | `H3` = 0.4253 | `QBGF_FULL` = **0.4121**
    - 1024 budget: `NONE` = 0.1653 | `RAW_SKIP` = 0.4521 | `FIXED_SENTENCE` = **0.4233** | `H3` = 0.4364 | `QBGF_FULL` = **0.4323**
  - **QASPER (1,005 queries):**
    - 256 budget: `NONE` = 0.0822 | `RAW_SKIP` = 0.1693 | `FIXED_SENTENCE` = **0.2634** | `H3` = 0.2544 | `QBGF_FULL` = **0.2355**
    - 1024 budget: `NONE` = 0.0822 | `RAW_SKIP` = 0.2880 | `FIXED_SENTENCE` = **0.2988** | `H3` = 0.2995 | `QBGF_FULL` = **0.2951**
  - **SciFact (177 claims):**
    - 256 budget: `NONE` = 0.4207 | `RAW_SKIP` = 0.4564 | `FIXED_SENTENCE` = **0.7001** | `H3` = 0.6856 | `QBGF_FULL` = **0.6750**
    - 1024 budget: `NONE` = 0.4207 | `RAW_SKIP` = 0.6990 | `FIXED_SENTENCE` = **0.6704** | `H3` = 0.6859 | `QBGF_FULL` = **0.6604**
- **Source Artifact:** [`results/W12/validation_and_ablations/summary.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W12/validation_and_ablations/summary.csv), [`primary_comparisons.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W12/validation_and_ablations/primary_comparisons.csv)
- **Source Code / Config:** `src/week12/algorithm.py`, `src/week12/baselines.py`, `configs/week12/protocol.yaml`
- **Scientific Status:** Extensive validation study.

---

## 8. Controlled Final Study: QBGF Ablations / Week 12

- **Claim:** Query-conditioning is a necessary mechanism for QBGF (removing query scores severely damages performance), but multi-granularity fusion behaves almost identically to sentence-only allocation under small budgets.
- **Metric:** Quality F1 / Macro-F1 across ablation variants.
- **Exact Stored Values (from `results/W12/validation_and_ablations/summary.csv`):**
  - **HotpotQA @ 256:**
    - `QBGF_FULL`: F1 = **0.4121**
    - `QBGF_NO_QUERY`: F1 = **0.3086** (severe degradation: -0.1035)
    - `QBGF_SENTENCE_ONLY`: F1 = **0.4122** ($\approx$ identical to FULL)
    - `QBGF_PASSAGE_ONLY`: F1 = **0.3935**
  - **SciFact @ 256:**
    - `QBGF_FULL`: Macro-F1 = **0.6750**
    - `QBGF_NO_QUERY`: Macro-F1 = **0.4880** (-0.1870 drop)
    - `QBGF_SENTENCE_ONLY`: Macro-F1 = **0.6750**
    - `QBGF_PASSAGE_ONLY`: Macro-F1 = **0.4578**
- **Source Artifact:** [`results/W12/validation_and_ablations/summary.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W12/validation_and_ablations/summary.csv), [`docs/final_notes/W12_D_ABLATION_RESULTS.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/docs/final_notes/W12_D_ABLATION_RESULTS.md)
- **Source Code / Config:** `src/week12/algorithm.py`, `notebooks/week12/week12_D_qbgf_ablations.ipynb`
- **Scientific Status:** Controlled ablation analysis.

---

## 9. Official W12 Frozen Decision

- **Preregistered Gate Rule:** If QBGF does not beat the simple fallback baseline across all validation datasets and budgets, the official policy for confirmation MUST freeze the simple fallback: **`FIXED_SENTENCE`**.
- **Outcome:** QBGF failed to outperform `FIXED_SENTENCE` on QASPER @ 256 (0.2355 vs 0.2634) and SciFact @ 256 (0.6750 vs 0.7001).
- **Official Policy Freeze:**
  ```text
  SFR top-10 retrieval → FIXED_SENTENCE → Qwen3-8B BASE_FP16 → no LoRA → budgets 256 / 1024
  ```
- **Source Artifact:** [`docs/protocol/W13_FINAL_METHOD_FREEZE.json`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/docs/protocol/W13_FINAL_METHOD_FREEZE.json), [`docs/protocol/W12_I_FINAL_FREEZE_REPORT.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/docs/protocol/W12_I_FINAL_FREEZE_REPORT.md)
- **Scientific Status:** Confirmatory freeze decision.

---

## 10. Reserved Final Confirmation / Week 12

- **Claim:** On reserved, untouched confirmation cohorts, the frozen `FIXED_SENTENCE` policy delivers massive, statistically significant improvements over `NONE` in all four conditions. On SciFact @ 256, sentence selection decisively outperforms passage RAG. At 1024 tokens, passage RAG shows higher point estimates, but differences are not statistically significant. In the predefined secondary comparison family, QBGF outperforms `FIXED_SENTENCE` on HotpotQA @ 1024.
- **Metric:** Answer F1 (HotpotQA), Macro-F1 (SciFact), cluster-bootstrap 95% CI, Holm-adjusted label-swap $p$-values.
- **Cohort:** 200 HotpotQA queries (200 clusters), 50 SciFact claims (43 clusters). 10,000 cluster resamples, seed 42.
- **Exact Stored Confirmation Metrics (from `results/W12/confirmation/summary.csv`):**
  - **HotpotQA @ 256:** `NONE` = 0.1399 | `RAW_SKIP` = 0.4227 | `FIXED_SENTENCE` = **0.4373** | `H3` = 0.4622 | `QBGF_FULL` = 0.4406
  - **HotpotQA @ 1024:** `NONE` = 0.1399 | `RAW_SKIP` = 0.4589 | `FIXED_SENTENCE` = **0.4329** | `H3` = 0.4570 | `QBGF_FULL` = 0.4672
  - **SciFact @ 256:** `NONE` = 0.3686 | `RAW_SKIP` = 0.4138 | `FIXED_SENTENCE` = **0.7014** | `H3` = 0.7067 | `QBGF_FULL` = 0.6870
  - **SciFact @ 1024:** `NONE` = 0.3686 | `RAW_SKIP` = 0.7680 | `FIXED_SENTENCE` = **0.7440** | `H3` = 0.7168 | `QBGF_FULL` = 0.6346
- **Exact Stored Paired Contrasts (from `results/W12/confirmation/contrasts.csv`):**
  - `FIXED_SENTENCE - NONE` (HotpotQA @ 256): $\Delta = +0.2974$, 95% CI: [0.2424, 0.3524], $p_{\text{Holm}} = 0.0008$ (Significant)
  - `FIXED_SENTENCE - NONE` (HotpotQA @ 1024): $\Delta = +0.2929$, 95% CI: [0.2421, 0.3452], $p_{\text{Holm}} = 0.0008$ (Significant)
  - `FIXED_SENTENCE - NONE` (SciFact @ 256): $\Delta = +0.3328$, 95% CI: [0.1386, 0.5142], $p_{\text{Holm}} = 0.0126$ (Significant)
  - `FIXED_SENTENCE - NONE` (SciFact @ 1024): $\Delta = +0.3754$, 95% CI: [0.1908, 0.5455], $p_{\text{Holm}} = 0.0126$ (Significant)
  - `FIXED_SENTENCE - RAW_SKIP` (SciFact @ 256): $\Delta = +0.2876$, 95% CI: [0.0971, 0.4721], $p_{\text{Holm}} = 0.0356$ (Significant)
  - `FIXED_SENTENCE - RAW_SKIP` (SciFact @ 1024): $\Delta = -0.0239$, 95% CI: [-0.1154, 0.0615], $p_{\text{Holm}} = 1.0000$ (Inconclusive)
  - `FIXED_SENTENCE - QBGF_FULL` (HotpotQA @ 1024): $\Delta = -0.0344$, 95% CI: [-0.0597, -0.0100], $p_{\text{Holm}} = 0.0316$ (QBGF wins cell in secondary family)
- **Source Artifact:** [`results/W12/confirmation/summary.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W12/confirmation/summary.csv), [`contrasts.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W12/confirmation/contrasts.csv), [`week12_M_final_confirmation_report.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W12/confirmation/week12_M_final_confirmation_report.md)
- **Source Code / Config:** `src/week12_confirmation/runner.py`, `notebooks/week12/week12_M_final_confirmation.ipynb`
- **Scientific Status:** Reserved Confirmatory Evaluation.

---

## 11. Causal Attribution & Relevance-vs-Utility Diagnosis / Week 12

- **Claim:** Semantic retrieval relevance is weakly or unpredictably correlated with downstream generation utility (measured by leave-one-out marginal F1 degradation). Highly relevant sentences can be redundant or distracting.
- **Metric:** Spearman correlation ($\rho$) between SFR relevance score and leave-one-out causal utility.
- **Exact Stored Values (from `results/W12/attribution/relevance_utility.csv`):**
  - HotpotQA @ 256 QBGF: $\rho = \mathbf{0.0681}$ (95% CI: [-0.0157, 0.1482])
  - HotpotQA @ 1024 QBGF: $\rho = \mathbf{0.0100}$ (95% CI: [-0.0892, 0.1199])
  - QASPER @ 256 QBGF: $\rho = \mathbf{0.1042}$ (95% CI: [-0.0544, 0.2463])
  - QASPER @ 1024 QBGF: $\rho = \mathbf{-0.0344}$ (95% CI: [-0.1256, 0.0572])
  - SciFact @ 256 QBGF: $\rho = \mathbf{0.1344}$ (95% CI: [0.0094, 0.2443])
  - SciFact @ 1024 QBGF: $\rho = \mathbf{0.0441}$ (95% CI: [-0.0285, 0.1127])
- **Source Artifact:** [`results/W12/attribution/relevance_utility.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W12/attribution/relevance_utility.csv), [`curve_summary.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/W12/attribution/curve_summary.csv), [`docs/final_notes/W12_K_L_ATTRIBUTION_REPORT.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/docs/final_notes/W12_K_L_ATTRIBUTION_REPORT.md)
- **Source Code / Config:** `src/week12_attribution/analysis.py`, `src/week12_attribution/experiment.py`
- **Scientific Status:** Diagnostic / Mechanistic attribution study.

---

## 12. POST-W12 Exploratory: Budgeted Evidence Allocator V1 (BEA-V1)

- **Claim:** BEA-V1 directly targeted causal evidence utility by optimizing a marginal threshold $\tau$. In exploratory pilot evaluation, BEA-V1 severely under-allocated context under large budgets and degraded performance.
- **Metric:** Quality F1 / Macro-F1, evidence tokens, budget utilization.
- **Cohort:** Matched pilot cohort (50 queries each: HotpotQA, QASPER, SciFact).
- **Exact Stored Values (from `results/POST_W12/BEA_V1/summary.csv`):**
  - HotpotQA @ 256: BEA-V1 = **0.2976** vs FIXED = **0.3661** vs QBGF = **0.4042**
  - HotpotQA @ 1024: BEA-V1 = **0.3441** (used only 284.6 tokens, 27.8% utilization!) vs FIXED = **0.3893** (1001.7 tokens)
  - QASPER @ 256: BEA-V1 = **0.1868** vs FIXED = **0.2668**
  - QASPER @ 1024: BEA-V1 = **0.2084** vs FIXED = **0.2896**
  - SciFact @ 256: BEA-V1 = **0.6127** vs FIXED = **0.6289**
  - SciFact @ 1024: BEA-V1 = **0.6432** vs FIXED = **0.5533**
- **Source Artifact:** [`results/POST_W12/BEA_V1/summary.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/BEA_V1/summary.csv), [`PILOT_REPORT.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/BEA_V1/PILOT_REPORT.md), [`FINAL_POST_W12_REPORT.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/docs/final_notes/POST_W12_BEA_V1_FINAL_REPORT.md)
- **Source Code / Config:** `src/post_w12/bea_qbgf/`, `W12-POST/BEA_QBGF.ipynb`
- **Scientific Status:** POST-W12 Exploratory.

---

## 13. POST-W12 Exploratory: BEA-V2 & Calibration Failure

- **Claim:** BEA-V2 replaced raw utility heuristics with trained cross-fit gradient-boosted utility models and a help-only allocation objective. During formal calibration, calibration failed to find valid non-trivial thresholds that satisfied preregistered safety criteria (`CALIBRATION_FAILED_TERMINATED`). A post-hoc reader run with relaxed threshold $\tau = 8 \times 10^{-5}$ achieved high point quality on HotpotQA but remained mixed on other tasks.
- **Metric:** Quality F1 / Macro-F1, paired cluster bootstrap contrasts.
- **Exact Stored Values (from `results/POST_W12/BEA_V2/posthoc_tau8e5/POSTHOC_SUMMARY.csv`):**
  - HotpotQA @ 256: BEA-V2 = **0.4352** vs FIXED = **0.3661** vs QBGF = **0.4042**
  - HotpotQA @ 1024: BEA-V2 = **0.4234** vs FIXED = **0.3893** vs QBGF = **0.4020**
  - QASPER @ 256: BEA-V2 = **0.2618** vs FIXED = **0.2668**
  - QASPER @ 1024: BEA-V2 = **0.2904** vs FIXED = **0.2896**
  - SciFact @ 256: BEA-V2 = **0.5522** vs FIXED = **0.6289**
  - SciFact @ 1024: BEA-V2 = **0.5772** vs FIXED = **0.5533**
- **Calibration Failure Artifact:** [`results/POST_W12/BEA_V2/CALIBRATION_TERMINATED.json`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/BEA_V2/CALIBRATION_TERMINATED.json)
- **Post-hoc Run Artifact:** [`results/POST_W12/BEA_V2/posthoc_tau8e5/POSTHOC_SUMMARY.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/BEA_V2/posthoc_tau8e5/POSTHOC_SUMMARY.csv), [`POSTHOC_PILOT_RESULTS.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/BEA_V2/posthoc_tau8e5/POSTHOC_PILOT_RESULTS.md)
- **Source Code / Config:** `src/post_w12/bea_v2/`, `src/post_w12/bea_v2_posthoc/`, `W12-POST/run_bea_v2_posthoc.py`
- **Scientific Status:** POST-W12 Exploratory (calibration terminated; post-hoc exploratory reader run).

---

## 14. POST-W12 Exploratory: MiniLM Cross-Encoder Reranker Baseline

- **Claim:** A standard, lightweight sentence reranker (`cross-encoder/ms-marco-MiniLM-L6-v2`, `MINILM_CE_SENTENCE`) serves as a conventional baseline against complex allocation methods. On the matched 50-query cohort, MiniLM achieved strong performance on SciFact but showed no statistically significant advantage over `FIXED_SENTENCE` after Holm family adjustment across all 24 comparisons.
- **Metric:** Quality F1 / Macro-F1, Token efficiency, paired cluster-bootstrap comparisons (10,000 resamples, seed 42, Holm family of 24).
- **Exact Stored 5-Method Matched Cohort Values (from `results/POST_W12/minilm_reranker/FINAL_COMPARISON.csv`):**

| Dataset | Budget | FIXED_SENTENCE | QBGF_FULL | BEA-V1 | BEA-V2 | MiniLM Reranker | Descriptive Point Winner |
|---|---|---|---|---|---|---|---|
| HotpotQA | 256 | 0.3661 | 0.4042 | 0.2976 | **0.4352** | 0.3404 | BEA-V2 |
| HotpotQA | 1024 | 0.3893 | 0.4020 | 0.3441 | **0.4234** | 0.3618 | BEA-V2 |
| QASPER | 256 | **0.2668** | 0.2641 | 0.1868 | 0.2618 | 0.2641 | FIXED_SENTENCE |
| QASPER | 1024 | 0.2896 | **0.2964** | 0.2084 | 0.2904 | 0.2827 | QBGF_FULL |
| SciFact | 256 | 0.6289 | 0.5310 | 0.6127 | 0.5522 | **0.6855** | MiniLM Reranker |
| SciFact | 1024 | 0.5533 | 0.5881 | 0.6432 | 0.5772 | **0.6479** | MiniLM Reranker |

- **Descriptive Win Counts (out of 6 cells):**
  - `BEA_V2`: 2 / 6
  - `MINILM_CE_SENTENCE`: 2 / 6
  - `FIXED_SENTENCE`: 1 / 6
  - `QBGF_FULL`: 1 / 6
  - `BEA_QBGF_V1`: 0 / 6
- **Paired Statistical Tests against FIXED_SENTENCE (from `PAIRED_COMPARISONS.csv`):**
  - HotpotQA @ 256: MiniLM - FIXED = -0.0257 (95% CI: [-0.1074, 0.0535], $p_{\text{Holm}} = 1.000$)
  - HotpotQA @ 1024: MiniLM - FIXED = -0.0275 (95% CI: [-0.0976, 0.0330], $p_{\text{Holm}} = 1.000$)
  - QASPER @ 256: MiniLM - FIXED = -0.0027 (95% CI: [-0.0255, 0.0186], $p_{\text{Holm}} = 1.000$)
  - QASPER @ 1024: MiniLM - FIXED = -0.0069 (95% CI: [-0.0353, 0.0172], $p_{\text{Holm}} = 1.000$)
  - SciFact @ 256: MiniLM - FIXED = +0.0565 (95% CI: [-0.0585, 0.1733], $p_{\text{Holm}} = 1.000$)
  - SciFact @ 1024: MiniLM - FIXED = +0.0945 (95% CI: [0.0000, 0.1970], $p_{\text{Holm}} = 1.000$)
- **Source Artifact:** [`results/POST_W12/minilm_reranker/FINAL_COMPARISON.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/minilm_reranker/FINAL_COMPARISON.csv), [`SUMMARY.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/minilm_reranker/SUMMARY.csv), [`PAIRED_COMPARISONS.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/minilm_reranker/PAIRED_COMPARISONS.csv), [`EFFICIENCY.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/results/POST_W12/minilm_reranker/EFFICIENCY.csv), [`FINAL_COMPARISON.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/docs/final_notes/POST_W12_MINILM_RERANKER_FINAL_COMPARISON.md)
- **Source Code / Config:** `src/reranker_baseline/minilm_reranker.py`, `src/reranker_baseline/runner.py`, `W12-POST/BaselineComparison_MiniLM.ipynb`
- **Scientific Status:** POST-W12 Exploratory Baseline Control.

---

## 15. UNRESOLVED_PROVENANCE

Per Rule 22, the following numerical claims or historical mentions found in early narrative prose have been audited:

| Item / Claim | Narrative Location | Issue Identified | Resolved Action |
|---|---|---|---|
| **W0 mock layer/attention exports** | Early project logs | Several Week 0 synthetic attention layer files were identified as mock exports rather than model executions. | Excluded from empirical claims; only verified empirical runs (`results/early_key_results/week0/tables/`) are retained. |
| **W1 training coverage mismatch** | Early SARA fine-tuning notes | Initial training logs cited exact sample coverage that could not be matched 1:1 against preserved checkpoint metadata. | Logged as non-auditable historical training; no final performance claims are attributed to W1 fine-tuning. |
| **W3 human-rating summary** | `week3_final_scientific_report.md` | Narrative mentioned human evaluation scores, but preserved rating files in `results/week3/human_audit/` contain incomplete ratings. | Classified as uncompleted human study; omitted from all scientific arguments. |
| **W4 malformed bootstrap row** | Historical W4 summary | One legacy bootstrap entry had conflicting resample indices. | The audited `model_comparison.csv` was verified and used exclusively; malformed row rejected. |
| **W9 QASPER TEST exposure** | Week 9 SentTopK logs | An exploratory retrieval run in Week 9 consumed QASPER test query IDs. | The project protocol locked QASPER test data from being used as a fresh confirmation cohort. No uncorrupted QASPER test claim is made. |
