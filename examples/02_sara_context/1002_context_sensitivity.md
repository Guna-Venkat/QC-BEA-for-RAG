# SARA Adaptive Context: Low-Context Query (k=0 Peak)

## What this example demonstrates
This example illustrates a query where **zero explicit context ($k=0$) achieves the highest downstream score**, outperforming larger allocations ($k=2, 4, 6, 8, 10$). Adding 2,400 explicit evidence tokens degrades generation quality due to distractor interference and verbosity, demonstrating why retrospective oracles select $k=0$ for 46.32% of queries.

---

## Query
**Question ID:** `1002`  
**Paper ID:** `293`  
**Question (verbatim):**
> How have the differences in communication styles between Twitter and Facebook increase the complexity of the problem?

---

## Gold Answer
```json
["Systems do not perform well both in Facebook and Twitter texts"]
```

---

## Candidate Passages & Retrieval Order
- **Rank 1:** `293_chunk_92b075a7-4be7-46b4-a3c4-56893abfb7e2` (BM25: 2.703) — General overview of social media aggression detection.
- **Rank 2:** `293_chunk_8f59e583-84ed-4876-81cf-b2d5f94040d8` (BM25: 2.571) — Discussion of domain adaptation between platforms.
- **Ranks 3–10:** Additional chunks describing data collection, preprocessing, and classifier baselines.

---

## Results by Explicit Context ($k$)

| $k$ (Explicit Passages) | Compressed Vectors ($n$) | Input Tokens | Answer F1 | Generated Answer (Verbatim) |
|:---:|:---:|:---:|:---:|:---|
| **$0$** | **10** | **146** | **0.2500** | *"Twitter has a more complex communication style than Facebook, as it allows for more direct interaction and real-time communication."* |
| $2$ | 8 | 671 | 0.2000 | *"The differences in communication styles between Twitter and Facebook increase the complexity of the problem by making it difficult to generalize the model across domains."* |
| $4$ | 6 | 1179 | 0.2000 | *"The differences in communication styles between Twitter and Facebook increase the complexity of the problem by making it difficult to generalize the model across domains."* |
| $5$ | 5 | 1450 | 0.2105 | *"The differences in communication styles between Twitter and Facebook increase the complexity of the problem by making it difficult to handle code-mixed data."* |
| $6$ | 4 | 1706 | 0.2105 | *"The differences in communication styles between Twitter and Facebook increase the complexity of the problem by making it difficult to handle code-mixed data."* |
| $8$ | 2 | 2200 | 0.2105 | *"The differences in communication styles between Twitter and Facebook increase the complexity of the problem by making it difficult to handle code-mixed data."* |
| $10$ | 0 | 2570 | 0.2000 | *"The differences in communication styles between Twitter and Facebook increase the complexity of the problem by making it difficult to handle code-mixed data and styles."* |

---

## Why this Motivated Query-Dependent Allocation
1. **$k=0$ Headroom:** At $k=0$, the model relies entirely on the query prompt and the 10 learned compressed latent vectors injected at `<COMPRESS>` token positions. It generates a concise 20-token response that overlaps with the gold reference better than the longer, diluted answers produced with explicit text.
2. **Context Dilution:** Supplying 10 full explicit passages ($2,570$ tokens) causes the reader to focus on technical jargon like *"code-mixed data and styles"*, reducing token F1 from $0.2500$ down to $0.2000$.
3. **Static Allocation Inefficiency:** Any static baseline ($k=8$ or $k=10$) wastes over 2,000 prompt tokens while returning a lower-quality answer.

---

## What this example does NOT prove
- This does not prove that latent compressed vectors always suffice; for queries requiring exact entity lists, $k=0$ fails completely (see Question 1001).
- It does not prove that $k=0$ is universally optimal for this paper; it is query-specific.

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Development Set ($N=231$)
- **Question ID:** `1002`
- **Paper ID:** `293`
- **Method:** SARA with `Mistral-7B-Instruct-v0.2` + learned latent projector
- **Original input artifact:** `results/week2/raw/dev_retrieval.jsonl`
- **Original execution artifact:** `results/week2/raw/dev_fixed_k_matrix.jsonl`
- **Original summary artifact:** `results/week2/processed/per_query_best_k.csv`
- **Reconstructed:** NO (Exact stored evaluation row from Week 2)

