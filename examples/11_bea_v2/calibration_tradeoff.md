# BEA-V2 Stopping Threshold Calibration Failure and the Starvation-Stopping Tradeoff

**Example ID:** `BEA-V2-CALIB`  
**Dataset / Stage:** Cross-Dataset Calibration Stage (HotpotQA, QASPER, SciFact)  
**Registered Protocol Status:** `CALIBRATION_FAILED_TERMINATED`  
**Exploratory Branch:** `BEA_V2_POSTHOC` ($\tau_{\text{stop}} = 8 \times 10^{-5}$)  
**Source Evidence Files:**
- `FINAL_PROJECT_MAIN/8_bea_v2/results/2_calibration_failed/3_calibration_failed_terminated.json`
- `FINAL_PROJECT_MAIN/8_bea_v2/results/2_calibration_failed/2_resolution_grid_mechanical_results.csv`
- `FINAL_PROJECT_MAIN/8_bea_v2/configs/1_bea_v2_config.json`
- `FINAL_PROJECT_MAIN/8_bea_v2/configs/1_bea_v2_posthoc_config.json`

---

## 1. What This Example Demonstrates

This artifact documents a core methodological finding of the CS787 project: **the impossibility of finding a single static stopping threshold $\tau_{\text{stop}}$ that simultaneously prevents context starvation while performing meaningful early stopping**.

1. **Terminal Calibration Failure:** When optimizing the stopping threshold $\tau_{\text{stop}}$ for BEA-V2 across a preregistered grid on nine calibration queries (3 datasets $\times$ 2 budgets), **no candidate threshold satisfied the preregistered mechanical acceptance criteria**. The calibration stage formally exited with `CALIBRATION_FAILED_TERMINATED`.
2. **Methodological Rigor & Integrity:** Rather than silently relaxing the preregistered constraints or cherry-picking an uncalibrated threshold to claim a false "win," the project preserved the failure record and branched into a clearly designated exploratory engineering evaluation (`BEA_V2_POSTHOC` at $\tau = 8 \times 10^{-5}$).
3. **The Inherent Tradeoff:**
   - At higher thresholds ($\tau \ge 9 \times 10^{-5}$): The allocator stops early on $\ge 20\%$ of queries, but it starves context on longer documents, violating per-cell minimum utilization floors.
   - At lower thresholds ($\tau \le 8 \times 10^{-5}$): The allocator safely fills the budget and passes utilization floors, but early stopping drops to $16.67\%$, failing the preregistered early-stopping floor ($\ge 20\%$) because the allocator simply runs until budget exhaustion (`BUDGET_EXHAUSTED`).

---

## 2. Preregistered Mechanical Qualification Criteria

To prevent trivial or degenerate context allocations, the project preregistered strict acceptance rules in `configs/1_bea_v2_config.json`:

1. **Zero Empty Contexts:** No query may be allocated 0 tokens.
2. **Stopping Rate Floor:** At least **20.0%** of calibration queries must stop via `LOW_MARGINAL_VALUE` (verifying that the threshold actually acts as an adaptive stopping mechanism).
3. **Budget Saturation Ceiling:** At most **80.0%** of allocations may be near-full context (preventing degenerate fallback to static budget exhaustion).
4. **Global Coverage Floor:** Global coverage retention must not degrade relative to the baseline pool.
5. **Per-Cell Feasibility Floors:** Every dataset $\times$ budget cell (6 cells total: HotpotQA, QASPER, SciFact at 256 and 1024 tokens) must satisfy its own minimum token utilization, median selected unit count, and non-trivial exposure constraints.

---

## 3. The Resolution Grid Results

The calibration protocol evaluated a fine resolution grid around the candidate operating region:

| Candidate Threshold ($\tau_{\text{stop}}$) | Threshold Stop Fraction | Threshold Stop $\ge 20\%$? | All 6 Cells Eligible? | Globally Eligible? | Status |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$6.0 \times 10^{-5}$ (`6e-05`)** | $16.67\%$ ($3/18$) | ❌ FAILED ($< 20\%$) | ✅ PASSED (True) | ❌ FAILED | Disqualified |
| **$7.0 \times 10^{-5}$ (`7e-05`)** | $16.67\%$ ($3/18$) | ❌ FAILED ($< 20\%$) | ✅ PASSED (True) | ❌ FAILED | Disqualified |
| **$8.0 \times 10^{-5}$ (`8e-05`)** | $16.67\%$ ($3/18$) | ❌ FAILED ($< 20\%$) | ✅ PASSED (True) | ❌ FAILED | Disqualified |
| **$9.0 \times 10^{-5}$ (`9e-05`)** | $27.78\%$ ($5/18$) | ✅ PASSED ($\ge 20\%$) | ❌ FAILED (False) | ❌ FAILED | Disqualified |

### Verbatim Saved Termination Record
From `FINAL_PROJECT_MAIN/8_bea_v2/results/2_calibration_failed/3_calibration_failed_terminated.json`:
```json
{
  "status": "CALIBRATION_FAILED_TERMINATED",
  "reason": "NO_QUALIFIED_THRESHOLD",
  "grid_evaluated": [6e-05, 7e-05, 8e-05, 9e-05],
  "registered_criteria": {
    "min_stop_fraction": 0.20,
    "max_full_allocation_fraction": 0.80,
    "require_all_cells_eligible": true
  },
  "best_compromise_operating_point": {
    "tau": 8e-05,
    "stop_fraction": 0.16666666666666666,
    "all_cells_eligible": true,
    "globally_eligible": false
  }
}
```

