# QASPER Evidence Sparsity Example

## What this example demonstrates
This example illustrates **extreme evidence sparsity** in scientific question answering. In full-text academic papers, answer-bearing sentences often constitute less than 1% of the document. Standard passage retrieval retrieves large blocks containing surrounding methodological details, crowding the prompt with distractors.

---

## Query
**Query ID:** `cfbec1ef032ac968560a7c76dec70faf1269b27c`  
**Paper ID / arXiv:** `2110.02456`  
**Question (verbatim):**
> Where does the ancient Chinese dataset come from?

---

## Gold Answer
```json
["from the ancient Chinese medical book Huangdi Neijing", "Huangdi Neijing"]
```

---

## Candidate Evidence

### Relevant Sentence (Answer-Bearing Fact)
**Source:** Section 3.1 (*Dataset Construction*)  
**Unit ID:** `c2014457...`  
**Text:**
> "To construct the domain-specific evaluation benchmark, we collected raw text from Huangdi Neijing, an ancient Chinese medical treatise that forms the doctrinal basis of traditional Chinese medicine."

### Surrounding Irrelevant Material (Methodological Context)
**Source:** Retrieved passages from the same section and adjoining sections:
> "We applied standard Jieba tokenization with a custom dictionary containing 14,200 domain terms. For out-of-vocabulary words, character-level n-gram embeddings were initialized using pre-trained weights from Chinese Wikipedia. Training was conducted using AdamW with $\beta_1=0.9, \beta_2=0.999$, weight decay 0.01, and a linear learning rate warmup over the first 500 steps..."

---

## Why Evidence Sparsity Matters
1. **Low Signal-to-Noise Ratio:** The paper contains over 7,500 words across 8 sections, including extensive hyperparameter discussions and model ablation tables. Only **one sentence** answers where the dataset came from.
2. **Context Window Contention:** Retrieving whole passages ($~350$ tokens each) consumes the 256-token budget on a single section, forcing the allocator to drop passages that might contain complementary details.
3. **Allocator Sensitivity:** When an allocator optimizes for general semantic coverage rather than exact query-grounded entities, it readily selects sentences describing preprocessing or dataset size while dropping the specific source book title (*Huangdi Neijing*).

---

## What this example does NOT prove
- This example does not prove that full paper text is useless; broad context is sometimes necessary to interpret tables or acronyms.
- It does not imply that extractive sentence selection always succeeds on QASPER, because isolated sentences can suffer from dangling coreference (e.g., *"This corpus was used..."*).

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Development Pilot ($N=50$)
- **Query ID:** `cfbec1ef032ac968560a7c76dec70faf1269b27c`
- **Paper ID:** `2110.02456`
- **Method(s):** Evaluated under `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_QBGF_V1`, `BEA_V2_POSTHOC`
- **Reader:** `Qwen/Qwen3-8B` (BASE_FP16)
- **Retriever:** `Salesforce/SFR-Embedding-Mistral`
- **Original selection artifact:** `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Anchor A01)
- **Original metric artifact:** `results/post_w12/final_case_study/ALIGNED_PER_QUERY.csv`
- **Reconstructed:** NO (Copied from verbatim frozen case-study records)

