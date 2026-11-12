# Out-of-fold usefulness models

CPU logistic regression, C=1, StandardScaler fit on training folds only. Separate models per dataset and binary target; no class reweighting or hyperparameter search.

| dataset   |   fold | target   |   n_units |   n_groups |   prevalence |   roc_auc |   pr_auc_average_precision |      brier |   constant_prevalence_brier |
|:----------|-------:|:---------|----------:|-----------:|-------------:|----------:|---------------------------:|-----------:|----------------------------:|
| HotpotQA  |      0 | HELPFUL  |       583 |         10 |   0.0308748  |  0.71706  |                  0.0761424 | 0.0320818  |                  0.0299215  |
| HotpotQA  |      0 | HARMFUL  |       583 |         10 |   0.0325901  |  0.483343 |                  0.0356819 | 0.0333872  |                  0.0315279  |
| HotpotQA  |      1 | HELPFUL  |       620 |         10 |   0.0483871  |  0.717345 |                  0.133362  | 0.0447361  |                  0.0460458  |
| HotpotQA  |      1 | HARMFUL  |       620 |         10 |   0.0903226  |  0.27992  |                  0.0601879 | 0.087574   |                  0.0821644  |
| HotpotQA  |      2 | HELPFUL  |       595 |         10 |   0.0722689  |  0.644949 |                  0.145478  | 0.0658094  |                  0.0670461  |
| HotpotQA  |      2 | HARMFUL  |       595 |         10 |   0.0655462  |  0.272344 |                  0.0427398 | 0.0637253  |                  0.0612499  |
| HotpotQA  |      3 | HELPFUL  |       561 |         10 |   0.0748663  |  0.596637 |                  0.120582  | 0.0690556  |                  0.0692613  |
| HotpotQA  |      3 | HARMFUL  |       561 |         10 |   0.0748663  |  0.366983 |                  0.0557688 | 0.0717445  |                  0.0692613  |
| HotpotQA  |      4 | HELPFUL  |       582 |         10 |   0.0945017  |  0.637588 |                  0.148274  | 0.0858623  |                  0.0855711  |
| HotpotQA  |      4 | HARMFUL  |       582 |         10 |   0.0687285  |  0.418335 |                  0.064731  | 0.0655397  |                  0.0640049  |
| QASPER    |      0 | HELPFUL  |       671 |         10 |   0.0402385  |  0.79805  |                  0.151253  | 0.0387368  |                  0.0386193  |
| QASPER    |      0 | HARMFUL  |       671 |         10 |   0.0298063  |  0.609716 |                  0.0638561 | 0.0337677  |                  0.0289178  |
| QASPER    |      1 | HELPFUL  |       816 |         10 |   0.144608   |  0.614722 |                  0.318398  | 0.11913    |                  0.123696   |
| QASPER    |      1 | HARMFUL  |       816 |         10 |   0.147059   |  0.603305 |                  0.208876  | 0.128234   |                  0.125433   |
| QASPER    |      2 | HELPFUL  |       699 |         10 |   0.0486409  |  0.748784 |                  0.11126   | 0.0470468  |                  0.046275   |
| QASPER    |      2 | HARMFUL  |       699 |         10 |   0.137339   |  0.510037 |                  0.140506  | 0.124812   |                  0.118477   |
| QASPER    |      3 | HELPFUL  |       670 |         10 |   0.153731   |  0.524238 |                  0.205878  | 0.137039   |                  0.130098   |
| QASPER    |      3 | HARMFUL  |       670 |         10 |   0.0656716  |  0.520349 |                  0.070283  | 0.065989   |                  0.0613589  |
| QASPER    |      4 | HELPFUL  |       687 |         10 |   0.0727802  |  0.637614 |                  0.148601  | 0.0660927  |                  0.0674832  |
| QASPER    |      4 | HARMFUL  |       687 |         10 |   0.0451237  |  0.66847  |                  0.122493  | 0.0447185  |                  0.0430876  |
| SciFact   |      0 | HELPFUL  |       376 |         10 |   0.00797872 |  0.899911 |                  0.0918748 | 0.00891305 |                  0.00791506 |
| SciFact   |      0 | HARMFUL  |       376 |         10 |   0.0212766  |  0.935292 |                  0.234065  | 0.0189677  |                  0.0208239  |
| SciFact   |      1 | HELPFUL  |       411 |         10 |   0.0218978  |  0.929243 |                  0.257211  | 0.019674   |                  0.0214183  |
| SciFact   |      1 | HARMFUL  |       411 |         10 |   0.0243309  |  0.843017 |                  0.0773465 | 0.0235758  |                  0.0237389  |
| SciFact   |      2 | HELPFUL  |       441 |         10 |   0.0249433  |  0.877273 |                  0.161035  | 0.0231356  |                  0.0243211  |
| SciFact   |      2 | HARMFUL  |       441 |         10 |   0.0136054  |  0.795594 |                  0.0664139 | 0.0132908  |                  0.0134203  |
| SciFact   |      3 | HELPFUL  |       417 |         10 |   0.0167866  |  0.760627 |                  0.0444023 | 0.0170164  |                  0.0165048  |
| SciFact   |      3 | HARMFUL  |       417 |         10 |   0.0359712  |  0.793284 |                  0.125457  | 0.0342217  |                  0.0346773  |
| SciFact   |      4 | HELPFUL  |       408 |         10 |   0.0122549  |  0.749628 |                  0.0299433 | 0.0136148  |                  0.0121047  |
| SciFact   |      4 | HARMFUL  |       408 |         10 |   0.0147059  |  0.529229 |                  0.0195619 | 0.0197169  |                  0.0144896  |

