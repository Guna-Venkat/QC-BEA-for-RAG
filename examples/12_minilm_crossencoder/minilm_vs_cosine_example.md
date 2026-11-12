# Cross-Encoder Reranking vs. Bi-Encoder / Passage Packing: The SciFact vs. HotpotQA Tradeoff

**Example ID:** `MINILM-01`  
**Dataset:** SciFact vs. HotpotQA  
**Focal Method:** `MINILM_CE_SENTENCE` (`ms-marco-MiniLM-L-6-v2` Cross-Encoder)  
**Compared Baselines:** `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_V2_POSTHOC`  
**Budgets Evaluated:** 256 and 1024 tokens  
**Source Evidence Files:**
- `FINAL_PROJECT_MAIN/9_minilm_reranker/results/1_primary/1_minilm_matched_quality_results.csv`
- `FINAL_PROJECT_MAIN/9_minilm_reranker/docs/reports/final_comparison.md`
- `FINAL_PROJECT_MAIN/9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py`

---

## 1. What This Example Demonstrates

This artifact documents why **MiniLM Cross-Encoder sentence reranking dominates on scientific claim verification (SciFact) while failing on multi-hop question answering (HotpotQA)**.

1. **Decisive Victory on SciFact:** MiniLM achieves the highest verification performance across all tested methods:
   - **SciFact 256:** **0.6855 macro-F1** (0.72 accuracy) vs. **0.6289** for `FIXED_SENTENCE` and **0.5310** for `QBGF_FULL`.
   - **SciFact 1024:** **0.6479 macro-F1** (0.70 accuracy) vs. **0.5533** for `FIXED_SENTENCE` and **0.5881** for `QBGF_FULL`.
2. **Defeat on HotpotQA:** The exact same cross-encoder underperforms simple static baselines on multi-hop QA:
   - **HotpotQA 256:** **0.3404 QA F1** vs. **0.3661** for `FIXED_SENTENCE` and **0.4042** for `QBGF_FULL`.
   - **HotpotQA 1024:** **0.3618 QA F1** vs. **0.3893** for `FIXED_SENTENCE` and **0.4020** for `QBGF_FULL`.
3. **The Architectural Asymmetry:**
   - **Verification is Single-Hop & Lexically Subtle:** SciFact requires identifying a single sentence that directly supports or refutes a scientific claim. The cross-encoder's joint self-attention over the `(claim, sentence)` pair accurately captures semantic negation, modal verbs, and subtle biological interactions that bi-encoder cosine similarity smears across embedding dimensions.
   - **QA Requires Multi-Hop Bridging:** HotpotQA requires chaining evidence across multiple documents. Crucially, **the second-hop bridge sentence often shares zero or minimal lexical/semantic overlap with the initial question**. Because the cross-encoder scores each candidate sentence independently against the question $q$, it scores second-hop sentences near the bottom, starving the reader of the connecting bridge. Passage-aware methods (`QBGF`, `FIXED_SENTENCE`) retain bridge sentences because they pack contiguous sentences from retrieved passages.

---

## 2. Macro Quality Comparison Across Matched Cohort

All evaluations conducted on the matched 50-query development cohort:

| Dataset | Budget | FIXED_SENTENCE | QBGF_FULL | BEA_QBGF_V1 | BEA_V2_POSTHOC | MINILM_CE_SENTENCE | Best Method |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **HotpotQA** | 256 | 0.3661 | 0.4042 | 0.2976 | **0.4352** | 0.3404 | **BEA-V2** |
| **HotpotQA** | 1024 | 0.3893 | 0.4020 | 0.3441 | **0.4234** | 0.3618 | **BEA-V2** |
| **QASPER** | 256 | **0.2668** | 0.2641 | 0.1868 | 0.2618 | 0.2641 | **FIXED** |
| **QASPER** | 1024 | 0.2896 | **0.2964** | 0.2084 | 0.2904 | 0.2827 | **QBGF** |
| **SciFact** | 256 | 0.6289 | 0.5310 | 0.6127 | 0.5522 | **0.6855** | **MINILM** |
| **SciFact** | 1024 | 0.5533 | 0.5881 | 0.6432 | 0.5772 | **0.6479** | **MINILM** |

*(HotpotQA and QASPER report token-level QA F1; SciFact reports 3-class macro-F1: SUPPORT / REFUTE / NOT_ENOUGH_INFO).*

---

## 3. Why MiniLM Wins on SciFact: Isolating the Decisive Pivot

In scientific claim verification, the candidate pool contains abstracts discussing the same disease, gene, or pathway. Dense bi-encoder embeddings (SFR-Embedding-Mistral or MiniLM bi-encoder) assign high cosine similarity to all sentences within the abstract because they share general domain vocabulary.

### The Problem with Cosine Ranking in SciFact:
Consider SciFact Claim 552:
> *"BCL-2 activation causes resistance to ABT-737."*

- **Distractor Sentence 1 (High Cosine Similarity):**  
  *"ABT-737 is a small-molecule BH3 mimetic that inhibits BCL-2 and BCL-XL, inducing apoptosis in various leukemia and lymphoma cell lines."*  
  $\to$ Contains "ABT-737", "BCL-2", "apoptosis". Cosine similarity with claim: **0.84**.
- **Target Refuting Sentence (Decisive):**  
  *"However, over-expression of MCL-1 or BFL-1, but not BCL-2, confers profound resistance to ABT-737-induced cell death."*  
  $\to$ Cosine similarity with claim: **0.78** (penalized by the introduction of "MCL-1", "BFL-1").

