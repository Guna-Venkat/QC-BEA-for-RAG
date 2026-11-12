# Matched Five-Method Comparison: HotpotQA Multi-Hop Chain Recovery

**Example ID:** `MATCHED-HOTPOT-01`  
**Dataset:** HotpotQA (Multi-Hop QA)  
**Query ID:** `5a7df25a5542990b8f503b02` (Anchor `A05` / Cases `C02`, `C05`)  
**Question:** *"What did the screewriter for a 2013 psychological thriller film directed by Denis Villeneuve get a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for?"*  
**Gold Answer:** `"Invader (Invasor)"`  
**Methods Compared:** `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_QBGF_V1`, `BEA_V2_POSTHOC`, `MINILM_CE_SENTENCE`  
**Budgets Evaluated:** 256 and 1024 tokens  
**Controlled Reader:** Qwen2.5-7B-Instruct (4-bit NF4 quantized, temperature = 0.0)

---

## 1. What This Example Demonstrates

This artifact provides a complete 5-way matched comparison on a single multi-hop reasoning query, illustrating how different evidence selection mechanisms succeed or fail to construct the reasoning bridge:
$$\text{Denis Villeneuve} \xrightarrow{\text{directed}} \text{Enemy (2013)} \xrightarrow{\text{written by}} \text{Javier Gullón} \xrightarrow{\text{27th Goya nomination}} \text{Invader (Invasor)}$$

1. **The Decisive Bridge Sentence ($S_{005}$ in Passage P02):**
   > *"He garnered a Canadian Screen Award nomination for Best Adapted Screenplay at the 2nd Canadian Screen Awards for 'Enemy', and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for 'Invader (Invasor)'."*
2. **Context Starvation Omission in BEA-V1:** BEA-V1 terminated at Step 17 due to its fixed $\tau_{\text{stop}} = 0.01$ threshold, allocating only 168 tokens (leaving 88 unused). It omitted $S_{005}$, causing the reader to hallucinate that the nomination was for *Enemy* (**0.0 F1**).
3. **Recovery Across Dense & Passage Baselines:** `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_V2_POSTHOC`, and `MINILM_CE_SENTENCE` all successfully retained $S_{005}$ at budget 256 and produced the exact gold target entity (**1.0000 F1**).

---

## 2. Five-Method Matched Results at Budget 256

| Metric / Dimension | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC | MINILM_CE_SENTENCE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Evidence Tokens** | 255 | 255 | **168** | 243 | 255 |
| **Budget Utilization** | 99.6% | 99.6% | **65.6%** | 94.9% | 99.6% |
| **Unused Tokens** | 1 | 1 | **88** | 13 | 1 |
| **Selected Units** | 8 | 10 | 17 | 7 | 10 |
| **Represented Parents** | 5 | 5 | 10 | 5 | 5 |
| **Stop Reason** | `FROZEN_BASELINE` | `FROZEN_BASELINE` | `LOW_MARGINAL_VALUE` | `BUDGET_EXHAUSTED` | `FROZEN_BASELINE` |
| **Exposed Decisive $S_{005}$?** | **YES** | **YES** | **NO (OMITTED)** | **YES** | **YES** |
| **Raw Prediction** | `"Invader (Invasor)."` | `"Invader (Invasor)"` | *"The screenwriter... received a Goya Award nomination... for the screenplay of 'Enemy.'"* | `"Invader (Invasor)"` | `"Invader (Invasor)."` |
| **Exact Match (EM)** | **1.0000** | **1.0000** | **0.0000** | **1.0000** | **1.0000** |
| **QA Token F1 Score** | **1.0000** | **1.0000** | **0.0000** | **1.0000** | **1.0000** |

---

## 3. Five-Method Matched Results at Budget 1024

| Metric / Dimension | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC | MINILM_CE_SENTENCE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Evidence Tokens** | 1001.7 (mean) | 995.3 (mean) | **284.6 (mean)** | 960.7 (mean) | 1000.3 (mean) |
| **Query 5a7d... Tokens** | 1022 | 1018 | **268** | 960 | 924 |
| **Query Stop Reason** | `FROZEN_BASELINE` | `FROZEN_BASELINE` | `LOW_MARGINAL_VALUE` | `BUDGET_EXHAUSTED` | `FROZEN_BASELINE` |
| **Raw Prediction** | `"Invader (Invasor)"` | `"Invader (Invasor)"` | Hallucination (*"Enemy"*) | `"Invader (Invasor)"` | `"Invader (Invasor)"` |
| **QA Token F1 Score** | **1.0000** | **1.0000** | **0.0000** | **1.0000** | **1.0000** |

