# Case 2 — SciFact Claim 343: Harmful Evidence Under Leave-One-Out (LOO) Attribution

## Executive Summary & Scientific Significance
This case study documents a striking empirical manifestation of the **Relevance $\neq$ Utility Disconnect** discovered in the Week 12 Leave-One-Out (LOO) downstream utility attribution study. 

A sentence with high retrieval semantic relevance ($r = 0.7882$, retrieval rank 1) was allocated to the reader context. Its presence confused the reader into concluding that insufficient evidence existed (`NOT_ENOUGH_INFO`). When this exact high-scoring unit was ablated (deleted) without refilling the context, the reader immediately produced the correct gold verdict (`SUPPORT`), yielding a downstream utility gain of **$\Delta_{\text{LOO}} = +1.0000$** and categorizing the unit as **HARMFUL**.

---

## Benchmark & Query Metadata

- **Dataset:** SciFact (Scientific Claim Verification)
- **Claim ID:** `343`
- **Cluster / Group ID:** `cited-paper-component:342`
- **Claim Text (verbatim):**
  > `Diabetic patients with acute coronary syndrome experience increased short-term and long-term risk for bleeding events.`
- **Gold Label:** `SUPPORT`
- **Gold Evidence Document:** PMID `5884524` (Sentence 5)
- **Ablation Budget Condition:** Method `C2` (budget $B = 256$ tokens)
- **Controlled Reader:** Qwen2.5-7B-Instruct (greedy decoding, temperature=0)

---

## The Harmful Evidence Unit

- **Unit ID:** `4074995272a575a0e24ff01a684d14f4`
- **Granularity:** `SENTENCE`
- **Token Length:** 40 tokens
- **Dense Relevance Score:** 0.7882 (78.82% similarity to query)
- **Parent Retrieval Rank:** 1 (Parent similarity: 0.7763)
- **Parent Document PMID:** `7873737`
- **Parent Paper Title:** *Platelet glycoprotein IIb/IIIa inhibitors reduce mortality in diabetic patients with non-ST-segment-elevation acute coronary syndromes.*
- **Verbatim Sentence:**

> `Because this disease may be associated with increased platelet aggregation, we investigated whether diabetic patients with ACS derive particular benefit from platelet glycoprotein (GP) IIb/IIIa receptor inhibition.`

---

## Attribution & LOO Ablation Results

| Condition | Prompt Context State | Reader Output | Correctness | LOO Delta ($\Delta$) | Attribution Category |
|:---|:---|:---:|:---:|:---:|:---:|
| **Baseline (Pre-Ablation)** | Full 5-unit context (165 tokens) | `NOT_ENOUGH_INFO` | 0.0000 | Baseline | — |
| **Ablation (Post-Ablation)** | Unit `4074...` deleted (125 tokens) | `SUPPORT` | **1.0000** | **+1.0000** | **HARMFUL** |

- **Exact Flip:** `True`
- **Correctness Flip:** `True`
- **Importance Metric ($U - U_{-i}$):** $-1.0000$

---

## Full Selected Context Before Ablation (All 5 Units)

The reader received the following 5 sentences (total 165 evidence tokens) ordered by source document structure:

### Unit 0 (`7d0f52a27e3095df35939a83bbd474aa`)
- **Parent PMID:** `5884524` (*Impact of diabetes on long-term prognosis in patients with unstable angina...*)
- **Tokens:** 32 | **Relevance:** 0.7857 | **Category:** NEUTRAL
- **Verbatim Text:**
> `This is particularly true for patients with diabetes mellitus, who are known to have a high morbidity and mortality after an acute myocardial infarction.`

### Unit 1 (`f12f27f100e35b7c6a8cf2367654d2fe`)
- **Parent PMID:** `6158879` (*Greater clinical benefit of more intensive oral antiplatelet therapy with prasugrel...*)
- **Tokens:** 34 | **Relevance:** 0.8286 | **Category:** NEUTRAL
- **Verbatim Text:**
> `BACKGROUND Patients with diabetes mellitus (DM) are at high risk for recurrent cardiovascular events after acute coronary syndromes, in part because of increased platelet reactivity.`

### Unit 2 (`53cb9e3602fecf6e65070ba8e81b00a7`)
- **Parent PMID:** `7873737` (*Platelet glycoprotein IIb/IIIa inhibitors reduce mortality...*)
- **Tokens:** 21 | **Relevance:** 0.8268 | **Category:** NEUTRAL
- **Verbatim Text:**
> `BACKGROUND Diabetes mellitus is a major risk factor for adverse outcomes after acute coronary syndromes (ACS).`

