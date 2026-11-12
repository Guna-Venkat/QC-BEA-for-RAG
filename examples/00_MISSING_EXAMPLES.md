# Record of Missing Historical Artifacts and Zero-Fabrication Compliance

**Status:** Complete Forensic Audit  
**Strict Policy:** Zero Invention, Zero Synthetic Fill, Zero Post-Hoc Falsification  
**Authoritative Reference:** `results/post_w12/pilot_aspect_mechanism_audit/W12-POST/UNRESOLVED_PROVENANCE.md`

---

## 1. Overview of Artifact Integrity Protocol

In accordance with strict scientific integrity rules for CS787:
1. **No Data Fabrication:** Under no circumstances were missing historical inputs, model generations, prompt strings, or per-query metrics invented.
2. **Explicit Labeling of Historical Gaps:** Where historical files were purged or logged only at aggregate level, this artifact formally documents the gap rather than synthesizing plausible mock data.
3. **Traceability to Preserved Audit Records:** Every qualitative example presented in this collection originates from surviving frozen receipts, attribution CSVs, or the comprehensive forensic ledger in `FINAL_QUALITATIVE_CASE_STUDY_REPORT.md`.

---

## 2. Documented Historical Missing Rows

### A. Week 0–3 Raw Prompt Caches Purged During Disk Cleanup
- **Incident Description:** During the Week 12 disk space reclamation pass (recorded in `results/week12/W2_W9_DISK_CLEANUP_2026-11-01.json`), raw intermediate prompt text files and individual generation caches for Weeks 0–3 were compressed and partially purged to free workspace storage for the Week 12 reader execution.
- **Surviving Evidence:**
  - Benchmark JSONs: `results/week1/evaluation/sara_benchmark.json`
  - Cost-aware oracle files: `results/week3/evaluation/cost_aware_oracle_benchmark.json`
  - Weekly summary reports: `results/week1/reports/W1_SUMMARY.md`, `results/week3/reports/W3_SUMMARY.md`
- **Integrity Compliance:**
  - In `examples/02_sara_context/1001_context_sensitivity.md` and `1002_context_sensitivity.md`, example queries (Questions 1001 and 1002 from Paper 293) are presented with their exact surviving numerical scores ($k=0 \dots 10$) and paper metadata.
  - Missing raw intermediate Command-R-Plus logits and exact token prompt texts are explicitly labeled `HISTORICAL_VAL_BENCHMARK (RAW PROMPT LOG PURGED 2026-11-01)` rather than being re-generated or fabricated.

### B. Week 7 Pointwise Router Prediction Caches
- **Incident Description:** The pointwise learned utility router (W7-C2) evaluated in Week 7 recorded aggregate validation metrics (F1 = 0.3922 vs. 0.4010 for static $k=8$) in `results/week7/evaluation/pipeline_comparison.json`. Per-query raw ranking outputs for the full 1,000-query validation set were not archived in full.
- **Surviving Evidence:** The model weights, cross-validation split indices, and aggregate test comparison tables.
- **Integrity Compliance:** Documented in `examples/05_intermediate_routing/learned_utility_vs_semantic_k8.md` as an aggregate benchmark finding. No fictitious per-query router rankings were backfilled.

### C. SciFact Pre-W11 Baseline Reader Violations
- **Incident Description:** Before Week 11, Mistral-7B-Instruct and Llama-3-8B-Instruct were tested on SciFact, producing 1,849 and 1,826 format violations out of 1,850 queries respectively. The failed generation logs were recorded as aggregate failure counts in `results/week11/monitoring/memory_handoff_recovery.json`.
- **Surviving Evidence:** Monitoring error logs, format validation parser exceptions, and the aggregate recovery report.
- **Integrity Compliance:** Documented in `examples/06_reader_retriever_confounds/scifact_reader_format_confound.md` using the exact recorded error frequency. Individual failed generation text snippets are cited only where verbatim parser exceptions were preserved.

### D. Week 12 Formal Calibration Rejection Data
- **Incident Description:** As documented in `FINAL_PROJECT_MAIN/8_bea_v2/docs/2_failed_calibration_and_posthoc_reader.md`, the stopping threshold grid calibration failed preregistered constraints (`CALIBRATION_FAILED_TERMINATED`).
- **Integrity Compliance:** The negative calibration outcome was preserved exactly as `CALIBRATION_FAILED_TERMINATED`. Rather than inventing a "successful" calibration run or modifying acceptance criteria post-hoc, the project documented the failure in `examples/11_bea_v2/calibration_tradeoff.md` and separately evaluated the exploratory `BEA_V2_POSTHOC` branch.

---

## 3. Scope of Fully Recovered Surviving Datasets

All primary qualitative case studies in folders `08_qbgf`, `09_loo`, `10_bea_v1`, `11_bea_v2`, `12_minilm_crossencoder`, and `13_final_comparisons` are backed by **100% complete, uncompromised, verbatim experimental data**:

1. **Anchors A01 through A08:** Completely preserved in `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (32,034 lines), including exact evidence token IDs, verbatim prompt strings, input/evidence hashes, selected unit lists, and reader outputs.
2. **LOO Attribution Dataset:** 9,607 unit ablation rows preserved in `results/week12/attribution/v1/analysis/unit_importance.csv`.
3. **Five-Method Matched Cohort:** 1,200 evaluation rows preserved in `FINAL_PROJECT_MAIN/9_minilm_reranker/results/4_diagnostics/` and `FINAL_PROJECT_MAIN/8_bea_v2/results/3_posthoc_reader_run/`.

---

## 4. Summary Audit Table of Archival Completeness

| Phase / Artifact Area | Survival Status | Documentation Policy in `examples/` |
| :--- | :---: | :--- |
| **Week 1 SARA Sweep** | Aggregate JSON + Sample Cases | Reported from exact JSON; missing prompt tokens noted |
| **Week 3 Cost-Aware Oracle** | Full Benchmark JSON | Reported from exact benchmark matrices |
| **Week 6 Passage Selection** | Full Benchmark JSON + Key Query | Reported from exact candidate pool files |
| **Week 7 Router Regression** | Aggregate Pipeline JSON | Reported as aggregate finding |
| **Week 8 Draft Promotion** | Benchmark JSON + Trace Log | Reported from exact controller logs |
| **Week 9 Generative Compression** | Benchmark CSV + Logs | Reported from exact summary files |
| **Week 10 SFR Retriever Audit** | Full Benchmark JSON | Reported from exact recall tables |
| **Week 11 Reader Compliance** | Monitoring JSON + Audit Logs | Reported from exact recovery records |
| **Week 11 Granularity Pilot** | Full Metric CSV | Reported from exact pilot CSV |
| **Week 12 QBGF Solver & MCKP** | 100% Frozen Code + Ledgers | Complete verbatim reconstruction |
| **Week 12 LOO Attribution** | 100% Full Unit CSV (9,607 rows) | Exact delta calculations |
| **Week 12 BEA-V1 Starvation** | 100% Diagnostic Step Records | Verbatim step-by-step transition tables |
| **Week 12 BEA-V2 Post-Hoc** | 100% Diagnostic Rows & Hashes | Exact output strings and hashes |
| **Post-W12 MiniLM Reranker** | 100% Diagnostic Rows & Hashes | Exact output strings and hashes |

*Certified: No simulated, imagined, or backfilled data points exist within `FINAL_PROJECT_MAIN/examples/`.*

