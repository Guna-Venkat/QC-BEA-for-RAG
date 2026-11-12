# Important numbers — defense cheat sheet

All tables select recorded fields from stored sources; source bytes/precision remain unchanged. F1 for QA, macro-F1 for SciFact; no pooled cross-dataset quality. Each table names its exact canonical artifact.

## Early quantity/oracle

Source: [1_fixed_k_oracle_qasper_summary.json](2_adaptive_evidence_quantity/results/1_primary/1_fixed_k_oracle_qasper_summary.json);231queries.

| Recorded metric | Value |
| --- | --- |
| mean_static_sara_k8_f1 | 0.395 |
| mean_oracle_sara_f1 | 0.5008 |
| mean_vanilla_rag_k10_f1 | 0.409 |
| mean_oracle_overall_f1 | 0.5264 |

W3 restricted-action oracle is a different surface, not a conflicting rerun.

## W12 validation

Source: [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv) (`5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv`).

| Dataset | Budget | Method | n | Quality |
| --- | --- | --- | --- | --- |
| HotpotQA | 1024 | FIXED_SENTENCE | 7155 | 0.4233103966803955 |
| HotpotQA | 256 | FIXED_SENTENCE | 7155 | 0.4082469551102361 |
| HotpotQA | 1024 | QBGF_FULL | 7155 | 0.43234387920765305 |
| HotpotQA | 256 | QBGF_FULL | 7155 | 0.41206807780926064 |
| HotpotQA | 1024 | QBGF_NO_QUERY | 7155 | 0.4122516946980074 |
| HotpotQA | 256 | QBGF_NO_QUERY | 7155 | 0.30859344833943314 |
| HotpotQA | 1024 | QBGF_PASSAGE_ONLY | 7155 | 0.4525071338142889 |
| HotpotQA | 256 | QBGF_PASSAGE_ONLY | 7155 | 0.39350944040725905 |
| HotpotQA | 1024 | QBGF_SENTENCE_ONLY | 7155 | 0.4322948785130742 |
| HotpotQA | 256 | QBGF_SENTENCE_ONLY | 7155 | 0.4121892052259855 |
| HotpotQA | 1024 | RAW_SKIP | 7155 | 0.4521325548200152 |
| HotpotQA | 256 | RAW_SKIP | 7155 | 0.40697427526741264 |
| QASPER | 1024 | FIXED_SENTENCE | 1005 | 0.2987884473314289 |
| QASPER | 256 | FIXED_SENTENCE | 1005 | 0.26343006872390434 |
| QASPER | 1024 | QBGF_FULL | 1005 | 0.2950546055190129 |
| QASPER | 256 | QBGF_FULL | 1005 | 0.23551531377816418 |
| QASPER | 1024 | QBGF_NO_QUERY | 1005 | 0.22837332175413008 |
| QASPER | 256 | QBGF_NO_QUERY | 1005 | 0.14730256957991894 |
| QASPER | 1024 | QBGF_PASSAGE_ONLY | 1005 | 0.2895806232236927 |
| QASPER | 256 | QBGF_PASSAGE_ONLY | 1005 | 0.16928258980092692 |
| QASPER | 1024 | QBGF_SENTENCE_ONLY | 1005 | 0.297739930470004 |
| QASPER | 256 | QBGF_SENTENCE_ONLY | 1005 | 0.23558405231606808 |
| QASPER | 1024 | RAW_SKIP | 1005 | 0.2879568225586981 |
| QASPER | 256 | RAW_SKIP | 1005 | 0.16928258980092692 |
| SciFact | 1024 | FIXED_SENTENCE | 177 | 0.6703980265846391 |
| SciFact | 256 | FIXED_SENTENCE | 177 | 0.7000623840543657 |
| SciFact | 1024 | QBGF_FULL | 177 | 0.6604127881084317 |
| SciFact | 256 | QBGF_FULL | 177 | 0.6749686524946782 |
| SciFact | 1024 | QBGF_NO_QUERY | 177 | 0.5426283485343889 |
| SciFact | 256 | QBGF_NO_QUERY | 177 | 0.4879669540229885 |
| SciFact | 1024 | QBGF_PASSAGE_ONLY | 177 | 0.6031073446327683 |
| SciFact | 256 | QBGF_PASSAGE_ONLY | 177 | 0.4577750890636552 |
| SciFact | 1024 | QBGF_SENTENCE_ONLY | 177 | 0.6846926713947991 |
| SciFact | 256 | QBGF_SENTENCE_ONLY | 177 | 0.6749686524946782 |
| SciFact | 1024 | RAW_SKIP | 177 | 0.6989786840325967 |
| SciFact | 256 | RAW_SKIP | 177 | 0.4563775340644733 |

