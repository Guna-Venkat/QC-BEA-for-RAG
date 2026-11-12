# Dependencies and preserved implementation

Canonical original package layout is retained under11_shared_infrastructure/runtime. Numbered local code files are internal symlinks to those modules; they are navigation views, not executable standalone rewrites. Relative import context matters when executing a viewed module directly; use its original entry script in a restored environment.

Internal original-relative config/result aliases were rewired to the new canonical result locations. Notebook cells, absolute dataset paths, source-version guards, model/parser/prompt definitions and package pins were preserved. No refactor, formula, threshold, tie-breaking or serializer change was made.

Remaining limitations: native corpora/weights/checkpoints are external; historical W12 C/D/M raw outputs and attribution perturbations are missing; the demo dependency list is not a complete research lock; old namespace packages named src require correct original launch context. Static syntax/link checks do not establish all dynamic third-party imports or model execution.

Superseded generated navigation/audit generations were removed with explicit retirement receipts. Use the current verifier for metadata only. Historical report links may still embed original paths; use the source map/provenance and current navigation. None of these issues was hidden by a new score or silently changed source artifact.

Official baseline source is pinned and verified separately; see [upstream limitations](1_problem_and_baselines/baselines/UPSTREAM_LIMITATIONS.md). Third-party reference code is not a claim of successful installation or reproduced paper performance.
