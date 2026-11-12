# MiniLM cross-encoder: matched-cohort comparison

POST-W12 exploratory matched-cohort comparison on previously analyzed development data. No fresh holdout, confirmation or test claim. Official Week-12 policy unchanged.

| Dataset   |   Budget | FIXED      | QBGF       |   BEA-V1 | BEA-V2     | MiniLM Reranker   | Winner          |
|:----------|---------:|:-----------|:-----------|---------:|:-----------|:------------------|:----------------|
| HotpotQA  |      256 | 0.3661     | 0.4042     |   0.2976 | **0.4352** | 0.3404            | BEA-V2          |
| HotpotQA  |     1024 | 0.3893     | 0.4020     |   0.3441 | **0.4234** | 0.3618            | BEA-V2          |
| QASPER    |      256 | **0.2668** | 0.2641     |   0.1868 | 0.2618     | 0.2641            | FIXED           |
| QASPER    |     1024 | 0.2896     | **0.2964** |   0.2084 | 0.2904     | 0.2827            | QBGF            |
| SciFact   |      256 | 0.6289     | 0.5310     |   0.6127 | 0.5522     | **0.6855**        | MiniLM Reranker |
| SciFact   |     1024 | 0.5533     | 0.5881     |   0.6432 | 0.5772     | **0.6479**        | MiniLM Reranker |

HotpotQA/QASPER: answer F1; SciFact: three-class macro-F1. Bold indicates highest point estimate, not statistical superiority.

## Efficiency

| label                                  | Dataset   |   Budget | Method             |   Quality |   Mean Evidence Tokens |   Budget Utilization |   Selected Units |   Represented Parents |   mean_redundancy |
|:---------------------------------------|:----------|---------:|:-------------------|----------:|-----------------------:|---------------------:|-----------------:|----------------------:|------------------:|
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | BEA_QBGF_V1        |  0.297642 |                 225.26 |             0.879922 |            18.16 |                  9.66 |          0.594611 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | BEA_V2             |  0.435211 |                 246.88 |             0.964375 |             7.46 |                  4.98 |          0.611181 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | FIXED_SENTENCE     |  0.366109 |                 254.84 |             0.995469 |             9.8  |                  5.28 |          0.650451 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | MINILM_CE_SENTENCE |  0.340368 |                 254.86 |             0.995547 |            10.54 |                  6.46 |          0.624712 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | QBGF_FULL          |  0.404225 |                 251.62 |             0.982891 |            11.74 |                  4.94 |          0.627003 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | BEA_QBGF_V1        |  0.344117 |                 284.64 |             0.277969 |            20.02 |                  9.72 |          0.591976 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | BEA_V2             |  0.423387 |                 960.66 |             0.938145 |            16.2  |                  9.5  |          0.572894 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | FIXED_SENTENCE     |  0.389292 |                1001.74 |             0.978262 |            36.06 |                  9.62 |          0.585496 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | MINILM_CE_SENTENCE |  0.361826 |                1000.3  |             0.976855 |            38.16 |                  9.94 |          0.574948 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | QBGF_FULL          |  0.402047 |                 995.26 |             0.971934 |            38.28 |                  9.24 |          0.573011 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | BEA_QBGF_V1        |  0.186849 |                 245.74 |             0.959922 |            20.3  |                  8.78 |          0.58434  |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | BEA_V2             |  0.261756 |                 245.04 |             0.957187 |            10.66 |                  5.28 |          0.662262 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | FIXED_SENTENCE     |  0.266794 |                 255.06 |             0.996328 |             9.34 |                  5.7  |          0.686346 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | MINILM_CE_SENTENCE |  0.264111 |                 255    |             0.996094 |            10.14 |                  6.06 |          0.653842 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | QBGF_FULL          |  0.264119 |                 252.52 |             0.986406 |            10.22 |                  5.82 |          0.68218  |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | BEA_QBGF_V1        |  0.208418 |                 472.78 |             0.461699 |            31.9  |                  9.3  |          0.587056 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | BEA_V2             |  0.290417 |                1009.1  |             0.985449 |            22.96 |                  8.14 |          0.626671 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | FIXED_SENTENCE     |  0.289603 |                1023.16 |             0.99918  |            32.2  |                  9.62 |          0.66966  |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | MINILM_CE_SENTENCE |  0.282723 |                1021.64 |             0.997695 |            38.74 |                  9.64 |          0.627879 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | QBGF_FULL          |  0.296416 |                1020.44 |             0.996523 |            24.5  |                  8.56 |          0.639274 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | BEA_QBGF_V1        |  0.612738 |                 250.08 |             0.976875 |            15.46 |                  8.16 |          0.629506 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | BEA_V2             |  0.552189 |                 242.48 |             0.947187 |             6.44 |                  4.02 |          0.741641 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | FIXED_SENTENCE     |  0.628915 |                 252.62 |             0.986797 |             6.56 |                  3.22 |          0.750613 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | MINILM_CE_SENTENCE |  0.685463 |                 252.82 |             0.987578 |             7.1  |                  3.9  |          0.726335 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | QBGF_FULL          |  0.530994 |                 250.56 |             0.97875  |             8.5  |                  3.36 |          0.721572 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | BEA_QBGF_V1        |  0.643155 |                 696.02 |             0.679707 |            33.98 |                  9.8  |          0.634118 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | BEA_V2             |  0.577204 |                 171.72 |             0.167695 |             3.88 |                  2.46 |          0.763898 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | FIXED_SENTENCE     |  0.553333 |                1020.7  |             0.996777 |            24.1  |                  8.3  |          0.718169 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | MINILM_CE_SENTENCE |  0.647868 |                1020.7  |             0.996777 |            27.76 |                  8.38 |          0.693309 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | QBGF_FULL          |  0.588105 |                1018.72 |             0.994844 |            27.7  |                  7.02 |          0.674211 |