## QBGF query-conditioning deltas

Source: [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv) (`5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv`).

| Dataset | Budget | FULL−NO_QUERY | CI low | CI high | Stored joint Holm p |
| --- | --- | --- | --- | --- | --- |
| QASPER | 256 | 0.08821274419824524 | 0.07163596321652856 | 0.1053558453846999 | 0.005099490050994901 |
| QASPER | 1024 | 0.06668128376488272 | 0.051494599255667996 | 0.08184432694342175 | 0.005099490050994901 |
| HotpotQA | 256 | 0.10347462946982583 | 0.09539650461113358 | 0.11174630766977428 | 0.005099490050994901 |
| HotpotQA | 1024 | 0.020092184509645672 | 0.015356355187004353 | 0.024760053515628388 | 0.005099490050994901 |
| SciFact | 256 | 0.18700169847168968 | 0.10313583108656688 | 0.27097333670398555 | 0.007799220077992201 |
| SciFact | 1024 | 0.11778443957404283 | 0.05571136024533611 | 0.18202430981033813 | 0.011398860113988602 |

## Reserved confirmation

Source: [1_frozen_system_confirmation_results.csv](5_qbgf/results/5_reserved_confirmation/1_frozen_system_confirmation_results.csv) (`5_qbgf/results/5_reserved_confirmation/1_frozen_system_confirmation_results.csv`).

| Dataset | Budget | Method | n | Quality |
| --- | --- | --- | --- | --- |
| HotpotQA | 256 | NONE | 200 | 0.13991512115622023 |
| HotpotQA | 256 | RAW_SKIP | 200 | 0.4226671058060481 |
| HotpotQA | 256 | FIXED_SENTENCE | 200 | 0.4373325432970035 |
| HotpotQA | 256 | H3 | 200 | 0.4622285652428067 |
| HotpotQA | 256 | QBGF_FULL | 200 | 0.440625423632013 |
| HotpotQA | 1024 | NONE | 200 | 0.13991512115622023 |
| HotpotQA | 1024 | RAW_SKIP | 200 | 0.4589173816125694 |
| HotpotQA | 1024 | FIXED_SENTENCE | 200 | 0.4328600462918574 |
| HotpotQA | 1024 | H3 | 200 | 0.45699713452182494 |
| HotpotQA | 1024 | QBGF_FULL | 200 | 0.4672436478410937 |
| SciFact | 256 | NONE | 50 | 0.3686117467581998 |
| SciFact | 256 | RAW_SKIP | 50 | 0.4138029405310511 |
| SciFact | 256 | FIXED_SENTENCE | 50 | 0.7014197530864198 |
| SciFact | 256 | H3 | 50 | 0.7066666666666667 |
| SciFact | 256 | QBGF_FULL | 50 | 0.687037037037037 |
| SciFact | 1024 | NONE | 50 | 0.3686117467581998 |
| SciFact | 1024 | RAW_SKIP | 50 | 0.7679586563307493 |
| SciFact | 1024 | FIXED_SENTENCE | 50 | 0.7440476190476191 |
| SciFact | 1024 | H3 | 50 | 0.716821553762126 |
| SciFact | 1024 | QBGF_FULL | 50 | 0.6346153846153846 |

## LOO helpful/neutral/harmful fractions

Source: [2_helpful_neutral_harmful_summary.csv](6_downstream_utility_attribution/results/1_primary/2_helpful_neutral_harmful_summary.csv) (`6_downstream_utility_attribution/results/1_primary/2_helpful_neutral_harmful_summary.csv`).

