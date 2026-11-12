# Learned Utility Rescue in BEA-V2: Restoring the Gold Multi-Hop Chain

**Example ID:** `BEA-V2-01`  
**Dataset:** HotpotQA  
**Query ID:** `5a7df25a5542990b8f503b02` (Anchor `A05` / Cases `C02`, `C05`)  
**Question:** *"What did the screewriter for a 2013 psychological thriller film directed by Denis Villeneuve get a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for?"*  
**Gold Answer:** *"Invader (Invasor)"*  
**Focal Methods:** `BEA_V2_POSTHOC` vs. `BEA_QBGF_V1` (with `FIXED_SENTENCE` and `QBGF_FULL` references)  
**Budgets Evaluated:** 256 tokens (and 1024 tokens)  
**Recovery Status:** Fully recovered from exact saved execution traces, diagnostic logs, and reader outputs.

---

## 1. What This Example Demonstrates

This artifact documents how **BEA-V2** repaired the multi-hop reasoning failure of BEA-V1 by incorporating a learned usefulness weight ($P_{\text{help}}$) and a re-scaled stopping threshold ($\tau_{\text{stop}} = 8 \times 10^{-5}$).

1. **V1 Multi-Hop Omission (F1 = 0.0000):** In BEA-V1, the allocator terminated at 168 tokens due to its coarse stopping threshold ($\tau = 0.01$). It omitted the critical bridge sentence $S_{005}$ (*"He garnered a Canadian Screen Award nomination... and a Goya Award nomination... for 'Invader (Invasor)'"*). As a result, the Qwen reader hallucinated that the screenwriter was nominated for *Enemy*, producing a long incorrect response with **0.0 F1**.
2. **V2 Prioritization & Recovery (F1 = 1.0000):** In BEA-V2, sentence $S_{005}$ was assigned a high learned helpfulness probability ($P_{\text{help}} = 0.1259$, among the highest in the candidate pool). In Step 1, V2 selected $S_{005}$ immediately with value $0.152065$ and marginal ratio $0.002715 \gg 0.00008$. With both Denis Villeneuve's film *Enemy* and Javier Gullón's nomination for *Invader* present in context, the reader generated the exact gold entity: `"Invader (Invasor)"` (**F1 = 1.0000**).
3. **The Mathematical Formulation:**
   BEA-V2 computes the step-wise utility of sentence $s$ as:
   $$U(s) = P_{\text{help}}(s) \cdot \max(0, \Delta \text{Gain}(s))$$
   $$\Delta \text{Gain}(s) = \text{Rel}(s) + 0.5 \cdot \Delta \text{Cov}(S \cup \{s\}) - 0.5 \cdot \text{Red}(s, S)$$
   Critically, while $P_{\text{harm}}$ was predicted by a parallel cross-fitted classifier, it was retained as **diagnostic-only** after pilot testing revealed that penalizing $P_{\text{harm}}$ led to catastrophic under-allocation on multi-hop questions.

---

## 2. Quantitative Comparison on Anchor A05

### At Budget 256 Tokens

| Metric / Dimension | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC |
| :--- | :---: | :---: | :---: | :---: |
| **Evidence Tokens** | 255 | 255 | **168** | 243 |
| **Budget Utilization** | 99.6% | 99.6% | **65.6%** | 94.9% |
| **Unused Tokens** | 1 | 1 | **88** | 13 |
| **Stop Reason** | `FROZEN_BASELINE` | `FROZEN_BASELINE` | `LOW_MARGINAL_VALUE` | `BUDGET_EXHAUSTED` |
| **Exposed Decisive $S_{005}$?** | **YES** | **YES** | **NO (OMITTED)** | **YES** |
| **Full Gold-Span Recall** | 100.0% | 50.0% | **0.0%** | 100.0% |
| **Gold-Token Coverage** | 100.0% | 49.1% | **0.0%** | 100.0% |
| **Mean Selected $P_{\text{help}}$** | N/A | N/A | N/A | **0.062871** |
| **QA Exact Match (EM)** | **1.0000** | **1.0000** | **0.0000** | **1.0000** |
| **QA F1 Score** | **1.0000** | **1.0000** | **0.0000** | **1.0000** |

---

## 3. Microscopic Trace: Why V2 Selected $S_{005}$ on Step 1

From the exact recorded execution trace of BEA-V2 on Query `5a7df25a5542990b8f503b02` at budget 256:

### Step 1 Hypothetical Addition Terms
- **Candidate:** Sentence $S_{005}$ (Unit `3cce4986f2a64a7b5645e808649eea5b`, Passage P02, 56 tokens)
  > *"He garnered a Canadian Screen Award nomination for Best Adapted Screenplay at the 2nd Canadian Screen Awards for 'Enemy', and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for 'Invader (Invasor)'."*
- **Relevance ($\text{Rel}$):** $0.805983$
- **Incremental Coverage Gain ($\Delta \text{Cov}$):** $0.803187$
- **Redundancy Penalty ($\text{Red}$):** $0.000000$ (first selected unit)
- **Information Gain ($\text{IG}$):** $0.805983 + 0.5 \times 0.803187 - 0 = \mathbf{1.207577}$
- **Learned Utility Weight ($P_{\text{help}}$):** $\mathbf{0.125925}$
- **Combined Value ($U$):** $0.125925 \times 1.207577 = \mathbf{0.152065}$
- **Incremental Cost ($\Delta c$):** $56$ tokens
- **Marginal Ratio:** $0.152065 / 56 = \mathbf{0.00271544}$
- **Stopping Threshold:** $\tau_{\text{stop}} = \mathbf{0.00008}$
- **Selection Decision:** Since $0.00271544 \gg 0.00008$, candidate was **`CHOSEN`** as Step 1.

