# Matched Five-Method Comparison: QASPER Baseline Identification

**Example ID:** `MATCHED-QASPER-01`  
**Dataset:** QASPER (Long-Document Scientific QA)  
**Query ID:** `7b4992e2d26577246a16ac0d1efc995ab4695d24` (Anchor `A02`)  
**Paper ID:** `1707.05236`  
**Question:** *"What was the baseline used?"*  
**Gold Answer:** `["Rei2016", "Rei2016 model", "the model of Rei (2016)"]`  
**Methods Compared:** `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_QBGF_V1`, `BEA_V2_POSTHOC`, `MINILM_CE_SENTENCE`  
**Budget Evaluated:** 256 tokens  
**Controlled Reader:** Qwen2.5-7B-Instruct (4-bit NF4 quantized, temperature = 0.0)

---

## 1. What This Example Demonstrates

This artifact documents a standout case where **QBGF (Query-Conditioned Budget-Aware Evidence Allocation) decisively defeated all other allocation strategies, scoring F1 = 0.8000 while all four competing methods scored F1 = 0.0000**.

1. **The Decisive Target Fact:** In scientific NLP papers, multiple baselines or annotation standards may be mentioned in passing. The target baseline for the paper's primary model evaluation is the **`Rei2016`** model.
2. **The "Annotation" Distractor Trap:** The paper also discusses dataset preparation, mentioning *"manual annotation"* as a baseline process for ground-truth curation. Competing allocators (`FIXED_SENTENCE`, `BEA_QBGF_V1`, `BEA_V2_POSTHOC`, and `MINILM_CE_SENTENCE`) all fell into this lexical trap, prioritizing sentences that discuss manual annotation and omitting the model baseline.
3. **How QBGF Solved It:** QBGF's knapsack formulation evaluates combinations of candidate passage fidelities ($\text{SENT}_2, \text{SENT}_4, \text{SENT}_8, \text{FULL}$) against a multi-aspect query coverage objective. The dynamic program selected the specific 2-sentence option from the experimental setup section that explicitly introduced the Rei (2016) model comparison, providing the reader with the precise fact needed to output `"Rei2016 model"`.

---

## 2. Five-Method Matched Results at Budget 256

| Metric / Dimension | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC | MINILM_CE_SENTENCE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Evidence Tokens** | 255 | 255 | 245 | 245 | 255 |
| **Budget Utilization** | 99.6% | 99.6% | 95.7% | 95.7% | 99.6% |
| **Unused Tokens** | 1 | 1 | 11 | 11 | 1 |
| **Selected Units** | 9 | 10 | 20 | 11 | 10 |
| **Represented Parents** | 6 | 6 | 9 | 5 | 7 |
| **Stop Reason** | `FROZEN_BASELINE` | `FROZEN_BASELINE` | `BUDGET_EXHAUSTED` | `BUDGET_EXHAUSTED` | `FROZEN_BASELINE` |
| **Exposed `Rei2016` Sentence?** | **NO** | **YES** | **NO** | **NO** | **NO** |
| **Raw Model Output** | *"manual annotation"* | *"Rei2016 model"* | *"manual annotation"* | *"manual annotation"* | *"The baseline used was manual annotation."* |
| **Exact Match (EM)** | **0.0000** | **0.0000** | **0.0000** | **0.0000** | **0.0000** |
| **QA Token F1 Score** | **0.0000** | **0.8000** | **0.0000** | **0.0000** | **0.0000** |
| **Outcome** | Distractor Trap | **WINNER** | Distractor Trap | Distractor Trap | Distractor Trap |

---

## 3. Microscopic Failure Analysis: The Distractor Trap

### What the Four Failing Methods Selected
`FIXED_SENTENCE`, `BEA-V1`, `BEA-V2`, and `MINILM` evaluated sentences based on high isolated relevance to *"What was the baseline used?"*. They selected:
> *"For dataset curation, we use manual annotation as a baseline reference for error analysis..."*

Because the words *"annotation as a baseline"* perfectly match the query phrase *"baseline used"*, the cross-encoder and bi-encoder models assigned this sentence top rank. Under the 256-token budget ceiling, there was no room left for the experimental section. Deprived of the model comparison text, the Qwen reader faithfully answered:
```text
"The baseline used was manual annotation." (F1 = 0.0000)
```

### What QBGF Selected
Instead of independently greedy sentence ranking, QBGF solves a Multiple-Choice Knapsack Problem (MCKP) across candidate passage blocks:
$$\max \sum_{i=1}^m \sum_{k \in \mathcal{K}} x_{i,k} \cdot U(i, k) \quad \text{s.t.} \quad \sum_{i=1}^m \sum_{k \in \mathcal{K}} x_{i,k} \cdot c(i, k) \le B$$
Where option $k \in \{\text{SENT}_2, \text{SENT}_4, \text{SENT}_8, \text{FULL}\}$ for passage $i$.

Because QBGF evaluates the joint coverage of query aspects across entire selected blocks, the solver selected a 2-sentence slice from the experimental results section:
> *"We compare our approach against the state-of-the-art sequence labeling baseline proposed by Rei (2016)."*

With this sentence exposed in context, the reader identified the true algorithmic baseline and generated:
```text
"Rei2016 model" (F1 = 0.8000)
```

---

## 4. What This Example Does NOT Prove

1. **Does NOT prove QBGF is universally superior on QASPER:** Across the entire 50-query QASPER cohort at budget 256, `FIXED_SENTENCE` achieved **0.2668 F1**, slightly outperforming `QBGF_FULL` (**0.2641 F1**). QBGF's knapsack optimization helps on structured comparative queries, but adds negligible value over uniform sentence packing on broad informational queries.
2. **Does NOT prove cross-encoders are defective:** MiniLM correctly ranked a sentence matching the literal query tokens; it failed because the query itself was ambiguous without broader document structure.

---

## 5. Provenance & Artifact Hashes

- **Query ID:** `7b4992e2d26577246a16ac0d1efc995ab4695d24`
- **Case Reference:** Anchor `A02` (lines 75, 4140–4150 in `FINAL_QUALITATIVE_CASE_STUDY_REPORT.md`)
- **QBGF Directory:** `FINAL_PROJECT_MAIN/examples/08_qbgf/7b4992e2d26577246a16ac0d1efc995ab4695d24_worked_example/`
- **MiniLM Raw Diagnostic:** `FINAL_PROJECT_MAIN/9_minilm_reranker/results/4_diagnostics/rows/cbd40a825d5be9c4b4b45bf54ae25d004794d6dc5d23ea46018d43171288f871.json` (line 355)
- **Controlled Reader:** Qwen2.5-7B-Instruct (hash `ad461e40ced4c4adb8ef25430e56e0852d9b0f4a9939018d9f37ab9768fc1158`)