| Dataset | Budget | Method | Units | Helpful fraction | Neutral fraction | Harmful fraction |
| --- | --- | --- | --- | --- | --- | --- |
| HotpotQA | 256 | H3 | 451 | 0.0975609756097561 | 0.8536585365853658 | 0.04878048780487805 |
| HotpotQA | 256 | QBGF_FULL | 587 | 0.08858603066439523 | 0.8398637137989778 | 0.07155025553662692 |
| HotpotQA | 1024 | QBGF_FULL | 1914 | 0.050156739811912224 | 0.8808777429467085 | 0.06896551724137931 |
| HotpotQA | 1024 | QBGF_PASSAGE_ONLY | 395 | 0.13164556962025317 | 0.8202531645569621 | 0.04810126582278481 |
| QASPER | 256 | FIXED_SENTENCE | 467 | 0.15631691648822268 | 0.7644539614561028 | 0.07922912205567452 |
| QASPER | 256 | QBGF_FULL | 511 | 0.17025440313111545 | 0.6947162426614482 | 0.1350293542074364 |
| QASPER | 1024 | H3 | 1824 | 0.06962719298245613 | 0.8700657894736842 | 0.06030701754385965 |
| QASPER | 1024 | QBGF_FULL | 1225 | 0.07918367346938776 | 0.8179591836734694 | 0.10285714285714286 |
| SciFact | 256 | C2 | 267 | 0.07116104868913857 | 0.8651685393258427 | 0.06367041198501873 |
| SciFact | 256 | QBGF_FULL | 425 | 0.02823529411764706 | 0.9223529411764706 | 0.04941176470588235 |
| SciFact | 1024 | BM25_PLAIN_RAG | 156 | 0.1346153846153846 | 0.8269230769230769 | 0.038461538461538464 |
| SciFact | 1024 | QBGF_FULL | 1385 | 0.005054151624548736 | 0.9891696750902527 | 0.005776173285198556 |

## BEA-V1 pilot

Source: [1_bea_v1_pilot_quality_results.csv](7_bea_v1/results/1_primary/1_bea_v1_pilot_quality_results.csv) (`7_bea_v1/results/1_primary/1_bea_v1_pilot_quality_results.csv`).

| Dataset | Budget | Method | n | Quality | Evidence tokens |
| --- | --- | --- | --- | --- | --- |
| HotpotQA | 256 | BEA_QBGF | 50 | 0.29764216885700256 | 225.26 |
| HotpotQA | 256 | FIXED_SENTENCE | 50 | 0.3661089991281807 | 254.84 |
| HotpotQA | 256 | QBGF_FULL | 50 | 0.4042251408721997 | 251.62 |
| HotpotQA | 1024 | BEA_QBGF | 50 | 0.34411732413650575 | 284.64 |
| HotpotQA | 1024 | FIXED_SENTENCE | 50 | 0.38929223872103125 | 1001.74 |
| HotpotQA | 1024 | QBGF_FULL | 50 | 0.4020473578708873 | 995.26 |
| QASPER | 256 | BEA_QBGF | 50 | 0.18684869602361862 | 245.74 |
| QASPER | 256 | FIXED_SENTENCE | 50 | 0.2667942999627805 | 255.06 |
| QASPER | 256 | QBGF_FULL | 50 | 0.264119453248936 | 252.52 |
| QASPER | 1024 | BEA_QBGF | 50 | 0.20841776177496998 | 472.78 |
| QASPER | 1024 | FIXED_SENTENCE | 50 | 0.28960275346225595 | 1023.16 |
| QASPER | 1024 | QBGF_FULL | 50 | 0.2964159634497106 | 1020.44 |
| SciFact | 256 | BEA_QBGF | 50 | 0.6127383197150639 | 250.08 |
| SciFact | 256 | FIXED_SENTENCE | 50 | 0.6289147093120108 | 252.62 |
| SciFact | 256 | QBGF_FULL | 50 | 0.5309941520467836 | 250.56 |
| SciFact | 1024 | BEA_QBGF | 50 | 0.6431549537932516 | 696.02 |
| SciFact | 1024 | FIXED_SENTENCE | 50 | 0.5533333333333333 | 1020.7 |
| SciFact | 1024 | QBGF_FULL | 50 | 0.5881045751633986 | 1018.72 |

## BEA-V2 post-hoc

Source: [1_bea_v2_posthoc_quality_results.csv](8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv) (`8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv`).

