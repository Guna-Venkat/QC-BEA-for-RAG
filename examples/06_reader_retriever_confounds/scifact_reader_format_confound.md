# SciFact Output-Format Evaluation Confound: Qwen vs. Mistral vs. Llama

## What this example demonstrates
This example documents the critical **evaluation-interface confound** discovered during the Week 10–11 reader panel on SciFact. 

Under the frozen benchmark evaluation contract, models were required to produce **an exact label token (`SUPPORT`, `REFUTE`, or `NOT_ENOUGH_INFO`) with zero additional text**. Under this strict parser:
- **Mistral** produced **1,849 invalid outputs out of 1,850 conditions** (99.95% format violation rate).
- **Llama** produced **1,826 invalid outputs out of 1,850 conditions** (98.70% format violation rate).
- **Qwen** produced **0 invalid outputs out of 1,850 conditions** (0.00% format violation rate).

Because conversational models like Mistral and Llama appended reasoning explanations after the label, their outputs were scored as invalid (equivalent to zero accuracy), heavily confounding reader comparisons. This finding motivated selecting **Qwen/Qwen3-8B** as the controlled reader for all subsequent allocation and granularity studies.

---

## The Evaluated Claim & Evidence Context

**Claim ID:** `1132`  
**Claim:** *"TCR/CD3 microdomains are a required to induce the immunologic synapse to activate T cells."*  
**Gold Target Label:** `SUPPORT`  
**Context:** Abstract of PMID 33499189 describing TCR-CD3 recruitment in immunological synapse maturation.

---

## Frozen System Prompt Contract
```text
Given the following scientific evidence, determine whether the claim is SUPPORTED, 
REFUTED, or whether there is NOT_ENOUGH_INFO. 
Output exactly one word from [SUPPORT, REFUTE, NOT_ENOUGH_INFO].
Do not output explanations, markdown formatting, or punctuation.
```

---

## Raw Model Outputs and Parser Audit

### 1. Qwen/Qwen3-8B (BASE_FP16)
- **Raw Generated Text:**
  ```text
  SUPPORT
  ```
- **Strict Parser Result:** **`VALID`**
- **Scored Label:** `SUPPORT` (Match $\to$ Accuracy = 1.0)

---

### 2. Mistral-7B-Instruct-v0.2
- **Raw Generated Text:**
  ```text
  SUPPORT

  The provided study demonstrates that TCR-CD3 recruitment of Nck is critical 
  for maturation of the immunological synapse and T cell activation.
  ```
- **Strict Parser Result:** **`INVALID`** (Failed exact single-token contract; scored as 0.0)
- **Auditor Note:** The model correctly comprehended the claim and identified the exact supporting sentence, but its chat-tuning policy compelled it to provide a helpful justification.

---

### 3. Llama-3-8B-Instruct
- **Raw Generated Text:**
  ```text
  Based on the provided abstract, the correct classification is: SUPPORT.
  ```
- **Strict Parser Result:** **`INVALID`** (Prefix conversational formatting; scored as 0.0)
- **Auditor Note:** The classification itself was correct, but conversational framing violated the exact regex parser.

---

## Scientific Implication
1. **Never Claim Qwen "Reasons Better":** Mistral and Llama both correctly identified that the evidence supported the claim. Claiming that Qwen is intrinsically superior at biomedical claim reasoning is scientifically false and methodologically unsound.
2. **Standardizing the Reader:** Qwen was selected as the frozen primary reader not because it was an intrinsically superior reasoner, but because it adhered reliably to the strict evaluation contract, thereby removing interface compliance as a confounding variable in the evidence allocation experiments.

---

## What this example does NOT prove
- This does not prove that Mistral or Llama are incapable of format compliance under constrained sampling (e.g., regex-guided decoding via Outlines or Guidance); under unconstrained greedy decoding with frozen prompt strings, however, their conversational priors dominated.
- It does not mean Qwen is immune to reasoning errors; Qwen still made genuine classification errors on ambiguous scientific claims.

---

## Provenance
- **Dataset:** SciFact
- **Split/cohort:** Development Panel (150 queries across 37 conditions = 1,850 evaluations per model)
- **Stage:** Week 10 Diagnostic / Week 11 Memory Handoff Audit
- **Original audit file:** `results/week11/monitoring/memory_handoff_recovery.json` (`Mistral_SciFact_invalid_format: 1849`)
- **Original panel summary:** `results/week10/root_cause/v1/full_reader_panel_summary.csv`
- **Reconstructed:** NO (Copied from verbatim frozen records)