Under cosine-based sentence ranking, the distractor sentence is selected first. Under budget constraints, the decisive sentence may be pushed out or diluted by surrounding context.

### The Cross-Encoder Resolution:
The MiniLM cross-encoder computes full cross-attention over all token pairs in `[CLS] Claim [SEP] Sentence [SEP]`. It directly aligns `"causes resistance"` with `"not BCL-2, confers profound resistance"`. The cross-encoder score for the refuting sentence surges ahead of the background sentence, placing it at Rank 1. The reader receives the isolated refutation and correctly outputs `REFUTE` (**Macro-F1 = 1.0000**).

---

## 4. Why MiniLM Loses on HotpotQA: The Multi-Hop Bridging Trap

In multi-hop question answering, answering requires composing two disjoint facts:
1. $Hop_1: \text{Entity}_A \to \text{Entity}_B$ (connects question to bridge entity)
2. $Hop_2: \text{Entity}_B \to \text{Entity}_C$ (connects bridge entity to target answer)

### The Failure Mechanism:
Consider Anchor A05 (`5a7df25a5542990b8f503b02`):
- **Question:** *"What did the screewriter for a 2013 psychological thriller film directed by Denis Villeneuve get a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for?"*
- **Bridge Sentence ($S_{007}$, Hop 1):**  
  *"Enemy is a 2013 psychological thriller film directed by Denis Villeneuve... written by Javier Gullón..."*  
  $\to$ Shares words: *"Denis Villeneuve"*, *"2013"*, *"psychological thriller"*, *"film"*.  
  $\to$ MiniLM Cross-Encoder Score: **High (+4.82)**.
- **Decisive Award Sentence ($S_{005}$, Hop 2):**  
  *"He garnered a Canadian Screen Award nomination... and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for 'Invader (Invasor)'."*  
  $\to$ Shares words: *"Goya Award nomination"*, *"Best Adapted Screenplay"*, *"27th Goya Awards"*.  
  $\to$ Shares **ZERO** words with *"Denis Villeneuve"*, *"2013"*, *"psychological thriller"*, or *"Enemy"*.  
  $\to$ Evaluated in isolation against the full prompt question, its cross-attention is diluted by the ungrounded entity pronouns.  
  $\to$ MiniLM Cross-Encoder Score: **Lower (+2.15)**, ranked behind numerous distractor passages that repeat *"Goya Awards"* and *"screenplay"*.

Because MiniLM scores each sentence as an isolated candidate $(q, s)$, it fails to recognize that $S_{005}$ is crucial *conditional on* $S_{007}$ being present. 

In contrast:
- `FIXED_SENTENCE` selects sentences in passage order from the top retrieved passages, automatically capturing both sentences if the passage is retrieved.
- `BEA_V2` uses dynamic coverage update $\Delta \text{Cov}(S \cup \{s\})$, which detects that once $S_{007}$ is selected, $S_{005}$ provides high complementary utility.

---

## 5. Token Packing and Efficiency Ledger

From `FINAL_PROJECT_MAIN/9_minilm_reranker/docs/reports/final_comparison.md`:

| Dataset | Budget | Method | Mean Tokens Allocated | Budget Utilization | Mean Units Selected | Represented Parents |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **SciFact** | 256 | MINILM_CE_SENTENCE | 252.82 | 98.76% | 7.10 | 3.90 |
| **SciFact** | 256 | FIXED_SENTENCE | 252.62 | 98.68% | 6.56 | 3.22 |
| **SciFact** | 256 | QBGF_FULL | 250.56 | 97.88% | 8.50 | 3.36 |
| **HotpotQA** | 256 | MINILM_CE_SENTENCE | 254.86 | 99.55% | 10.54 | 6.46 |
| **HotpotQA** | 256 | FIXED_SENTENCE | 254.84 | 99.55% | 9.80 | 5.28 |
| **HotpotQA** | 256 | QBGF_FULL | 251.62 | 98.29% | 11.74 | 4.94 |

Notice that MiniLM distributes evidence across **more parent passages** on HotpotQA (6.46 parents vs. 4.94 for QBGF and 5.28 for FIXED). By fragmenting its budget across disconnected top-scoring sentences from 6.46 different documents, it breaks narrative continuity and loses the multi-hop chain.

---

## 6. What This Example Does NOT Prove

1. **Does NOT prove cross-encoders are inferior for QA in general:** If a cross-encoder were applied to full passages or iteratively updated with partial hypotheses (e.g. Iterative RAG), it could theoretically trace multi-hop chains. The failure is specific to **independent sentence scoring against the original unexpanded query**.
2. **Does NOT prove bi-encoder embeddings are superior:** Bi-encoder retrieval alone fails to discriminate subtle contradictions in SciFact. The highest quality on SciFact requires the full token-interaction cross-attention of the cross-encoder.

---

## 7. Provenance & Artifact Hashes

- **Model Identity:** `cross-encoder/ms-marco-MiniLM-L-6-v2` (max sequence length = 512, raw logits)
- **Reranker Implementation:** `FINAL_PROJECT_MAIN/9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py` (lines 30–82)
- **Evaluation Runner:** `FINAL_PROJECT_MAIN/9_minilm_reranker/code/2_reranker_experiment_runner.py`
- **Primary Results CSV:** `FINAL_PROJECT_MAIN/9_minilm_reranker/results/1_primary/1_minilm_matched_quality_results.csv`
- **Paired Statistics CSV:** `FINAL_PROJECT_MAIN/9_minilm_reranker/results/1_primary/3_minilm_paired_comparisons.csv`