## Predicted probabilities by actual historical class

| dataset   | category   |    p_help |    p_harm |
|:----------|:-----------|----------:|----------:|
| HotpotQA  | HARMFUL    | 0.0608187 | 0.0506711 |
| HotpotQA  | HELPFUL    | 0.0835712 | 0.0599146 |
| HotpotQA  | NEUTRAL    | 0.0616137 | 0.0649417 |
| QASPER    | HARMFUL    | 0.120869  | 0.0890629 |
| QASPER    | HELPFUL    | 0.137458  | 0.105227  |
| QASPER    | NEUTRAL    | 0.083091  | 0.0841868 |
| SciFact   | HARMFUL    | 0.0413681 | 0.0494947 |
| SciFact   | HELPFUL    | 0.0602918 | 0.0525073 |
| SciFact   | NEUTRAL    | 0.0159728 | 0.021044  |

## Per-fold actual-class probabilities

| dataset   |   fold | category   |   units |   mean_p_help |   mean_p_harm |   prevalence |
|:----------|-------:|:-----------|--------:|--------------:|--------------:|-------------:|
| HotpotQA  |      0 | HARMFUL    |      19 |     0.101695  |     0.0686553 |   0.0325901  |
| HotpotQA  |      0 | HELPFUL    |      18 |     0.112407  |     0.0554905 |   0.0308748  |
| HotpotQA  |      0 | NEUTRAL    |     546 |     0.0753316 |     0.0706487 |   0.936535   |
| HotpotQA  |      1 | HARMFUL    |      56 |     0.0627949 |     0.0387249 |   0.0903226  |
| HotpotQA  |      1 | HELPFUL    |      30 |     0.104764  |     0.0611883 |   0.0483871  |
| HotpotQA  |      1 | NEUTRAL    |     534 |     0.0656609 |     0.0584403 |   0.86129    |
| HotpotQA  |      2 | HARMFUL    |      39 |     0.033909  |     0.0479234 |   0.0655462  |
| HotpotQA  |      2 | HELPFUL    |      43 |     0.0744193 |     0.0679223 |   0.0722689  |
| HotpotQA  |      2 | NEUTRAL    |     513 |     0.0524486 |     0.0636656 |   0.862185   |
| HotpotQA  |      3 | HARMFUL    |      42 |     0.0664534 |     0.0558084 |   0.0748663  |
| HotpotQA  |      3 | HELPFUL    |      42 |     0.0803364 |     0.0571461 |   0.0748663  |
| HotpotQA  |      3 | NEUTRAL    |     477 |     0.0613695 |     0.0690972 |   0.850267   |
| HotpotQA  |      4 | HARMFUL    |      40 |     0.0589563 |     0.056138  |   0.0687285  |
| HotpotQA  |      4 | HELPFUL    |      55 |     0.0721994 |     0.0565214 |   0.0945017  |
| HotpotQA  |      4 | NEUTRAL    |     487 |     0.0516895 |     0.0629465 |   0.83677    |
| QASPER    |      0 | HARMFUL    |      20 |     0.0917257 |     0.11718   |   0.0298063  |
| QASPER    |      0 | HELPFUL    |      27 |     0.138988  |     0.122728  |   0.0402385  |
| QASPER    |      0 | NEUTRAL    |     624 |     0.084811  |     0.0944764 |   0.929955   |
| QASPER    |      1 | HARMFUL    |     120 |     0.159346  |     0.0884466 |   0.147059   |
| QASPER    |      1 | HELPFUL    |     118 |     0.189525  |     0.0964794 |   0.144608   |
| QASPER    |      1 | NEUTRAL    |     578 |     0.0905662 |     0.071091  |   0.708333   |
| QASPER    |      2 | HARMFUL    |      96 |     0.0926004 |     0.073458  |   0.137339   |
| QASPER    |      2 | HELPFUL    |      34 |     0.13666   |     0.113665  |   0.0486409  |
| QASPER    |      2 | NEUTRAL    |     569 |     0.0902923 |     0.0714674 |   0.81402    |
| QASPER    |      3 | HARMFUL    |      44 |     0.110376  |     0.0940268 |   0.0656716  |
| QASPER    |      3 | HELPFUL    |     103 |     0.0920433 |     0.096876  |   0.153731   |
| QASPER    |      3 | NEUTRAL    |     523 |     0.0687911 |     0.0933342 |   0.780597   |
| QASPER    |      4 | HARMFUL    |      31 |     0.0931564 |     0.114588  |   0.0451237  |
| QASPER    |      4 | HELPFUL    |      50 |     0.107852  |     0.127889  |   0.0727802  |
| QASPER    |      4 | NEUTRAL    |     606 |     0.0797696 |     0.0901307 |   0.882096   |
| SciFact   |      0 | HARMFUL    |       8 |     0.0683902 |     0.1048    |   0.0212766  |
| SciFact   |      0 | HELPFUL    |       3 |     0.134771  |     0.0505552 |   0.00797872 |
| SciFact   |      0 | NEUTRAL    |     365 |     0.0234729 |     0.0269021 |   0.970745   |
| SciFact   |      1 | HARMFUL    |      10 |     0.0179149 |     0.0490067 |   0.0243309  |
| SciFact   |      1 | HELPFUL    |       9 |     0.0746631 |     0.0633765 |   0.0218978  |
| SciFact   |      1 | NEUTRAL    |     392 |     0.0131161 |     0.0201391 |   0.953771   |
| SciFact   |      2 | HARMFUL    |       6 |     0.105612  |     0.0408901 |   0.0136054  |
| SciFact   |      2 | HELPFUL    |      11 |     0.0680073 |     0.0353546 |   0.0249433  |
| SciFact   |      2 | NEUTRAL    |     424 |     0.0134131 |     0.0157183 |   0.961451   |
| SciFact   |      3 | HARMFUL    |      15 |     0.0302909 |     0.0356474 |   0.0359712  |
| SciFact   |      3 | HELPFUL    |       7 |     0.0234412 |     0.0268124 |   0.0167866  |
| SciFact   |      3 | NEUTRAL    |     395 |     0.0124281 |     0.0143663 |   0.947242   |
| SciFact   |      4 | HARMFUL    |       6 |     0.0078758 |     0.0197905 |   0.0147059  |
| SciFact   |      4 | HELPFUL    |       5 |     0.0243527 |     0.107823  |   0.0122549  |
| SciFact   |      4 | NEUTRAL    |     397 |     0.0181586 |     0.0288836 |   0.973039   |

PR-AUC is average precision; ROC-AUC is undefined for one-class held-out targets. Calibration bins are in calibration.csv. Historical selected-unit data are context-specific and imbalanced; probabilities are predictive surrogates, not causal necessity. No gold/answer/LOO value enters the feature vector. The cohort is developmental; even cross-fitting does not make it fresh validation.
