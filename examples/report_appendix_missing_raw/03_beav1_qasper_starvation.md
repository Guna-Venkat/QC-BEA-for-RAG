# Case 3 — BEA-V1 Context Starvation: QASPER Query `deb89bca...` / Paper 1904.04358

## Executive Summary & Scientific Significance
This case study documents the **Context Starvation Pathology** in Budget-Aware Evidence Allocation Version 1 (BEA-V1). 

When allocated a generous budget of $B = 1024$ tokens, BEA-V1 prematurely terminated selection after collecting only **245 evidence tokens (23.9% budget utilization)**, abandoning **779 tokens unused**. The uncalibrated early stopping threshold ($\tau = 0.01$) triggered because the maximum marginal score of the remaining 66 candidate sentences fell to $0.009965 < 0.01$.

Because the explicit task-list sentence was omitted, the frozen reader hallucinated dataset stimulus words as the classification categories, scoring **0.0000 F1**. In contrast, baseline methods (FIXED, QBGF) and the corrected allocator (BEA-V2) utilized the full budget, included the decisive sentence, and achieved **0.7826 F1**.

---

## Benchmark & Query Metadata

- **Dataset:** QASPER
- **Query ID:** `deb89bca0925657e0f91ab5daca78b9e548de2bd`
- **Group / Paper ArXiv ID:** `1904.04358`
- **Case Reference:** Anchor A04 / Case C12 (Budget 1024)
- **Question (verbatim):**
  > `What are the five different binary classification tasks?`
- **Gold Answers (verbatim):**
  - Reference 1: `presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels.`
  - Reference 2: `presence/absence of consonants, presence/absence of phonemic nasal, presence/absence of bilabial, presence/absence of high-front vowels, and presence/absence of high-back vowels`
- **Controlled Reader:** Qwen2.5-7B-Instruct (greedy decoding, temperature=0)

---

## Method Comparison at Budget $B=1024$ Tokens

| Method | Evidence Tokens | Budget Utilization | Unused Tokens | Stop Reason | Raw Reader Output | Token F1 | Exact Match |
|:---|:---:|:---:|:---:|:---|:---|:---:|:---:|
| **FIXED** | 1022 | 99.8% | 2 | `FROZEN_BASELINE` | The five different binary classification tasks are presence/absence of consonants, phonemic nasal, bilabial, high-front vowels, and high-back vowels. | 0.7826 | 0.0 |
| **QBGF** | 1018 | 99.4% | 6 | `FROZEN_BASELINE` | The five different binary classification tasks are presence/absence of consonants, phonemic nasal, bilabial, high-front vowels, and high-back vowels. | 0.7826 | 0.0 |
| **BEA-V1** | **245** | **23.9%** | **779** | `LOW_MARGINAL_VALUE` | The five different binary classification tasks are pat, pot, knew, gnaw, and INLINEFORM0. | **0.0000** | **0.0** |
| **BEA-V2** | **965** | **94.2%** | **59** | `BUDGET_EXHAUSTED` | The five different binary classification tasks are presence/absence of consonants, phonemic nasal, bilabial, high-front vowels, and high-back vowels. | **0.7826** | **0.0** |

---

## The Decisive Evidence Sentence

The ground truth answer is explicitly stated in Sentence **S005** of Parent Document P01:

- **Sentence ID:** `S005`
- **Exact Unit ID:** `89dec5c880a37c7f44833d3ef0d0cfa0`
- **Parent Chunk ID:** `P01` (`b736fdb8ed6f45bf7f8ccd13ce4ec636`)
- **Document Character Offsets:** 11139:11362
- **Unit Token Cost:** 48 tokens
- **Verbatim Text:**

> `In order to explore the problem space, we thus specifically target five binary classification problems addressed in  ,  , i.e presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels.`

