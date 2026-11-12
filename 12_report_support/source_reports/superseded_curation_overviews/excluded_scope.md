# Excluded Scope Documentation: `FINAL_PROJECT_MAIN`

**Project Title:** Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation  
**Status:** Canonical scope boundary definition  
**Repository Source:** CS787 RAG Project  

---

## 1. Principles of Exclusion

The goal of `FINAL_PROJECT_MAIN/` is to serve as the **smallest scientifically complete and auditable directory** required to understand, reproduce, verify, defend, and report the final CS787 research findings.

In accordance with project guidelines, material that constitutes exploratory branches, intermediate parameter sweeps, superseded model iterations, redundant large caches, or non-essential historical clutter has been intentionally excluded from this clean distribution.

---

## 2. Major Excluded Phases

### Week 8 — Token-Budgeted Adaptive Extraction & Controller Studies
- **Scope excluded:** `results/week8/`, `configs/week8/`, `scripts/week8/`, `notebooks/week8/`, `tests/week8/`, `src/week8/`.
- **Reason for exclusion:** Week 8 explored sentence-level and token-budgeted controllers on preliminary data splits. The component-level evaluations suffered from incomplete integrated outcomes (as audited in `results/FINAL_PROJECT_REPORT.md` Section 17) and did not isolate full final-system performance. This phase was completely superseded by the rigorous multi-granularity study in Week 11 and controlled study in Week 12. No downstream code in W11, W12, or Post-W12 imports from Week 8.

### Week 9 — Large-Scale Sentence Retrieval Caches & Utilization Sweeps
- **Scope excluded:** `results/week9/` (876 MB of intermediate retrieval caches, embeddings, lock files, SQLite databases, and answer jsonls), `scripts/week9/`, `notebooks/week9/`, `configs/week9/`, and majority of `src/week9/`.
- **Reason for exclusion:** Week 9 investigated fine-grained sentence retrieval (SentTopK), grounded faithfulness, and extraction-utilization tradeoffs. It generated massive intermediate SQLite sentence databases (`sentences.sqlite3`), dense vector caches, and raw generation shards that are not required for final report claims. Furthermore, audit findings indicated QASPER test data consumption occurred in W9, which led to a strict protocol freeze forbidding fresh test claims on that cohort.
- **Minimal Retained Exception:** Exactly 6 small utility files (`sentences.py`, `retrieval.py`, `historical_backend.py`, `literal.py`, `backend.py`, `evaluation.py`) were retained in `src/week9/` because W11/W12 modules directly import their sentence splitting and BM25 functions. All experiment result directories of W9 were excluded.

### Week 10 — Root-Cause Diagnostic Sweeps & Training Pipelines
- **Scope excluded:** `results/week10/`, `configs/week10/`, `scripts/week10/`, `notebooks/week10/`, `tests/week10/`.
- **Reason for exclusion:** Week 10 conducted extensive diagnostic sweeps, training runs, and dataset audits to isolate root causes of earlier controller failures. These served as internal methodological checks rather than primary final deliverables.
- **Minimal Retained Exception:** The root-cause storage, encoding, and base reader primitives (`src/week10/root_cause/storage.py`, `encoding.py`, `data.py`, `runtime.py`, `protocol.py`, `analysis.py`, `runner.py`, `preflight.py`, `smoke.py`) were retained in `src/week10/` to support self-contained execution of W11 cache hashing and W12 embedding management.

---

## 3. Excluded Large Artifacts and Caches

To preserve disk space and maintain repository hygiene without sacrificing scientific auditability, the following non-canonical or machine-generated data stores were excluded:

| Excluded Category | Approximate Size | Repository Path | Rationale |
|---|---|---|---|
| **BEA-V1 Derived Answer Caches** | ~1.7 GB | `results/post_w12/bea_qbgf/v3/cache/` | Ephemeral LLM response caches and raw intermediate shards; all audited metrics, tables, and pilot reports are preserved in `results/POST_W12/BEA_V1/`. |
| **Week 7 Router Model Weights** | ~4.2 GB | `results/week7/w7d_cross_encoder_router/models/` | Binary PyTorch model checkpoints from exploratory cross-encoder experiments. Final analyses rely on saved CSV metrics. |
| **Week 5 Model Checkpoints & Surfaces** | ~3.9 GB | `results/week5/content_allocator/` | Intermediate checkpoint weights and large response-surface grids. Final summary tables and figures are preserved. |
| **Virtual Environments** | ~19 MB | `results/week12/tools/llmlingua_env/`, `.venv/`, `sara_env/` | Ephemeral Python virtual environments containing local system binaries and compiled wheels. Excluded per Rule 13. |
| **Large Compressed Split Audits** | ~90 MB | `results/week12/W12_SPLIT_FREEZE.json.gz`, `v2_audit_only.json.gz` | Oversized raw dump of split manifests. Canonical protocol summaries and split verification markdown files are retained. |
| **Hugging Face Model Caches** | >10 GB | `~/.cache/huggingface/` | Public pre-trained weights (`Qwen/Qwen2.5-7B-Instruct`, `Salesforce/SFR-Embedding-Mistral`, `ms-marco-MiniLM-L6-v2`) must be downloaded via standard scripts rather than checked into git. |
| **Pycache & Test Caches** | Multi-MB | `**/__pycache__/`, `**/.pytest_cache/`, `**/.ipynb_checkpoints/` | Temporary Python bytecode and test run state. |

---

## 4. Methodological Exclusions

1. **LoRA Fine-Tuning Execution:** Full final LoRA adapter training for the Qwen3-8B generator was skipped during W12 due to compute and stability considerations. The repository retains qualification scripts and protocols, but reports no speculative final quality gains from unexecuted LoRA arms.
2. **LLMLingua-2 Compression:** LLMLingua-2 was audited and tested via smoke checks, but full production runs were not part of the final frozen confirmation policy.
3. **Unrestricted Wikipedia Retrieval:** HotpotQA experiments were restricted to the 10-paragraph distractor context benchmark; open-web Wikipedia retrieval was intentionally outside the scope of this research.
