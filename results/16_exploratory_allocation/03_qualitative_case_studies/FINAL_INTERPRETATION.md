# Final retrospective interpretation

Retrospective, outcome-selected explanatory case studies, not confirmation or population failure frequencies. Gold annotations are diagnostic only and were not available to the allocator. No allocation, predictor, threshold or answer is changed. The BEA_V2 preregistered calibration remains CALIBRATION_FAILED_TERMINATED; the V2 answers come from the separately labelled post-hoc tau=8e-5 study.

## Full saved-cohort observations

**HotpotQA @256:** FIXED_SENTENCE: answer_f1=0.3661, tokens=254.8, parents=5.28, runs=6.54, threshold stops=0.0%, mapped-gold recall=0.833; QBGF_FULL: answer_f1=0.4042, tokens=251.6, parents=4.94, runs=5.46, threshold stops=0.0%, mapped-gold recall=0.808; BEA_QBGF_V1: answer_f1=0.2976, tokens=225.3, parents=9.66, runs=15.38, threshold stops=62.0%, mapped-gold recall=0.520; BEA_V2: answer_f1=0.4352, tokens=246.9, parents=4.98, runs=6.00, threshold stops=0.0%, mapped-gold recall=0.838.

**HotpotQA @1024:** FIXED_SENTENCE: answer_f1=0.3893, tokens=1001.7, parents=9.62, runs=13.18, threshold stops=0.0%, mapped-gold recall=0.983; QBGF_FULL: answer_f1=0.4020, tokens=995.3, parents=9.24, runs=10.34, threshold stops=0.0%, mapped-gold recall=0.983; BEA_QBGF_V1: answer_f1=0.3441, tokens=284.6, parents=9.72, runs=15.92, threshold stops=100.0%, mapped-gold recall=0.617; BEA_V2: answer_f1=0.4234, tokens=960.7, parents=9.50, runs=11.76, threshold stops=34.0%, mapped-gold recall=0.983.

**QASPER @256:** FIXED_SENTENCE: answer_f1=0.2668, tokens=255.1, parents=5.70, runs=7.94, threshold stops=0.0%, mapped-gold recall=0.050; QBGF_FULL: answer_f1=0.2641, tokens=252.5, parents=5.82, runs=8.24, threshold stops=0.0%, mapped-gold recall=0.001; BEA_QBGF_V1: answer_f1=0.1868, tokens=245.7, parents=8.78, runs=17.44, threshold stops=28.0%, mapped-gold recall=0.018; BEA_V2: answer_f1=0.2618, tokens=245.0, parents=5.28, runs=8.58, threshold stops=2.0%, mapped-gold recall=0.051.

**QASPER @1024:** FIXED_SENTENCE: answer_f1=0.2896, tokens=1023.2, parents=9.62, runs=19.84, threshold stops=0.0%, mapped-gold recall=0.130; QBGF_FULL: answer_f1=0.2964, tokens=1020.4, parents=8.56, runs=13.42, threshold stops=0.0%, mapped-gold recall=0.328; BEA_QBGF_V1: answer_f1=0.2084, tokens=472.8, parents=9.30, runs=22.96, threshold stops=96.0%, mapped-gold recall=0.029; BEA_V2: answer_f1=0.2904, tokens=1009.1, parents=8.14, runs=14.08, threshold stops=2.0%, mapped-gold recall=0.304.

**SciFact @256:** FIXED_SENTENCE: macro_f1=0.6289, tokens=252.6, parents=3.22, runs=5.02, threshold stops=0.0%, mapped-gold recall=0.656; QBGF_FULL: macro_f1=0.5310, tokens=250.6, parents=3.36, runs=4.52, threshold stops=0.0%, mapped-gold recall=0.403; BEA_QBGF_V1: macro_f1=0.6127, tokens=250.1, parents=8.16, runs=13.26, threshold stops=4.0%, mapped-gold recall=0.214; BEA_V2: macro_f1=0.5522, tokens=242.5, parents=4.02, runs=5.34, threshold stops=4.0%, mapped-gold recall=0.599.

