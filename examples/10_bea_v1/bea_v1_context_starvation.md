# Context Starvation in BEA-V1: Hard Stopping Thresholds at Large Budgets

**Example ID:** `BEA-V1-01`  
**Dataset:** HotpotQA / QASPER  
**Primary Worked Queries:**
- QASPER `deb89bca0925657e0f91ab5daca78b9e548de2bd` (Paper `1904.04358`, Anchor `A04` / Case `C12`)
- HotpotQA `5a7df25a5542990b8f503b02` (Denis Villeneuve / Javier Gullón, Anchor `A05` / Cases `C02`, `C05`)  
**Focal Methods:** `BEA_QBGF_V1` vs. `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_V2_POSTHOC`  
**Budgets Evaluated:** 256 and 1024 tokens  
**Recovery Status:** Fully recovered from exact saved execution logs, candidate-level diagnostic records, and qualitative ledgers.

---

## 1. What This Example Demonstrates

This artifact documents the core algorithmic pathology that crippled **BEA-V1** (Budget-Aware Evidence Allocation, Version 1): **Context Starvation**.

1. **Premature Termination:** At high token budgets (1024 tokens), BEA-V1 consistently stopped allocating evidence far before filling the available context window. Across HotpotQA at 1024 tokens, BEA-V1 allocated an average of only **284.6 tokens**, leaving **739.4 tokens unused** (only 27.8% budget utilization), and terminated on `LOW_MARGINAL_VALUE` in 100% of cases.
2. **Downstream Quality Collapse:** Because it starved the reader of context, BEA-V1 suffered a severe quality collapse: scoring **0.3441 F1** on HotpotQA 1024 versus **0.3893 F1** for the naive `FIXED_SENTENCE` baseline (a statistically significant regression of $-0.0452$ F1, $p < 0.001$).
3. **The Microscopic Mechanism:** BEA-V1 used a greedy bottom-up selection rule with a static stopping threshold $\tau_{\text{stop}} = 0.01$:
   $$\text{Marginal Efficiency} = \frac{\Delta \text{Gain}}{\Delta \text{Cost}} = \frac{\text{Rel}(s) + 0.5 \cdot \Delta \text{Cov}(S \cup \{s\}) - 0.5 \cdot \text{Red}(s, S)}{|\text{Tok}(s)|} \ge \tau_{\text{stop}}$$
   Once the first few sentences were added, semantic coverage saturated ($\Delta \text{Cov} \to 0$) and redundancy against selected sentences grew ($\text{Red} > 0.70$). Consequently, the numerator shrank while the denominator (token length) remained substantial, causing marginal efficiency to fall below $0.01$. The allocator aborted early, rejecting decisive multi-hop and factual sentences that happened to have longer phrasing or moderate redundancy.

---

## 2. Macro Benchmark Evidence: HotpotQA 1024 Cohort

Across the controlled 50-query development cohort at budget 1024:

| Metric | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC |
| :--- | :---: | :---: | :---: | :---: |
| **Mean Evidence Tokens Allocated** | 1018.4 | 1015.2 | **284.6** | 948.7 |
| **Budget Utilization (%)** | 99.5% | 99.1% | **27.8%** | 92.6% |
| **Unused Token Capacity** | 5.6 | 8.8 | **739.4** | 75.3 |
| **Stop Reason: BUDGET_EXHAUSTED** | 100% | 100% | **0.0%** | 88.0% |
| **Stop Reason: LOW_MARGINAL_VALUE** | 0.0% | 0.0% | **100.0%** | 12.0% |
| **Downstream QA F1** | **0.3893** | **0.3891** | **0.3441** | **0.3890** |
| **Delta vs. FIXED_SENTENCE** | baseline | $-0.0002$ | **$-0.0452$** | $-0.0003$ |

While `FIXED_SENTENCE` and `QBGF_FULL` saturated the 1024-token budget to pack comprehensive background, BEA-V1 stranded three-quarters of the available context window.

---

## 3. Microscopic Case 1: QASPER Query `deb89bca0925657e0f91ab5daca78b9e548de2bd` (Anchor A04)

### Context & Query
- **Question:** *"What are the five different binary classification tasks?"*
- **Paper:** `1904.04358` (*Deep Learning the EEG Manifold for Phonological Categorization from Active Thoughts*)
- **Target Answer:** *"presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels."*
- **Decisive Sentence ($S_{005}$ in $P_{01}$):**
  > *"In order to explore the problem space, we thus specifically target five binary classification problems addressed in [17] , [18] , i.e presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels."* (Unit `89dec5c880a37c7f44833d3ef0d0cfa0`, 39 tokens)

### Comparative Allocation at Budget 1024

