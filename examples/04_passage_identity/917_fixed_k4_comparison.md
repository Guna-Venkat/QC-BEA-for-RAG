# Passage Identity at Fixed Budget: k=4 Comparison

## What this example demonstrates
This example provides a controlled demonstration that **evidence identity matters independently of context quantity ($k$)**. Holding the candidate pool and token budget fixed at $k=4$ passages, changing *which* passages are exposed alters downstream answer F1 from 0.0 to 1.0.

Specifically, lexical BM25 retrieval places the decisive passage containing the language pair (*"English, German"*) at **Rank 8**. A standard prefix policy ($k=4$) truncates the list at Rank 4 and fails. A learned router identifies the utility of Rank 8, recovering the correct answer.

---

## Query
**Question ID:** `917`  
**Paper ID:** `266`  
**Question (verbatim):**
> What languages are seen in the news and TED datasets?

---

## Gold Answer
```json
["English, German"]
```

---

## Candidate Pool (Top 10 BM25 Retrieval)
All methods below select exactly 4 passages ($k=4$) from the identical candidate pool:

- **Rank 1:** `266_chunk_2226fcac...` — Variation in chain numbers between translations of TED talks and news.
- **Rank 2:** `266_chunk_256a5dde...` — Machine translation evaluation using BLEU and automated metrics.
- **Rank 3:** `266_chunk_5066b412...` — Error analysis across 10 defined coreference categories.
- **Rank 4:** `266_chunk_82bed694...` — Discussion of erroneous mentions and syntax types.
- **Rank 5:** `266_chunk_05e76fe2...` — Comparison of coreference chain features.
- **Rank 6:** `266_chunk_5651734c...` — Description of state-of-the-art transformer NMT architectures.
- **Rank 7:** `266_chunk_1caf17c1...` — System performance vs. coreference error counts.
- **Rank 8:** `266_chunk_f28e546d...` — **Section: Test data under analysis:** Explicitly defines the translation datasets and reports the English-to-German language direction for both TED talks and news.
- **Rank 9:** `266_chunk_ee20e5ec...` — Example German sentences from the Stasi corpus.
- **Rank 10:** `266_chunk_cd890417...` — Summary and conclusions.

---

## Router Comparison at Fixed $k=4$

| Policy | Selected Ranks | Context Tokens | Generated Answer | Token F1 | Exact Match |
|:---|:---:|:---:|:---|:---:|:---:|
| **R0: Retrieval Prefix** | `[1, 2, 3, 4]` | 826 | *"English"* (Missing German) | 0.0000 | 0.0000 |
| **R1: Semantic Cosine** | `[2, 3, 4, 5]` | 991 | *"English, Spanish"* (Hallucinated Spanish) | 0.5000 | 0.0000 |
| **R2: Learned Router** | `[1, 2, 6, 8]` | 945 | **"English, German"** | **1.0000** | **1.0000** |

---

## What Changed?
1. **Passage 8 Inclusion:** The decisive language pair definition resides in **Rank 8** (*Test data under analysis*). 
2. **Prefix Failure (R0):** By taking the top-4 lexical candidates (`[1, 2, 3, 4]`), R0 exposes passages that mention *"TED talks and news"* frequently (high BM25 term frequency) but omit the actual language names. The reader infers only *"English"*.
3. **Semantic Drift (R1):** Selecting the top-4 passages by query–passage embedding cosine (`[2, 3, 4, 5]`) clusters around abstract error terminology. The reader hallucinates *"Spanish"*.
4. **Learned Routing (R2):** The learned router predicts that Rank 8 provides high marginal value despite its lower initial lexical rank (BM25 rank 8), replacing Rank 3 and 4 with Rank 6 and 8. Exposing Rank 8 directly supplies *"German"*, resulting in a perfect $1.0$ F1 score.

---

## What this example does NOT prove
- This example does not prove that learned routers outperform prefix retrieval on every query; across all 231 queries, learned routing yielded a modest $+0.0084$ F1 average gain over prefix retrieval, which was not statistically significant after multiple-testing correction.
- It does not prove that Rank 8 is the *only* passage that could inform the answer; Rank 9 contains German text snippets that could also offer partial clues.

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Development Set ($N=231$)
- **Question ID:** `917`
- **Paper ID:** `266`
- **Budget:** Fixed $k=4$ passages
- **Retriever:** BM25 candidate pool
- **Reader:** SARA (`Mistral-7B-Instruct-v0.2` + learned latent projector)
- **Original routing assignments:** `results/week6/passage_routing/routing_predictions/dev_routing_assignments.csv`
- **Original generations:** `results/week6/passage_routing/sara_generations/dev_sara_generations.jsonl`
- **Original failure analysis:** `results/week6/passage_routing/tables/w6_failure_analysis.csv`
- **Reconstructed:** NO (Verbatim extraction from Week 6 experimental logs)

