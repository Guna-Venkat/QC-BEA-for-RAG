# Source organization and current demo review

Reviewed 11 November 2026. The user's final folder is named `FINAL_PROJECT_MAIN/` on disk. No `FINAL_MAIN_PROJECT/` directory exists.

## Source organization completed

The physical `src/` package folders now describe research responsibilities rather than weeks. See [the complete source map](src/README.md).

| Code group | Main responsibility |
|---|---|
| `dataset_diagnostics` | Dataset adapters and evidence-utilization diagnostics |
| `context_budget_surfaces`, `context_oracle_analysis` | Fixed-context response surfaces and oracle/headroom analysis |
| `query_context_allocation`, `content_aware_allocation` | Query- and content-conditioned context prediction |
| `passage_routing`, `adaptive_routing_policies` | Passage identity, routing, continuation and fidelity policies |
| `evidence_representation`, `reader_diagnostics`, `granularity_study` | Evidence representations, reader diagnostics and controlled granularity experiments |
| `budgeted_evidence_fusion` | QBGF, baseline evidence packing, protocol, reader and analysis |
| `baseline_comparisons` | Matched passage RAG and specialist baseline adapters |
| `evidence_attribution` | No-refill deletion and downstream utility |
| `frozen_confirmation` | Frozen final-policy confirmation |
| `exploratory_allocation` | BEA-v1, learned-helpfulness BEA-v2 and qualitative cases |
| `final_method_review.py` | Final-policy review checks |

24 directory/file moves include descriptive names for the routing subpackages. Existing source files were moved without rewriting their content. Historical names remain relative compatibility links: removing them would break imports, source-hash registries and notebook paths. Use descriptive folders to read code and keep historical imports for execution; mixing both import namespaces in a process is not recommended. No architecture, model, algorithm, parameter, split, prompt, result or notebook changed.

The archive verification passed **52/52 checks**, including 7,391 source records and all 50 preserved notebooks. This verifies preserved material and navigation; it does not claim the archive contains all deleted historical raw shards or all model weights. See [migration receipt](11_shared_infrastructure/audit/source_name_migration.json).

## Separate archive execution limitation

A fresh-process import check from the final-folder root passed QBGF, BEA-v1 and BEA-v2 allocator imports. Importing the hierarchy failed because `src.week9.provenance` is absent from the curated archive. The original top-level project has that module; it was not one of the folders or files moved in this migration. The renamed `evidence_representation` folder and its `week9` compatibility link resolve to the same preserved contents.

This is a pre-existing archive dependency gap, not a naming regression. It was left unchanged to honor the naming-only scope. The 52 archive checks establish integrity of retained material, not complete import/runtime coverage. Before claiming standalone execution, restore and audit the exact omitted dependency and its dependency closure. See [import check](11_shared_infrastructure/audit/source_import_check.json).

## Demo verdict

**The current app renders, but the new live four-method comparison needs correctness fixes before it can be described as faithful to the research pipeline.**

The reviewed app is the active top-level `demo/`, not the older copy in this archive. Demo source was not modified during this review. No real models, scientific runs or research outputs were created. Automated synthetic tests use fake resources; they do not qualify real SFR/Qwen loading or generation.

Full CPU-only suite: **160 passed, 8 failed**, 28.16 seconds. All current `test_app.py` cases passed, including the four workspaces and the new comparison UI. Passing UI tests establish renderability, not methodological fidelity. Six failed older tests expect the former single-method controls or retriever-comparison flow; another expects CPU SFR availability, and another expects the demo source to be unignored. The outer ignore policy was left unchanged. Do not remove tests merely to claim a clean suite; reconcile the intended supported UI first.

### 1. High: dense sentence scores silently become lexical scores

`demo/live/impact.py:171` calls `cosine(qvec, sv).tolist()`. The canonical cosine helper already returns a Python list. That raises `AttributeError`, swallowed by the next `except`, and sentence scoring falls back to BM25 even after successful dense encoding. With SFR passage scores this creates a mixed scoring pipeline. When sentence embedding succeeded before the error, `sv` is then cleared and BEA also receives the synthetic fallback signals.

A synthetic reproduction with a successful fake encoder recorded one BM25 call on the sentence texts. No real embeddings or answers were generated.

**Correction needed:** consume the canonical list directly; explicitly record the actual scorer. If required semantic scoring fails, mark the relevant method unavailable instead of changing the scientific computation silently.

### 2. High: BEA-v2 uses incompatible features and an unqualified predictor fallback

`demo/live/bea_adapter.py:44–146` implements a separate feature extractor. It substitutes sentence relevance for parent-passage relevance, uses source-order count instead of within-parent relevance rank, and normalizes sentence position differently. A two-sentence synthetic comparison against canonical `src.post_w12.bea_v2.data.feature_rows` found **five mismatched values across three feature definitions**.

`get_utility_model` defaults to one dataset/fold, can choose any available joblib when a requested model is missing, and caches a single bundle globally. Prediction errors are swallowed and replaced by `0.08 + 0.15*(relevance - mean_relevance)`, labelled an empirical prior. This fallback is not the trained research predictor. The canonical research predictor explicitly refuses unseen queries without a separately frozen all-development model.

