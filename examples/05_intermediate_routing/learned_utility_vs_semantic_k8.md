# Learned Utility Ranking vs. Static Semantic k=8

## What this example demonstrates
This benchmark demonstrates why **learned whole-passage utility rankers failed to improve upon static semantic ranking**. In Week 7, a pairwise/regression model was trained on 64 multimodal features to rank passages by predicted downstream marginal utility. On the DEV evaluation, learned ranking reached 0.3922 F1, failing to surpass static semantic $k=8$ (0.4010 F1).

This negative result was a pivotal milestone that halted whole-passage ranker engineering and redirected the project toward sub-passage (sentence/span) granularity.

---

## Comparison Table (DEV Set, N=231)

| Method | Mean $k$ | Mean F1 | Mean Context Tokens | Outcome vs. Semantic $k=8$ |
|:---|:---:|:---:|:---:|:---|
| **Static Semantic $k=8$ (B3)** | **8.00** | **0.4010** | **1,737.4** | **Best Static Reference** |
| Static Semantic $k=6$ (B2) | 6.00 | 0.3957 | 1,325.1 | $-0.0053$ F1 |
| Static Semantic $k=4$ (B1) | 4.00 | 0.3909 | 921.1 | $-0.0101$ F1 (Token efficient) |
| Static Semantic $k=2$ (B0) | 2.00 | 0.3118 | 509.6 | $-0.0892$ F1 |
| **W7-C2 Winner (M1 Regression)** | **7.39** | **0.3922** | **1,622.1** | **$-0.0088$ F1 (Failed to beat $k=8$)** |
| W7-C1 (Sufficiency Classifier) | 6.85 | 0.3783 | 1,503.8 | $-0.0227$ F1 |
| Retrospective Epsilon-Oracle | 3.30 | 0.4869 | 775.2 | $+0.0859$ F1 (Theoretical bound) |

---

## Why Learned Ranking Failed
1. **Passage-Level Incoherence:** A whole passage (~200–350 tokens) contains multiple assertions. A learned ranker attempting to predict whether an entire passage is "helpful" struggles with mixed-signal passages containing one relevant sentence buried within 10 irrelevant ones.
2. **Feature Collinearity:** Many of the 64 features (BM25 score, dense cosine, aspect coverage) were highly correlated, leading to overfitting on training folds that failed to generalize under GroupKFold cross-validation.
3. **High Ceiling of Semantic Cosine:** Simple query–passage dense embedding cosine ranking (using SFR-Embedding-Mistral) already provides a very strong ordering; re-ordering full passages adds noise without removing internal passage distractors.

---

## What this example does NOT prove
- This does not prove that learned rerankers are generally useless; sentence-level cross-encoders (such as MiniLM evaluated in Week 12) exhibit strong performance on tasks like SciFact where single sentences are decisive.
- It does not prove that features had zero predictive signal, only that whole-passage utility prediction lacked sufficient signal-to-noise ratio to beat static semantic $k=8$.

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Development Set ($N=231$)
- **Stage:** Week 7 (W7-C2 Utility Ranking Benchmark)
- **Model:** $L_2$ Regularized Direct Utility Regressor (M1) vs. Static Semantic Cosine
- **Original summary artifact:** `results/week7/w7c2_utility_ranking/tables/w7c2_main_dev_results.csv`
- **Reconstructed:** NO (Copied from verbatim frozen records)

