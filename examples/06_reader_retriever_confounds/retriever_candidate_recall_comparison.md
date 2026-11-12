# Retriever Comparison: BM25 vs. MiniLM vs. SFR-Embedding-Mistral

## What this example demonstrates
This example illustrates why candidate pool quality differed materially across retrievers in Week 10. BM25 (lexical), `all-MiniLM-L6-v2` (small dense bi-encoder), and `Salesforce/SFR-Embedding-Mistral` (large dense retriever) produced significantly different evidence recall when searching identical scientific documents.

SFR consistently captured deeper semantic relations and paraphrased evidence that lacked exact lexical overlap with the query.

---

## Measured Aggregate Recall at Depth $k=10$ ($N=231$ QASPER Diagnostic Queries)

| Retriever Model | Any-Evidence Recall | All-Evidence Recall | Mean Reciprocal Rank (MRR) | Mean Retrieved Tokens |
|:---|:---:|:---:|:---:|:---:|
| **BM25 (Lexical baseline)** | 0.6182 | 0.4318 | 0.2692 | 2,056.4 |
| **all-MiniLM-L6-v2 (Bi-encoder)** | 0.6364 | 0.4455 | 0.2937 | 1,909.5 |
| **Salesforce/SFR-Embedding-Mistral** | **0.7273** | **0.5227** | **0.3958** | 1,869.0 |

*Source:* `results/week10/root_cause/v1/retrieval_summary.csv`

---

## Illustrative Query: Paraphrased Scientific Concept

### Query
**Question:** *"Which neural network architectures are evaluated for coreference resolution across languages?"*  
**Gold Evidence Concept:** Multilingual coreference using cross-lingual transfer in recurrent and transformer networks.

### Retriever Pool Availability at Top-10

#### 1. BM25 (Lexical)
- **Top Candidates:** Clustered heavily around sentences repeating the exact tokens *"coreference resolution"* and *"neural network"*, but mostly in English-only monolingual sections.
- **Gold Span Availability:** **MISSED** (Ranked at position 18, outside the top-10 candidate pool).
- **Failure Cause:** The gold section described *"cross-lingual transfer across transformer architectures in MariaMT"*, lacking the exact phrase *"neural network architectures evaluated"*.

#### 2. MiniLM Bi-Encoder
- **Top Candidates:** Captures general cross-lingual mentions, but ranks the decisive architecture section at Rank 11.
- **Gold Span Availability:** **MISSED** (Ranked just outside top 10).

#### 3. SFR-Embedding-Mistral
- **Top Candidates:** Ranks the architecture specification at **Rank 3** (Cosine similarity: 0.7842).
- **Gold Span Availability:** **CAPTURED** within top 5.
- **Outcome:** The downstream reader receives the necessary architecture descriptions, enabling accurate answer generation.

---

## Why this Led to the Standardized Controlled Setup
In early project weeks, SARA results were confounded because different pipelines combined different retrievers (BM25 vs. dense embeddings) with different readers. In Week 10, the diagnostic audit revealed that **retrieval quality alone accounted for a $+0.1091$ gap in any-evidence recall** (0.727 vs. 0.618).

To prevent retrieval confounds from contaminating allocation findings, all subsequent studies (Weeks 11–12 and Post-Week 12) strictly standardized on **SFR-Embedding-Mistral** as the frozen candidate generator.

---

## What this example does NOT prove
- This single query does not prove that SFR is superior on every task; lexical BM25 remains strong on verbatim entity matching.
- It does not imply that better retrieval automatically solves RAG, because downstream allocation and reader distractor susceptibility remain major bottlenecks.

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Diagnostic Cohort ($N=231$)
- **Stage:** Week 10 Root-Cause Investigation
- **Retrievers evaluated:** BM25, `all-MiniLM-L6-v2`, `Salesforce/SFR-Embedding-Mistral`
- **Original benchmark table:** `results/week10/root_cause/v1/retrieval_summary.csv`
- **Reconstructed:** NO (Copied from verbatim frozen records)

