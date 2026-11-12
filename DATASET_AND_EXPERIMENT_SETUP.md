# Dataset and experiment setup

| Dataset | Project task / candidate evidence | Primary metric | Frozen W12 VAL | Reserved confirmation |
| --- | --- | --- | --- | --- |
| QASPER | Scientific-paper QA; complete matching paper is the retrieval corpus | Answer F1; EM secondary where recorded |1005queries/281paper groups |0; historical TEST already consumed |
| HotpotQA | Multi-hop QA; provided distractor context paragraphs, not a newly retrieved whole-Wikipedia corpus | Answer F1; EM secondary |7155queries/7155groups |200queries/200groups |
| SciFact | Claim verification over all provided corpus abstracts, never just the cited/gold document | Three-class macro-F1; accuracy/per-class and invalid-format diagnostics |177claims/157groups |50claims/43groups |

The corpora and tasks stress different forms of evidence use: multi-source combination, scientific-paper context and label-sensitive claim verification. Those are task descriptions, not proof that one allocator universally solves them. SciFact invalid outputs count under the original parser; no parser repair based on results occurred.

Common W12 pipeline: query → pinned SFR-Embedding-Mistral → candidate pool capped at10 → exact source units/allocator →256or1024serialized evidence tokens → Qwen/Qwen3-8B BASE_FP16 with no LoRA. Query/instructions/chat framing are outside the evidence-token allowance; output caps are separate. The exact source-block token IDs are inserted into the prompt. Short original pools are preserved, not padded.

QA generation cap128; verification cap16; max context8192; greedy do_sample=False; seed42; Qwen thinking disabled in chat construction, as frozen configuration/source specifies. These reader parameters are not evidence budgets. Confirm against [1_protocol.yaml](5_qbgf/configs/1_protocol.yaml) and [reader.py](11_shared_infrastructure/runtime/src/week12/reader.py).

W11 is a smaller exploratory50-query-per dataset pilot with its own action grids/retrieval width and reader controls; it must not be described as identical to W12. Historical W2–W7 use earlier SARA surfaces/checkpoints.

V1 pilot, LOO, V2 post-hoc and MiniLM share50developmental queries per dataset. V1 expansion has150/dataset and includes the pilot. These are not fresh confirmation. QASPER is paper-grouped, SciFact uses cited-document components, Hotpot normalized-question groups; frozen TRAIN/VAL/CONFIRM are group/ID disjoint.

Exact membership/source identity: [w12_split_freeze.json](5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json); [split_summary.json](5_qbgf/results/4_frozen_decision/split_protocol/split_summary.json). Missing historical raw outputs and external weight/data dependencies remain listed in UNRESOLVED_PROVENANCE.md.
