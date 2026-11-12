# Equations and pipeline → exact code

Line numbers are extracted from the unchanged copied modules; use the named function if your editor does not support line anchors. Code views are internal symlinks, not rewritten implementations.

| Mathematical / pipeline component | Function and current source lines |
| --- | --- |
| Historical LOO inputs, cohort and provenance audit. | [audit](../code/3_loo_feature_data.py) (lines 32–96) |
| Inference features and exact sentence label mapping. | [feature_rows](../code/3_loo_feature_data.py) (lines 10–27) |
| StandardScaler + fixed L2 logistic regression. | [fit_binary](../code/2_group_crossfit_phelp_models.py) (lines 15–20) |
| GroupKFold and group/query exclusion, separate help/harm predictors. | [train](../code/2_group_crossfit_phelp_models.py) (lines 40–94) |
| Held-out predictor routing, feature order and probability bounds. | [predict](../code/2_group_crossfit_phelp_models.py) (lines 96–107) |
| P_help×positive IG; P_harm diagnostic only. | [utility](../code/1_usefulness_weighted_allocator.py) (lines 8–11) |
| Recompute values after every hypothetical addition. | [sequence](../code/1_usefulness_weighted_allocator.py) (lines 13–21) |
| Fidelity transitions, FULL eligibility, exact cost, deterministic ties and threshold stopping. | [allocate](../code/1_usefulness_weighted_allocator.py) (lines 23–89) |
| Unchanged global and dataset/budget mechanical qualification criteria. | [calibration_summary](../code/4_calibration_and_reader_stages.py) (lines 36–64) |
| Nine-query preregistration and original grid. | [calibrate](../code/4_calibration_and_reader_stages.py) (lines 67–98) |
| Single prespecified fine grid and terminal calibration failure. | [run](../code/6_final_calibration_resolution.py) (lines 32–113) |
| Distinct post-hoc reader branch; no official calibration repair. | [generate](../code/5_posthoc_reader_runner.py) (lines 114–193) |
