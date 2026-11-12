# Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation

**CS787 Final Project Working Repository**  
**Repository Working Copy:** `FINAL_PROJECT_MAIN/`  
**Base Source of Truth:** `CS787-RAG-Project`  
**Curation Policy:** Strict COPY-ONLY; all original repository files outside this folder remain pristine and unaltered.

---

## 1. Research Question

> When an autoregressive language model operates under a fixed evidence-token budget (e.g., 256 or 1024 tokens), which parts of retrieved documents should it see, in what granularity (passages vs. sentences), and how should evidence space be allocated across candidates?

---

## 2. Purpose of this Directory

`FINAL_PROJECT_MAIN/` is the curated, self-contained final-project working copy. It filters out historical parameter sweeps, abandoned prototypes, intermediate generation shards, and multi-gigabyte binary caches to leave only the code, configurations, results, notebooks, and documentation necessary to:

- Explain the chronological scientific evolution of the project.
- Reproduce and inspect core methods and baselines.
- Trace every reported numerical claim back to a machine-readable artifact.
- Support the final project report, presentation, and technical defense.

---

## 3. Core Scientific Distinction

### A. The Official W12 Frozen Pipeline (Confirmatory)
- **Retriever:** Salesforce `SFR-Embedding-Mistral` top-10 retrieval.
- **Reader:** `Qwen/Qwen2.5-7B-Instruct` in **BASE_FP16** precision (no LoRA).
- **Budgets:** Exact token constraints of **256** and **1024** tokens.
- **Official Policy:** **`FIXED_SENTENCE`** (preregistered fallback frozen after validation gate).
- **Status:** Evaluated on reserved, untouched confirmation cohorts (200 HotpotQA queries, 50 SciFact claims) with 10,000 cluster bootstrap resamples and Holm family adjustment.

### B. Post-W12 Exploratory Investigations
- **Scope:** Budgeted Evidence Allocation (BEA-V1, BEA-V2), utility calibration analysis (`CALIBRATION_FAILED_TERMINATED`), post-hoc reader runs ($\tau = 8 \times 10^{-5}$), qualitative case study, and MiniLM cross-encoder reranker baseline (`MINILM_CE_SENTENCE`).
- **Status:** Strictly **exploratory / diagnostic**. These investigations provide mechanistic understanding of relevance-versus-utility tradeoffs on development data; they do not overwrite the official W12 confirmation results or change the frozen policy.

---

## 4. Directory Map

```text
FINAL_PROJECT_MAIN/
│
├── README.md                      # Project overview and guide (this document)
├── PROJECT_SCOPE.md               # Research evolution and scope definitions
├── RESULTS_INDEX.md               # Map from research claims to exact result artifacts
├── PROVENANCE_MANIFEST.csv        # Comprehensive manifest of all copied files with SHA256 hashes
├── EXCLUDED_SCOPE.md              # Documentation of excluded phases (W8-W10, large caches)
├── DEPENDENCY_AUDIT.md            # Audit of code imports and machine-specific absolute paths
│
├── docs/
│   ├── research_story/            # Overarching audited cross-week report and metrics glossary
│   ├── protocol/                  # Frozen protocols, data split audits, and freeze specifications
│   ├── weekly_key_summaries/      # Curated weekly reports (W0-W7, W11-W13) and audit logs
│   └── final_notes/               # Review notes, attribution reports, and post-W12 summaries
│
├── src/
│   ├── common/ & utils/           # Shared utility functions
│   ├── week0/ to week7/           # Early baseline and controller implementations
│   ├── week9/ & week10/           # Minimal retained dependencies (sentence splitting, storage, BM25)
│   ├── week11/                    # Multi-granularity study implementation
│   ├── week12/                    # QBGF, baselines, and core W12 reader
│   ├── week12_attribution/        # Causal attribution and leave-one-out (LOO) analysis
│   ├── week12_confirmation/       # Reserved confirmation evaluation engine
│   ├── post_w12/                  # BEA-V1, BEA-V2, and qualitative case study modules
│   └── reranker_baseline/         # MiniLM cross-encoder reranker implementation
│
├── configs/
│   ├── week0/ to week7/           # Historical configurations
│   ├── week11/                    # Multi-granularity study configs
│   ├── week12/                    # W12 protocol and split configurations
│   └── post_w12/                  # BEA-V2 and reranker configurations
│
├── experiments/                   # Experiment runner scripts organized by phase (W0_W7, W11, W12, POST_W12)
│
├── results/
│   ├── early_key_results/         # Key metrics and plots for W0 through W7
│   ├── W11/                       # Multi-granularity master summaries, pareto fronts, and reports
│   ├── W12/                       # Controlled final study results
│   │   ├── validation_and_ablations/  # Validation summaries, QBGF ablations, and primary contrasts
│   │   ├── c_extension/               # Baseline extensions and specialist comparisons
│   │   ├── freeze/                    # Frozen method specification (W13_FINAL_METHOD_FREEZE.json)
│   │   ├── attribution/               # Relevance vs utility correlations and unit importance
│   │   └── confirmation/              # Official confirmation results, contrasts, and reports
│   └── POST_W12/                  # Post-W12 exploratory results
│       ├── BEA_V1/                    # BEA-V1 pilot summaries and calibration reports
│       ├── BEA_V2/                    # Calibration termination records and post-hoc tau=8e-5 results
│       ├── qualitative_case_study/    # Query-level case studies, failure modes, and gold retention
│       └── minilm_reranker/           # Matched-cohort 5-method comparison, paired tests, and efficiency
│
├── notebooks/                     # Clean Jupyter notebooks organized by phase (W0-W7, W11, W12, POST_W12)
│
├── tests/                         # Pytest suites for all active phases
│
└── environment/                   # Pinned requirements.txt and pytest configuration
```

