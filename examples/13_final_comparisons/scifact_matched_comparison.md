# Matched Five-Method Comparison: SciFact Scientific Claim Verification

**Example ID:** `MATCHED-SCIFACT-01`  
**Dataset:** SciFact (Scientific Claim Verification)  
**Query ID:** `1132` (PMID `33499189`)  
**Claim:** *"TCR/CD3 microdomains are a required to induce the immunologic synapse to activate T cells."*  
**Gold Label:** `SUPPORT`  
**Methods Compared:** `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_QBGF_V1`, `BEA_V2_POSTHOC`, `MINILM_CE_SENTENCE`  
**Budgets Evaluated:** 256 and 1024 tokens  
**Controlled Reader:** Qwen2.5-7B-Instruct (4-bit NF4 quantized, temperature = 0.0, strict 1-token output contract)

---

## 1. What This Example Demonstrates

This artifact documents the performance of the five allocation methods on a strict 3-class scientific claim verification task (`SUPPORT`, `REFUTE`, `NOT_ENOUGH_INFO`).

1. **The Decisive Biological Assertion ($S_{\text{gold}}$ in PMID 33499189):**
   > *"The ligation of TCR/CD3 on CD4 or CD8 T cells led to CD3 nanoscale co-clustering or interaction with CD4 or CD8 co-receptors forming 200-500 nm nano-domains or >500 nm micro-domains... critical for maturation of the immune synapse and for T cell activation."*
2. **Failure of Coarse Allocation at Tight Budgets:** At budget 256, both `QBGF_FULL` and `BEA_QBGF_V1` failed to allocate the decisive sentence, allocating instead surrounding contextual background about general synapse imaging. As a result, the reader output `NOT_ENOUGH_INFO` (**Score = 0.0**).
3. **Cross-Encoder & Sentence Packing Success:** `MINILM_CE_SENTENCE`, `FIXED_SENTENCE`, and `BEA_V2_POSTHOC` successfully selected the decisive microdomain sentence within the 256-token limit, enabling the reader to verify the claim as `SUPPORT` (**Score = 1.0**).
4. **General SciFact Superiority of MiniLM:** Across the 50-query cohort, MiniLM won decisively at both 256 tokens (**0.6855 macro-F1** vs. 0.6289 for FIXED, 0.5310 for QBGF) and 1024 tokens (**0.6479 macro-F1** vs. 0.5533 for FIXED, 0.5881 for QBGF).

---

## 2. Five-Method Matched Results at Budget 256

| Metric / Dimension | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC | MINILM_CE_SENTENCE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Evidence Tokens** | 253 | 251 | 250 | 242 | 253 |
| **Budget Utilization** | 98.7% | 97.9% | 97.7% | 94.7% | 98.8% |
| **Unused Tokens** | 3 | 5 | 6 | 14 | 3 |
| **Selected Units** | 6 | 8 | 15 | 6 | 7 |
| **Represented Parents** | 3 | 3 | 8 | 4 | 6 |
| **Stop Reason** | `FROZEN_BASELINE` | `FROZEN_BASELINE` | `BUDGET_EXHAUSTED` | `BUDGET_EXHAUSTED` | `FROZEN_BASELINE` |
| **Exposed Decisive $S_{\text{gold}}$?** | **YES** | **NO** | **NO** | **YES** | **YES** |
| **Reader Prediction** | `SUPPORT` | `NOT_ENOUGH_INFO` | `NOT_ENOUGH_INFO` | `SUPPORT` | `SUPPORT` |
| **Correctness (0/1)** | **1.0** | **0.0** | **0.0** | **1.0** | **1.0** |
| **Format Valid?** | YES (3 tokens) | YES (3 tokens) | YES (3 tokens) | YES (3 tokens) | YES (3 tokens) |

---

## 3. Five-Method Matched Results at Budget 1024

