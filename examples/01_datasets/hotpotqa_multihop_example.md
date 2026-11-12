# HotpotQA Multi-Hop Question Answering Example

## What this example demonstrates
This example illustrates why **multi-hop question answering** requires aggregating evidence across disjoint documents. Single-hop retrieval based purely on query similarity often retrieves only the first entity mention, failing to retrieve the bridge fact needed for the final answer.

---

## Query
**Query ID:** `5a7df25a5542990b8f503b02`  
**Question (verbatim):**
> What did the screewriter for a 2013 psychological thriller film directed by Denis Villeneuve get a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for?

---

## Gold Answer
```json
["Invader (Invasor)"]
```

---

## Candidate Evidence

### Candidate Source 1: The Bridge Entity (Film $\to$ Screenwriter)
**Document:** *Enemy (film)*  
**Unit ID:** `1cfe1b016bd2ab38348240b906b38375` (Rank 3 in SFR pool)  
**Text:**
> Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M.S. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel "The Double".

### Candidate Source 2: The Decisive Fact (Screenwriter $\to$ Goya Award)
**Document:** *Javier Gullón*  
**Unit ID:** `3cce4986f2a64a7b5645e808649eea5b` (Rank 2 in SFR pool)  
**Text:**
> He garnered a Canadian Screen Award nomination for Best Adapted Screenplay at the 2nd Canadian Screen Awards for "Enemy", and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for "Invader (Invasor)".

---

## Why this is Multi-Hop
To answer the question, a model must resolve a reasoning chain across two separate Wikipedia articles:
$$\text{Denis Villeneuve} \xrightarrow{\text{directed (2013)}} \text{Enemy} \xrightarrow{\text{screenwriter}} \text{Javier Gullón} \xrightarrow{\text{Goya Award nomination}} \textbf{Invader (Invasor)}$$

1. **Hop 1:** Identify that the 2013 psychological thriller directed by Denis Villeneuve is *Enemy*, and that its screenwriter is Javier Gullón.
2. **Hop 2:** Identify what work earned Javier Gullón a Best Adapted Screenplay nomination at the 27th Goya Awards (distinguishing it from his Canadian Screen Award nomination for *Enemy*).

If an allocator selects only Source 1, the reader hallucinates *"Enemy"* as the answer (as observed in BEA-V1's under-allocated output: *"received a Goya Award nomination... for the screenplay of 'Enemy'"*).

---

## What this example does NOT prove
- This example does not prove that all HotpotQA queries require two documents; single-document distractor queries also exist.
- It does not prove that multi-hop retrieval is impossible with bi-encoders, only that independent sentence scoring without context linkage risks dropping downstream bridge facts.

---

## Provenance
- **Dataset:** HotpotQA
- **Split/cohort:** Development Pilot ($N=50$)
- **Query ID:** `5a7df25a5542990b8f503b02`
- **Group ID:** `question:235c74b6db1108e1136692c1b036043aa87618748f1aeecd3614086c5360b651`
- **Method(s):** Evaluated under `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_QBGF_V1`, `BEA_V2_POSTHOC`, `MINILM_CE_SENTENCE`
- **Reader:** `Qwen/Qwen3-8B` (BASE_FP16)
- **Retriever:** `Salesforce/SFR-Embedding-Mistral`
- **Original input artifact:** `data/week11/hotpot_dev_distractor_v1.json`
- **Original selection artifact:** `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Anchor A05, Case C02/C05)
- **Original metric artifact:** `results/post_w12/final_case_study/ALIGNED_PER_QUERY.csv`
- **Reconstructed:** NO (Copied from verbatim frozen case-study records)

