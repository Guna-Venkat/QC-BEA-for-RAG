# SARA baseline reference

Mixed explicit passages and compressed latent retrieval vectors; parent architecture, not the frozen final proposed policy.

**Official source:** [Ahren09/SARA](https://github.com/Ahren09/SARA), pinned commit `639f5f48b86672c270046141f44a1b5eab6c8b96`. 163 selected code/config/license files are preserved byte-for-byte; this is a source subset, not weights or a full runnable environment. [Source lock](UPSTREAM_SOURCE_LOCK.json) records URLs, license paths, SHA256 and Git blob IDs.

**Open official code:** [run_sara.py](upstream_source/src/run_sara.py).

**Open project integration:** [1_w12_sara_specialist_runner.py](project_adaptation/1_w12_sara_specialist_runner.py). The reference snapshot and project adaptation are not silently interchangeable.

**Project results:** [query-level specialist records](project_results/1_query_level_specialist_results.csv) and [availability/scope](project_results/2_specialist_availability.csv). BM25/SFR SARA k5/n10 are QASPER adapted-Mistral specialist references (1005queries each), not matched Qwen256/1024 controls. Historical SFR-SARA k6 remains historical only. [Project-versus-upstream byte comparison](project_adaptation/PROJECT_VS_UPSTREAM.csv) explains shared/different files.

**Paper results:** [literature-only reference](PAPER_RESULTS_REFERENCE.md); do not use these as project scores.

**Execution:** this pass did not install packages, train, load models or run evaluations. The original upstream README describes its execution interface; project reproduction additionally needs its historical checkpoint/data/prompt/parser/environment identities. Published paper scores use different systems and protocols.