---

## 4. Why BEA-V1 Failed While the Other Four Methods Succeeded

1. **The Greed of the Marginal Threshold:**  
   BEA-V1's marginal threshold $\tau = 0.01$ was scaled for raw relevance gains in unpopulated contexts. Once early passages were added, redundancy grew to $0.7576$ and incremental coverage dropped to $0.0959$. Sentence $S_{005}$ was penalized because it was relatively long (56 tokens), pushing its ratio to $0.00848 < 0.01$. The allocator aborted early, leaving 88 tokens empty at budget 256 and over 700 tokens empty at budget 1024.
2. **How BEA-V2 Rescued the Chain:**  
   BEA-V2 weighted marginal gain by the learned usefulness model: $P_{\text{help}}(S_{005}) = 0.1259$. Because $S_{005}$ was identified as highly useful, it was selected in Step 1 before redundancy penalties accumulated. Dropping the stopping threshold to $\tau = 8 \times 10^{-5}$ ensured the allocator filled the budget.
3. **Why Baselines Were Robust:**  
   Both `FIXED_SENTENCE` and `QBGF_FULL` unpack evidence by top-retrieved passages. Because passage P02 (*Javier Gullón*) had high retrieval similarity, its top sentences were packed directly into the budget without being prematurely pruned by an aggressive marginal threshold. MiniLM Cross-Encoder reranking scored $S_{005}$ high enough to fit within the top 255 tokens.

---

## 5. What This Example Does NOT Prove

- **Does NOT prove BEA-V2 is globally superior to FIXED_SENTENCE or QBGF:** On this query, `FIXED_SENTENCE`, `QBGF_FULL`, and `BEA_V2_POSTHOC` all scored 1.0000. Across the full 50-query HotpotQA cohort, BEA-V2 (0.4234 F1) slightly exceeded FIXED (0.3893 F1), but this difference is not statistically significant under Holm-Bonferroni correction.
- **Does NOT prove MiniLM cross-encoders always solve multi-hop QA:** On this query, $S_{005}$ contained explicit Goya Award tokens that aligned with the query text. On multi-hop queries where the second hop has zero lexical overlap with the query, MiniLM systematically ranks bridge sentences lower (explaining its lower macro F1 of 0.3404 on HotpotQA 256).

---

## 6. Provenance & Artifact Hashes

- **Query ID:** `5a7df25a5542990b8f503b02`
- **Case Reference:** Anchor `A05` (lines 5404–6078 in `FINAL_QUALITATIVE_CASE_STUDY_REPORT.md`)
- **Evidence Hashes (Budget 256):**
  - FIXED: `8e6f8a7cbe0cc1cde3aace9b63f85c05bde22bfc6f77b747436ab5d9d0201519`
  - QBGF: `0883722d11b0271bf789ed15caa251ffbfd03b6809d8a1d58f49bf917d4a3319`
  - BEA-V1: `b31bd479767a7b4cdfe5f5ed863d782efd25ffcc229e3556939db8d72812af1a`
  - BEA-V2: `ed177f6c84c33fb4be41f2c13311f07f9b92d47bd0ddfc90d5f8d142ea90211f`
  - MiniLM: `415427aff723710db80241bd8295996bd7096e752cdad3863e085edce4b8c8bb`
- **Prompt Hashes (Budget 256):**
  - FIXED / MiniLM: `a903c7e6f176c5106419c552007f5b72ca7f6a356eef88ce102cf57ff48efc7e`
  - QBGF: `9ff7b1d184c9093d1847cd6588a599010b6ba66ab10ed389204f962a77d00d17`
  - BEA-V1: `4c8231257a321425fc4cf64f8c75aefe1f22e01bc8da4511c319848823b715f0`
  - BEA-V2: `be21d42adfb5c2aaa18b7640069ceaa456466cea72b4f1db21634d2af0c2745b`

