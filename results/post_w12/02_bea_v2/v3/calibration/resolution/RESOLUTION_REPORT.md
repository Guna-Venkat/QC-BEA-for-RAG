# Final BEA_V2 allocation-only resolution

The initial preregistered grid identified the qualifying boundary between 5e-5 and 1e-4, but no grid point satisfied all mechanical constraints. A single prespecified resolution sweep of 6e-5,7e-5,8e-5,9e-5 will be performed. The original eligibility rules remain unchanged. Select the smallest threshold satisfying every original criterion. If none qualifies, terminate BEA_V2 calibration.

|   threshold |   n |   threshold_stop_fraction |   budget_stop_fraction |   mean_utilization |   near_full_fraction |   empty_fraction |   coverage_retention | all_cells_eligible   |   failed_cells | eligible   |
|------------:|----:|--------------------------:|-----------------------:|-------------------:|---------------------:|-----------------:|---------------------:|:---------------------|---------------:|:-----------|
|       6e-05 |  18 |                  0.166667 |               0.833333 |           0.855523 |             0.722222 |                0 |             1        | True                 |              0 | False      |
|       7e-05 |  18 |                  0.166667 |               0.833333 |           0.845595 |             0.722222 |                0 |             1        | True                 |              0 | False      |
|       8e-05 |  18 |                  0.166667 |               0.833333 |           0.843804 |             0.722222 |                0 |             1        | True                 |              0 | False      |
|       9e-05 |  18 |                  0.277778 |               0.722222 |           0.830295 |             0.666667 |                0 |             0.999715 | False                |              1 | False      |

## Dataset/budget checks

|   threshold | dataset   |   budget |   n_queries |   empty_contexts |   mean_utilization |   median_units |   trivial_fraction |   coverage_retention |   threshold_stop_fraction | eligible   | failure_reasons      |
|------------:|:----------|---------:|------------:|-----------------:|-------------------:|---------------:|-------------------:|---------------------:|--------------------------:|:-----------|:---------------------|
|       6e-05 | HotpotQA  |      256 |           3 |                0 |           0.960938 |              8 |           0        |              1       |                  0        | True       |                      |
|       6e-05 | HotpotQA  |     1024 |           3 |                0 |           0.976237 |             11 |           0        |              1       |                  0        | True       |                      |
|       6e-05 | QASPER    |      256 |           3 |                0 |           0.97526  |             10 |           0        |              1       |                  0        | True       |                      |
|       6e-05 | QASPER    |     1024 |           3 |                0 |           0.980143 |             22 |           0        |              1       |                  0        | True       |                      |
|       6e-05 | SciFact   |      256 |           3 |                0 |           0.96224  |              6 |           0        |              1       |                  0        | True       |                      |
|       6e-05 | SciFact   |     1024 |           3 |                0 |           0.27832  |              6 |           0        |              1       |                  1        | True       |                      |
|       7e-05 | HotpotQA  |      256 |           3 |                0 |           0.960938 |              8 |           0        |              1       |                  0        | True       |                      |
|       7e-05 | HotpotQA  |     1024 |           3 |                0 |           0.976237 |             11 |           0        |              1       |                  0        | True       |                      |
|       7e-05 | QASPER    |      256 |           3 |                0 |           0.97526  |             10 |           0        |              1       |                  0        | True       |                      |
|       7e-05 | QASPER    |     1024 |           3 |                0 |           0.980143 |             22 |           0        |              1       |                  0        | True       |                      |
|       7e-05 | SciFact   |      256 |           3 |                0 |           0.96224  |              6 |           0        |              1       |                  0        | True       |                      |
|       7e-05 | SciFact   |     1024 |           3 |                0 |           0.21875  |              4 |           0.333333 |              1       |                  1        | True       |                      |
|       8e-05 | HotpotQA  |      256 |           3 |                0 |           0.960938 |              8 |           0        |              1       |                  0        | True       |                      |
|       8e-05 | HotpotQA  |     1024 |           3 |                0 |           0.976237 |             11 |           0        |              1       |                  0        | True       |                      |
|       8e-05 | QASPER    |      256 |           3 |                0 |           0.97526  |             10 |           0        |              1       |                  0        | True       |                      |
|       8e-05 | QASPER    |     1024 |           3 |                0 |           0.980143 |             22 |           0        |              1       |                  0        | True       |                      |
|       8e-05 | SciFact   |      256 |           3 |                0 |           0.96224  |              6 |           0        |              1       |                  0        | True       |                      |
|       8e-05 | SciFact   |     1024 |           3 |                0 |           0.208008 |              4 |           0.333333 |              1       |                  1        | True       |                      |
|       9e-05 | HotpotQA  |      256 |           3 |                0 |           0.960938 |              8 |           0        |              1       |                  0        | True       |                      |
|       9e-05 | HotpotQA  |     1024 |           3 |                0 |           0.966146 |             11 |           0        |              1       |                  0.333333 | True       |                      |
|       9e-05 | QASPER    |      256 |           3 |                0 |           0.97526  |             10 |           0        |              1       |                  0        | True       |                      |
|       9e-05 | QASPER    |     1024 |           3 |                0 |           0.964193 |             21 |           0        |              1       |                  0.333333 | True       |                      |
|       9e-05 | SciFact   |      256 |           3 |                0 |           0.96224  |              6 |           0        |              1       |                  0        | True       |                      |
|       9e-05 | SciFact   |     1024 |           3 |                0 |           0.152995 |              3 |           0.333333 |              0.99829 |                  1        | False      | low_mean_utilization |

Status: **CALIBRATION_FAILED_TERMINATED**; selected threshold: None. Original inputs are unchanged. No reader, answer scores, gold labels, held-out LOO labels or refitting were used.