**SciFact @1024:** FIXED_SENTENCE: macro_f1=0.5533, tokens=1020.7, parents=8.30, runs=15.36, threshold stops=0.0%, mapped-gold recall=0.895; QBGF_FULL: macro_f1=0.5881, tokens=1018.7, parents=7.02, runs=10.12, threshold stops=0.0%, mapped-gold recall=0.838; BEA_QBGF_V1: macro_f1=0.6432, tokens=696.0, parents=9.80, runs=22.72, threshold stops=90.0%, mapped-gold recall=0.420; BEA_V2: macro_f1=0.5772, tokens=171.7, parents=2.46, runs=3.26, threshold stops=98.0%, mapped-gold recall=0.565.

## Hypotheses kept separate

**QASPER @256:** Compare V1 versus V2/FIXED at matched exposure: source count, sentences per parent, adjacent-sentence rate, contiguous runs, exact support retention and discarded sentences. More parents alone does not demonstrate over-diversification, and low cosine redundancy alone does not prove an excessive penalty. The required missing rejected-candidate semantic terms may not have been saved.

**QASPER @1024:** Inspect threshold stopping, unused budget and annotated support absent from V1 but present in saved alternative contexts. This is a separate potential exposure mechanism, not the same claim as fragmentation @256. No alternative answer is generated after the V1 stopping point.

**HotpotQA:** Inspect V2-rescue dossiers for retention of two annotated support facts, bridge entities, and newly FULL-exposed neighboring sentences. Annotation overlap and a quality improvement do not isolate multi-hop causality.

**SciFact @256:** Maximum-disagreement ties prefer FIXED-only correct cases if present. Direct claim–sentence evidence should be checked against the exact predicted label and raw output.

**SciFact @1024:** Maximum-disagreement ties prefer V1-only correct cases if present. Compare stopped V2 context, retained V1 support and saved P_help terms; unavailable scores on omitted candidates are not manufactured. Low predicted usefulness for a known-correct reference is a hypothesis about utility calibration, not an observed causal usefulness label.

## Reviewed case evidence

No human-confirmed mechanism labels yet. Automatic patterns are candidate explanations, except explicit source-overlap/invalid-format observations. Complete MANUAL_REVIEW.csv after inspecting dossiers, then rerun this notebook to refresh the interpretation.

## Ten final questions

1. **What does FIXED do well?** It provides a simple query-ranked sentence policy. Identify its positive cells and cases in the quality/support tables; do not generalize its success across all datasets or budgets.

2. **What does QBGF add and where does it hurt?** Its saved per-parent fidelity choices show where whole-source context or multi-sentence states differ from FIXED. Quality differences and dilution/retention patterns are descriptive; fusion was not re-optimized here.

3. **What specifically caused BEA-V1’s major failures?** Causal attribution is not established by this analysis. Separate matched-exposure fragmentation @256 from threshold/exposure @1024 using exact case text and reviewed labels; retrieval misses remain upstream failures.

4. **What did P_help change in BEA-V2?** Inspect recovered underlying sentences, FULL transitions and saved selected P_help/IG/marginal values. The V1–V2 comparison also changes allocation/stopping, so a P_help-only causal contribution is not isolated.

5. **When does more context help?** Cases with better quality and recovered annotated/coherent context support a context-recovery association. They do not show that every added token helped; no new counterfactual/deletion generation is run.

6. **When does pruning help?** Inspect cases where a shorter saved context matches or exceeds a longer one, including near ties. This supports outcome preservation in those cases, not a universal shorter-context rule.

7. **When does redundancy reduction become harmful?** Only treat this as supported interpretation if exact discarded facts, saved semantic/penalty terms and reader outcomes jointly support it. Aggregate lower redundancy with lower quality is insufficient; most such flags remain hypotheses.

8. **Why is there no universal best allocator?** Compare task metrics separately across the six cells, strict budget reversals and case texts. Evidence needs, annotation sufficiency, packing and reader behavior can differ; mixed rankings do not identify a single cause.

9. **Which explanations are strongly supported by individual cases?** The reviewed-evidence list above records human-confirmed case interpretations with source/trace references. Exact context/source membership, measured quality and saved stopping events are directly observed. Human confirmation still does not turn an observational case into a causal intervention.

10. **Which explanations remain hypotheses?** Unreviewed mechanism candidates, excessive redundancy penalties without rejected-candidate terms, P_help miscalibration on unscored discarded candidates, and claims that FULL or multi-hop recovery alone caused an answer change remain hypotheses.