### Unit 3 (`4074995272a575a0e24ff01a684d14f4`) — **[HARMFUL UNIT]**
- **Parent PMID:** `7873737` (*Platelet glycoprotein IIb/IIIa inhibitors reduce mortality...*)
- **Tokens:** 40 | **Relevance:** 0.7882 | **Category:** HARMFUL ($\Delta = +1.0$)
- **Verbatim Text:**
> `Because this disease may be associated with increased platelet aggregation, we investigated whether diabetic patients with ACS derive particular benefit from platelet glycoprotein (GP) IIb/IIIa receptor inhibition.`

### Unit 4 (`75d64b9c3614c0b8cce8471b3f72b41c`) — **[DECISIVE SUPPORT UNIT]**
- **Parent PMID:** `23783727` (*Ticagrelor vs. clopidogrel in patients with acute coronary syndromes and diabetes: a substudy from the PLATelet inhibition and patient Outcomes (PLATO) trial*)
- **Tokens:** 38 | **Relevance:** 0.8224 | **Category:** NEUTRAL under standard LOO (masked by distractor)
- **Verbatim Text:**
> `AIMS patients with diabetes mellitus (DM) have high platelet reactivity and are at increased risk of ischaemic events and bleeding post-acute coronary syndromes (ACS).`

---

## Detailed Causal Mechanism: Why Deleting Unit 3 Fixed the Error

1. **The Ground Truth Alignment:**
   - The claim asserts two core propositions: (a) *diabetic patients with ACS*, (b) *experience increased risk of bleeding events*.
   - Unit 4 explicitly and unequivocally confirms both: `"...patients with diabetes mellitus (DM) have high platelet reactivity and are at increased risk of ischaemic events and bleeding post-acute coronary syndromes (ACS)."`

2. **The Distraction Created by Unit 3:**
   - Unit 3 introduces a trial methodology statement focused on a specific drug mechanism: `"...investigated whether diabetic patients with ACS derive particular benefit from platelet glycoprotein (GP) IIb/IIIa receptor inhibition."`
   - Because Unit 3 immediately follows Unit 2 from the same paper (PMID 7873737), it establishes an unresolved research question about pharmaceutical trial efficacy.
   - The reader model (Qwen2.5-7B) perceived the combination of Units 0, 1, 2, and 3 as discussing clinical trials that *investigate* therapies rather than establishing proven outcomes. Given the absence of trial outcome numbers within Unit 3 itself, the reader conservatively defaulted to `NOT_ENOUGH_INFO`.

3. **The Unmasking Effect of Ablation:**
   - When Unit 3 is ablated, the prompt loses the distracting pharmaceutical trial hypothesis.
   - Unit 4 is brought into direct perceptual prominence. The reader directly evaluates Unit 4's factual assertion (*"at increased risk of ischaemic events and bleeding post-acute coronary syndromes"*) against the claim, outputting `SUPPORT` with 100% confidence.

---

## Methodological Takeaway for RAG & Allocation

1. **High Semantic Relevance Does Not Imply Positive Marginal Utility:** Unit 3 had a similarity of $0.7882$ to the claim, yet reduced downstream task accuracy from 100% to 0%. Allocators that rank purely by similarity risk packing prompts with coherent but disruptive distractors.
2. **Strict Preregistered Attribution Rule Applied:** In accordance with the preregistered LOO protocol, SciFact used a binary flip threshold ($\delta_{\text{SciFact}} = 0$) and the context was **not** refilled after deleting the unit. The improvement resulted strictly from removing destructive interference, not from filling the space with alternative text.

---

## Verifiable Source Artifacts
- LOO row record: `results/week12/attribution/v1/analysis/unit_importance.csv` (Row 2121: `SciFact,343,cited-paper-component:342,C2,256,4074995272a575a0e24ff01a684d14f4...`)
- Unit verbatim text and metadata: `results/post_w12/bea_v2/v1/utility_model/training_units.csv` (`unit_id: 4074995272a575a0e24ff01a684d14f4`)
- Claim and gold evidence: `data/week11/scifact/claims_dev.jsonl` (`id: 343`)
- Corpus paper abstracts: `data/week11/scifact/corpus.jsonl` (PMIDs `7873737`, `5884524`, `6158879`, `23783727`)
- Machine-readable case bundle: [02_scifact343_harmful_loo.json](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/02_scifact343_harmful_loo.json)

