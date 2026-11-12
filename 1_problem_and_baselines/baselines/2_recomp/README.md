# RECOMP baseline reference

Extractive/abstractive context compression and selective augmentation; motivation/reference, not a measured matched W12 arm.

**Official source:** [carriex/recomp](https://github.com/carriex/recomp), pinned commit `51d4432151efb3275257a9407dc71d1e5ec6634d`. 10 selected code/config/license files are preserved byte-for-byte; this is a source subset, not weights or a full runnable environment. [Source lock](UPSTREAM_SOURCE_LOCK.json) records URLs, license paths, SHA256 and Git blob IDs.

**Open official code:** [run_extractive_compressor.py](upstream_source/run_extractive_compressor.py).

**Project results:** no matched RECOMP evaluation is recorded in the project’s canonical W12 surface. Status is NOT_EVALUATED, not a zero and not a reproduction of the paper. Official source includes extractive scoring/training, abstractive training, QA and LM evaluation. Dataset/checkpoint downloads and dependencies are not bundled or installed.

**Paper results:** [literature-only reference](PAPER_RESULTS_REFERENCE.md).

**Execution:** this pass did not install packages, train, load models or run evaluations. The original upstream README describes its execution interface; project reproduction additionally needs its historical checkpoint/data/prompt/parser/environment identities. Published paper scores use different systems and protocols.