**Correction needed:** reuse canonical features; validate feature/model hashes and names; use an explicitly qualified custom-input predictor or mark live BEA-v2 unavailable. Do not present arbitrary-fold or heuristic substitution as the frozen learned method.

### 3. High: live BEA parameters differ from the reported experiments

`demo/live/impact.py:244,268` runs both BEA methods at `0.001`. `demo/live/bea_adapter.py:166` also changes v1 `tau_context` to `0.0`.

The archived effective v1 freeze uses `tau_stop=tau_expand=0.01` and `tau_context=0.05`. V2's calibration officially failed; the reported reader comparison at `8e-5` is explicitly post-hoc. A live threshold of `0.001` reproduces neither setting.

**Correction needed:** keep the historical distinction and display the exact demo configuration. If offering a research-comparison mode, load the relevant saved configuration without describing the post-hoc v2 setting as calibrated or deployable.

### 4. High: lexical scores are fed into cosine-oriented QBGF

`demo/live/impact.py:222–229` rescales BM25 scores into a pseudo-cosine range and passes them to QBGF. The older corrected engine explicitly blocks BM25-native QBGF because its scoring scale differs from the frozen cosine contract. The new runner bypasses that safeguard. Its BEA fallback also replaces semantic redundancy with an identity matrix and aspect similarity with scaled relevance.

**Correction needed:** share the corrected engine's protocol checks. Provide clearly labelled lexical context inspection for supported methods; require common SFR downstream scoring for a controlled QBGF/BEA comparison or show those methods unavailable.

### 5. High: failed deletion generations can be classified as helpful evidence

`demo/live/impact.py:405–414` catches reader failure and assigns an ablated score of zero when no answer exists. Subtracting the original score can then label the removed unit helpful, even though the intervention failed technically.

**Correction needed:** mark failed ablations unavailable; do not produce a utility delta/category for them. Preserve the exact original generation contract when retrying. The deletion cache key at line 395 also needs prompt/model/decoding/task/evidence identity rather than query, selected IDs and method alone.

### 6. Medium: claim verification changes scoring, but not the reader task

The four-method runner calculates a `task_type` but does not pass it to `resources.generate`. `demo/live/resources.py:121–136` always calls the reader with `freeform_qa`. Selecting claim verification therefore changes the evaluation view without invoking the frozen verification prompt/parser contract.

**Correction needed:** propagate the task through original and deletion generation, or label this mode as scoring a freeform answer against a user-provided claim label.

### 7. Medium: passage removal and empty-query handling need state regression tests

`demo/live/ui.py:287` removes a passage list entry while retaining index-based widget keys. On rerun, values from the old index can overwrite the passage shifted into that position. A blank query is also replaced by the preset at line 225, which can conceal empty-input validation. Editing inputs leaves earlier four-method results available; impact analysis should explicitly bind to the original run and reference.

These are code-review risks, not claims of a reproduced browser session in this review.

**Correction needed:** stable passage IDs independent of list position, explicit preset loading, and a visible stale-input guard. Add interaction tests for removing first/middle passages and changing query/budget/task before deletion analysis.

### 8. Medium: curated example metadata conflicts with the frozen-system presentation

`demo/curated_examples.py:21–28` labels the showcased Hotpot example `Qwen2.5-7B-Instruct`, top-4 BM25/dense candidates and a word-boundary ceiling. The app's frozen-system banner states Qwen3-8B, SFR top-10 and exact token budgets. Other hardcoded examples also identify Qwen2.5.

This is a confirmed metadata inconsistency, not proof that their displayed scores were fabricated. The current suite does not establish provenance for every hardcoded example field.

**Correction needed:** validate showcased metadata against retained per-query rows and show each example's actual model/pool/tokenizer. If the fields are illustrative, label them as such; do not silently relabel them as frozen results.

### 9. Low: QBGF explanation overstates the implemented solver

`demo/views/algorithm_explorer.py` and `research_and_live.py` describe an exact branch-and-bound dynamic program with dominated-option pruning. The canonical `algorithm.solve` implementation is exact cost-state dynamic programming, with a separate greedy ablation. It does not implement the stated branch-and-bound procedure.

**Correction needed:** describe exact cost-state DP and its relevance-surrogate objective; exact optimization does not establish downstream answer optimality. Broader statistical claims in the hardcoded journey also need explicit links to the registered contrasts and scope.

## Recommended order

1. Repair score handling and remove silent scientific fallbacks.
2. Qualify BEA-v2 model/features and expose the true parameter identities.
3. Exclude failed ablations from quality effects and propagate task/generation identities.
4. Validate curated metadata against saved rows.
5. Reconcile the redesigned UI tests and stable-input state; then perform a small real-model qualification separately, only if authorized.

No demo fixes were applied as part of this naming-and-review request. The application can be inspected, but I would not use its current new four-method live scores as evidence that the frozen research methods have been reproduced.

Evidence: [synthetic reproduction](11_shared_infrastructure/audit/live_demo_review_evidence.json), [test output](11_shared_infrastructure/audit/demo_review_test_output.txt), [CPU-only reproduction script](11_shared_infrastructure/audit/review_live_demo.py).
