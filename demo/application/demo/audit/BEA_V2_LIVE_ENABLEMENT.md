# BEA-v2 enabled for Live Lab

User-requested update, 11 November 2026.

BEA-v2 now executes at **tau = 0.00008** in the four-method comparison and LOO analysis.

- Uses the actual 15 saved logistic-regression bundles, with file SHA256, dataset/fold and canonical feature-schema checks.
- Predicts helpfulness/harmfulness for canonical outcome-free features. Averages five folds within each dataset, then weights the three datasets equally. No dataset is guessed from the user's question, no arbitrary single fold is selected, and no probability prior is invented.
- Executes the unchanged canonical BEA-v2 allocator: P_help × max(0, relevance + .5 coverage gain − .5 redundancy), marginal utility/token transitions, tau=8e-5. P_harm remains diagnostic only.
- Predictions, model hashes, threshold and ensemble policy are available in the method's execution metadata. Evidence, answers and no-refill LOO use the existing corrected reader/cache contracts.
- This is an exploratory custom-input ensemble using saved research models, not the historical held-out cross-fit evaluation. Research calibration termination, scientific results and predictor weights remain unchanged. No training or full research run was performed.

**Tests:** 185 passed in 29.22 seconds, including actual saved-model probability equality, all-four-method execution, BEA-v2 LOO, cache isolation and UI rendering.

A second genuine GPU qualification was attempted but safely stopped before model loading: Local pins or idle GPU memory unavailable; free GPU memory was 6574 MiB. The active application/GPU process was left untouched. The real SFR/Qwen six-generation qualification from the prior repair remains valid for the unchanged reader path; the newly enabled BEA-v2 predictor/allocator integration was checked with saved trained models and synthetic reader tests.

Reload the application and click **Compare Four Methods** again. Enable Live Models as usual. BEA-v2 no longer carries the previous availability block.
