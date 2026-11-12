# Final Forensic Audit: Experimental Example Collection

**Project:** Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation (CS787)  
**Audit Date:** 2026-11-09  
**Audit Target:** `FINAL_PROJECT_MAIN/examples/`  
**Compliance Standard:** Mandatory Zero Fabrication, Full Traceability, Immutable Historical Bounds.

---

## 1. Compliance Checklist & Integrity Sign-Off

| Requirement | Audit Criterion | Audit Result | Evidence / Verification |
| :--- | :--- | :---: | :--- |
| **Workspace Boundary** | Work strictly inside `FINAL_PROJECT_MAIN/examples/`. Zero files outside modified, deleted, or moved. | ✅ **PASSED** | Verified via `git status`; only `FINAL_PROJECT_MAIN/examples/` contains new files. |
| **Zero Fabrication** | Zero synthetic passages, zero invented model outputs, zero mock data presented as experimental results. | ✅ **PASSED** | All outputs, hashes, token counts, and metrics match frozen disk files. |
| **Per-Query Grounding** | No inferring per-query behavior from aggregate cohort means. | ✅ **PASSED** | All individual query rows link to exact saved records or explicit historical logs. |
| **Traceability Protocol** | Every example traces to saved inputs, outputs, selections, attributions, or metric files. | ✅ **PASSED** | Explicit hashes, line numbers, and file paths documented in every file. |
| **Calibration Rigor** | Failed calibrations documented as failed; exploratory runs labeled as exploratory. | ✅ **PASSED** | `CALIBRATION_FAILED_TERMINATED` recorded; `BEA_V2_POSTHOC` clearly flagged. |
| **Cohort Separation** | Never pool early exploratory runs (Weeks 1–9) with frozen reader runs (Weeks 11–12). | ✅ **PASSED** | Early Command-R-Plus runs strictly separated from Week 11–12 Qwen runs. |

---

## 2. Quantitative Recovery Summary

- **Total Curated Artifact Files Created:** 24 example markdown files + 4 master audit files + 7 worked-example machine files = **35 files**.
- **Total Master Index Entries:** 24 rows in `00_EXAMPLE_INDEX.csv` across 22 required columns.
- **Fully Recovered with Exact Hashes & Raw Outputs:** 18 examples (100% byte-exact across inputs, prompt hashes, evidence hashes, and generation strings).
- **Recovered from Historical Benchmark JSONs / Traces:** 6 examples (Weeks 1–9 historical logs where raw intermediate prompt caches were purged in disk cleanups, fully documented in `00_MISSING_EXAMPLES.md`).
- **Fabricated / Synthetic Examples:** **0 (ZERO)**.
- **Modified Parent Files Outside `examples/`:** **0 (ZERO)**.

---

## 3. Coverage of Scientific Questions Addressed

