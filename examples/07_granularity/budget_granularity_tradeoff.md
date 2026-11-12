# Evidence Granularity vs. Budget Tradeoff: 256 vs. 1024 Tokens

## What this example demonstrates
This benchmark illustrates why the **optimal evidence unit changes with available token budget**:
1. **Tight Budget (256 tokens):** Whole-passage allocation is heavily constrained by unit size ($~250$ tokens per passage). It consumes almost the entire budget on a single source, starving the prompt of multi-hop facts. Sentence-level selection extracts the highest-relevance sentences from multiple sources, boosting Answer F1 (+0.0838 advantage for sentences).
2. **Generous Budget (1024 tokens):** Whole-passage evidence becomes competitive and slightly surpasses sentence selection (+0.0082 advantage for passages). Having enough space to include complete passages preserves surrounding discourse context, pronouns, and narrative coherence, eliminating the fragmentation penalty of isolated sentences.

---

## Controlled Multi-Granularity Pilot Results (HotpotQA, $N=50$, SFR + Qwen3-8B)

| Evidence Granularity | Budget = 256 Tokens | Budget = 512 Tokens | Budget = 1024 Tokens |
|:---|:---:|:---:|:---:|
| **Whole Passage** | 0.3375 F1 (163.7 tokens) | **0.4563 F1** (389.1 tokens) | **0.4803 F1** (933.3 tokens) |
| **Fine-Grained Span** | 0.4079 F1 (193.5 tokens) | 0.4306 F1 (362.4 tokens) | 0.4755 F1 (941.2 tokens) |
| **Sentence Selection** | **0.4213 F1** (201.2 tokens) | 0.4203 F1 (398.2 tokens) | 0.4721 F1 (995.3 tokens) |

*Source:* `FINAL_PROJECT_MAIN/4_multigranular_evidence_study/results/1_primary/2_matched_reader_results.csv` and report Figure 1.

---

## Detailed Case Walkthrough: HotpotQA Query `5a7df25a5542990b8f503b02`

**Question:** *"What did the screewriter for a 2013 psychological thriller film directed by Denis Villeneuve get a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for?"*  
**Gold Target:** `["Invader (Invasor)"]`  
**Required Hops:** Source A (*Enemy* $\to$ screenwriter Javier Gullón) and Source B (*Javier Gullón* $\to$ 27th Goya Award for *Invader*).

---

### Condition 1: Budget = 256 Tokens (Sentence Dominance)

#### A. Whole-Passage Selection (Budget Exceeded after 1 Passage)
- **Selected Evidence:** Exactly 1 passage (Passage 1: *Enemy* film article, 238 serialized tokens).
- **Available Space Remaining:** 18 tokens (Cannot fit Passage 2, which requires 245 tokens).
- **Missing Information:** The article about Javier Gullón and his Goya Award nomination for *Invader*.
- **Generated Answer:** *"Enemy"* (Hallucinated work based on available context).
- **Score:** **$\text{F1} = 0.0000$**

#### B. Sentence-Level Selection (Cross-Document Distribution)
- **Selected Evidence:** 
  - Sentence 1 from Source A (32 tokens): *"Enemy is a 2013 psychological thriller film directed by Denis Villeneuve... written by Javier Gullón."*
  - Sentence 1 from Source B (41 tokens): *"He garnered a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for 'Invader (Invasor)'."*
- **Total Serialized Tokens:** 73 tokens (Well within the 256-token ceiling).
- **Generated Answer:** **"Invader (Invasor)"**
- **Score:** **$\text{F1} = 1.0000$**

---

### Condition 2: Budget = 1024 Tokens (Passage Recovery & Coherence)

#### A. Whole-Passage Selection
- **Selected Evidence:** Both complete passages from Source A and Source B (total 483 tokens).
- **Context Quality:** Retains full paragraphs, complete coreference links (*"he"* $\to$ *"Javier Gullón"*), and surrounding details about Canadian Screen Awards vs. Goya Awards.
- **Generated Answer:** **"Invader (Invasor)"**
- **Score:** **$\text{F1} = 1.0000$**
- **Macro Benefit:** Across the dataset, passages at 1024 tokens achieve **0.4803 F1 vs. 0.4721 F1** for sentences because complex reasoning questions frequently suffer from antecedent ambiguity when sentences are stripped of their parent paragraphs.

---

## Why this Led to the QBGF Formulation
The observation that **sentences win at low budgets while full passages win at high budgets** directly motivated the Multiple-Choice Knapsack design of QBGF. Rather than forcing a global choice between "all sentences" or "all passages," QBGF enables the allocator to dynamically select full passages when budget allows, and down-sample to top-1 or top-2 sentences when budget is constrained.

---

## What this example does NOT prove
- This does not prove that whole passages always beat sentences at 1024 tokens on all datasets; on SciFact, sentence-level extraction remains superior even at 1024 tokens because abstracts contain only 1–2 decisive claim-bearing sentences.
- It does not prove that fine spans are universally worse; spans performed well at 256 tokens but lacked sufficient context for complex QA.

---

## Provenance
- **Dataset:** HotpotQA
- **Split/cohort:** Development Pilot ($N=50$)
- **Query ID:** `5a7df25a5542990b8f503b02`
- **Reader:** `Qwen/Qwen3-8B` (BASE_FP16)
- **Retriever:** `Salesforce/SFR-Embedding-Mistral`
- **Original benchmark artifact:** `FINAL_PROJECT_MAIN/4_multigranular_evidence_study/results/1_primary/2_matched_reader_results.csv`
- **Original case reference:** `results/post_w12/final_case_study/FINAL_QUALITATIVE_CASE_STUDY_REPORT.md` (Anchor A05)
- **Reconstructed:** NO (Copied from verbatim frozen records)

