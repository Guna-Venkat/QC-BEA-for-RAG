# Failed calibration versus post-hoc reader study

**Official status: CALIBRATION_FAILED_TERMINATED.** Source: [3_calibration_failed_terminated.json](../results/2_calibration_failed/3_calibration_failed_terminated.json).

The original grid and one prespecified resolution grid used the same nine queries (three per dataset) at both budgets, the same predictors and the same mechanical constraints. No Qwen answer/F1/gold/held-out LOO outcomes selected the threshold. The constraints were not relaxed after failure.

The registered rule includes zero empty contexts, at least 20% threshold stopping, at most 80% near-full allocations, global coverage retention, and every dataset/budget cell passing its utilization/median-unit/trivial-exposure/coverage floors. The exact specification is [1_bea_v2_config.json](../configs/1_bea_v2_config.json).

Stored resolution output (no recalibration performed): [2_resolution_grid_mechanical_results.csv](../results/2_calibration_failed/2_resolution_grid_mechanical_results.csv).

| Threshold | Stop fraction | All cells eligible | Globally eligible |
| --- | --- | --- | --- |
| 6e-05 | 0.16666666666666666 | True | False |
| 7e-05 | 0.16666666666666666 | True | False |
| 8e-05 | 0.16666666666666666 | True | False |
| 9e-05 | 0.2777777777777778 | False | False |

None qualifies. The post-hoc reader uses a separately labelled engineering operating point tau=8e-5 in [1_bea_v2_posthoc_config.json](../configs/1_bea_v2_posthoc_config.json). It does not convert the failed calibration into a pass. The four-method matched grid has1,200 logical rows;300 are BEA_V2 (50 queries × 3 datasets × 2 budgets). This is previously analyzed VAL, not fresh confirmation.

Open the local original V2 notebook to inspect the terminal guard; open the separate post-hoc notebook for the reader branch. Do not rerun either during defense.
