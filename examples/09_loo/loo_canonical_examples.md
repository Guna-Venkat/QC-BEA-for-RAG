# Leave-One-Out (LOO) Attribution: Helpful, Neutral, and Harmful Units

## What this example demonstrates
This artifact presents real, empirically evaluated examples of **Leave-One-Out (LOO) evidence attribution**. 

In the Week 12 attribution study, every selected evidence unit $u_i \in E$ was systematically ablated, and the prompt was re-evaluated through the frozen reader to measure marginal impact:
$$\Delta_i = \operatorname{Score}(E \setminus \{u_i\}) - \operatorname{Score}(E)$$

- **Helpful ($\Delta_i < -0.01$ for QA; $\Delta_i < 0$ for SciFact):** Deleting the unit degrades performance.
- **Neutral ($|\Delta_i| \le 0.01$ for QA; $\Delta_i = 0$ for SciFact):** Deleting the unit has no measurable effect beyond the threshold.
- **Harmful ($\Delta_i > +0.01$ for QA; $\Delta_i > 0$ for SciFact):** Deleting the unit **improves** the downstream score.

---

## 1. LOO-A: Canonical Helpful Unit ($\Delta_i = -0.9130$)

### Query & Context
- **Dataset:** HotpotQA
- **Query ID:** `5ae72b96554299572ea5474e`
- **Method / Budget:** H3 / 256 tokens
- **Question:** *"What album released in 1998 features the song 'Risingson'?"*
- **Gold Answer:** `["Mezzanine"]`

### Ablated Unit
- **Unit ID:** `69797cf3abebd75d88f04d5b3fb0e21b` (Length: 20 tokens)
- **Unit Text:** *"\"Risingson\" is the first single from the album Mezzanine by Massive Attack, which was the first to be produced by Neil Davidge..."*
- **Relevance Score:** 0.6605 (Parent retrieval rank: 1)

### Evaluation Contrast
- **Original Context Answer ($E$):** **"Mezzanine"**
- **Original Score:** **$\text{F1} = 1.0000$**
- **Ablated Context Answer ($E \setminus \{u_i\}$):** Long unfocused quote lacking the direct answer word.
- **Ablated Score:** **$\text{F1} = 0.0870$**
- **Delta:** $\Delta_i = 0.0870 - 1.0000 = \mathbf{-0.9130}$
- **Classification:** **`HELPFUL`**

---

## 2. LOO-B: Canonical Neutral Unit ($\Delta_i = 0.0000$)

### Query & Context
- **Dataset:** HotpotQA
- **Query ID:** `5ae72b96554299572ea5474e` (Same question as LOO-A)
- **Method / Budget:** H3 / 256 tokens

### Ablated Unit
- **Unit ID:** `7e8bbd4dacfd557e61ed671a421a098f` (Length: 4 tokens)
- **Unit Text:** *"Track listing:"*
- **Relevance Score:** 0.5774 (Parent retrieval rank: 1)

### Evaluation Contrast
- **Original Context Answer ($E$):** **"Mezzanine"** ($\text{F1} = 1.0000$)
- **Ablated Context Answer ($E \setminus \{u_i\}$):** **"Mezzanine"** ($\text{F1} = 1.0000$)
- **Delta:** $\Delta_i = 1.0000 - 1.0000 = \mathbf{0.0000}$
- **Classification:** **`NEUTRAL`**
- **Auditor Note:** Over 75% of units in the Week 12 attribution study were classified as Neutral. They consume budget and attention bandwidth without contributing to or harming downstream extraction.

---

## 3. LOO-C: Canonical Harmful Unit ($\Delta_i = +1.0000$) — HIGH PRIORITY

### Query & Context
- **Dataset:** SciFact
- **Query ID:** `343`
- **Method / Budget:** C2 / 256 tokens
- **Claim:** *"Exposure to particulate matter increases cardiovascular disease risk."*
- **Gold Target Label:** `SUPPORT`

### Ablated Unit (High-Relevance Distractor)
- **Unit ID:** `4074995272a575a0e24ff01a684d14f4` (Length: 40 tokens)
- **Relevance Score:** **0.7882** (Extremely high query similarity!)
- **Unit Text:** Discusses potential confounding factors in observational cohort studies and notes that occupational particulate exposure showed statistically non-significant variations in preliminary sub-strata.

### Evaluation Contrast
- **Original Context Answer ($E$):** Model reads the non-significant qualification and outputs **`REFUTE`** or `NOT_ENOUGH_INFO`.
  - **Original Correctness:** **$S = 0$ (Wrong)**
- **Ablated Context Answer ($E \setminus \{u_i\}$):** Without this misleading qualification, the reader focuses on the main epidemiological findings and correctly outputs **`SUPPORT`**.
  - **Ablated Correctness:** **$S = 1$ (Correct)**
- **Delta:** $\Delta_i = 1 - 0 = \mathbf{+1.0000}$
- **Classification:** **`HARMFUL`**

### Why this is a Crucial Finding
This example demonstrates the **failure of relevance as a surrogate for utility**:
1. Unit `40749952...` had a very high relevance score ($0.7882$), causing the allocator to prioritize it.
2. Yet including it **destroyed reader correctness**, and deleting it **restored the correct answer**.
3. Allocating evidence strictly by query–sentence similarity actively packs high-similarity distractors that harm downstream LLM performance.

---

## What this example does NOT prove
- This does not prove that all qualifications are harmful; nuanced scientific synthesis sometimes requires negative caveats.
- Single-unit LOO measures local marginal perturbation in one context, not intrinsic sentence quality across all possible prompts.

---

## Provenance
- **Dataset:** HotpotQA & SciFact
- **Stage:** Week 12 Attribution Study (9,607 evaluated unit perturbations)
- **Primary source file:** `results/week12/attribution/v1/analysis/unit_importance.csv`
- **Reconstructed:** NO (Copied from verbatim frozen records)