### Contrast with V1
In BEA-V1, $S_{005}$ was not evaluated first because unweighted coverage heuristics favored other introductory snippets. By Step 17 (cumulative tokens = 168), when $S_{005}$ was finally evaluated:
- $\text{Red} = 0.7576$ (penalized by prior Goya Award text)
- $\Delta \text{Cov} = 0.0959$
- Marginal gain $= 0.4751$
- Marginal ratio $= 0.4751 / 56 = \mathbf{0.008484}$
- Because BEA-V1 used $\tau = \mathbf{0.01}$, it was **`REJECTED_THRESHOLD`**, and allocation terminated.

---

## 4. Complete Transition Sequence of BEA-V2 at Budget 256

Verbatim from `FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (lines 5932–5942):

| Step | Parent | Kind | Selected Sentence | Incremental Tokens | Saved Gain | Marginal Value/Token | Cumulative Tokens |
| :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | P02 | SENTENCES | $S_{005}$ (Award nomination for *Invader*) | 56 | 0.152065 | 0.002715 | 56 |
| 2 | P02 | SENTENCES | $S_{004}$ (*Javier Gullón is a Spanish screenwriter*) | 11 | 0.015451 | 0.001405 | 67 |
| 3 | P02 | FULL | $S_{003}$ (Title header upgrade) | 6 | 0.005420 | 0.000903 | 73 |
| 4 | P07 | SENTENCES | $S_{018}$ (Actor Javier Pereira Goya nomination) | 33 | 0.024860 | 0.000753 | 106 |
| 5 | P01 | SENTENCES | $S_{002}$ (Goya Award for Best Adapted Screenplay def.) | 39 | 0.028349 | 0.000727 | 145 |
| 6 | P01 | SENTENCES | $S_{001}$ (Header) | 10 | 0.012270 | 0.001227 | 155 |
| 7 | P09 | SENTENCES | $S_{024}$ (*It won the Goya Award for Best Film...*) | 19 | 0.012349 | 0.000650 | 174 |
| 8 | P09 | SENTENCES | $S_{025}$ (*It is available in the United States...*) | 12 | 0.009791 | 0.000816 | 186 |
| 9 | P03 | SENTENCES | $S_{007}$ (*Enemy is a 2013 psychological thriller film...*) | 57 | 0.033791 | 0.000593 | **243** |

At Step 9, remaining budget was $256 - 243 = 13$ tokens. Subsequent candidates required $\ge 27$ tokens and were rejected with `REJECTED_COST`. Allocator terminated with **`BUDGET_EXHAUSTED`**.

---

## 5. Raw Reader Outputs Comparison

### BEA-V1 Reader Output (168 evidence tokens, F1 = 0.0000)
```text
The screenwriter for the 2013 psychological thriller film "Enemy" directed by Denis Villeneuve received a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for the screenplay of "Enemy."
```
*Failure mechanism:* Without $S_{005}$, the reader saw mentions of Denis Villeneuve and *Enemy*, and fabricated that the nomination was for *Enemy*.

### BEA-V2 Reader Output (243 evidence tokens, F1 = 1.0000)
```text
"Invader (Invasor)"
```
*Success mechanism:* With both $S_{005}$ (P02) and $S_{007}$ (P03) exposed, the reader resolved the two-hop bridge: Denis Villeneuve directed *Enemy*, Javier Gullón wrote *Enemy*, and Javier Gullón was nominated at the 27th Goya Awards for *Invader (Invasor)*.

---

## 6. What This Example Does NOT Prove

1. **Does NOT prove BEA-V2 is globally superior to baselines:** Across the entire 50-query cohort, BEA-V2 post-hoc achieved 0.3890 F1 at 1024 tokens, essentially identical to `FIXED_SENTENCE` (0.3893 F1) and `QBGF_FULL` (0.3891 F1). It repaired V1's severe starvation, but did not outperform static sentence selection.
2. **Does NOT prove $P_{\text{harm}}$ is useless in principle:** The finding that $P_{\text{harm}}$ had to be disabled was specific to this pipeline's linear logistic calibration. A more expressive model or joint probability calibration might theoretically use harmfulness signals without inducing context starvation.
3. **Does NOT constitute a valid calibration pass:** As detailed in `calibration_tradeoff.md`, the stopping threshold $\tau = 8 \times 10^{-5}$ was selected post-hoc after formal calibration failed preregistered constraints.

---

## 7. Provenance & Artifact Hashes

- **Query ID:** `5a7df25a5542990b8f503b02`
- **Case Reference:** Anchor `A05` (lines 5404–6078 in `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md`)
- **Code:** `FINAL_PROJECT_MAIN/8_bea_v2/code/1_usefulness_weighted_allocator.py`
- **V2 Post-Hoc Config:** `FINAL_PROJECT_MAIN/8_bea_v2/configs/1_bea_v2_posthoc_config.json`
- **Evidence Hashes:**
  - V1 Evidence Hash: `b31bd479767a7b4cdfe5f5ed863d782efd25ffcc229e3556939db8d72812af1a`
  - V2 Evidence Hash: `ed177f6c84c33fb4be41f2c13311f07f9b92d47bd0ddfc90d5f8d142ea90211f`
- **Reader Prompt Hash (V2):** `be21d42adfb5c2aaa18b7640069ceaa456466cea72b4f1db21634d2af0c2745b`

