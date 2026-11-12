# Budget-Aware Evidence Allocation for RAG

**CS787 · Generative AI · IIT Kanpur**

This project asks a practical question: **when a language model can read only a limited amount of retrieved text, which parts should it receive?** We study retrieval, whole passages, query-relevant sentences, mixed-granularity allocation and context-specific evidence utility on **QASPER, HotpotQA and SciFact**.

The evidence budget (256 or 1024 tokens in the primary comparisons) limits **input evidence**, not generated answer length. QA uses answer F1; SciFact uses three-class macro-F1. Scores across tasks are not pooled.

## Main findings

- Evidence granularity depends on the task and budget; sentences are a strong simple constrained-budget policy, while whole passages can recover or lead at larger budgets.
- Query conditioning helps QBGF allocation on validation, but validation did not establish a universal mixed-granularity QBGF advantage.
- High retrieval/semantic relevance does not guarantee that a particular unit improves a reader's answer.
- The frozen final policy is **SFR top-10 → FIXED_SENTENCE → Qwen3-8B BASE_FP16**, at 256/1024 evidence tokens, without LoRA.
- BEA-V1, BEA-V2 and the MiniLM reranker are separate exploratory work. BEA-V2's official calibration failed; the threshold-8e-5 reader branch and current custom-input ensemble are exploratory, not a new confirmed final system.

See [claim-to-evidence map](CLAIM_TO_EVIDENCE_MAP.md), [important numbers](IMPORTANT_NUMBERS.md), [scientific status](SCIENTIFIC_STATUS.md) and the [final report](report/CS787_Final_Project_Report.pdf). Dataset-specific tables and uncertainty take priority over simplified presentation examples.

## Quick start: saved demo

Use **Python 3.11** on Linux for the tested environment. Git LFS must fetch the registered large artifacts after cloning:

```bash
git lfs install --local
git lfs pull
bash setup_demo.sh --saved
bash demo/launch.sh
```

Run these commands from this repository's root after cloning it as its **own repository**, not inside the original ignored working folder. Open the Streamlit URL; forward the port if using SSH. Saved views need no GPU, credentials or model weights. They do not rerun experiments.

The demo includes Start Here, Compare Methods, How the Algorithms Work and Live Lab. Saved curated examples retain their exact questions, evidence, answers and deletion results. The original 15-passage World Cup preset remains the default. [Application guide](demo/APPLICATION_GUIDE.md).

## Optional live models

```bash
bash setup_demo.sh --live
bash demo/launch.sh
```

This installs the live software stack, not model weights. Live SFR/Qwen execution requires the exact pinned checkpoints already present in the current user's Hugging Face cache and enough CPU RAM or GPU memory. No silent checkpoint substitution or automatic download occurs. Use `demo/application/results/week12/qbgf/v3/protocol/protocol_config.json` for exact model IDs/revisions. A missing reader remains unavailable rather than yielding an invented answer. See [installation details](INSTALLATION.md).

For another installed environment: `DEMO_PYTHON=/absolute/path/to/python bash demo/launch.sh`.

## Repository map

| Folder | Purpose |
|---|---|
| `1_problem_and_baselines` | Initial problem, official baseline snapshots, project adaptations and references |
| `2_adaptive_evidence_quantity` | Evidence-count experiments and oracle headroom |
| `3_evidence_identity_and_routing` | Which source to expose and routing diagnostics |
| `4_multigranular_evidence_study` | Retriever, reader, granularity and budget study |
| `5_qbgf` | Query-conditioned fusion, ablations and frozen decision |
| `6_downstream_utility_attribution` | Post-freeze evidence deletion diagnostics |
| `7_bea_v1`, `8_bea_v2`, `9_minilm_reranker` | Separate post-W12 exploratory methods |
| `10_final_method_comparison` | Matched exploratory method comparisons |
| `11_shared_infrastructure`, `12_report_support` | Canonical runtime, provenance and report support |
| `demo` | Independently copied app, data and selector dependencies |
| `report` | Final report and supporting figures |
| `publication` | Publication checks and packaging documentation |

Numbered code views and top-level compatibility names are **relative symlinks within this folder**. Preserve them when copying. The copied demo has its own exact runtime snapshot so it does not depend on the original working repository's code/results.

## Verification

```bash
.venv/bin/python publication/check_readiness.py
.venv/bin/python demo/verify_copy.py
```

To run the full demo regression suite without actual model generation:

```bash
bash setup_demo.sh --dev
cd demo/application
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ../../.venv/bin/python -m pytest demo/tests -q -p no:cacheprovider
```

Browser testing additionally needs `python -m playwright install chromium`. The checked snapshot has **193 passing demo regressions in each demo copy**, plus navigation and theme checks; see [publication report](publication/PUBLICATION_READINESS_REPORT.md) for the exact scope and installation-test limitations.

## Research reproduction limits

This is a curated research archive, not an automatic full-experiment runner. Missing historical raw shards and external datasets/checkpoints prevent universal end-to-end reproduction; consult [unresolved provenance](UNRESOLVED_PROVENANCE.md), [reproducibility map](REPRODUCIBILITY_MAP.md), [dataset setup](DATASET_AND_EXPERIMENT_SETUP.md) and [code map](CODE_MAP.md). Historical notebooks may retain enabled full-run flags: inspect them before execution; **do not Run All for a demo**. No new experiments are required to browse saved results.

Reserved confirmation and development/exploratory cohorts remain distinct. No fresh QASPER confirmation is claimed. No scientific artifact was altered for publication packaging.

## License and citation

Project-authored code/documentation: [MIT](LICENSE). Upstream source, dataset excerpts, model references and papers retain their own terms: [third-party notices](THIRD_PARTY_NOTICES.md). Use [CITATION.cff](CITATION.cff) and cite the relevant original work.

## Publishing this snapshot

Follow [PUBLICATION.md](PUBLICATION.md) to create a **new repository from a separate copy**, preserve symlinks, configure LFS before the first commit and check the staged files. No commit, remote or push is performed by the setup/check scripts.
