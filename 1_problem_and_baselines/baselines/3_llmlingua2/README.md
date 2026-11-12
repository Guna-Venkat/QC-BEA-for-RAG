# LLMLingua-2 baseline reference

Distilled token-classification prompt compression; the project qualified the smaller official multilingual BERT checkpoint.

**Official source:** [microsoft/LLMLingua](https://github.com/microsoft/LLMLingua), pinned commit `a411a3fa61df74411157b2512b592d5357bd8f17`. 30 selected code/config/license files are preserved byte-for-byte; this is a source subset, not weights or a full runnable environment. [Source lock](UPSTREAM_SOURCE_LOCK.json) records URLs, license paths, SHA256 and Git blob IDs.

**Open official code:** [prompt_compressor.py](upstream_source/llmlingua/prompt_compressor.py).

**Open project integration:** [1_qwen_budgeted_compressor.py](project_adapter/1_qwen_budgeted_compressor.py). The reference snapshot and project adaptation are not silently interchangeable.

**Project results:** [qualification lock](project_results/1_qualification_lock.json) records QUALIFIED for the mBERT MeetingBank checkpoint and package0.2.2. It is a technical qualification, not answer-quality performance. No full W12 LLMLINGUA2 quality row or confirmation arm is recorded. Do not invent one or label this an XLM-R-large reproduction.

**Paper results:** [literature-only reference](PAPER_RESULTS_REFERENCE.md). Code-level MIT licensing does not redefine the paper’s copyright.

**Execution:** this pass did not install packages, train, load models or run evaluations. The original upstream README describes its execution interface; project reproduction additionally needs its historical checkpoint/data/prompt/parser/environment identities. Published paper scores use different systems and protocols.
