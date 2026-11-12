# Project Scope and Research Evolution: `FINAL_PROJECT_MAIN`

**Project Title:** Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation  
**Course:** CS787 Advanced Topics in Machine Learning / RAG  
**Document Type:** Scope and Provenance Overview  

---

## 1. Core Research Question

In Retrieval-Augmented Generation (RAG), when an autoregressive language model has a constrained evidence-token budget (e.g., 256 or 1024 tokens), **which evidence units should be selected, at what granularity (passages vs. sentences), and how should context space be allocated across candidate documents?**

---

## 2. Chronological Research Evolution

The trajectory of this project developed through a series of empirical investigations, hypothesis tests, and diagnostic pivots:

```text
RECOMP Motivation
       │
       ▼
SARA: Explicit vs. Compressed Latent Evidence
       │
       ▼
Fixed-k Baseline & Oracle Upper Bounds (W2)
       │
       ▼
Cost-Aware / Epsilon-Targeted Allocation (W3)
       │
       ▼
Query-Conditioned Controller (QCCA) (W4)
       │
       ▼
Content-Aware Dynamic Allocator (W5)
       │
       ▼
Passage Identity & Routing (W6)
       │
       ▼
Learned Utility & Ranking Investigations (W7)
       │
       ▼
Multi-Granularity Evidence Study (W11)
       │
       ▼
Controlled Final Study & Frozen Decision (W12)
 ├── QBGF (Query-Conditioned Budgeted Granularity Fusion)
 ├── Controlled Baselines (NONE, RAW_SKIP, FIXED_SENTENCE, H3)
 ├── QBGF Ablations (NO_QUERY, SENTENCE_ONLY, PASSAGE_ONLY)
 ├── Causal Downstream Attribution / Leave-One-Out (LOO) Analysis
 └── Preregistered Frozen Policy Decision: FIXED_SENTENCE
       │
       ▼
POST-W12 Exploratory Investigations
 ├── Budgeted Evidence Allocator V1 (BEA-V1)
 ├── Budgeted Evidence Allocator V2 (BEA-V2) & Calibration Failure Analysis
 ├── Post-hoc tau=8e-5 Exploratory Reader Run
 ├── Qualitative Query-Level Diagnostics & Case Studies
 └── Conventional MiniLM Cross-Encoder Reranker Baseline (MINILM_CE_SENTENCE)
```

### Detailed Evolution Stages

1. **RECOMP Motivation & SARA Parent Architecture (Weeks 0–1):**  
   Motivated by RECOMP and SARA, early investigations tested whether combining readable textual passages with compact learned latent vectors could save context space without degrading answer generation.
2. **Fixed-k and Oracle Evidence Allocation (Week 2):**  
   Evaluated whether static context sizes ($k \in \{1, 2, 4, 8\}$) were optimal or if an oracle context chooser could unlock substantial quality gains. The oracle showed large theoretical headroom, motivating learnable controllers.
3. **Cost-Aware & Restricted Oracle Analysis (Week 3):**  
   Explored budget-constrained and cost-penalized allocation policies. Showed that marginal utility degrades rapidly beyond primary evidence.
4. **Query-Conditioned Controllers (Week 4):**  
   Implemented query-conditioned controllers to predict allocation from query features. While learning predictive signals, simple fixed baselines proved unexpectedly resilient.
5. **Content-Aware Dynamic Controllers (Week 5):**  
   Expanded the controller to condition on both query semantics and candidate passage content.
6. **Passage Identity & Routing (Week 6):**  
   Discovered that *which* passage is provided (passage identity) often dominates *how many* passages are shown, exposing retrieval quality as a primary bottleneck.
7. **Learned Utility & Evidence Ranking (Week 7):**  
   Attempted to train cross-encoder routers to score candidate utility directly, observing that retrieval relevance does not perfectly align with downstream generation success.
8. **Multi-Granularity Evidence Representation (Week 11):**  
   Conducted a large-scale evaluation across passages, sentences, and hierarchical proposition units across QASPER, HotpotQA, and SciFact. Established that sentence-level evidence packs significantly more relevant information under strict token limits (256 tokens).
9. **Controlled Final Study & Frozen Decision (Week 12):**  
   Formulated **QBGF** (Query-Conditioned Budgeted Granularity Fusion), which dynamically packs sentences and passages via knapsack optimization. Tested QBGF against strict baselines (`NONE`, `RAW_SKIP`, `FIXED_SENTENCE`, `H3`).  
   **Crucial Protocol Decision:** When QBGF failed the strict validation gate across all dataset/budget cells, the preregistered protocol locked **`FIXED_SENTENCE`** as the official frozen policy for final confirmation. Downstream attribution (LOO) demonstrated weak alignment between retrieval relevance and generation utility.
10. **Post-W12 Exploratory Research (Weeks 12+):**  
    Addressed the relevance-versus-utility gap via Budgeted Evidence Allocation (BEA-V1, BEA-V2), explored utility calibration thresholds, performed a qualitative query-level case study, and introduced a standard MiniLM cross-encoder reranker control.

---

## 3. Strict Boundary: Official W12 Confirmation vs. POST-W12 Exploratory

To maintain complete scientific and academic integrity, `FINAL_PROJECT_MAIN/` maintains an unambiguous distinction between the **official frozen W12 study** and **post-W12 exploratory investigations**:

### The Official W12 Controlled Study
- **Retrieval:** Salesforce `SFR-Embedding-Mistral` top-10 retrieval.
- **Reader Model:** `Qwen/Qwen2.5-7B-Instruct` evaluated in **BASE_FP16** precision (no LoRA).
- **Budgets:** Exact token constraints of **256** and **1024** tokens.
- **Evaluated Methods:** `NONE`, `RAW_SKIP`, `FIXED_SENTENCE`, `H3`, `QBGF_FULL`, and ablations (`QBGF_NO_QUERY`, `QBGF_SENTENCE_ONLY`, `QBGF_PASSAGE_ONLY`).
- **Official Frozen Policy:** **`FIXED_SENTENCE`** (SFR top-10 $\to$ sentence splitting $\to$ top sentence packing up to budget).
- **Confirmation Cohort:** 200 HotpotQA validation examples and 50 SciFact claims, evaluated with 10,000 cluster bootstrap resamples and Holm family adjustment.
- **Scientific Status:** Preregistered, frozen, audited, confirmatory.

### The POST-W12 Exploratory Investigations
- **Scope:** BEA-V1, BEA-V2, utility model training, calibration termination, post-hoc $\tau = 8 \times 10^{-5}$ reader runs, qualitative query-level case studies, and MiniLM reranker baseline (`MINILM_CE_SENTENCE`).
- **Data Boundary:** Conducted post-hoc on previously observed development data.
- **Scientific Status:** Strictly **exploratory / diagnostic**. They provide mechanistic insights into why relevance-based selectors fail, but **they do NOT alter, replace, or rewrite the official W12 frozen decision**.
