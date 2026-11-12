# Reproducibility and entry-point map

For each central method CODE_MAP.md identifies main code, runner, config, notebook, primary and statistical results. NOTEBOOK_MAP.md adds inputs, outputs and unchanged switch values. Local README files explain the inspected algorithm and actual historical entry interface.

This archive has exact recorded result bytes and method code, not a fully installed portable research environment. External datasets and pinned weights/SARA checkpoints, original package/code identities and missing historical raw W12 output shards are still needed for independent reproduction. Current source snapshots are not assumed identical to historical freeze commits.

No benchmark, training, retrieval, predictor fitting, calibration or generation was rerun. Original V2 calibration remains terminated. The separate post-hoc notebook does not repair that status. Archived model/install/full-run switches may already be True; opening code and tables is the intended viva workflow.

Metadata-only verification (from the repository root) is available after this pass:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 FINAL_PROJECT_MAIN/11_shared_infrastructure/audit/verify_defense_archive.py
```

This verifies copies, source hashes, navigation and notebook preservation; it does not reproduce experimental science.
