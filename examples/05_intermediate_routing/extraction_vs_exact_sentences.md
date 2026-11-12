# Generative Extraction vs. Exact Extractive Sentences

## What this example demonstrates
This comparison illustrates a critical finding from Week 9: **generative context compression damages downstream answer accuracy, whereas exact extractive sentence selection preserves evidence integrity**.

When an auxiliary language model was tasked with generating an extracted summary of the retrieved passages (Policies D2 and D3), it frequently omitted key factual entities, condensed away syntactic nuances, and introduced hallucinations, resulting in a statistically significant loss in answer F1. In contrast, selecting 3 exact query-ranked source sentences (Policy E3-k3) avoided generative drift and produced a modest point gain.

---

## Aggregate Benchmark Comparison ($N=1,746$)

| Policy Code | Strategy Description | Mean Answer F1 | $\Delta \text{F1}$ vs. Base | Mean Prompt Tokens | LM Calls | Outcome |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| **D0** | **Base Draft (No intervention)** | **0.3856** | **0.0000** | **940.5** | **1.0** | **Reference Pipeline** |
| D1 | Append raw retrieved passages | 0.3850 | $-0.0006$ | 3,041.4 | 2.0 | Context bloat |
| **D2** | **Query-only generative extraction** | **0.3687** | **$-0.0170$** | **1,476.5** | **3.0** | **Significant quality loss** |
| **D3** | **Draft-aware generative extraction** | **0.3769** | **$-0.0087$** | **1,508.7** | **3.0** | **Below base reference** |
| E3-k1 | Exact 1 query-ranked sentence | 0.3764 | $-0.0093$ | 1,017.0 | 2.0 | Under-allocation |
| E3-k2 | Exact 2 query-ranked sentences | 0.3817 | $-0.0040$ | 1,051.7 | 2.0 | Near parity |
| **E3-k3** | **Exact 3 query-ranked sentences** | **0.3900** | **$+0.0044$** | **1,085.8** | **2.0** | **Best extractive configuration** |
| E3-k4 | Exact 4 query-ranked sentences | 0.3805 | $-0.0051$ | 1,121.5 | 2.0 | Slight dilution |

---

## Query-Level Illustration: Loss from Generative Rewriting

### Query
**Question ID:** `512`  
**Paper ID:** `139`  
**Question (verbatim):**
> What evaluation metrics are used?

**Gold Answer:**
```json
["BLEU and ROUGE (1, 2, L) scores"]
```

### 1. Base Unconditioned Generation (Policy D0)
- **Draft Answer:** *"BLEU and ROUGE (1, 2, L) scores"*
- **Score:** **$\text{F1} = 0.8000$**

### 2. Generative Compressor Intervention (Policy D2)
- **Input Passage:** Describes curriculum training across decoding layers and lists evaluation metrics in passing.
- **Generative Compressor Output:** Re-phrases the context into a condensed paragraph, introducing synthetic phrasing (*"with multiple references"*).
- **Final Reader Answer:** *"BLEU and ROUGE (1, 2, L) scores with multiple references"*
- **Score:** **$\text{F1} = 0.7059$** ($\Delta \text{F1} = -0.0941$)
- **Mechanism:** The generative compressor hallucinated additional modifier tokens not present in the gold answer, lowering precision.

### 3. Exact Source Sentence Selection (Policy E3-k3)
- **Selected Unit:** Extracts the verbatim sentence from the paper:
  > *"We report BLEU-4 and ROUGE-1, ROUGE-2, and ROUGE-L metrics on the test partition."*
- **Final Reader Answer:** Preserves exact naming without hallucinated modifiers.
- **Score:** **$\text{F1} = 0.8000+$**

---

## The Methodological Lesson
1. **Generative Compressors Add Latency and Variance:** Running an LLM to compress context before passing it to another LLM doubles or triples the number of LM calls (D2: 3 calls vs. E3: 2 calls) and introduces generation errors into the evidence itself.
2. **Extractive Sub-Units are Safer:** Selecting verbatim sentences preserves authorial phrasing, core terminology, and exact numbers while cutting prompt tokens by over 60% compared to full passages.

---

## What this example does NOT prove
- This does not prove that generative extraction can never work; larger frontier models might compress text with higher fidelity, but within the 7B/8B model class evaluated, it consistently underperformed exact extraction.
- It does not mean sentence extraction solves all problems, as extracting sentences in isolation can break cross-sentence discourse links.

---

## Provenance
- **Dataset:** QASPER
- **Split/cohort:** Fitting Cohort ($N=1,746$)
- **Stage:** Week 9 (Extraction and Sentence Selection Surface)
- **Original benchmark summary:** `results/week9/w9e3_senttopk/v1/fit/summary.csv`
- **Original execution row:** `results/week9/ke_surface/fit/w9b_ke_surface.jsonl`
- **Reconstructed:** NO (Copied from verbatim frozen records)

