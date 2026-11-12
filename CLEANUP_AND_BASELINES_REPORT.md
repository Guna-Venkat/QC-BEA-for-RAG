# Cleanup and baseline-library report

All changes are confined to **FINAL_PROJECT_MAIN/**. The original repository and its outer .gitignore are untouched. No model was loaded, no environment installed, and no experiment/statistical result was generated.

## Cleanup

- Removed 45superseded generated navigation/audit/interface files:2,781,283bytes (~2.65MiB). These were absent from the scientific provenance manifest; pre-deletion path/hash/reason receipts are retained.
- Removed temporary paper extraction/render/download intermediates after copying the final unchanged papers into the baseline library.
- Preserved scientific source, all 50original notebooks, query-level rows, source pools, fold models, figures, result/statistics tables, frozen splits and current provenance/action logs.
- Moved 59SARA parent configs from the generic configs list into baselines/1_sara/project_adaptation/configs, preserving contents and rewiring internal references. This cleans navigation without discarding reference configurations.
- Most of the archive’s remaining size is essential evidence, not a disposable cache. No large scientific data folder was deleted or hidden wholesale.

Exact removals: [cleanup_retirements.json](11_shared_infrastructure/audit/cleanup_retirements.json). Config moves: [baseline_config_moves.json](11_shared_infrastructure/audit/baseline_config_moves.json).

## Baseline organization

[Open the baseline library](1_problem_and_baselines/baselines/README.md).

| Baseline | Original source/reference | Project integration/results |
| --- | --- | --- |
| SARA | Official Ahren09/SARA pinned source, license, unchanged paper, literature-only Table1 excerpt | Preserved adaptation/loader, specialist runner, real 2,010 query-level BM25/SFR k5/n10 records; QASPER adapted-Mistral specialist, not matched Qwen256/1024 |
| RECOMP | Official carriex/recomp source, license, unchanged ICLR paper, literature-only Table2 excerpt | No matched project evaluation; no invented score |
| LLMLingua-2 | Official microsoft/LLMLingua v0.2.2 source, license, unchanged ACL paper | Actual project compressor wrapper and smaller-mBERT qualification receipt; no full W12 quality/confirmation result |
| BM25/SFR RAG controls | Actual project retrieval, RAW_SKIP/sentence/hierarchy code and frozen config | Recorded merged validation and paired-extension tables; explicitly budget-matched RAW_SKIP |
| MiniLM | Official checkpoint reference and one canonical project implementation | Links to matched exploratory quality/efficiency/statistics; no duplicate implementation |

Each external baseline has README, upstream_source, UPSTREAM_SOURCE_LOCK.json, original license and an isolated PAPER_RESULTS_REFERENCE.md. Published-paper values remain literature references, not project benchmark rows. See [baseline results index](1_problem_and_baselines/baselines/BASELINE_RESULTS_INDEX.md).

Pinned source commits:

- SARA: 639f5f48b86672c270046141f44a1b5eab6c8b96.
- RECOMP: 51d4432151efb3275257a9407dc71d1e5ec6634d.
- LLMLingua: v0.2.2 /a411a3fa61df74411157b2512b592d5357bd8f17.

All 203 selected upstream source/config/license files were checked against SHA256 and Git blob IDs. Saved tree-hash metadata was corrected from commit IDs to actual Git tree IDs, retaining the previous value for audit. The official SARA ancillary plotting-file syntax issue is recorded, not fixed or hidden. Current source snapshots are not asserted to be historical execution revisions.

## Local .gitignore

[FINAL_PROJECT_MAIN/.gitignore](.gitignore) excludes regenerable Python/test/notebook caches, local environments, large external checkpoint/embedding-database files and temporary review output. It deliberately keeps scientific CSV/JSON/query results, frozen identities, notebooks, figures, provenance and *.joblib predictors visible.

The parent repository currently ignores the entire final folder. A nested .gitignore cannot override that outer exclusion. This task leaves the outer file unchanged; lifting that exclusion later is a separate action.

## Verification and remaining limits

The current metadata verifier checks source preservation, moved links, notebooks, frozen identities, matched rows, model hashes, official source blob identities and active navigation. Details are in [defense_verification_summary.json](11_shared_infrastructure/audit/defense_verification_summary.json). No claim of full execution/testing of imported models is made.

Missing historical W12 validation/confirmation raw outputs and attribution perturbation receipts remain unresolved. External model weights/data/environment remain external. Cleanup does not manufacture missing historical evidence or make the archive a complete independent reproduction bundle.