| Dataset | Budget | Method | n | Quality | Evidence tokens |
| --- | --- | --- | --- | --- | --- |
| HotpotQA | 256 | BEA_QBGF_V1 | 50 | 0.29764216885700256 | 225.26 |
| HotpotQA | 256 | BEA_V2 | 50 | 0.43521106671106674 | 246.88 |
| HotpotQA | 256 | FIXED_SENTENCE | 50 | 0.3661089991281807 | 254.84 |
| HotpotQA | 256 | QBGF_FULL | 50 | 0.4042251408721997 | 251.62 |
| HotpotQA | 1024 | BEA_QBGF_V1 | 50 | 0.34411732413650575 | 284.64 |
| HotpotQA | 1024 | BEA_V2 | 50 | 0.42338747853453734 | 960.66 |
| HotpotQA | 1024 | FIXED_SENTENCE | 50 | 0.38929223872103125 | 1001.74 |
| HotpotQA | 1024 | QBGF_FULL | 50 | 0.4020473578708873 | 995.26 |
| QASPER | 256 | BEA_QBGF_V1 | 50 | 0.18684869602361862 | 245.74 |
| QASPER | 256 | BEA_V2 | 50 | 0.261756159303116 | 245.04 |
| QASPER | 256 | FIXED_SENTENCE | 50 | 0.2667942999627805 | 255.06 |
| QASPER | 256 | QBGF_FULL | 50 | 0.264119453248936 | 252.52 |
| QASPER | 1024 | BEA_QBGF_V1 | 50 | 0.20841776177496998 | 472.78 |
| QASPER | 1024 | BEA_V2 | 50 | 0.2904172350893211 | 1009.1 |
| QASPER | 1024 | FIXED_SENTENCE | 50 | 0.28960275346225595 | 1023.16 |
| QASPER | 1024 | QBGF_FULL | 50 | 0.2964159634497106 | 1020.44 |
| SciFact | 256 | BEA_QBGF_V1 | 50 | 0.6127383197150639 | 250.08 |
| SciFact | 256 | BEA_V2 | 50 | 0.5521885521885521 | 242.48 |
| SciFact | 256 | FIXED_SENTENCE | 50 | 0.6289147093120108 | 252.62 |
| SciFact | 256 | QBGF_FULL | 50 | 0.5309941520467836 | 250.56 |
| SciFact | 1024 | BEA_QBGF_V1 | 50 | 0.6431549537932516 | 696.02 |
| SciFact | 1024 | BEA_V2 | 50 | 0.5772038792633758 | 171.72 |
| SciFact | 1024 | FIXED_SENTENCE | 50 | 0.5533333333333333 | 1020.7 |
| SciFact | 1024 | QBGF_FULL | 50 | 0.5881045751633986 | 1018.72 |

## MiniLM matched comparison

Source: [1_quality_comparison.csv](10_final_method_comparison/results/1_quality_comparison.csv) (`10_final_method_comparison/results/1_quality_comparison.csv`).

| Dataset | Budget | FIXED | QBGF | V1 | V2 post-hoc | MiniLM |
| --- | --- | --- | --- | --- | --- | --- |
| HotpotQA | 256 | 0.3661 | 0.4042 | 0.2976 | **0.4352** | 0.3404 |
| HotpotQA | 1024 | 0.3893 | 0.4020 | 0.3441 | **0.4234** | 0.3618 |
| QASPER | 256 | **0.2668** | 0.2641 | 0.1868 | 0.2618 | 0.2641 |
| QASPER | 1024 | 0.2896 | **0.2964** | 0.2084 | 0.2904 | 0.2827 |
| SciFact | 256 | 0.6289 | 0.5310 | 0.6127 | 0.5522 | **0.6855** |
| SciFact | 1024 | 0.5533 | 0.5881 | 0.6432 | 0.5772 | **0.6479** |

## V2 final resolution calibration

Source: [2_resolution_grid_mechanical_results.csv](8_bea_v2/results/2_calibration_failed/2_resolution_grid_mechanical_results.csv) (`8_bea_v2/results/2_calibration_failed/2_resolution_grid_mechanical_results.csv`).

| Threshold | Threshold stop fraction | All cells eligible | Globally eligible |
| --- | --- | --- | --- |
| 6e-05 | 0.16666666666666666 | True | False |
| 7e-05 | 0.16666666666666666 | True | False |
| 8e-05 | 0.16666666666666666 | True | False |
| 9e-05 | 0.2777777777777778 | False | False |

## Frozen policy

Source: [1_fixed_sentence_final_policy_freeze.json](5_qbgf/results/4_frozen_decision/1_fixed_sentence_final_policy_freeze.json). FIXED_SENTENCE; SFR width10; Qwen3-8B BASE_FP16; no LoRA; budgets 256/1024. BEA-V2 calibration is CALIBRATION_FAILED_TERMINATED; tau8e-5 is post-hoc only. Matched exploratory winners do not replace this freeze.
