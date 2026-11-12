# Live Lab correctness repairs

**Subsequent user-requested update:** BEA-v2 is now enabled at τ=0.00008 with a verified saved-model ensemble. See [the enablement note](BEA_V2_LIVE_ENABLEMENT.md). The unavailable status described below records the earlier repair state.

11 November 2026 · Active top-level `demo/` only · Branch `gagan`.

## Outcome

The confirmed Live Lab cache, failed-inference, dense-scoring, BEA integration, claim-task and UI threshold defects were repaired without changing research code or scientific results. **183 automated tests passed**. A separate tiny **real SFR + Qwen3-8B CUDA qualification completed with 6 actual model generations** on fictional inputs.

**Important availability boundary:** live FIXED_SENTENCE, QBGF and BEA-v1 execute their canonical selectors with SFR scores. BEA-v2 is explicitly **unavailable for arbitrary custom input**: the retained predictors are research cross-fit models, there is no qualified all-development custom-input predictor, and global calibration officially failed. The implementation does not reuse a random fold, invent probabilities, train a new model or promote the post-hoc threshold. Historical saved BEA-v2 examples/results were not changed.

## What changed

| Area | Correction |
|---|---|
| Reader-output cache | New versioned key binds actual final prompt IDs, model ID/revision, task, tokenizer/template/assets, reader/wrapper code, device/precision, generation settings and seed. Legacy strings and corrupt/incompatible entries are ineligible. Successful entries are bounded in session memory; failures are never cached as answers. |
| Request receipts | Original and ablated requests retain exact prompt IDs/text/hash, evidence hash, selected IDs, reader contract and explicit fresh/cache-hit status. Reader-returned prompt hashes must match prepared requests. Receipt configuration is deep-copied, so later model/config edits cannot rewrite history. |
| Failed original answer | No receipt/answer, wrong configuration or changed serialization makes that method unavailable for LOO. Another method having an answer cannot validate a failed baseline. |
| Failed ablated answer | No score difference and no helpful/harmful/neutral classification. UI displays unavailable/failed interventions separately. Empty output, prompt mismatch and exceptions are failures. |
| SFR scoring | Removed `.tolist()` on the already-list cosine result. No BM25 fallback, pseudo-cosine rescaling, identity-matrix redundancy or synthetic aspect signals in the strict comparison. Failed required SFR scoring makes dependent methods unavailable. |
| Canonical methods | FIXED_SENTENCE/QBGF use the research `choose`; BEA-v1 calls the research allocator and checks exact frozen parameters: tau_stop=tau_expand=.01, tau_context=.05, eta_cov=lambda_red=.5, min_parent_sentences=2. |
| BEA-v2 | Feature extraction delegates to canonical `feature_rows`, including true parent relevance, relevance rank and source-normalized position. The prior/fold fallback is removed. No custom-input generation is represented as qualified BEA-v2. |
| Verification task | Original and ablated generation receive `verification`, with the frozen label prompt and strict parser. Arbitrary prose or negated label substrings do not count as SUPPORT; invalid text does not become NEI. Nonempty invalid outputs count as incorrect; missing generations are unavailable. |
| LOO convention | Live delta remains ablated minus original; QA tolerance .01, verification 0. Same rule drives labels, UI and rescoring. Historical W12 attribution (zero tolerance, reverse sign) remains distinct. |
| Stale controls | Comparisons bind source passages/query, budget, task, segmentation, reader contract and scoring model to a run ID. Changed controls block impact analysis until Compare is rerun. Reference-only changes permit rescoring without generation. |
| Session safety | Comparison, request and LOO paths share the resource lock. Stable passage IDs prevent removal of one card from overwriting another. Blank queries stay blank and empty cards require correction/removal. |
| Legacy inspector | CPU BM25 context inspection remains a labelled separate diagnostic. Its answer reuse now checks current reader identity. It is not silently used as the canonical SFR four-method pipeline. |

The reference remains evaluation-only. It is absent from allocation features, generation requests and inference cache identity. Identical reader requests can legitimately reuse an answer across methods when they expose identical evidence under the same reader contract. That reuse is visible, not reported as a fresh generation.

## Tests

Final command:

```bash
PYTHONDONTWRITEBYTECODE=1 demo/.venv/bin/python -m pytest demo/tests -q -p no:cacheprovider --disable-warnings --tb=short
```

**Result: 183 passed in 28.98 seconds.** Focused tests cover incompatible model/device/seed/decoding/template keys, old/corrupt cache entries, canonical feature equality, no lexical substitution, reference isolation, exact source-order deletion, no refill, empty post-deletion contexts, duplicate facts with different IDs, missing baselines, failed readers, prompt mismatch, strict labels, threshold boundaries, immutable receipts, stale-input blocking, rescoring and passage removal.

