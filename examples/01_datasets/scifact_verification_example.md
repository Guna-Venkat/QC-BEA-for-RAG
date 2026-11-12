# SciFact Scientific Claim Verification Example

## What this example demonstrates
This example illustrates the distinct structure of **scientific claim verification**. Unlike free-form or multi-hop question answering, claim verification requires assessing whether a retrieved abstract provides sufficient biomedical evidence to support or refute a synthetic claim, adhering to a strict categorical label contract.

---

## Claim
**Query ID:** `1132`  
**Claim (verbatim):**
> TCR/CD3 microdomains are a required to induce the immunologic synapse to activate T cells.

---

## Gold Label
```text
SUPPORT
```

---

## Relevant Evidence
**PMID:** `33499189`  
**Selected Unit ID:** `a81b51ded29bbba5ad8273f15e5d67aa` (Relevance: 0.7965)  
**Abstract Sentence (verbatim):**
> "Finally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation."

**Supporting Abstract Context:**
> "The conformational change is elicited by cooperative rearrangements of two TCR-CD3 complexes and does not require accompanying changes in the structure of the TCRalphabeta ectodomains. This conformational change at CD3 reverts upon ligand dissociation and is required for T cell activation."

---

## Exact Expected Output Format
The reader must output **exactly one label token** from the allowed vocabulary:
```text
SUPPORT
REFUTE
NOT_ENOUGH_INFO
```
Any additional conversational boilerplate (e.g., *"Based on the abstract, the claim is SUPPORTED"* or *"The label is: SUPPORT"*) is scored as **INVALID** under the frozen strict parser.

---

## Why Claim Verification Differs from Question Answering
1. **Decisive Semantic Modifiers:** A single word such as *"not"*, *"dispensable"*, or *"insufficient"* can invert the truth condition from `SUPPORT` to `REFUTE`.
2. **Conservative Null Hypothesis (`NOT_ENOUGH_INFO`):** If the retrieved sentences discuss T-cell activation in general but omit the specific role of the CD3 microdomain, the correct label is `NOT_ENOUGH_INFO`.
3. **Format Sensitivity:** As demonstrated in the Week 10 reader study, generative models without strict output constraints often default to explaining their reasoning, causing near-total parser failure despite sound comprehension.

---

## What this example does NOT prove
- This example does not prove that all claims can be verified from single sentences; some claims require synthesizing quantitative results across multiple sentences in an abstract.
- It does not prove that macro-F1 is identical to per-claim accuracy; macro-F1 is unweighted across the three classes and sensitive to class distribution imbalances.

---

## Provenance
- **Dataset:** SciFact
- **Split/cohort:** Development Pilot ($N=50$)
- **Query ID:** `1132`
- **Method(s):** Evaluated under `FIXED_SENTENCE`, `QBGF_FULL`, `BEA_QBGF_V1`, `BEA_V2_POSTHOC`, `MINILM_CE_SENTENCE`
- **Reader:** `Qwen/Qwen3-8B` (BASE_FP16)
- **Retriever:** `Salesforce/SFR-Embedding-Mistral`
- **Original input artifact:** `data/week11/scifact/claims_dev.jsonl`
- **Original selection artifact:** `results/week12/attribution/v1/analysis/qualitative_candidates.json` (Case C19)
- **Original metric artifact:** `results/week12/attribution/v1/analysis/unit_importance.csv`
- **Reconstructed:** NO (Copied from verbatim frozen records)