### Allocation Status of the Decisive Sentence:
- **FIXED:** Included as individual SENTENCE
- **QBGF:** Included as part of FULL chunk upgrade
- **BEA-V1:** **OMITTED** (selection stopped early before reaching S005)
- **BEA-V2:** Included as individual SENTENCE

---

## Detailed Causal Analysis: How BEA-V1 Failed

### 1. The Greedy Marginal Value Curve
BEA-V1 sequentially adds candidate units that maximize marginal gain divided by token cost:
$$\text{Score}(u) = \frac{\Delta \text{Utility}(u)}{\text{Cost}(u)}$$
Selection continues in a greedy loop until the cost exceeds remaining budget or the maximum available marginal score drops below stopping threshold $\tau = 0.01$.

### 2. Transition Trace to Premature Termination
Between Step 1 and Step 15, BEA-V1 accumulated 15 sentences totaling 245 tokens:
- **Step 1 (P07):** Gain 0.8169, Cost 5 tokens $\rightarrow$ Marginal value = $0.16338$
- **Step 5 (P09):** Gain 0.1780, Cost 9 tokens $\rightarrow$ Marginal value = $0.01978$
- **Step 10 (P02):** Gain 0.4430, Cost 30 tokens $\rightarrow$ Marginal value = $0.01477$
- **Step 15 (P06):** Gain 0.2528, Cost 24 tokens $\rightarrow$ Marginal value = $0.01054$ (Cumulative tokens: 245)

*(See complete 15-step trace in [03_beav1_transition_trace.csv](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_beav1_transition_trace.csv))*

### 3. The Low Marginal Value Cliff
At Step 15, the allocator evaluated all 66 remaining candidate sentences in the pool:
- **Maximum remaining marginal score:** `0.009965016`
- **Stopping threshold:** $\tau = 0.010000000$
- Because `0.009965 < 0.010000`, the allocator evaluated stopping condition:
  ```json
  {
    "stop_reason": "LOW_MARGINAL_VALUE",
    "final_marginal_score": 0.009965016057558354,
    "step": 15,
    "cumulative_tokens": 245,
    "budget": 1024
  }
  ```
The loop terminated immediately, leaving **779 available tokens on the table**.

### 4. Downstream Hallucination
Without the decisive sentence S005, the reader encountered only stimulus words in S001 (*"as 4 words(pat, pot, knew and gnaw)."*) and S019 (*"task and the minimum (49.14%) is recorded for the INLINEFORM0 ."*). Lacking the actual task descriptions, the reader synthesized:
> `"The five different binary classification tasks are pat, pot, knew, gnaw, and INLINEFORM0."`
resulting in complete task failure ($F_1 = 0.0000$).

---

## How BEA-V2 Fixed Context Starvation
BEA-V2 implemented two decisive design corrections:
1. **Calibrated Thresholding:** Replacing the rigid static stopping threshold with a dynamic cost-sensitive stopping parameter calibrated on validation splits ($\tau = 8 \times 10^{-5}$), preventing early cutoff when generous budget remains.
2. **Context-Filling Guarantee:** Allowing BEA-V2 to continue selecting informative candidates as long as remaining budget permitted, reaching **965 tokens (94.2% utilization)** and stopping only on `BUDGET_EXHAUSTED`.
3. **Decisive Recovery:** BEA-V2 selected sentence S005, providing the reader with the exact classification tasks and restoring F1 to **0.7826**.

---

## Companion Raw Artifacts
- **Full BEA-V1 15-step transition ledger:** [03_beav1_transition_trace.csv](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_beav1_transition_trace.csv)
- **Verbatim 245-token BEA-V1 reader context:** [03_beav1_selected_context.txt](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_beav1_selected_context.txt)
- **Verbatim 1022-token FIXED reader context:** [03_fixed_selected_context.txt](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_fixed_selected_context.txt)
- **Verbatim 1018-token QBGF reader context:** [03_qbgf_selected_context.txt](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/03_qbgf_selected_context.txt)
- **Original source artifact:** `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Anchor A04 / Case C12, lines 4151–4750)

