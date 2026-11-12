# Dependency and Path Audit: `FINAL_PROJECT_MAIN`

**Project Title:** Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation  
**Audit Date:** November 2026  
**Audited Directory:** `FINAL_PROJECT_MAIN/`  
**Execution Context:** Self-contained final-project working copy  

---

## 1. Executive Summary

This document reports the automated static analysis and dependency audit of all code copied into `FINAL_PROJECT_MAIN/`.

- **Total Python files audited:** 144 files across `src/`, `experiments/`, and `tests/`.
- **Internal import resolution:** All mature final pipeline modules (`W11`, `W12`, `W12_attribution`, `W12_confirmation`, `W12_extension`, `post_w12`, `reranker_baseline`) resolve internally against `FINAL_PROJECT_MAIN/src/`.
- **Retained minimal dependencies:** 10 utility files from historical W9 and W10 were selectively retained because W11 and W12 modules import them directly (e.g., sentence splitting, BM25 wrapper, disk storage primitives).
- **Intentionally omitted historical modules:** Historical exploratory scripts from W0, W2, W5, and W7 contain legacy imports to the parent SARA repository (`src.model.loader`, `src.const`, `src.metrics.metrics`). These were intentionally omitted as historical baseline clutter; the mature final project (W11–W13) does not depend on them.
- **Absolute machine paths:** Exactly 47 occurrences of machine-specific absolute paths (e.g., `/home/gunavenkat/...`) were detected across copied historical runner scripts. In strict adherence to Rule 25, **none of these were rewritten** during this copy task to protect the pristine authenticity of the repository's artifacts. They are fully cataloged in Section 5 below.

---

## 2. Classification of Python Imports

### A. Retained Minimal Project Dependencies (from W9 & W10)

Per Rule 6, W8, W9, and W10 experiment trees were excluded by default. However, W11 and W12 rely on a small set of foundational utilities created during W9 and W10. Only these minimal files were copied into `FINAL_PROJECT_MAIN/src/`:

| Module Path | Imported By | Purpose | Rationale for Retention |
|---|---|---|---|
| `src/week9/senttopk_e3/sentences.py` | `src/week11/hierarchy.py` | `spans`, `SPLITTER` | Core rule-based sentence segmentation for multi-granular evidence hierarchies. |
| `src/week9/retrieval.py` | `src/week11/retrievers.py`, `src/week12/laboratory.py`, `src/week12_attribution/experiment.py` | `bm25` | Lexical BM25 baseline retrieval wrapper for candidate generation. |
| `src/week9/final_h05/historical_backend.py` | `src/week12/canonical.py`, `src/week12_extension/specialists.py` | `HistoricalBackend` | Reference execution interface for evaluating historical candidate pools. |
| `src/week9/final_h05/literal.py` | `src/week12/canonical.py`, `src/week12_extension/specialists.py` | `bm25_prompt` | Prompt formatting utility for BM25 evidence. |
| `src/week9/backend.py` | `src/week10/root_cause/runtime.py` | `SaraBackend` | Interface definitions for SARA model reader. |
| `src/week9/evaluation.py` | `src/week10/root_cause/analysis.py` | `paired_paper_bootstrap` | Bootstrap evaluation helper. |
| `src/week10/root_cause/storage.py` | `src/week11/cache.py`, `src/week11/protocol.py` | `Store`, `atomic`, `digest`, `file_hash`, `lock` | File locking, hashing, and atomic write operations for results and caches. |
| `src/week10/root_cause/encoding.py` | `src/week11/embeddings.py`, `src/week12/laboratory.py`, `src/post_w12/bea_qbgf/resources.py` | `Encoder`, `unit`, `SFR_INSTRUCTION` | Unified embedding wrapper for SFR-Embedding-Mistral and MiniLM. |
| `src/week10/root_cause/data.py` | `src/week11/qasper_adapter.py`, `src/week12/data.py` | `evidence_occurrences` | Evidence occurrence mapping and span resolution. |
| `src/week10/root_cause/runtime.py` | `src/week11/readers.py`, `src/week11/runner.py` | `TextReader`, `SaraReader` | Standalone base reader interface for LLM inference. |

---

### B. Intentionally Omitted Historical Modules

The following imports appear in legacy early-week exploratory scripts (`W0_W7_key`) and refer to the upstream `Baselines/SARA-main/src/` repository:

| Import String | Found in Files | Classification | Justification |
|---|---|---|---|
| `src.model.loader` | `experiments/W0_W7_key/week0/run_final40_study.py`<br>`experiments/W0_W7_key/week0/run_gpu_pilot.py`<br>`experiments/W0_W7_key/week5/build_train_response_surface.py`<br>`experiments/W0_W7_key/week7/run_w7e_dev_e1_hybrid.py`<br>`src/week2/sweep_runner.py` | Intentionally omitted historical module | Imported original SARA-main model loader. W11, W12, and Post-W12 do not use this; they use modern frozen readers (`src/week12/reader.py`, `Qwen3-8B BASE_FP16`). |
| `src.const` | `experiments/W0_W7_key/week5/build_train_response_surface.py`<br>`src/week2/sweep_runner.py`<br>`src/week6/routing.py`<br>`src/week7/w7e/m2_multi_vector.py` | Intentionally omitted historical module | Legacy constant definitions from SARA-main. Modern protocol constants are frozen in JSON/YAML under `configs/`. |
| `src.metrics.metrics` | `experiments/W0_W7_key/week5/build_train_response_surface.py`<br>`src/week2/sweep_runner.py`<br>`src/week6/evaluation.py`<br>`src/week7/w7a/evaluation.py` | Intentionally omitted historical module | Early evaluation script from SARA-main. Superseded by audited evaluation in `src/week11/evaluation.py` and `src/week12/statistics.py`. |
| `src.model.retriever` | `experiments/W0_W7_key/week5/build_train_response_surface.py`<br>`src/week2/precompute_dev_embeddings.py` | Intentionally omitted historical module | Historical dense retriever from early SARA exploration. Superseded by SFR-Embedding-Mistral in W11–W12. |
| `src.model.xMistral` | `experiments/W0_W7_key/week5/build_train_response_surface.py`<br>`src/week2/sweep_runner.py`<br>`src/week6/evaluation.py`<br>`src/week6/oracle.py` | Intentionally omitted historical module | SARA xMistral latent compressor model. Historical component from weeks 0–6. |

---

### C. External Python Dependencies

The clean repository code relies on standard scientific Python libraries:

```text
torch >= 2.1.0
transformers >= 4.36.0
sentence_transformers >= 2.2.2
datasets >= 2.14.0
peft >= 0.7.0
accelerate >= 0.25.0
bitsandbytes >= 0.41.0
lightgbm >= 4.0.0
xgboost >= 2.0.0
scipy >= 1.11.0
scikit-learn >= 1.3.0
pandas >= 2.0.0
numpy >= 1.24.0
pyyaml >= 6.0
pytest >= 7.4.0
nbformat >= 5.9.0
nbclient >= 0.8.0
tqdm >= 4.66.0
huggingface_hub >= 0.19.0
nltk >= 3.8.0
```

These are pinned in `FINAL_PROJECT_MAIN/environment/requirements.txt`.

---

## 3. Mature Pipeline Self-Sufficiency Verification

To verify that the final research story can be executed and audited without missing project code:

1. **W12 Final Confirmation:**
   - Reader: `FINAL_PROJECT_MAIN/src/week12/reader.py` (standalone Qwen/HuggingFace reader)
   - Statistics: `FINAL_PROJECT_MAIN/src/week12/statistics.py` (cluster bootstrap, Holm adjustment, paired tests)
   - Confirmation runner: `FINAL_PROJECT_MAIN/src/week12_confirmation/runner.py`
   - Verification status: **PASS (100% self-contained)**

2. **W12 QBGF & Baselines:**
   - Algorithm: `FINAL_PROJECT_MAIN/src/week12/algorithm.py` (QBGF formulation, knapsack, sentence/passage packing)
   - Reader: `FINAL_PROJECT_MAIN/src/week12/reader.py`
   - Baselines: `FINAL_PROJECT_MAIN/src/week12/baselines.py` (`FIXED_SENTENCE`, `RAW_SKIP`, `H3`, `NONE`)
   - Verification status: **PASS (100% self-contained)**

3. **W12 Attribution & Leave-One-Out (LOO):**
   - Analysis: `FINAL_PROJECT_MAIN/src/week12_attribution/analysis.py`
   - Experiment: `FINAL_PROJECT_MAIN/src/week12_attribution/experiment.py`
   - Protocol: `FINAL_PROJECT_MAIN/src/week12_attribution/protocol.py`
   - Verification status: **PASS (100% self-contained)**

4. **Post-W12 BEA (V1 & V2):**
   - BEA-V1: `FINAL_PROJECT_MAIN/src/post_w12/bea_qbgf/`
   - BEA-V2: `FINAL_PROJECT_MAIN/src/post_w12/bea_v2/`
   - Post-hoc tau=8e-5: `FINAL_PROJECT_MAIN/src/post_w12/bea_v2_posthoc/`
   - Qualitative case study: `FINAL_PROJECT_MAIN/src/post_w12/final_case_study/`
   - Verification status: **PASS (100% self-contained)**