Older tests that expected synthetic four-method outputs without SFR or a permissive label parser were replaced with explicit contract tests. The old UI test that manually injected an answer string now verifies that this cannot manufacture an eligible LOO baseline. The ignore test follows the user's current instruction to leave demo ignored. No tests were skipped to obtain a green suite.

## Genuine reader qualification

Only fictional custom passages were used. Pinned models were local; no checkpoint/download, training, validation, confirmation or QASPER TEST run was launched. SFR was released before Qwen loading. A separate process observed the real `model.generate` input tensors and checked their hashes against the stored receipts. There was no `past_key_values` argument or previous assistant/reference prompt injection.

Fixture: *What is the access code of the fictional vessel Merava-507229?*

Original fact: `NEXUL-7319`. Contradictory fact: `ZALUN-9048`.

| Condition | Observed real Qwen output |
|---|---|
| Full evidence | The access code of the fictional vessel Merava-507229 is NEXUL-7319. |
| Delete answer-bearing unit | The access code of the fictional vessel Merava-507229 is not provided in the context. |
| Delete station-only unit | The access code of the fictional vessel Merava-507229 is NEXUL-7319. |
| No external evidence | The access code of the fictional vessel Merava-507229 is not provided in the context. |
| Contradictory evidence | The access code of the fictional vessel Merava-507229 is ZALUN-9048. |
| Verification claim against contradictory evidence | SUPPORT |
| Repeat identical LOO | Cache hit; no additional model generation |
| Reference-only rescoring | No additional model generation |

FIXED_SENTENCE, QBGF and BEA-v1 all exposed 43 evidence tokens on this tiny example and returned the same original answer. It is a plumbing qualification, **not** evidence that these algorithms generally select the same context or achieve equal quality. Request-equivalent generations were shared safely; total actual calls were **6**. The local elapsed time was about **24.5 seconds**, including local loading; this is not a serving-speed or efficiency benchmark.

Technical receipts: [real qualification](../runtime/qa/corrected_live_verification.json), [log](../runtime/qa/corrected_live_verification.log), [automated suite](../runtime/qa/corrected_live_tests.log), [verification hashes](live_repair_verification.json). These contain synthetic inputs only and live under ignored demo paths.

The real qualification was followed by configuration-snapshot and scorer-identity hardening; the final automated suite covers those non-numerical changes. Model loading/prompt/decoding functions used in the genuine check were not altered afterward.

## Files

- `demo/live/inference.py`: new request/receipt/cache boundary.
- `demo/live/impact.py`: repaired canonical comparison, LOO and rescoring.
- `demo/live/resources.py`: full identity, task propagation and generation lock.
- `demo/live/bea_adapter.py`: canonical features/parameters; honest BEA-v2 availability.
- `demo/live/ui.py`: correct statuses/threshold/receipts, stale-run guards, stable passage state.
- `demo/tests/test_live_impact.py`, `test_live_repair_ui.py`, `test_app.py`, `test_final_freeze.py`: meaningful regression coverage and current intended behavior.
- `demo/APPLICATION_GUIDE.md`, `README.md`, `FINAL_FREEZE_STATUS.md`: current workflow and distinction from historical release/research records.
- `demo/runtime/qa/verify_corrected_live.py`: explicit-opt-in synthetic qualification script; no automatic model loading.

## Preservation and limits

Compared **481 protected non-demo source/config/test/freeze files** with the earlier forensic before-inventory: **zero changes**. Root `.gitignore` and all scientific source/settings/results remain unchanged by this repair. Pre-existing user edits were retained. No Git staging/commit/push or tracking change was made. No saved curated answer or research result was rewritten. The checks do not claim to hash every byte of every historical model/data artifact.

The prior forensic report under `/tmp/cs787_loo_integrity_audit/` remains an unchanged record of the old implementation. The historical World Cup run is still unauthenticated; these repairs do not retroactively validate its cache, prompt or score.

The UI still samples the first 1–3 selected units in source order. It is not exhaustive LOO or proof of internal causal reasoning. Optional explicit-unit picking/fact-level evaluation and a future qualified custom-input BEA-v2 model were not added. Real end-to-end qualification used CUDA; CPU sequential dispatch has automated coverage, but no new full CPU-model qualification was run.

## Use now

Restart an already running Streamlit process once to discard old loaded resource objects/session results, then:

```bash
demo/.venv/bin/python -m streamlit run demo/app.py
```

In Live Lab, enable local live models, select CPU or CUDA, enter nonempty passages/query, optionally supply the reference, run Compare, and then Analyze. Inspect the session-only receipts for original and ablated requests. BEA-v2 will explain its unavailable status. Fresh custom outputs remain demonstrations and never enter research result tables.
