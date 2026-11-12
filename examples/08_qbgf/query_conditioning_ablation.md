# QBGF Query-Conditioning Ablation: QBGF_FULL vs. QBGF_NO_QUERY

## What this example demonstrates
This ablation isolates the exact role of **query conditioning inside the evidence allocator**. 

In both conditions, upstream retrieval is identical: `Salesforce/SFR-Embedding-Mistral` retrieves the top-10 candidate passages conditioned on the query. However:
- **`QBGF_FULL` (Query-Conditioned):** Uses dense query–passage similarity to weight passage relevance $R_i = \operatorname{Softmax}(\tau_p \cdot s_{\text{pool}}(q, p_i))$ and sentence similarities to compute mass within each passage.
- **`QBGF_NO_QUERY` (Unconditioned Allocator):** Flattens passage weights to uniform $R_i = 1/10$ and sentence masses to uniform proportions $m = k/|S_i|$. It solves the knapsack purely based on length packing without knowing which passage is most relevant.

---

## Validation Surface Comparison (HotpotQA Pilot, N=50)

| Method Variant | Budget | Primary Metric | Score | Token Utilization | Primary Contrast ($\Delta$) | 95% CI |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **QBGF_FULL** | **256** | **Answer F1** | **0.4042** | **251.6** | Reference | — |
| **QBGF_NO_QUERY** | 256 | Answer F1 | 0.3582 | 249.8 | $-0.0460$ F1 | $[-0.0892, -0.0031]$ |
| **QBGF_FULL** | **1024** | **Answer F1** | **0.4020** | **995.3** | Reference | — |
| **QBGF_NO_QUERY** | 1024 | Answer F1 | 0.3712 | 988.4 | $-0.0308$ F1 | $[-0.0645, 0.0028]$ |

*Source:* `FINAL_PROJECT_MAIN/5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv`

---

## Query-Level Illustration: Divergent Allocation on Multi-Hop Query

### Query
**Question:** *"What did the screewriter for a 2013 psychological thriller film directed by Denis Villeneuve get a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for?"*  
**Gold Answer:** `["Invader (Invasor)"]`  
**Candidate Pool:** Identical 10 passages retrieved by SFR.

### 1. `QBGF_FULL` Allocation (Query-Conditioned)
- **Mechanism:** Identifies Passage 2 (*Javier Gullón*, relevance $R_2 = 0.284$) and Passage 3 (*Enemy*, relevance $R_3 = 0.221$) as carrying the dominant query-similarity mass.
- **Menu Choice:** Allocates `SENT_2` from P02 (containing the Goya nomination sentence) and `SENT_2` from P03 (containing the screenwriter identity).
- **Resulting Answer:** **"Invader (Invasor)"**
- **Score:** **$\text{F1} = 1.0000$**

### 2. `QBGF_NO_QUERY` Allocation (Unconditioned Knapsack)
- **Mechanism:** Treats all 10 passages as having uniform relevance $R_i = 0.100$. The knapsack optimizes purely for short, token-efficient sentence combinations across all 10 passages.
- **Menu Choice:** Spreads budget across P01, P04, P05, P07, and P08 (which happen to have short sentences), allocating only `DROP` or `SENT_1` to P02 and P03.
- **Evidence Omission:** Omits the specific sentence linking Javier Gullón to *Invader*.
- **Resulting Answer:** *"Enemy"* (Hallucinated work)
- **Score:** **$\text{F1} = 0.0000$** ($\Delta \text{F1} = -1.0000$)

---

## Teaching Point
Upstream retrieval brings relevant documents into the candidate set, but **is not sufficient on its own**. If the downstream allocator treats all retrieved candidates as uniformly useful, it easily drops the decisive sentence in favor of shorter, irrelevant sentences from distractor passages. Query conditioning inside the knapsack is required to guide fidelity choices toward the true evidence center.

---

## What this example does NOT prove
- This does not mean query conditioning produces huge gains in every cell; at 1024 tokens on QASPER and SciFact, the 95% bootstrap intervals for `QBGF_FULL` minus `QBGF_NO_QUERY` crossed zero, indicating that when budget is abundant, unconditioned packing often captures enough context by brute force.
- It does not mean `QBGF_FULL` is universally superior to simple sentence ranking (see Section 6 on the noninferiority freeze rule).

---

## Provenance
- **Dataset:** HotpotQA
- **Split/cohort:** Validation Surface ($N=50$)
- **Retriever:** `Salesforce/SFR-Embedding-Mistral`
- **Reader:** `Qwen/Qwen3-8B` (BASE_FP16)
- **Original ablation table:** `FINAL_PROJECT_MAIN/5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv`
- **Original statistical tests:** `FINAL_PROJECT_MAIN/5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv`
- **Reconstructed:** NO (Copied from verbatim frozen records)

