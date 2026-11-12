# Evidence Lab — copied final-project application

This is a **copy** of the current working demo, including its original 15-passage World Cup preset, current UI repairs, curated examples, research findings and live selectors. The original repository `demo/` was not moved or changed.

## Launch from a standalone copy

From the published repository root, first run `bash setup_demo.sh --saved`, then `bash demo/launch.sh`. Use `--live` for optional SFR/Qwen software and `--dev` for tests. [Installation details](../INSTALLATION.md). The root `.venv` now takes precedence over the original server environment.

## Existing server launch (original folder layout)

From the main repository:

```bash
bash FINAL_PROJECT_MAIN/demo/launch.sh
```

For a separate port:

```bash
bash FINAL_PROJECT_MAIN/demo/launch.sh --server.port 8502
```

Open the URL Streamlit prints; forward that port if connecting through SSH. The launcher starts only the UI. It does not start model inference, download anything, rebuild examples, or execute research notebooks.

The launcher uses an explicitly supplied `DEMO_PYTHON` first, a local `.venv` second, then the original demo's **existing Python environment** on this server. It shares installed software, not original application code or original result files. To use another compatible environment:

```bash
DEMO_PYTHON=/absolute/path/to/python bash FINAL_PROJECT_MAIN/demo/launch.sh
```

## Layout

| Item | Purpose |
|---|---|
| `app.py`, `launch.sh` | Small entry points for the copied app |
| `APPLICATION_GUIDE.md` | Full user/method guide |
| `application/demo/` | Exact copied application: UI, assets, live code, curated bundle and tests |
| `application/src/` | 77 exact transitive research-source dependencies; no rewritten algorithms |
| `application/results/` | Only demo-required research tables, freezes, configuration and saved BEA-V2 predictors |
| `application/configs/` | Small configuration snapshots |
| `COPY_MANIFEST.json`, `verify_copy.py` | Per-file SHA256 inventory and read-only verification |
| `verification/` | Browser checks and workspace screenshots |
| `COPY_TEST_RESULTS.log`, `COPY_REPORT.md` | Validation evidence and copy scope |

The internal `application/` directory preserves the original `demo/`, `src/`, `results/` relative paths. This keeps Python imports and root-relative data access consistent without overwriting the final project's existing reorganized source/results folders. Every payload file is a real local copy, not a link back to the original.

## Available functionality

- Start Here, Compare Methods, How the Algorithms Work, and Live Lab.
- All 30 saved curated questions / 1,620 saved conditions, exact saved evidence and answers, and published saved attribution within the bundle.
- Research findings and their registered source tables; publication/freeze checksum checks remain active.
- Original World Cup 15-passage preset; custom passages/query; run history and answer comparison.
- Current source segmentation, input budgets, four-method comparison and deletion analysis.
- BEA-V2 uses the same fifteen saved predictors and exploratory threshold as the working demo; no qualification claim was changed.
- Existing lazy CPU/CUDA model loading, generation caching, unavailable-reader handling and no-hidden-reasoning display.

Saved views use CPU and do not require model weights. **Live SFR retrieval/Qwen generation still needs the existing pinned checkpoints and a compatible software environment.** Weights remain in the current user's shared Hugging Face cache; no weights, tokens, credentials, environment directories or GPU memory were copied. Reader availability is checked at runtime. No new real-model inference was performed to qualify this copy; synthetic selector/reader regression tests and browser checks passed.

Raw benchmark corpora and historical processing caches are not included. The saved demo and custom-input pipeline do not require them. Rebuilding research/curated examples from raw datasets is outside this copied presentation bundle and should not be launched for a demonstration. Old copied build/audit documentation is historical; use this README for launching this bundle.

## Verify / test

With the same Python environment:

```bash
demo/.venv/bin/python FINAL_PROJECT_MAIN/demo/verify_copy.py
```

To rerun the copied test suite from the repository root:

```bash
cd FINAL_PROJECT_MAIN/demo/application
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  ../../../demo/.venv/bin/python -m pytest demo/tests -q -p no:cacheprovider
```

The final folder remains Git-ignored. Nothing was staged, committed or pushed as part of this copy.
