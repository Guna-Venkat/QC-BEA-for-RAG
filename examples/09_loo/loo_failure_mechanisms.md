# Qualitative Failure Mechanisms: Redundancy, Distractors, and Fragmentation

## What this document demonstrates
This document provides concrete qualitative case profiles illustrating the three major evidence failure mechanisms identified during the post-freeze attribution and case-study audits:
1. **Redundancy:** Allocators pack multiple units repeating the same established fact, wasting budget that could have captured complementary hops.
2. **High-Similarity Distractor:** Evidence units exhibit high lexical or dense cosine similarity to the query but mislead the reader into an incorrect answer.
3. **Context Fragmentation / Lost Antecedent:** Extracted sentences look relevant in isolation but lose essential pronouns, subject bindings, or discourse context when separated from their parent paragraph.

*Note on status:* These mechanisms represent conservative qualitative interpretations of observed outcomes, not mathematically proven causal mechanisms.

---

## 1. Failure Mode A: Redundancy (Wasted Context Bandwidth)

### Case Reference
- **Dataset:** QASPER · **Query ID:** `cfbec1ef032ac968560a7c76dec70faf1269b27c` (Anchor A01)
- **Question:** *"Where does the ancient Chinese dataset come from?"*
- **Gold Answer:** `["from the ancient Chinese medical book Huangdi Neijing"]`

### Observed Allocation Behavior
Under `FIXED_SENTENCE`, the allocator selects 8 sentences from the top-retrieved documents. 
- Sentence 1: *"We evaluate our method on an ancient Chinese medical dataset."*
- Sentence 2: *"The ancient Chinese dataset was curated to benchmark domain adaptation."*
- Sentence 3: *"Text processing on the ancient Chinese corpus was performed with custom tools."*

### Qualitative Mechanism
All three sentences share high cosine similarity with the query because they contain the n-gram *"ancient Chinese dataset"*. However, none of them contain the actual book title (*Huangdi Neijing*). Packing three paraphrases of the same introductory fact consumed 95 tokens without adding any new factual information, leaving insufficient space to reach the section that named the source text.

---

## 2. Failure Mode B: High-Similarity Distractor (Negative Utility)

### Case Reference
- **Dataset:** SciFact · **Query ID:** `343` / `552` (LOO Harmful Unit)
- **Claim:** Exposure-related health outcome verification.

### Observed Allocation Behavior
- The retriever returns a candidate sentence containing almost every keyword in the claim with an SFR embedding similarity of **0.7882**.
- However, the sentence is from an introductory literature review section discussing an older, discredited hypothesis or noting that a specific sub-population had non-significant findings.
- When this sentence is presented to the reader alongside the actual findings, the reader hedges and flips its prediction from `SUPPORT` to `NOT_ENOUGH_INFO` or `REFUTE`.

### Qualitative Mechanism
The dense retriever scores query–sentence relevance purely based on semantic overlap. It cannot distinguish between a sentence asserting a finding versus a sentence citing an opposing viewpoint as background. By maximizing relevance density, the allocator prioritizes the distractor, directly harming accuracy.

---

## 3. Failure Mode C: Context Fragmentation / Lost Antecedents

### Case Reference
- **Dataset:** QASPER · **Query ID:** `869feb7f47606105005efdb6bea1c549824baea0` (Anchor A03)
- **Question:** *"Which 7 Indian languages do they experiment with?"*
- **Gold Answer:** `["Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati, Urdu"]`

### Observed Allocation Behavior
- **Sentence Allocator Action:** Extracted sentence:
  > *"These seven languages represent four distinct language families across the subcontinent."*
- **Parent Paragraph Context (Dropped):**
  > *"We select seven official Indian languages: Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati, and Urdu. These seven languages represent four distinct language families across the subcontinent."*

### Qualitative Mechanism
In isolation, the extracted sentence had high dense similarity to *"7 Indian languages"*. However, because the sentence used a demonstrative pronoun (*"These seven languages"*), the actual list of languages resided in the preceding sentence. By extracting sentences individually without discourse resolution, the allocator stripped away the referent, making it impossible for the reader to answer the question.

---

## Scientific Summary
These three failure modes demonstrate why naive relevance optimization is fundamentally limited:
- Optimizing relevance alone ignores **information redundancy** (Mode A).
- High relevance does not prevent **distractor interference** (Mode B).
- Isolated extractive units risk **syntactic and coreference breakage** (Mode C).

---

## Provenance
- **Dataset:** QASPER and SciFact development cohorts
- **Primary sources:**
  - `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Anchors A01, A03)
  - `results/week12/attribution/v1/analysis/unit_importance.csv`
  - `W12-POST/PILOT_ASPECT_MECHANISM_AUDIT.md`
- **Reconstructed:** NO (Synthesized from verbatim saved qualitative cases)