---

## 5. Locating Key Results

| Milestone / Claim | Primary Result Artifact | Summary Report / Documentation |
|---|---|---|
| **Early Oracle Ceiling** | `results/early_key_results/week2/processed/oracle_vs_static_summary.json` | `results/early_key_results/week2/week2_scientific_validation_report.md` |
| **QCCA Controller** | `results/early_key_results/week4/processed/model_comparison.csv` | `docs/weekly_key_summaries/week_04/WeeklySummaryAnalysis.md` |
| **Passage Routing** | `results/early_key_results/week6/passage_routing/tables/w6_main_results.csv` | `results/early_key_results/week6/README.md` |
| **Multi-Granularity (W11)** | `results/W11/final_report/main_granularity_summary_df.csv` | `results/W11/final_report/REPORT.md` |
| **W12 Validation** | `results/W12/validation_and_ablations/summary.csv` | `docs/final_notes/W12_H_FINAL_REVIEW.md` |
| **W12 QBGF Ablations** | `results/W12/validation_and_ablations/summary.csv` | `docs/final_notes/W12_D_ABLATION_RESULTS.md` |
| **W12 Frozen Decision** | `results/W12/freeze/W13_FINAL_METHOD_FREEZE.json` | `docs/protocol/W12_I_FINAL_FREEZE_REPORT.md` |
| **W12 Attribution (LOO)** | `results/W12/attribution/relevance_utility.csv` | `docs/final_notes/W12_K_L_ATTRIBUTION_REPORT.md` |
| **W12 Final Confirmation** | `results/W12/confirmation/summary.csv`, `contrasts.csv` | `results/W12/confirmation/week12_M_final_confirmation_report.md` |
| **POST-W12 BEA-V1** | `results/POST_W12/BEA_V1/summary.csv` | `docs/final_notes/POST_W12_BEA_V1_FINAL_REPORT.md` |
| **POST-W12 BEA-V2 Failure** | `results/POST_W12/BEA_V2/CALIBRATION_TERMINATED.json` | `results/POST_W12/BEA_V2/HELP_ONLY_PATCH_REPORT.md` |
| **POST-W12 BEA-V2 Post-hoc** | `results/POST_W12/BEA_V2/posthoc_tau8e5/POSTHOC_SUMMARY.csv` | `results/POST_W12/BEA_V2/posthoc_tau8e5/POSTHOC_PILOT_RESULTS.md` |
| **POST-W12 Qualitative Study**| `results/POST_W12/qualitative_case_study/ALIGNED_PER_QUERY.csv` | `results/POST_W12/qualitative_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` |
| **POST-W12 MiniLM Control** | `results/POST_W12/minilm_reranker/FINAL_COMPARISON.csv`, `PAIRED_COMPARISONS.csv` | `docs/final_notes/POST_W12_MINILM_RERANKER_FINAL_COMPARISON.md` |

---

## 6. Provenance & Scientific Integrity

- Every copied file has its origin tracked in [`PROVENANCE_MANIFEST.csv`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/PROVENANCE_MANIFEST.csv).
- The manifest records: `final_path`, `original_repo_path`, `category`, `week_or_phase`, `method`, `reason_included`, `file_size`, `sha256`, and `copied_exactly`.
- In strict adherence to Rule 25, no historical file was rewritten. Any absolute path that was present in the source repository remains intact and is cataloged in [`DEPENDENCY_AUDIT.md`](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/DEPENDENCY_AUDIT.md).