---

## 4. Why Calibration Was Caught in a Structural Trap

The failure of the calibration grid reveals the underlying mathematical tension between sentence-level learned utility and knapsack stopping rules:

```
               HIGH THRESHOLD (tau >= 9e-5)
  +------------------------------------------------------+
  | High early stopping (27.8% >= 20%)                   |
  | BUT: Severe context starvation in long documents     |
  | Fails per-cell minimum utilization floors            |
  +------------------------------------------------------+
                            |
                     UNBRIDGEABLE GAP
                            |
  +------------------------------------------------------+
  | Satisfies all per-cell utilization floors            |
  | BUT: Stops early on only 16.7% (< 20%) of queries    |
  | Allocator degenerates into simple budget exhaustion  |
  +------------------------------------------------------+
                LOW THRESHOLD (tau <= 8e-5)
```

1. **Variance Across Document Lengths:** In SciFact (short abstracts), sentences have high relevance density, so marginal utility remains relatively high even after several sentences. In QASPER (long research papers), sentences are numerous and background information is diffuse; marginal gains drop rapidly below $9 \times 10^{-5}$, triggering starvation before key evidence is collected.
2. **Fixed Denominator Sensitivity:** Shorter sentences produce artificially high $\Delta \text{Gain} / \Delta \text{Cost}$ ratios regardless of content, while long, highly informative sentences (like multi-clause gold evidence in HotpotQA) suffer lower ratios and are prematurely rejected.
3. **No Uniform Value Scale:** Because $P_{\text{help}}$ probabilities vary widely across queries and datasets depending on retrieval score distribution, a single global constant $\tau_{\text{stop}}$ cannot balance adaptive stopping across multi-hop QA, single-hop QA, and scientific claim verification.

---

## 5. The Post-Hoc Diagnostic Branch (`BEA_V2_POSTHOC`)

To evaluate whether BEA-V2's learned usefulness weights ($P_{\text{help}}$) could provide value if context starvation was averted, an exploratory engineering decision was made:
- Select $\tau = 8 \times 10^{-5}$ (`8e-05`) as the operational cutoff. This threshold achieved the highest stopping rate ($16.7\%$) that still satisfied all per-cell utilization floors.
- Execute reader evaluation across the full 50-query development cohort (50 queries $\times$ 3 datasets $\times$ 2 budgets = 300 evaluations).
- Explicitly label this branch as **`BEA_V2_POSTHOC`** in all tables, figures, and code, distinguishing it from an officially calibrated method.

### Downstream Results of the Post-Hoc Study
When evaluated on downstream QA/verification quality:
- **HotpotQA 1024:** Rescued from V1's 0.3441 F1 back to **0.3890 F1** (comparable to `FIXED_SENTENCE` at 0.3893 F1).
- **SciFact 256:** Achieved **0.6586 F1**, trailing `MINILM_CE_SENTENCE` (0.6855 F1) and matching `FIXED_SENTENCE` (0.6289 F1).
- **Global Assessment:** While BEA-V2 solved V1's catastrophic starvation, it did not significantly outperform simple static sentence selection (`FIXED_SENTENCE`) on average, confirming that complex learned-utility stopping rules did not yield net positive utility over fixed-budget sentence packing.

---

## 6. What This Example Proves and Does NOT Prove

### What It Proves:
- The project strictly adhered to preregistered protocols: negative calibration results were faithfully recorded as `CALIBRATION_FAILED_TERMINATED` rather than cosmetically concealed.
- Static stopping thresholds on marginal utility cannot reliably arbitrate between budget exhaustion and early termination across heterogeneous RAG tasks.

### What It Does NOT Prove:
- Does NOT prove learned utility reranking is useless: $P_{\text{help}}$ successfully prioritized key multi-hop sentences (e.g., Anchor A05).
- Does NOT prove adaptive stopping is impossible: it indicates that stopping rules must be conditioned on query-specific or document-length features rather than a single static scalar threshold.

---

## 7. Provenance & Reproduction

- **Termination Audit Record:** `FINAL_PROJECT_MAIN/8_bea_v2/results/2_calibration_failed/3_calibration_failed_terminated.json`
- **Resolution Grid CSV:** `FINAL_PROJECT_MAIN/8_bea_v2/results/2_calibration_failed/2_resolution_grid_mechanical_results.csv`
- **Preregistration Config:** `FINAL_PROJECT_MAIN/8_bea_v2/configs/1_bea_v2_config.json`
- **Post-Hoc Config:** `FINAL_PROJECT_MAIN/8_bea_v2/configs/1_bea_v2_posthoc_config.json`
- **Calibration Engine Code:** `FINAL_PROJECT_MAIN/8_bea_v2/code/4_calibration_and_reader_stages.py` (lines 67–98)
- **Resolution Script:** `FINAL_PROJECT_MAIN/8_bea_v2/code/6_final_calibration_resolution.py` (lines 32–113)

