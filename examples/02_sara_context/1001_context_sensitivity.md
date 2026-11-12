# SARA Adaptive Context: High-Context Query (k=6 Peak)

## What this example demonstrates
This example illustrates a query where **increasing explicit evidence materially improves downstream F1 from 0.1333 to 0.6000**. Compressed latent vectors alone are completely inadequate for recalling detailed lists of linguistic features, proving that certain information-seeking queries fundamentally require explicit textual evidence.

---

## Query
**Question ID:** `1001`  
**Paper ID:** `293`  
**Question (verbatim):**
> Which psycholinguistic and basic linguistic features are used?

---

## Gold Answer
```json
["Emotion Sensor Feature, Part of Speech, Punctuation, Sentiment Analysis, Empath, TF-IDF Emoticon features"]
```

---

## Candidate Passages & Retrieval Order
- **Ranks 1–5:** `293_chunk_...` — Passages covering dataset collection, task definitions, and broad methodology. None enumerate the full feature set.
- **Rank 6:** `293_chunk_b79370db...` — Section 4.2 (*Feature Engineering*): Explicitly lists Emotion Sensor features, Empath topical signals, POS tags, and punctuation statistics.
- **Ranks 7–10:** Classifier configuration, SVM hyperparameters, and test set evaluation tables.

---

## Results by Explicit Context ($k$)

| $k$ (Explicit Passages) | Compressed Vectors ($n$) | Input Tokens | Answer F1 | Generated Answer (Verbatim) |
|:---:|:---:|:---:|:---:|:---|
| $0$ | 10 | 141 | 0.1333 | *"No linguistic features are used."* (Complete hallucination) |
| $2$ | 8 | 506 | 0.1429 | *"NLP Features"* (Vague, uninformative) |
| $4$ | 6 | 1048 | 0.1429 | *"NLP Features"* |
| $5$ | 5 | 1217 | 0.1429 | *"NLP Features"* |
| **$6$** | **4** | **1447** | **0.6000** | **"Emotion Sensor Feature, Empath, Parts-of-speech tags, Punctuation features"** |
| $8$ | 2 | 1700 | 0.4167 | *"Emotion Sensor Dataset, Controlled Topical Signals from Empath, Emoticons, punctuation features, parts-of-speech tags"* |
| $10$ | 0 | 2013 | 0.3478 | *"Emotion Sensor Feature, Controlled Topical Signals from Empath, Normalized frequency of POS tags"* |

---

## Why this Motivated Query-Dependent Allocation
1. **Latent Representation Failure:** At $k=0$, the latent vectors fail to encode fine-grained named feature categories; the reader falsely claims *"No linguistic features are used."*
2. **Step-Function Payoff:** For $k \in \{0, 2, 4, 5\}$, the critical Rank 6 passage is omitted, yielding a flat $F1 \approx 0.14$. The moment $k$ expands to $6$, the answer captures the exact feature inventory, jumping $+0.4571$ F1.
3. **Contrast with Question 1002:** Both Question 1001 and Question 1002 originate from the **exact same paper** (Paper 293). Yet Question 1002 peaks at $k=0$ ($F1=0.250$), whereas Question 1001 requires $k=6$ ($F1=0.600$). A static context policy (e.g., fixed $k=8$) degrades both queries relative to their respective optima.

---

## What this example does NOT prove
- This does not prove that $k=6$ is a globally optimal stopping point across the dataset; other queries require $k=2, 4,$ or $10$.
- It does not prove that SARA's latent vectors are harmful, only that they cannot replace exact textual definitions of complex multi-element sets.

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Development Set ($N=231$)
- **Question ID:** `1001`
- **Paper ID:** `293`
- **Method:** SARA with `Mistral-7B-Instruct-v0.2` + learned latent projector
- **Original input artifact:** `results/week2/raw/dev_retrieval.jsonl`
- **Original execution artifact:** `results/week2/raw/dev_fixed_k_matrix.jsonl`
- **Original summary artifact:** `results/week2/processed/per_query_best_k.csv`
- **Reconstructed:** NO (Exact stored evaluation row from Week 2)