## Descriptive point-estimate wins only

- FIXED_SENTENCE: 1 / 6
- QBGF_FULL: 1 / 6
- BEA_QBGF_V1: 0 / 6
- BEA_V2: 2 / 6
- MINILM_CE_SENTENCE: 2 / 6

Exact ties credit all tied methods, so counts can sum above six.

## Paired comparisons

| label                                  | dataset   |   budget | left               | right          |        point |      ci_low |   ci_high |     raw_p |   resamples |   seed |   n_queries |   n_clusters | metric   | test                                                                          |   holm_p |   exploratory_family_size |
|:---------------------------------------|:----------|---------:|:-------------------|:---------------|-------------:|------------:|----------:|----------:|------------:|-------:|------------:|-------------:|:---------|:------------------------------------------------------------------------------|---------:|--------------------------:|
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | MINILM_CE_SENTENCE | FIXED_SENTENCE | -0.025741    | -0.107376   | 0.0534584 | 0.558844  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | MINILM_CE_SENTENCE | QBGF_FULL      | -0.0638571   | -0.171352   | 0.039398  | 0.247275  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | MINILM_CE_SENTENCE | BEA_QBGF_V1    |  0.0427258   | -0.0416063  | 0.133215  | 0.346065  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |      256 | MINILM_CE_SENTENCE | BEA_V2         | -0.0948431   | -0.217733   | 0.0257214 | 0.143486  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | MINILM_CE_SENTENCE | FIXED_SENTENCE | -0.0274664   | -0.0975936  | 0.0329731 | 0.476652  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | MINILM_CE_SENTENCE | QBGF_FULL      | -0.0402215   | -0.115768   | 0.0265603 | 0.289971  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | MINILM_CE_SENTENCE | BEA_QBGF_V1    |  0.0177085   | -0.0649059  | 0.103461  | 0.689131  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | HotpotQA  |     1024 | MINILM_CE_SENTENCE | BEA_V2         | -0.0615617   | -0.147642   | 0.0146889 | 0.144186  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | MINILM_CE_SENTENCE | FIXED_SENTENCE | -0.00268351  | -0.0254521  | 0.0185513 | 0.819818  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | MINILM_CE_SENTENCE | QBGF_FULL      | -8.66263e-06 | -0.0451504  | 0.0398189 | 0.9994    |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | MINILM_CE_SENTENCE | BEA_QBGF_V1    |  0.0772621   |  0.0136261  | 0.147747  | 0.0248975 |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 0.572643 |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |      256 | MINILM_CE_SENTENCE | BEA_V2         |  0.00235463  | -0.0220387  | 0.0257597 | 0.850015  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | MINILM_CE_SENTENCE | FIXED_SENTENCE | -0.00688011  | -0.0353136  | 0.0172327 | 0.643536  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | MINILM_CE_SENTENCE | QBGF_FULL      | -0.0136933   | -0.0393675  | 0.0106242 | 0.29757   |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | MINILM_CE_SENTENCE | BEA_QBGF_V1    |  0.0743049   |  0.00610939 | 0.148522  | 0.0467953 |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | QASPER    |     1024 | MINILM_CE_SENTENCE | BEA_V2         | -0.00769459  | -0.0518498  | 0.0326695 | 0.740026  |       10000 |     42 |          50 |           50 | f1       | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | MINILM_CE_SENTENCE | FIXED_SENTENCE |  0.0565479   | -0.0585276  | 0.173319  | 0.371963  |       10000 |     42 |          50 |           50 | macro_f1 | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | MINILM_CE_SENTENCE | QBGF_FULL      |  0.154469    |  0.0381457  | 0.280546  | 0.0107989 |       10000 |     42 |          50 |           50 | macro_f1 | two-sided paired cluster label-swap randomization; exchangeability under null | 0.259174 |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | MINILM_CE_SENTENCE | BEA_QBGF_V1    |  0.0727243   | -0.0731647  | 0.22464   | 0.335466  |       10000 |     42 |          50 |           50 | macro_f1 | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |      256 | MINILM_CE_SENTENCE | BEA_V2         |  0.133274    | -0.00476515 | 0.2767    | 0.0953905 |       10000 |     42 |          50 |           50 | macro_f1 | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | MINILM_CE_SENTENCE | FIXED_SENTENCE |  0.0945342   |  0          | 0.197004  | 0.249775  |       10000 |     42 |          50 |           50 | macro_f1 | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | MINILM_CE_SENTENCE | QBGF_FULL      |  0.059763    | -0.0384106  | 0.16502   | 0.253175  |       10000 |     42 |          50 |           50 | macro_f1 | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | MINILM_CE_SENTENCE | BEA_QBGF_V1    |  0.00471261  | -0.122236   | 0.133681  | 0.943306  |       10000 |     42 |          50 |           50 | macro_f1 | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |
| POST_W12_RERANKER_BASELINE_EXPLORATORY | SciFact   |     1024 | MINILM_CE_SENTENCE | BEA_V2         |  0.0706637   | -0.0844944  | 0.230917  | 0.409059  |       10000 |     42 |          50 |           50 | macro_f1 | two-sided paired cluster label-swap randomization; exchangeability under null | 1        |                        24 |