| Metric / Attribute | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC |
| :--- | :---: | :---: | :---: | :---: |
| **Evidence Tokens** | 1022 | 1018 | **245** | 965 |
| **Utilization** | 99.8% | 99.4% | **23.9%** | 94.2% |
| **Unused Tokens** | 2 | 6 | **779** | 59 |
| **Stop Reason** | `FROZEN_BASELINE` | `FROZEN_BASELINE` | `LOW_MARGINAL_VALUE` | `BUDGET_EXHAUSTED` |
| **Exposed $S_{005}$?** | **YES** (Sentence) | **YES** (FULL block) | **NO (OMITTED)** | **YES** (Sentence) |
| **Model Output** | Explicit list of 5 tasks | Explicit list of 5 tasks | *"The five different binary classification tasks are pat, pot, knew, gnaw, and INLINEFORM0."* | Explicit list of 5 tasks |
| **QA F1 Score** | **0.7826** | **0.7826** | **0.0000** | **0.7826** |

### Failure Analysis
BEA-V1 stopped after allocating only 245 tokens out of the 1024 available. In those 245 tokens, it selected early introductory sentences describing stimulus words (`pat`, `pot`, `knew`, `gnaw`). When evaluating $S_{005}$, its incremental coverage was low because the query terms ("binary classification tasks") were already lexically covered by previous sentences, while the redundancy penalty was high. As a result, its $\Delta \text{Gain} / \Delta \text{Cost}$ ratio fell below 0.01. BEA-V1 aborted, leaving 779 tokens empty. Deprived of the explicit list, the reader hallucinated that the stimulus words were the classification tasks, yielding F1 = 0.0.

---

## 4. Microscopic Case 2: HotpotQA Query `5a7df25a5542990b8f503b02` (Anchor A05)

### The Step-by-Step Transition Collapse
In Anchor A05 at budget 256, BEA-V1 performed 17 greedy selection steps before terminating prematurely at 168 tokens (leaving 88 tokens unused). 

