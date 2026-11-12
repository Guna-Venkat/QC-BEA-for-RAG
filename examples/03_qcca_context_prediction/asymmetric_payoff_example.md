# QCCA Context Prediction & Asymmetric Payoff Example

## What this example demonstrates
This example illustrates the **asymmetry of evidence allocation payoffs**. When an allocator under-allocates and stops early, missing a critical bridge passage, the downstream answer suffers a catastrophic quality drop ($\Delta \text{F1} = -1.0$). In contrast, when an allocator over-allocates and includes unneeded passages, downstream quality suffers only a minor dilution penalty ($\Delta \text{F1} \approx -0.05$).

This asymmetry explains why balanced classifiers and cost-sensitive controllers in Week 4 and Week 5 heavily penalized false stops (`false_stop_pct`) relative to false expansions.

---

## Case A: Catastrophic Under-Allocation (False Stop)

### Query Information
**Question ID:** `2030`  
**Paper ID:** `695`  
**Question (verbatim):**
> What are the near-offensive language categories?

**Gold Answer:**
```json
["inappropriate, discriminating"]
```

### Context Comparison

#### 1. Under-Allocated Context ($k=2$, 526 tokens)
- **Included Passages:** Ranks 1 and 2.
- **Passage 1:** Abstract discussing transfer learning from LDA to BiLSTM-CNN for offensive language.
- **Passage 2:** Related work noting crowd-sourcing challenges in hate speech annotations.
- **Missing Information:** The specific sub-categories defining *"near-offensive"* language in the target corpus.
- **Generated Answer ($k=2$):**
  > *"hate speech, discrimination, abusive language, offensive language"*
- **Score:** **$\text{F1} = 0.0000$**

#### 2. Target Context ($k=4$, 1,071 tokens)
- **New Evidence Introduced (Rank 4):**
  > *"As introduced above, the 'One Million Post' corpus provides annotation labels for more than 11,000 user comments. Although not designed for offensive language detection, some categories are close to it, such as **inappropriate** and **discriminating**..."*
- **Generated Answer ($k=4$):**
  > **"inappropriate, discriminating"**
- **Score:** **$\text{F1} = 1.0000$** ($\Delta \text{F1} = +1.0000$)

---

## Case B: Mild Over-Allocation Penalty (False Expansion)

### Query Information
**Question ID:** `1002`  
**Paper ID:** `293`  
**Question:** *"How have the differences in communication styles between Twitter and Facebook increase the complexity of the problem?"*  
**Gold Answer:** `["Systems do not perform well both in Facebook and Twitter texts"]`

### Context Comparison
- **Target Context ($k=0$, 146 tokens):** Relying on query-latent compression, the model predicts:
  > *"Twitter has a more complex communication style than Facebook, as it allows for more direct interaction and real-time communication."*  
  > **Score:** **$\text{F1} = 0.2500$**
- **Over-Expanded Context ($k=2$, 671 tokens):** Adding two background passages, the model predicts:
  > *"The differences in communication styles between Twitter and Facebook increase the complexity of the problem by making it difficult to generalize the model across domains."*  
  > **Score:** **$\text{F1} = 0.2000$** ($\Delta \text{F1} = -0.0500$)

---

## The Asymmetric Payoff Principle
Comparing the two real cases:
$$\text{Cost of Under-Allocation (Missing Rank 4): } -1.0000 \text{ F1 (Total failure)}$$
$$\text{Cost of Over-Allocation (Adding 500 tokens): } -0.0500 \text{ F1 (Mild dilution)}$$

This per-query behavior mirrors the macro-level benchmark recorded across 12 models in Week 4/5:
- **Average gain from capturing necessary evidence:** $+0.3395$ F1
- **Average penalty from unnecessary expansion:** $-0.1345$ F1

Under-allocation risks omitting the decisive token sequence, leading to complete hallucination or irrelevance. Over-allocation merely dilutes context or introduces mild distractor noise.

---

## What this example does NOT prove
- This does not prove that adding passages never hurts severely; distractor passages can cause prompt confusion and catastrophic flips (as documented in LOO harmful analyses).
- It does not mean the optimal strategy is to always maximize context, since longer contexts incur linear inference latency and quadratic self-attention memory costs.

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Development Set ($N=231$)
- **Question IDs:** `2030` (Under-allocation) and `1002` (Over-expansion)
- **Method:** QCCA-V1 / SARA evaluated in Week 2 and Week 4
- **Original error analysis:** `results/week4/processed/qcca_error_cases.csv` (Row 1: `2030.0, 695.0, true_k=4, predicted_k=2, regret=1.0`)
- **Original benchmark artifact:** `results/week4/model_benchmark/error_analysis.csv`
- **Reconstructed:** NO (Copied from verbatim frozen records)

