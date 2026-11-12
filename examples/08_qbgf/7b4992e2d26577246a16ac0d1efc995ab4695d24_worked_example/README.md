# QBGF Worked Allocation Example: Query 7b4992e2d26577246a16ac0d1efc995ab4695d24

## Overview
This directory contains a complete, traceable worked example of the **Query-Conditioned Budget-Aware Evidence Allocation (QBGF)** Multiple-Choice Knapsack Problem (MCKP) solver under a 256-token budget on QASPER.

### Key Finding
QBGF alone allocates 4 sentences from candidate parent P01 (including the decisive reference sentence `S006`), reaching an Answer F1 of **0.8000**, while FIXED, BEA-V1, and BEA-V2 all fail (F1 = 0.0000) by allocating sentences from other passages or early stopping.

---

## Directory Contents
- `query.json`: Question text, gold reference answers, paper ID, and query ID.
- `candidate_passages.json`: The 10 retrieved candidate passages from the SFR candidate pool with relevance weights $R_i$.
- `option_table.csv`: The complete Multiple-Choice menu per passage: $\{\texttt{DROP}, \texttt{SENT\_1}, \texttt{SENT\_2}, \texttt{SENT\_4}, \texttt{SENT\_8}, \texttt{FULL}\}$, including exact token cost $c(i, o)$, utility $u(i, o)$, and knapsack selection indicator.
- `selected_evidence.txt`: The exact serialized evidence block passed to Qwen3-8B.
- `answer.txt`: The verbatim generated answer from Qwen3-8B and the resulting score.
- `provenance.json`: Hashes, source paths, and verification status.

---

## The Multiple-Choice Knapsack Formulation
For each retrieved passage $i \in \{1, \dots, K\}$:
1. **Passage Relevance Weight:**
   $$R_i = \operatorname{Softmax}(\tau_p \cdot s_{\text{pool}}(q, p_i)), \quad \tau_p = 5.0$$
2. **Sentence Relevance Mass within Passage:**
   $$\text{Mass}(i, \text{top-}k) = \sum_{j \in \text{top-}k} \operatorname{Softmax}(\tau_s \cdot s_{\text{sent}}(q, s_{i, j})), \quad \tau_s = 5.0$$
3. **Menu of Mutually Exclusive Representations:**
   $$o \in \{\texttt{DROP}, \texttt{SENT\_1}, \texttt{SENT\_2}, \texttt{SENT\_4}, \texttt{SENT\_8}, \texttt{FULL}\}$$
4. **Exact Serialized Cost:**
   $$c(i, o) = \left|\operatorname{Tok}(\operatorname{Serialize}(o))\right|$$
5. **Option Utility:**
   $$u(i, o) = R_i \cdot \text{Mass}(i, o)$$
6. **Optimization:**
   $$\max \sum_{i=1}^K \sum_{o \in \mathcal{O}_i} u(i, o) x_{i, o} \quad \text{s.t.} \quad \sum_{i=1}^K \sum_{o \in \mathcal{O}_i} c(i, o) x_{i, o} \le 256, \quad \sum_{o \in \mathcal{O}_i} x_{i, o} = 1, \quad x_{i, o} \in \{0, 1\}$$
   Solved exactly using integer dynamic programming (`solve()` in `5_qbgf/code/1_qbgf_and_sentence_allocator.py`).