| Scientific Question Addressed in Collection | Primary Artifact File | Key Finding Demonstrated |
| :--- | :--- | :--- |
| **What does each dataset actually look like?** | `01_datasets/*.md` | HotpotQA multi-hop chains, QASPER long-paper sparsity, SciFact 1-token verification contracts. |
| **Why did SARA motivate adaptive context allocation?** | `02_sara_context/*.md` | Query 1002 peaks at $k=0$ (distractor avoidance); Query 1001 requires $k=6$ (context starvation). |
| **Why was predicting context size difficult?** | `03_qcca_context_prediction/*.md` | Asymmetric loss landscape: under-allocation causes complete failure (-1.0 F1), over-allocation causes mild dilution (-0.05 F1). |
| **Why did passage identity matter?** | `04_passage_identity/*.md` | At fixed $k=4$, retrieving the correct Rank 8 passage swings F1 from 0.00 to 1.00. |
| **Why did exact sentence selection beat learned alternatives?** | `05_intermediate_routing/*.md` | Generative sentence extraction distorts entities (-0.0213 F1 regression); learned utility routers suffer distribution shift. |
| **Why was Qwen chosen as the controlled reader?** | `06_reader_retriever_confounds/*.md` | Mistral (1849/1850) and Llama (1826/1850) suffered catastrophic format violations; Qwen produced 0 violations. |
| **Why did evidence granularity change with budget?** | `07_granularity/*.md` | Sentences dominate at 256 tokens (precision); full passage blocks recover quality at 1024 tokens (continuity). |
| **How exactly does QBGF allocate evidence?** | `08_qbgf/7b4992.../` | Solves MCKP dynamic program across discrete passage fidelities ($\text{SENT}_2, \text{SENT}_4, \text{SENT}_8, \text{FULL}$) with query conditioning. |
| **Why did QBGF fail to consistently improve quality?** | `08_qbgf/` and `13_final_comparisons/` | Upgrading non-decisive passages to FULL crowded out decisive sentences on tight budgets (e.g. SciFact 256). |
| **What did LOO reveal about relevance vs. utility?** | `09_loo/*.md` | Identifies true helpful units ($\Delta=-0.91$), neutral units ($\Delta=0$, caused by redundancy), and harmful distractors ($\Delta=+1.0$). |
| **Why was BEA-V1 proposed?** | `10_bea_v1/*.md` | Bottom-up greedy selection designed to allocate fine-grained sentence spans directly under token budgets. |
| **Why did BEA-V1 suffer context starvation?** | `10_bea_v1/*.md` | Static stopping threshold $\tau=0.01$ stopped allocation early (mean 284.6 tokens at 1024 budget), stranding 739 tokens. |
| **How does BEA-V2 differ?** | `11_bea_v2/bea_v2_learned_utility_rescue.md` | Weights marginal gain by learned usefulness $P_{\text{help}}$, prioritizing key multi-hop sentences in Step 1. |
| **Why did BEA-V2 calibration fail?** | `11_bea_v2/calibration_tradeoff.md` | No threshold simultaneously satisfied early-stopping floors ($\ge 20\%$) and per-cell utilization floors (`CALIBRATION_FAILED_TERMINATED`). |
| **Why did each method win different conditions?** | `12_minilm_crossencoder/` & `13_final_comparisons/` | MiniLM wins SciFact (single decisive sentences); QBGF wins QASPER 1024 (variable granularity); FIXED wins QASPER 256 (uniform packing); BEA-V2 wins HotpotQA (multi-hop utility). |

---

## 4. Directory Inventory

```text
FINAL_PROJECT_MAIN/examples/
├── 00_ARTIFACT_MAP.md
├── 00_EXAMPLE_INDEX.csv
├── 00_MISSING_EXAMPLES.md
├── FINAL_EXAMPLE_AUDIT.md
├── README.md
├── 01_datasets/
│   ├── hotpotqa_multihop_example.md
│   ├── qasper_sparsity_example.md
│   └── scifact_verification_example.md
├── 02_sara_context/
│   ├── 1001_context_sensitivity.md
│   └── 1002_context_sensitivity.md
├── 03_qcca_context_prediction/
│   └── asymmetric_payoff_example.md
├── 04_passage_identity/
│   ├── 917_fixed_k4_comparison.md
│   └── 917_fixed_k4_extract.json
├── 05_intermediate_routing/
│   ├── draft_promotion_example.md
│   ├── extraction_vs_exact_sentences.md
│   └── learned_utility_vs_semantic_k8.md
├── 06_reader_retriever_confounds/
│   ├── retriever_candidate_recall_comparison.md
│   └── scifact_reader_format_confound.md
├── 07_granularity/
│   └── budget_granularity_tradeoff.md
├── 08_qbgf/
│   ├── 7b4992e2d26577246a16ac0d1efc995ab4695d24_worked_example/
│   │   ├── README.md
│   │   ├── answer.txt
│   │   ├── candidate_passages.json
│   │   ├── option_table.csv
│   │   ├── provenance.json
│   │   ├── query.json
│   │   └── selected_evidence.txt
│   └── query_conditioning_ablation.md
├── 09_loo/
│   ├── loo_canonical_examples.md
│   └── loo_failure_mechanisms.md
├── 10_bea_v1/
│   └── bea_v1_context_starvation.md
├── 11_bea_v2/
│   ├── bea_v2_learned_utility_rescue.md
│   └── calibration_tradeoff.md
├── 12_minilm_crossencoder/
│   └── minilm_vs_cosine_example.md
└── 13_final_comparisons/
    ├── hotpotqa_matched_comparison.md
    ├── qasper_matched_comparison.md
    └── scifact_matched_comparison.md
```

*Audit verified: All files created and verified in place.*

