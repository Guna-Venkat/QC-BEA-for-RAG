# Installation and runtime scope

## Software profiles

All profiles target Python 3.11. Direct dependencies are pinned to the environment used for the demo UI tests, tokenizer checks, saved sklearn predictors and synthetic pipeline tests. These are direct pins, **not a full platform-independent transitive lockfile**.

| File | Installs | Does not do |
|---|---|---|
| `requirements.txt` | Saved Streamlit UI, plots, tables and numerical/selector support | No Torch/checkpoint install, downloads or inference |
| `requirements-live.txt` | Base plus Torch, Transformers, SFR embedding software and real tokenizer support | No checkpoint downloads or benchmark runs |
| `requirements-dev.txt` | Live stack plus pytest and Playwright Python package | No browser binary download or real model generation |

`bash setup_demo.sh` installs the saved profile into the repository's `.venv`. Use `--live` or `--dev` explicitly. To select a Python executable: `PYTHON=/path/to/python3.11 bash setup_demo.sh --saved`. No administrative privileges or global package installation is required. The script runs `pip check` in that local environment. Network access/package availability is required for a new installation.

## Launch and environment selection

`bash demo/launch.sh` prefers `DEMO_PYTHON`, then the repository `.venv`, then a demo-local `.venv`. The last fallback to the old neighboring working demo exists only for convenience on the original server; a standalone checkout with its own `.venv` has no such dependency. Launch from any directory by passing the absolute launcher path.

Custom port: `bash demo/launch.sh --server.port 8502`. No public-network exposure is required; forward the port over SSH if needed. Do not use root privileges.

## CPU versus CUDA

Saved views need no GPU. Live SFR and Qwen are large models. CPU FP16 loading checks for at least 24,000 MiB available RAM and runs encoder/reader sequentially; latency may be high. CUDA execution checks available memory before loading. Checkpoint storage and software installation can consume substantial additional disk space.

Choose a PyTorch build compatible with your CPU/CUDA platform using PyTorch's official installation guidance. `requirements-live.txt` pins the tested Torch public version; it does not choose your CUDA driver or vendor-specific wheel index. If installing a CPU-specific build first, it must satisfy that pin. No FlashAttention or bitsandbytes requirement is imposed by the BASE_FP16 live demo.

## Model pins and access

The exact SFR/Qwen model IDs and revisions are in `demo/application/results/week12/qbgf/v3/protocol/protocol_config.json`. The app's local-only check expects the matching revision under the current user's Hugging Face cache. Model weights, tokens and credentials are intentionally excluded. Authenticate/download using your own account only when separately needed; setup does not do it for you. The bundled Qwen tokenizer can show counts without reader weights in the live profile.

The 15 saved BEA-V2 sklearn predictors are included with checksums. Keep the pinned scikit-learn/joblib/numpy stack when loading them. Their exploratory status and threshold are unchanged.

## Large files

Install Git LFS before cloning/fetching. After cloning, run `git lfs install --local` and `git lfs pull`. Two identical frozen split JSON copies and the saved demo bundle are tracked by exact-path LFS rules. Content SHA256s remain unchanged. If a file still contains an LFS pointer, the readiness checker explains that it must be fetched; a pointer is not an evaluation result.

A compressed curated archive and verified restore utility are also included. Prefer fetching LFS normally. Offline restore is described in `demo/application/demo/releases/README.md`; do not regenerate reader answers to repair a missing bundle.

## Tests and limitations

The demo suite exercises source segmentation, budget packing, cache/inference identity, simulated reader failures, model-predictor loading, navigation and output rendering. These tests do not qualify hardware performance or establish new answer-quality results. Browser binaries are installed separately with `python -m playwright install chromium` in the chosen environment.

Fresh network installation on a completely clean machine has not been executed during publication packaging. The local pinned environment, dependency metadata and copied-folder execution are verified; the publication report distinguishes these checks from a fresh install. Historical research/baseline notebooks have additional phase-specific dependencies/data/checkpoints and are not guaranteed runnable merely by installing these demo profiles.