Below is the verbatim step-by-step trace from `FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (lines 5708–5726):

| Step | Parent | Selected Type | Incremental Token Cost ($\Delta c$) | Saved Marginal Gain ($\Delta g$) | Marginal Value/Token ($\Delta g / \Delta c$) | Cumulative Tokens |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | P09 | SENTENCE | 4 | 0.767673 | 0.191918 | 4 |
| 2 | P02 | SENTENCE | 6 | 0.332049 | 0.055342 | 10 |
| 3 | P01 | SENTENCE | 10 | 0.383478 | 0.038348 | 20 |
| 4 | P03 | SENTENCE | 8 | 0.294477 | 0.036810 | 28 |
| 5 | P10 | SENTENCE | 5 | 0.164697 | 0.032939 | 33 |
| 6 | P05 | SENTENCE | 8 | 0.230270 | 0.028784 | 41 |
| 7 | P04 | SENTENCE | 9 | 0.232083 | 0.025787 | 50 |
| 8 | P07 | SENTENCE | 7 | 0.159054 | 0.022722 | 57 |
| 9 | P02 | SENTENCE | 11 | 0.232996 | 0.021181 | 68 |
| 10 | P06 | SENTENCE | 10 | 0.208716 | 0.020872 | 78 |
| 11 | P10 | SENTENCE | 12 | 0.216591 | 0.018049 | 90 |
| 12 | P09 | SENTENCE | 12 | 0.201025 | 0.016752 | 102 |
| 13 | P03 | SENTENCE | 14 | 0.229534 | 0.016395 | 116 |
| 14 | P09 | SENTENCE | 19 | 0.301903 | 0.015890 | 135 |
| 15 | P08 | SENTENCE | 12 | 0.176862 | 0.014738 | 147 |
| 16 | P10 | SENTENCE | 11 | 0.112646 | 0.010241 | 158 |
| 17 | P10 | SENTENCE | 10 | 0.101374 | 0.010137 | 168 |

### The Exact Termination Diagnostic at Step 17
From the saved execution log at step 17:
```json
{
  "stop_reason": "LOW_MARGINAL_VALUE",
  "final_marginal_score": 0.009581493207951706,
  "maximum": 0.009581493207951706,
  "positive_over_budget": 1,
  "step": 17,
  "last_saved_attempts": [
    {
      "parent": "d0a60ebc98f4fa1e54feb0818062a2f2",
      "eligible": true,
      "dc": 56,
      "gain": 0.47512278499109084,
      "ratio": 0.008484335446269479,
      "status": "REJECTED_THRESHOLD",
      "hypothetical": [
        {
          "index": 2,
          "relevance": 0.8059833127580173,
          "coverage_gain": 0.09591236012268278,
          "novelty": 0.24236658434346436,
          "redundancy": 0.7576334156565356,
          "gain": 0.47512278499109084
        }
      ]
    }
  ]
}
```

### Why the Gold Bridge Was Dropped
Look at candidate parent `d0a60ebc98f4fa1e54feb0818062a2f2` (Passage P02, which contains sentence $S_{005}$: *"He garnered a Canadian Screen Award nomination... and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for 'Invader (Invasor)'"*):
- Length: 56 tokens ($\Delta c = 56$).
- Gain: $0.4751$.
- Ratio: $\Delta g / \Delta c = 0.47512 / 56 = \mathbf{0.008484}$.
- Threshold: $\tau_{\text{stop}} = \mathbf{0.010000}$.
- Because $0.008484 < 0.010000$, status was set to **`REJECTED_THRESHOLD`**.
- The highest marginal ratio among all remaining 20 eligible candidates was $0.009581 < 0.01$.
- Allocator terminated with **`LOW_MARGINAL_VALUE`**.
- Result: $S_{005}$ was omitted; reader generated an incorrect hallucination based on Denis Villeneuve's film *Enemy* rather than *Invader*, scoring **F1 = 0.0000**.

---

## 5. What Changed Across Revisions?

| Parameter / Feature | BEA-V1 (Week 12 Initial) | BEA-V2 (Week 12 Refined) |
| :--- | :--- | :--- |
| **Objective Function** | Unweighted semantic heuristic: $\text{Rel} + 0.5 \Delta\text{Cov} - 0.5 \text{Red}$ | Learned utility: $P_{\text{help}} \cdot \max(0, \text{Rel} + 0.5 \Delta\text{Cov} - 0.5 \text{Red})$ |
| **Harm Probability ($P_{\text{harm}}$)** | Intended as negative penalty in draft | **Diagnostic-only** (excluded from allocation loop after collapse) |
| **Stopping Threshold ($\tau_{\text{stop}}$)** | Fixed heuristic: $\mathbf{0.01}$ | Calibrated search $\to$ Post-hoc set to $\mathbf{0.00008}$ |
| **Stopping Behavior** | Early exit via `LOW_MARGINAL_VALUE` | Budget exhaustion (`BUDGET_EXHAUSTED`) |
| **Mean HotpotQA 1024 Tokens** | **284.6** | **948.7** |
| **HotpotQA 1024 QA F1** | **0.3441** | **0.3890** (rescuing the baseline) |

---

## 6. What This Example Does NOT Prove

1. **Does NOT prove greedy allocation is fundamentally flawed:** A greedy knapsack approximation can achieve near-optimal packing if the stopping condition respects the budget capacity.
2. **Does NOT prove $S_{005}$ had low semantic relevance:** The raw relevance was very high ($0.80598$). It was penalized purely by the token-length denominator ($\Delta c = 56$) and the redundancy against already-selected sentences ($0.7576$).
3. **Does NOT mean V2's learned utility solved the calibration problem:** While V2 repaired token utilization by dropping the stopping threshold to $0.00008$, this was a post-hoc stabilization, not a validated learned stopping rule.

---

## 7. Provenance & Verification

- **Code Implementation:** `FINAL_PROJECT_MAIN/7_bea_v1/code/1_bea_qbgf_allocator.py`
- **Audit Logs:** `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (lines 4151–4350 for A04; lines 5406–5930 for A05)
- **Pilot Aspect Mechanism Audit:** `results/post_w12/pilot_aspect_mechanism_audit/W12-POST/PILOT_ASPECT_MECHANISM_AUDIT.md`
- **Unit Importance CSV:** `results/week12/attribution/v1/analysis/unit_importance.csv`
- **Raw Evidence Hashes (Anchor A04):**
  - FIXED: `67aa844189a424350a33addccb17a14e557d5e3023820eee949dcbd6d605937f`
  - QBGF: `1b74a47a22314ffeebd932dbf3bdc74c7ce9d700404454d908ce80293fdcbdc1`
  - V1: `2a98f7e6f85764dca6717a544b62e434f81014e7a83d78c3b4deefbb9c6360c7`
  - V2: `68a2bf6cb915e7178cf3dc2b8b9cbfa943e8ee79dfbf2ba61b17e4b2d3bf30f6`
- **Raw Evidence Hashes (Anchor A05):**
  - FIXED: `8e6f8a7cbe0cc1cde3aace9b63f85c05bde22bfc6f77b747436ab5d9d0201519`
  - QBGF: `0883722d11b0271bf789ed15caa251ffbfd03b6809d8a1d58f49bf917d4a3319`
  - V1: `b31bd479767a7b4cdfe5f5ed863d782efd25ffcc229e3556939db8d72812af1a`
  - V2: `ed177f6c84c33fb4be41f2c13311f07f9b92d47bd0ddfc90d5f8d142ea90211f`