Existing paired cluster-bootstrap 95% intervals and cluster label-swap raw p-values; one exploratory Holm family of all 24. QASPER paper groups and SciFact cited-document components remain unchanged. These intervals omit model-training uncertainty of historical learned controls. No per-query macro-F1, pooled task score, confirmation or new method selection.

## Defensive interpretation

**Question A — MiniLM versus FIXED_SENTENCE:** higher point quality in 2/6 cells, exact point ties in 0/6. Positive nominal-CI plus Holm-p<.05 cells: none. Inspect all signs, magnitudes and uncertainty; failure to reject is not equivalence.

**Question B — MiniLM versus QBGF_FULL:** higher point quality in 2/6 cells, exact point ties in 0/6. Positive nominal-CI plus Holm-p<.05 cells: none. Inspect all signs, magnitudes and uncertainty; failure to reject is not equivalence.

**Question C — MiniLM versus BEA_QBGF_V1:** higher point quality in 6/6 cells, exact point ties in 0/6. Positive nominal-CI plus Holm-p<.05 cells: none. Inspect all signs, magnitudes and uncertainty; failure to reject is not equivalence.

**Question D — MiniLM versus BEA_V2:** higher point quality in 3/6 cells, exact point ties in 0/6. Positive nominal-CI plus Holm-p<.05 cells: none. Inspect all signs, magnitudes and uncertainty; failure to reject is not equivalence.

**Question E — “Your method is only reranking”:** this control changes the relevance scorer while holding the candidate pool, source sentences, packing budget and reader fixed. Similar scores would be compatible with relevance ranking explaining substantial performance; they would not prove equivalence. MiniLM wins would require allocation methods to justify their added complexity. MiniLM losses would show this particular static relevance scorer does not reproduce those observed gains, but would not isolate state-dependent utility as their cause. This is a pretrained English MS-MARCO model applied to three different tasks, not every possible cross-encoder. Inspect exact contexts and task-specific errors rather than selecting a favorable cell.

## Cost and diagnostic limits

CPU CE scoring is query-time computation and remains conceptual cost on cache hits. Score-cache metadata retains original measured scoring seconds and pair/truncation counts. Reader prompt/generated-token costs remain counted on reused outputs. Evidence-token savings do not imply end-to-end latency improvements. Gold retention is computed only after selection; partial/unmapped annotations are explicit. No P_help, LOO labels or downstream quality enters ranking.

| Method | Evidence value | Allocation behavior |
| --- | --- | --- |
| FIXED_SENTENCE | embedding query–sentence relevance | static global ranking + packing |
| MiniLM reranker | cross-encoder query–sentence relevance | static global ranking + packing |
| QBGF | hierarchical passage/sentence relevance mass | joint DROP/SENT/FULL budget optimization |
| BEA-V1 | relevance + coverage − redundancy | dynamic marginal selection + stopping |
| BEA-V2 | P_help × positive semantic IG | dynamic learned-utility selection + stopping |

We began with query-conditioned evidence quantity, moved to evidence identity and granularity, then tested relevance-aware and downstream-utility-aware allocation. The MiniLM cross-encoder baseline provides a conventional reranking control over the same SFR candidate pool. Together, the comparison distinguishes simple relevance reranking from budgeted granularity allocation and dynamic marginal-utility selection. The official frozen policy remains SFR top-10 → FIXED_SENTENCE → Qwen3-8B BASE_FP16 → no LoRA. This is a final POST-W12 exploratory baseline, not a replacement for the frozen method.
