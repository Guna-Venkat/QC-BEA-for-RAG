# Defense reorganization log

Only FINAL_PROJECT_MAIN was changed. The previous inventory, manifest and symlink targets were captured before the defense pass under11_shared_infrastructure/audit.

- Existing11topic groups became numbered1–12defense groups; motivation and parent baselines were combined, shared infrastructure/report support made explicit.
- Code views, configs, notebooks, results, figures and explanations are now local to each method. Code views are symlinks to unchanged real modules; no artificial module separation, algorithm rewrite or new wrapper behavior occurred.
- Canonical result tables have numbered, descriptive names. Tables containing multiple contrasts were not split into invented/rewritten CSVs; the results index specifies actual row selectors.
- Every notebook was moved/renamed byte-for-byte. Same final-comparison notebook is linked from both MiniLM and final-comparison folders.
- Existing internal compatibility paths were rewired; no link should point outside this curated folder.
- Available V1 raw pilot/expanded rows and shared matched source pools were copied read-only to improve case/defense evidence completeness. No cache/model deletion or scientific rerun occurred.
- Old generated docs and migration scripts are historical, not current instructions. Use CODE_MAP, NOTEBOOK_MAP, ALGORITHM_DEFENSE_GUIDE and IMPORTANT_NUMBERS.

Detailed old→new paths and SHA: [defense_reorganization_actions.csv](11_shared_infrastructure/audit/defense_reorganization_actions.csv). Newly restored source records: [restored_defense_artifacts.csv](11_shared_infrastructure/audit/restored_defense_artifacts.csv). Full source trace: PROVENANCE_MANIFEST.csv. Unresolved original raw-output gaps remain explicit.

The final cleanup retired superseded generated guides/audits and moved parent-SARA configs beside its baseline. Exact retirement/move receipts and source-reference validation are recorded in CLEANUP_AND_BASELINES_REPORT.md. Current scientific artifacts were not removed.