| Metric / Dimension | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC | MINILM_CE_SENTENCE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Evidence Tokens** | 1021 | 1019 | 696 | **355** | 1021 |
| **Budget Utilization** | 99.7% | 99.5% | 68.0% | **34.7%** | 99.7% |
| **Unused Tokens** | 3 | 5 | 328 | **669** | 3 |
| **Stop Reason** | `FROZEN_BASELINE` | `FROZEN_BASELINE` | `LOW_MARGINAL_VALUE` | `LOW_MARGINAL_VALUE` | `FROZEN_BASELINE` |
| **Exposed Decisive $S_{\text{gold}}$?** | **YES** | **YES** | **NO** | **YES** | **YES** |
| **Reader Prediction** | `SUPPORT` | `SUPPORT` | `NOT_ENOUGH_INFO` | `SUPPORT` | `SUPPORT` |
| **Correctness (0/1)** | **1.0** | **1.0** | **0.0** | **1.0** | **1.0** |

---

## 4. Why MiniLM and Sentence Selection Excel on SciFact

1. **Precision vs. Dilution in Claim Verification:**  
   Unlike HotpotQA (which requires chaining disparate facts across documents), SciFact is intrinsically **single-sentence decisive**. A single sentence stating that *"TCR microdomains are critical for maturation of the immune synapse"* completely confirms the claim. Adding full passage blocks introduces irrelevant experimental protocols (e.g. imaging wavelengths, antibody concentrations) that dilute the context and risk triggering reader polarity errors.
2. **Why QBGF Suffered at 256 Tokens:**  
   QBGF solves an MCKP across discrete passage options. When evaluating candidate passages, it frequently upgrades whole passages to `FULL` or expands sentence groups to maximize aggregate lexical coverage of all claim terms. At a tight 256-token budget, upgrading one background passage to `FULL` consumed budget that squeezed out the decisive sentence from PMID 33499189.
3. **Cross-Encoder Direct Token Interactions:**  
   The `ms-marco-MiniLM-L-6-v2` cross-encoder compares the entire claim directly against each candidate sentence through 6 Transformer cross-attention layers. It directly aligns `"required to induce"` with `"critical for maturation"`, assigning the highest rank to the gold assertion and guaranteeing its inclusion in the prompt.

---

## 5. What This Example Does NOT Prove

1. **Does NOT prove adaptive allocation is useless:** In BEA-V2 at 1024 tokens, the allocator stopped after allocating only 355 tokens (leaving 669 unused) because all necessary evidence had been collected. The reader correctly predicted `SUPPORT`, demonstrating that when key evidence is captured early, expanding to 1024 tokens provides zero additional accuracy.
2. **Does NOT mean MiniLM eliminates all SciFact errors:** As seen in Anchor A06 (Claim 993, *Pyridostatin*), even when the decisive refuting sentence is exposed, readers can still conflate biological polarities (e.g., stabilizing a quadruplex vs. destabilizing telomeric DNA). Evidence selection is necessary but not sufficient for correct scientific reasoning.

---

## 6. Provenance & Reproduction

- **Claim ID:** `1132` (PMID `33499189`, Case Reference `C19`)
- **Diagnostic Row (MiniLM):** `FINAL_PROJECT_MAIN/9_minilm_reranker/results/4_diagnostics/rows/4aa989c3f367fc9d9c8251163ea190bf9650b9fc5ba665c7085bb23bbfae0d78.json` (line 351)
- **Diagnostic Row (BEA-V2 1024):** `FINAL_PROJECT_MAIN/8_bea_v2/results/3_posthoc_reader_run/rows/1b522193fc4e704bb7a5bf9c90ac97c6b482c914853694bb7c5060bde0985c99.json`
- **Diagnostic Row (FIXED 256):** `FINAL_PROJECT_MAIN/8_bea_v2/results/3_posthoc_reader_run/rows/349595a3b680a8119ac37bb663b813a688819f3f4fb8b184aa0710694b562aa3.json`
- **Diagnostic Row (QBGF 256):** `FINAL_PROJECT_MAIN/8_bea_v2/results/3_posthoc_reader_run/rows/54d13d0c88633fe04b3bcb2ecf8c16c0401df445fc1cbea62714983d04b60463.json`
- **Selection Change Record:** `FINAL_PROJECT_MAIN/8_bea_v2/results/3_posthoc_reader_run/posthoc_selection_changes.csv`