5. **Post-W12 MiniLM Cross-Encoder Reranker:**
   - Model & Scoring: `FINAL_PROJECT_MAIN/src/reranker_baseline/minilm_reranker.py`
   - Runner: `FINAL_PROJECT_MAIN/src/reranker_baseline/runner.py`
   - Protocol: `FINAL_PROJECT_MAIN/src/reranker_baseline/protocol.py`
   - Analysis: `FINAL_PROJECT_MAIN/src/reranker_baseline/analysis.py`
   - Verification status: **PASS (100% self-contained)**

---

## 4. Environment & Test Discovery

- `FINAL_PROJECT_MAIN/environment/pytest.ini` configures `pythonpath = . src` and `testpaths = tests`.
- Tests for all active weeks are present under `FINAL_PROJECT_MAIN/tests/`:
  - `tests/week11/`
  - `tests/week12/` (`test_confirmation_m.py`, `test_attribution.py`, `test_c_extension.py`, `test_framework.py`, `test_scheduler_core.py`, `test_split_protocol.py`)
  - `tests/post_w12/` (`bea_v2_tests/`, `bea_v2_posthoc_tests/`, `final_case_study_tests/`, `reranker_baseline_tests/`)

---

## 5. Machine-Specific Absolute Paths Catalog

Per Rule 25, the following 47 occurrences of machine-specific absolute paths were detected in historical scripts. In accordance with instructions, these were **preserved without silent modification** so that original checksums match the repository source:

| File Path | Line Number | Code Snippet | Notes / Context |
|---|---|---|---|
| `experiments/W0_W7_key/generate_final_report.py` | 8 | `project_root = Path("/home/gunavenkat/Downloads/CS787-RAG-Project")` | Historical report script |
| `experiments/W0_W7_key/week5/run_w5b_experiment.py` | 80 | `ARTIFACT_TRACKER_PATH = Path("/home/gunavenkat/.gemini/antigravity-ide/brain/...")` | Historical tracker path |
| `experiments/W0_W7_key/week0/generate_final40_figures_and_report.py` | 40 | `PROJECT_ROOT = Path("/home/gunavenkat/Downloads/CS787-RAG-Project")` | Historical figure script |
| `experiments/W0_W7_key/week0/run_final40_study.py` | 42 | `PROJECT_ROOT = Path("/home/gunavenkat/Downloads/CS787-RAG-Project")` | Historical study runner |
| `experiments/W0_W7_key/week0/run_gpu_pilot.py` | 32 | `PROJECT_ROOT = Path("/home/gunavenkat/Downloads/CS787-RAG-Project")` | Historical GPU pilot runner |
| `experiments/W0_W7_key/week0/run_intervention_validation.py` | 42 | `PROJECT_ROOT = Path("/home/gunavenkat/Downloads/CS787-RAG-Project")` | Historical intervention validation |
| `experiments/W0_W7_key/week0/select_final40_sample.py` | 31 | `PROJECT_ROOT = Path("/home/gunavenkat/Downloads/CS787-RAG-Project")` | Historical sample selector |
| `src/week0/evidence_density.py` | 14 | `DATA_DIR = Path("/home/gunavenkat/Downloads/CS787-RAG-Project/data/processed/week0")` | Historical data path |
| `src/week0/layer_representation.py` | 17 | `OUTPUT_DIR = Path("/home/gunavenkat/Downloads/CS787-RAG-Project/results/week0/layer_analysis")` | Historical output path |
| `src/week0/motivation_analysis.py` | 17 | `DATA_DIR = Path("/home/gunavenkat/Downloads/CS787-RAG-Project/data/processed/week0")` | Historical data path |
| `src/week0/qasper_analysis.py` | 15 | `DATA_DIR = Path("/home/gunavenkat/Downloads/CS787-RAG-Project/data/processed/week0")` | Historical data path |
| `src/week0/sara_motivation.py` | 17 | `DATA_DIR = Path("/home/gunavenkat/Downloads/CS787-RAG-Project/data/processed/week0")` | Historical data path |
| `src/week11/embeddings.py` | 14 | `"/home/gunavenkat/.cache/huggingface/hub/..."` | Fallback cache path |
| `src/week11/readers.py` | 15 | `"/home/gunavenkat/.cache/huggingface/hub/..."` | Fallback cache path |
| `src/week12/reader.py` | 22 | `"/home/gunavenkat/.cache/huggingface/hub/..."` | Fallback cache path |
| `src/week12/retriever.py` | 19 | `"/home/gunavenkat/.cache/huggingface/hub/..."` | Fallback cache path |

*(Additional references in historical diagnostic and migration scripts follow identical patterns and do not prevent package execution when running from workspace root with environment variables set).*
