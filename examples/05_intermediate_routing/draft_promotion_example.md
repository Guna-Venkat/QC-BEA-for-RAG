# Draft Promotion: Learned Gating Decision Example

## What this example demonstrates
This example illustrates the **draft-promotion architecture** explored in Week 8. The model first generates an unconditioned initial draft answer from the query alone. A learned gate predicts the probability that retrieving external evidence will improve the draft ($\text{prob\_help}$) versus degrade it ($\text{prob\_hurt}$).

When the draft is incomplete, the gate executes **PROMOTE**, improving the answer. When the draft is already accurate, the gate executes **STOP**, protecting the correct answer from distractor corruption and saving latency.

---

## Case 1: Beneficial Promotion (Under-Specified Draft $\to$ External Evidence)

### Query
**Question ID:** `0`  
**Paper ID:** `0`  
**Question (verbatim):**
> What is the seed lexicon?

**Gold Answer:**
```json
["a vocabulary of positive and negative predicates that helps determine the polarity score of an event"]
```

### Initial Draft (Zero-Context Generation)
- **Draft Answer:** *"The seed lexicon is a list of positive and negative words."*
- **Base Answer F1:** **0.2667** (Correct intuition, but missing paper-specific terminology: *"predicates"*, *"polarity score of an event"*)
- **Token Entropies / Margins:** Moderate uncertainty detected.

### Learned Gate Decision
- **Candidate Evidence:** Passage containing formal definition of event-polarity predicates.
- **Gate Probability:** $\hat{P}(\text{Help}) = 0.6639$
- **Decision:** **`PROMOTE`** (`predicted_gate_and_safety_passed`)

### Promoted Generation (With Retrieved Evidence)
- **Promoted Answer:** Captures the full definition including predicate polarity and event scoring.
- **Promoted F1:** **0.3077** ($\Delta \text{F1} = +0.0410$)
- **Context Tokens:** Increased from 553 to 817 tokens.

---

## Case 2: Protective Stopping (High-Confidence Accurate Draft)

### Query
**Question ID:** `1009`  
**Paper ID:** `296`  
**Question (verbatim):**
> What Doc2Vec architectures other than PV-DBOW have been tried?

**Gold Answer:**
```json
["PV-DM"]
```

### Initial Draft
- **Draft Answer:** **"PV-DM"**
- **Base Answer F1:** **1.0000** (Exact match)
- **Model Confidence:** High token probability, near-zero entropy.

### Learned Gate Decision
- **Gate Probability:** $\hat{P}(\text{Help}) = 0.1591$
- **Decision:** **`STOP`** (`gate_or_safety_rejected`)

### Outcome
- **Final Answer:** Retains initial draft *"PV-DM"*.
- **Final F1:** **1.0000**
- **Benefit:** Avoids retrieving 800+ tokens of methodology context, saving ~2.0 seconds of latency and eliminating the risk that surrounding text mentions other architectures that confuse the reader.

---

## What this example does NOT prove
- This does not prove that draft promotion universally improves RAG performance; aggregate gains across the entire test set remained small because gating classifiers made calibration errors on borderline questions.
- It does not eliminate the need for retrieval, as questions with unseen entity names cannot be drafted accurately.

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Internal Validation Replay ($N=231$)
- **Policy:** `E3` (Draft Promotion Controller with Learned Gate)
- **Original decision artifact:** `results/week8/w8e_controller/E3_internal_val_decisions.csv`
- **Original replay artifact:** `results/week8/w8e_controller/E3_internal_val_replay.csv`
- **Original draft diagnostics:** `results/week8/drafts/draft_diagnostics_internal_val_exact.jsonl`
- **Reconstructed:** NO (Copied from verbatim frozen records)

