# Shared infrastructure

`runtime/` is the canonical byte-exact source package layout. Method-local numbered code files point here. Reader/token-ID serialization, retrieval, sentence segmentation, task evaluation and storage are shared by reference, not copied into divergent algorithms.

`data/matched_source_pools/` contains exact frozen source records for the developmental matched cohort. `audit/` contains source/path/symbol/notebook indexes, snapshots and metadata checks. Old pass scripts are retained historically; only the current verifier is intended after this migration.

See CODE_MAP.md, REPRODUCIBILITY_MAP.md and DEPENDENCY_AUDIT.md for launch/environment boundaries.
