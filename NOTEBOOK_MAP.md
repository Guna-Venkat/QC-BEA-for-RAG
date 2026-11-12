# Notebook map

**Notebook bytes were not edited and no notebook was executed.** Full-run/install/download flags can already be True in saved snapshots. This inventory is for locating evidence, not permission to Run All. Freeze writers and saved analysis can also write artifacts.

## 1_problem_and_baselines

### [9_analysis.ipynb](1_problem_and_baselines/notebooks/9_analysis.ipynb)

**Purpose:**  Week 0: Dataset & RAG Evidence Understanding Study

 Adaptive Retrieval & Context Compression for Retrieval-Augmented Generation (SARA / QCCA)
Framework: SARA (ACL 2026) | Base Model: Mistral-7B-Instruct-v0.2 | Benchmark: QASPER

---

 Core Research Questions
1. Evidence Structure: How are evidence requirements distributed across scientific QA queries in QASPER?
2. Representation Evolution: How does Mistral contextualize the query against retrieved passages across transformer layers? Does it geometrically isolate true evidence from distractors

**Methods:** problem_and_baselines; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](1_problem_and_baselines/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

## 2_adaptive_evidence_quantity

### [9_dev_fixed_k_sweep.ipynb](2_adaptive_evidence_quantity/notebooks/9_dev_fixed_k_sweep.ipynb)

**Purpose:**  Week 2: Fixed-$k$ Development Baseline Response Surface & Oracle Analysis
Project: Query-Conditioned Evidence Allocation (QCCA)  
Parent Framework: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Benchmark: QASPER Development Set (231 questions across 86 papers)  
Hardware: NVIDIA TITAN RTX 24 GB  

---

 Scientific Objective
Week 2 establishes the empirical baseline quality/efficiency curve for static evidence allocation across:
$$k \in \{0, 2, 4, 5, 6, 8, 10\}$$
for all 231 development questions ($231 

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** RUN_SMOKE_TEST=False; RUN_STAGE_1=False; RUN_STAGE_2=False; RUN_STAGE_3=True.

### [9_oracle_target_analysis.ipynb](2_adaptive_evidence_quantity/notebooks/9_oracle_target_analysis.ipynb)

**Purpose:**  CS787 Generative AI Research Project — Week 3
 Oracle, Epsilon Target, Heterogeneity & Human Validation
Project: Query-Conditioned Context Allocator (QCCA) / SARA Framework  
Benchmark: QASPER Development Split (Paper-disjoint)  
Scientific Objective: Determine whether empirical query-level evidence requirements vary sufficiently across questions to justify learning a query-conditioned context allocator (QCCA).  
Guardrail: No QCCA training, no test set access, no expensive re-generation (100% frozen Week-2 data consumption).
  1. Environment 

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** RETROSPECTIVE_ORACLE.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_oracle_epsilon_human_audit.ipynb](2_adaptive_evidence_quantity/notebooks/9_oracle_epsilon_human_audit.ipynb)

**Purpose:**  CS787 Generative AI Research Project — Week 3
 Oracle, Epsilon Target, Heterogeneity & Human Validation
Project: Query-Conditioned Context Allocator (QCCA) / SARA Framework  
Benchmark: QASPER Development Split (Paper-disjoint)  
Scientific Objective: Determine whether empirical query-level evidence requirements vary sufficiently across questions to justify learning a query-conditioned context allocator (QCCA).  
Guardrail: No QCCA training, no test set access, no expensive re-generation (100% frozen Week-2 data consumption).
  1. Environment 

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** RETROSPECTIVE_ORACLE.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_qcca_v2_final_validation.ipynb](2_adaptive_evidence_quantity/notebooks/9_qcca_v2_final_validation.ipynb)

**Purpose:**  Week 4: Final Rigorous Validation of Stage-2 Selective Evidence Allocation (Policy C1)

Project: Query-Conditioned Context Allocator (QCCA) for Efficient Retrieval-Augmented Generation  
Parent Architecture: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Objective: Rigorous final empirical validation of Policy C1:
> "Can pre-generation retrieval/semantic/coverage features reliably identify when expanding evidence from $k=4$ to $k=6$ is useful, enabling near-static-$k=6/k=8$ answer quality at lower conte

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_model_benchmark.ipynb](2_adaptive_evidence_quantity/notebooks/9_model_benchmark.ipynb)

**Purpose:**  Week 5: Nonlinear Stage-2 ML Modeling Benchmark

Project: Query-Conditioned Context Allocator (QCCA) for Efficient Retrieval-Augmented Generation  
Parent Architecture: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Experiment: Week 5 Confirmatory Benchmark of Nonlinear Stage-2 Classifiers  
Evaluation Population: QASPER Development Split (86 papers, 231 questions)  
Governance: Strict Paper-Disjoint GroupKFold. Held-out test set remains 100% frozen & untouched.  

---

 Research Question:
> "Can a smal

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_feature_discovery.ipynb](2_adaptive_evidence_quantity/notebooks/9_feature_discovery.ipynb)

**Purpose:**  Week 4: Feature Discovery for Query-Conditioned Evidence Allocation (QCCA)
Project: CS787 Generative AI — Query-Conditioned Context Allocator  
Parent Framework: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Benchmark: QASPER Development Split (86 papers, 231 queries)  
Objective: Answer the fundamental scientific question:  
> What information available before generation correlates with how much textual evidence a query benefits from?

---
 Investigation Framing
The initial Week 4 experiment tested si

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_qcca_v2_modeling.ipynb](2_adaptive_evidence_quantity/notebooks/9_qcca_v2_modeling.ipynb)

**Purpose:**  Week 4: QCCA-V2 — Sequential Transition-Aware Evidence Allocation
Project: CS787 Generative AI — Query-Conditioned Context Allocator (QCCA)  
Parent Framework: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Benchmark: QASPER Development Split (86 papers, 231 queries)  
Core Hypothesis:  
> Can a lightweight sequential policy use pre-generation query/retrieval features to decide whether additional textual evidence is worth allocating at each stage, producing a better answer-quality/context-cost tradeoff 

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_qcca_v2_diagnostic.ipynb](2_adaptive_evidence_quantity/notebooks/9_qcca_v2_diagnostic.ipynb)

**Purpose:**  Week 4: QCCA-V2 Diagnostic and Policy-Refinement Study

Project: Query-Conditioned Context Allocator (QCCA) for Efficient Retrieval-Augmented Generation  
Parent Architecture: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Objective: Diagnose why the current learned sequential policy fails to convert discovered feature signal into a policy that clearly improves over static-k baselines, and determine what sequential policy structure is actually justified by the data.

 Strict Governance Controls:
1. Zero

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_qcca_development.ipynb](2_adaptive_evidence_quantity/notebooks/9_qcca_development.ipynb)

**Purpose:**  Week 4: Learning Query-Conditioned Evidence Allocation (QCCA)
Project: CS787 Generative AI — Query-Conditioned Context Allocator  
Parent Framework: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Benchmark: QASPER Development Split (Paper-disjoint from training)  
Evaluation Protocol: 5-Fold GroupKFold Cross-Validation by Paper ID (paper_id)  
Frozen Contract: Action space $\mathcal{K}_{\text{alloc}} = \{2, 4, 5, 6, 8\}$, Target tolerance $\epsilon^ = 0.01$

---
 Mode Configuration (Smoke Test vs Full C

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** RUN_SMOKE_TEST=False.

### [9_feature_validation.ipynb](2_adaptive_evidence_quantity/notebooks/9_feature_validation.ipynb)

**Purpose:**  Week 4-B: Feature Validation, Redundancy Analysis & Transition Modeling
Project: CS787 Generative AI — Query-Conditioned Context Allocator (QCCA)  
Parent Framework: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Benchmark: QASPER Development Split (86 papers, 231 queries)  
Objective: Statistically validate, reduce redundancy, and model transition-specific evidence requirements across the 64 pre-generation features discovered in Week 4-A.  

---
 CRITICAL EXPERIMENTAL GUARDRAILS & GOVERNANCE
- DO NOT B

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_encoder_adaptation.ipynb](2_adaptive_evidence_quantity/notebooks/9_encoder_adaptation.ipynb)

**Purpose:**  Week 5-C: Semantic Encoder Adaptation and Capacity Study

Project: Query-Conditioned Context Allocator (QCCA) for Efficient Retrieval-Augmented Generation  
Parent Architecture: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Experiment: Week 5-C Semantic Capacity and Encoder Adaptation Ladder (C0 Frozen, C1 Last-1 Layer, C2 Last-2 Layers)  
Population: QASPER TRAIN (2,088 queries) & DEV (231 queries)  
Governance: Strict Split Isolation. Held-out TEST set (1,309 queries) remains 100% frozen & untouched.

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_content_aware_allocator.ipynb](2_adaptive_evidence_quantity/notebooks/9_content_aware_allocator.ipynb)

**Purpose:**  Week 5: Content-Aware Adaptive Representation Allocation

Project: Query-Conditioned Context Allocator (QCCA) for Efficient Retrieval-Augmented Generation  
Parent Architecture: SARA — Selective and Adaptive Retrieval-augmented Generation with Context Compression  
Experiment: Week 5 Information Study & Formulation Comparison  
Population: QASPER TRAIN (2,088 queries) & DEV (231 queries)  
Governance: Strict Split Isolation. Held-out TEST set (1,309 queries) remains 100% frozen & untouched.  

---

 Core Research Question:
> "Does direct seman

**Methods:** adaptive_evidence_quantity; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](2_adaptive_evidence_quantity/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

## 3_evidence_identity_and_routing

### [9_hybrid_routing.ipynb](3_evidence_identity_and_routing/notebooks/9_hybrid_routing.ipynb)

**Purpose:**  Week 6-B: Hybrid Lexical-Semantic Passage Fidelity Routing

 Primary Research Question:
> Do lexical BM25 relevance and pretrained semantic relevance contain complementary routing information, such that combining them improves passage-fidelity routing beyond either signal alone?

In Week 6-A, we investigated passage fidelity routing and established that:
- $R_1$ (Pretrained Semantic Top-$k$ via zero-shot bi-encoder) significantly outperforms the standard $R_0$ BM25 prefix baseline at $k=4$ ($F_1 = 0.3913$ vs $0.3596$, $+3.17$ points) while sav

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_passage_fidelity_routing.ipynb](3_evidence_identity_and_routing/notebooks/9_passage_fidelity_routing.ipynb)

**Purpose:**  Week 6 — Query-Conditioned Passage Fidelity Routing

 Scientific Research Question
> At a fixed high-fidelity representation budget $k$, can we improve SARA by choosing WHICH retrieved passages remain in full text instead of automatically keeping the first $k$ BM25-ranked passages?

---

 Context & Transition from Weeks 3–5
- Weeks 3–5 asked: HOW MANY passages should remain in high fidelity? (Adaptive budget $k \in \{2, 4, 5, 6, 8\}$).
- Week 6 asks: WHICH passages deserve high fidelity at a fixed budget?
$$\boxed{\text{Hold } k \text{ fixed a

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** RUN_SUBSET_ORACLE=False; RUN_SUBSET_ORACLE=True.

### [9_budget_semantic_composition.ipynb](3_evidence_identity_and_routing/notebooks/9_budget_semantic_composition.ipynb)

**Purpose:**  Week 7-A: Modular Composition of Adaptive Budget Allocation and Semantic Passage Routing

 Primary Research Question:
> Can the existing adaptive budget allocator be directly combined with semantic passage routing, without retraining the allocator, to improve the quality–context frontier?

 The Critical Experimental Comparison:
$$\boxed{\hat{k}_{\text{W4}} + \text{BM25-prefix routing } (R_0) \quad\text{vs}\quad \hat{k}_{\text{W4}} + \text{semantic top-}\hat{k}\text{ routing } (R_1)}$$

 Experimental Framework & Boundaries:
1. Modular Compositi

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_week7c3_anchor_and_deviate_policy.ipynb](3_evidence_identity_and_routing/notebooks/9_week7c3_anchor_and_deviate_policy.ipynb)

**Purpose:**  Week 7-C3: Anchor-and-Deviate Semantic Budget Policy

 Section 0 — Research Question & Motivation
In Week 7-C1, the sufficiency-classification policy failed due to catastrophic large-$k$ fallback behavior ($F_1 = 0.3783$, context $\approx 1503.8$).
In Week 7-C2, direct response-surface regression and ranking recovered quality ($F_1 = 0.3922$) but massively over-allocated ($k=7.39$, tokens $\approx 1622.1$, dominated by static $k=6$ and $k=8$).

Error taxonomy analysis revealed that $63.6\%$ of queries were epsilon-admissible but over-budget, a

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_retrieval_aware_semantic_allocator.ipynb](3_evidence_identity_and_routing/notebooks/9_retrieval_aware_semantic_allocator.ipynb)

**Purpose:**  Week 7-C: Retrieval-Aware Semantic Sufficiency Allocation

 1. Scientific Motivation & The W7-B Failure Diagnosis

In Week 7-B, we established two critical findings:
1. Under semantic passage routing, the per-query quality-vs-budget response surface changes dramatically compared to lexical BM25 prefix routing:
   - For 49.8% of DEV queries, the $\epsilon$-optimal representation budget shifts.
   - The semantic $\epsilon$-oracle achieves $F_1 = 0.4869$ at mean $k = 3.30$ and context = 775.2 tokens (55.38% context reduction vs static $k=8$).
2. 

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_multifidelity_representation.ipynb](3_evidence_identity_and_routing/notebooks/9_multifidelity_representation.ipynb)

**Purpose:**  Week 7-E: Multi-Fidelity Evidence Representation — FULL / MEDIUM / HEAVY
Query-Conditioned Extractive Textual Compression for Marginal Passages in SARA

---

 Executive Scientific Overview
In Weeks 7-A through 7-D, we explored learned discrete adaptive allocation:
$$\text{Query } q, \text{Passages } \{D_i\} \longrightarrow k^ \in \{2, 4, 5, 6, 8\}$$
Across all architectures—modular composition (W7-A), semantic budget relearning (W7-B), rich-feature sufficiency classification (W7-C1), direct response surface regression (W7-C2), anchor-and-devia

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_semantic_budget_relearning.ipynb](3_evidence_identity_and_routing/notebooks/9_semantic_budget_relearning.ipynb)

**Purpose:**  Week 7-B: Semantic-Routing-Aware Budget Response Surface and Adaptive Allocation

 Primary Research Question
> How does semantic passage routing change the per-query quality-vs-budget response surface, and can a budget allocator learn this new regime?

 Scientific Context & Motivation from Week 7-A
In Week 7-A, we composed the frozen Week 4 adaptive budget allocator with Week 6 R1 semantic passage routing:
 W4 Adaptive + BM25 Prefix: $F_1 = 0.3842$, $1114.2$ tokens (mean $k = 4.82$)
 W4 Adaptive + Semantic Top-$k$: $F_1 = 0.3782$, $1095.0$ tok

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_cross_encoder_fidelity_router.ipynb](3_evidence_identity_and_routing/notebooks/9_cross_encoder_fidelity_router.ipynb)

**Purpose:**  Week 7-D: Generator-Aligned Cross-Encoder Fidelity Router
Joint Query-Document Representation Learning for Downstream SARA Utility Allocation

---

 Scientific Motivation & Historical Progression
All previous adaptive-budget models suffered from representation bottlenecks:
 W7-A: Frozen W4 allocator + semantic routing composition $\to$ modular composition failed.
 W7-B: Semantic-routing response surface + old W4 features $\to$ feature mismatch.
 W7-C1: Rich retrieval sufficiency classifier $\to$ over-allocation from large-$k$ fallback.
 W7-C2:

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

### [9_week7c2_utility_aware_budget_ranking.ipynb](3_evidence_identity_and_routing/notebooks/9_week7c2_utility_aware_budget_ranking.ipynb)

**Purpose:**  Week 7-C2: Utility-Aware Budget Ranking and Continuation Policy

 1. Why W7-C1 Failed: The Non-Monotonicity and Fallback Trap

In Week 7-C1, we attempted to formulate representation budget selection as candidate-level binary sufficiency classification:
$$P(z(q,k)=1) \ge 	au, \quad 	ext{fallback: } k=8$$

This produced a disappointing DEV result:
- $F_1 = 0.3783$ at mean $k = 6.85$ and context $\approx 1503.8$ tokens.
- Heavily dominated by static semantic $k=4$ ($F_1 = 0.3909$, tokens $\approx 921.1$).

 The Two Root Causes of W7-C1's Failure:

**Methods:** evidence_identity_and_routing; **datasets:** QASPER historical surface; **budgets:** Historical k/action surface; not automatically256/1024.

**Inputs:** Method-local configs and original source/cached response surface referenced in cells. **Outputs:** [results](3_evidence_identity_and_routing/results).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** DEVELOPMENT_OR_MOTIVATION.

**Saved switches:** No recognized literal boolean switch; inspect source cells.

## 4_multigranular_evidence_study

### [9_granularity_budget.ipynb](4_multigranular_evidence_study/notebooks/9_granularity_budget.ipynb)

**Purpose:**  Week 11 — C: granularity budget

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

  Execute or resume

Synthetic output is stored only under smoke/. Pending token-compressor conditions 

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True.

### [9_compressor_reader.ipynb](4_multigranular_evidence_study/notebooks/9_compressor_reader.ipynb)

**Purpose:**  Week 11 — E: compressor reader

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

  Execute or resume

Synthetic output is stored only under smoke/. Pending token-compressor conditions a

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True.

### [9_setup_and_data.ipynb](4_multigranular_evidence_study/notebooks/9_setup_and_data.ipynb)

**Purpose:**  Week 11 — 0: setup

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

Before full setup, prepare HotpotQA/SciFact once with sara_env/bin/python scripts/week11/prepare_datasets.py --downl

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True.

### [9_retriever_robustness.ipynb](4_multigranular_evidence_study/notebooks/9_retriever_robustness.ipynb)

**Purpose:**  Week 11 — F: retriever robustness

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

Full F refuses to execute until finalist_run_ids and their manually reviewed configurations are suppl

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True.

### [9_oracle_and_interactions.ipynb](4_multigranular_evidence_study/notebooks/9_oracle_and_interactions.ipynb)

**Purpose:**  Week 11 — H: oracle

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

  Execute or resume

Synthetic output is stored only under smoke/. Pending token-compressor conditions are reported

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=False.

### [9_master.ipynb](4_multigranular_evidence_study/notebooks/9_master.ipynb)

**Purpose:**  Week 11 MASTER — read-only dashboard

This notebook never starts generation or dataset/model downloads.  Exact manual execution order  Dataset, cache and result availability

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=False.

### [9_hierarchical_fidelity.ipynb](4_multigranular_evidence_study/notebooks/9_hierarchical_fidelity.ipynb)

**Purpose:**  Week 11 — G: hierarchical

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

  Execute or resume

Synthetic output is stored only under smoke/. Pending token-compressor conditions are re

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=True; RUN_FULL=False.

### [9_retrieval_granularity.ipynb](4_multigranular_evidence_study/notebooks/9_retrieval_granularity.ipynb)

**Purpose:**  Week 11 — A: retrieval

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

  Execute or resume

Synthetic output is stored only under smoke/. Pending token-compressor conditions are repor

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True.

### [9_passage_representation.ipynb](4_multigranular_evidence_study/notebooks/9_passage_representation.ipynb)

**Purpose:**  Week 11 — B: passage representation

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

  Execute or resume

Synthetic output is stored only under smoke/. Pending token-compressor conditi

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True.

### [9_reader_granularity.ipynb](4_multigranular_evidence_study/notebooks/9_reader_granularity.ipynb)

**Purpose:**  Week 11 — D: reader granularity

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

  Execute or resume

Synthetic output is stored only under smoke/. Pending token-compressor conditions 

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True.

### [9_final_report.ipynb](4_multigranular_evidence_study/notebooks/9_final_report.ipynb)

**Purpose:**  Week 11 — I: final report

SAFE BY DEFAULT. Run All loads saved real results if present; otherwise it uses fabricated smoke fixtures (H/I read saved results only). No datasets/models are downloaded automatically. QASPER TEST is blocked.

For a user full run: set RUN_FULL=True and RUN_SMOKE=False in the next cell. Every later setup is derived automatically. Existing validated rows are reused. OVERWRITE=True is deliberately unsupported.

  Execute or resume

Synthetic output is stored only under smoke/. Pending token-compressor conditions are re

**Methods:** multigranular_evidence_study; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** Registered W11 action grid (see configs).

**Inputs:** 4_multigranular_evidence_study/configs/1_base.yaml; 4_multigranular_evidence_study/configs/1_runs.yaml. **Outputs:** [1_multigranular_budget_results.csv](4_multigranular_evidence_study/results/1_primary/1_multigranular_budget_results.csv).

**Execution:** Primarily saved-result analysis; may write plots/reports. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=False.

## 5_qbgf

### [9_protocol_and_split_audit.ipynb](5_qbgf/notebooks/9_protocol_and_split_audit.ipynb)

**Purpose:**  Week12 0 — protocol and split audit

Run All is safe by default: synthetic smoke or read-only metadata. Full work requires changing the FLAGS cell yourself. The agent has not enabled full runs. Completed checksummed rows resume automatically; a changed scientific identity fails instead of overwriting. QASPER TEST and all Week13 confirmation outcomes are blocked.

W12-C uses the full frozen VALIDATION split. The historical W11 pilot is hypothesis generation only. W12-I freezes the reviewed method; Week13 is the future locked evaluation. No outc

**Methods:** qbgf; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json. **Outputs:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv); [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=True; RUN_FULL=False; RUN_REAL_MODEL_SMOKE=False; RUN_CANONICAL_SMOKE=False; ALLOW_LLMLINGUA_DOWNLOAD=False; RUN_LLMLINGUA_SMOKE=True; RUN_LLMLINGUA_FULL=False; RUN_TINY_LORA_SMOKE=True; RUN_FULL_LORA_TRAIN=False.

### [1_qbgf_algorithm.ipynb](5_qbgf/notebooks/1_qbgf_algorithm.ipynb)

**Purpose:**  Week12 A — qbgf algorithm

Run All is safe by default: synthetic smoke or read-only metadata. Full work requires changing the FLAGS cell yourself. The agent has not enabled full runs. Completed checksummed rows resume automatically; a changed scientific identity fails instead of overwriting. QASPER TEST and all Week13 confirmation outcomes are blocked.

W12-C uses the full frozen VALIDATION split. The historical W11 pilot is hypothesis generation only. W12-I freezes the reviewed method; Week13 is the future locked evaluation. No outcome from r

**Methods:** qbgf; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json. **Outputs:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv); [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=True; RUN_FULL=False; RUN_REAL_MODEL_SMOKE=True; RUN_CANONICAL_SMOKE=False; ALLOW_LLMLINGUA_DOWNLOAD=False; RUN_LLMLINGUA_SMOKE=True; RUN_LLMLINGUA_FULL=False; RUN_TINY_LORA_SMOKE=True; RUN_FULL_LORA_TRAIN=False.

### [2_baseline_qualification.ipynb](5_qbgf/notebooks/2_baseline_qualification.ipynb)

**Purpose:**  Week12 B — baseline qualification

Run All is safe by default: synthetic smoke or read-only metadata. Full work requires changing the FLAGS cell yourself. The agent has not enabled full runs. Completed checksummed rows resume automatically; a changed scientific identity fails instead of overwriting. QASPER TEST and all Week13 confirmation outcomes are blocked.

W12-C uses the full frozen VALIDATION split. The historical W11 pilot is hypothesis generation only. W12-I freezes the reviewed method; Week13 is the future locked evaluation. No outcom

**Methods:** qbgf; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json. **Outputs:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv); [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=True; RUN_FULL=False; RUN_REAL_MODEL_SMOKE=False; RUN_CANONICAL_SMOKE=True; ALLOW_LLMLINGUA_DOWNLOAD=False; RUN_LLMLINGUA_SMOKE=True; RUN_LLMLINGUA_FULL=False; RUN_TINY_LORA_SMOKE=True; RUN_FULL_LORA_TRAIN=False.

### [4_budget_matched_baseline_extension.ipynb](5_qbgf/notebooks/4_budget_matched_baseline_extension.ipynb)

**Purpose:**  W12 C-EXT — missing passage RAG and SARA references

Run after frozen C finishes. No change to C, splits, retrieval pins, QBGF or confirmation IDs. Budget-matched BM25/SFR RAW_SKIP passage RAG (BM25_RAG_RAW_SKIP_256/1024, SFR_RAG_RAW_SKIP_256/1024) uses the C RAW_SKIP allocator, BASE_FP16 Qwen prompt/parser/decoding and 256/1024 evidence-token budgets. SARA references use canonical adapted Mistral k5/n10 and are not budget- or reader-matched; they appear separately. Historical SFR-SARA k6 is reference-only. SFR-SARA k5 is optional until a real

**Methods:** qbgf; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json. **Outputs:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv); [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_C_EXT_FULL=True; RUN_SYNTHETIC_SMOKE=True; RUN_SPECIALIST_QUALIFICATION=False; RUN_CANONICAL_BM25_SARA=True; RUN_SFR_SARA=True.

### [3_qbgf_validation_surface.ipynb](5_qbgf/notebooks/3_qbgf_validation_surface.ipynb)

**Purpose:**  Week12 C — validation surface

Run All is safe by default: synthetic smoke or read-only metadata. Full work requires changing the FLAGS cell yourself. The agent has not enabled full runs. Completed checksummed rows resume automatically; a changed scientific identity fails instead of overwriting. QASPER TEST and all Week13 confirmation outcomes are blocked.

W12-C uses the full frozen VALIDATION split. The historical W11 pilot is hypothesis generation only. W12-I freezes the reviewed method; Week13 is the future locked evaluation. No outcome fr

**Methods:** qbgf; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json. **Outputs:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv); [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True; RUN_REAL_MODEL_SMOKE=False; RUN_CANONICAL_SMOKE=False; ALLOW_LLMLINGUA_DOWNLOAD=False; RUN_LLMLINGUA_SMOKE=True; RUN_LLMLINGUA_FULL=False; RUN_TINY_LORA_SMOKE=True; RUN_FULL_LORA_TRAIN=False.

### [5_qbgf_query_and_fusion_ablations.ipynb](5_qbgf/notebooks/5_qbgf_query_and_fusion_ablations.ipynb)

**Purpose:**  Week12 D — qbgf ablations

Run All is safe by default: synthetic smoke or read-only metadata. Full work requires changing the FLAGS cell yourself. The agent has not enabled full runs. Completed checksummed rows resume automatically; a changed scientific identity fails instead of overwriting. QASPER TEST and all Week13 confirmation outcomes are blocked.

W12-C uses the full frozen VALIDATION split. The historical W11 pilot is hypothesis generation only. W12-I freezes the reviewed method; Week13 is the future locked evaluation. No outcome from r

**Methods:** qbgf; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json. **Outputs:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv); [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True; RUN_REAL_MODEL_SMOKE=False; RUN_CANONICAL_SMOKE=False; ALLOW_LLMLINGUA_DOWNLOAD=False; RUN_LLMLINGUA_SMOKE=False; RUN_LLMLINGUA_FULL=False; RUN_TINY_LORA_SMOKE=False; RUN_FULL_LORA_TRAIN=False.

### [6_qbgf_validation_analysis.ipynb](5_qbgf/notebooks/6_qbgf_validation_analysis.ipynb)

**Purpose:**  Week12 H — validation analysis

Run All is safe by default: synthetic smoke or read-only metadata. Full work requires changing the FLAGS cell yourself. The agent has not enabled full runs. Completed checksummed rows resume automatically; a changed scientific identity fails instead of overwriting. QASPER TEST and all Week13 confirmation outcomes are blocked.

W12-C uses the full frozen VALIDATION split. The historical W11 pilot is hypothesis generation only. W12-I freezes the reviewed method; Week13 is the future locked evaluation. No outcome f

**Methods:** qbgf; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json. **Outputs:** [1_qbgf_validation_and_ablation_summary.csv](5_qbgf/results/1_primary/1_qbgf_validation_and_ablation_summary.csv); [1_validation_and_query_conditioning_paired_tests.csv](5_qbgf/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv); [2_sentence_and_passage_fusion_paired_tests.csv](5_qbgf/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv).

**Execution:** Saved-table analysis; may write analysis outputs; not read-only. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True; RUN_REAL_MODEL_SMOKE=False; RUN_CANONICAL_SMOKE=False; ALLOW_LLMLINGUA_DOWNLOAD=False; RUN_LLMLINGUA_SMOKE=True; RUN_LLMLINGUA_FULL=False; RUN_TINY_LORA_SMOKE=True; RUN_FULL_LORA_TRAIN=False.

### [7_final_policy_freeze.ipynb](5_qbgf/notebooks/7_final_policy_freeze.ipynb)

**Purpose:**  Week12 I — week13 freeze

Run All is safe by default: synthetic smoke or read-only metadata. Full work requires changing the FLAGS cell yourself. The agent has not enabled full runs. Completed checksummed rows resume automatically; a changed scientific identity fails instead of overwriting. QASPER TEST and all Week13 confirmation outcomes are blocked.

W12-C uses the full frozen VALIDATION split. The historical W11 pilot is hypothesis generation only. W12-I freezes the reviewed method; Week13 is the future locked evaluation. No outcome from re

**Methods:** qbgf; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json. **Outputs:** [1_fixed_sentence_final_policy_freeze.json](5_qbgf/results/4_frozen_decision/1_fixed_sentence_final_policy_freeze.json).

**Execution:** Saved decision/freeze writer; not model generation. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=False.

### [8_reserved_confirmation.ipynb](5_qbgf/notebooks/8_reserved_confirmation.ipynb)

**Purpose:**  Week12 M — final untouched confirmation

Metadata-only by default. J/K/L attribution cannot change this frozen experiment. No real confirmation smoke is permitted. Run All safely performs readiness checks only until you explicitly unlock the full run.

Frozen: SFR top-10 → five BASE_FP16 Qwen systems; budgets 256/1024. Final method remains FIXED_SENTENCE. QASPER confirmation is empty; historical TEST stays closed.  Readiness — metadata only

Verifies both byte-identical Part I freezes, split and source identities, exact membership/counts, regi

**Methods:** qbgf; **datasets:** HotpotQA200; SciFact50; QASPER0; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; 5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json; 5_qbgf/results/4_frozen_decision/1_fixed_sentence_final_policy_freeze.json. **Outputs:** [1_frozen_system_confirmation_results.csv](5_qbgf/results/5_reserved_confirmation/1_frozen_system_confirmation_results.csv); [2_confirmation_paired_tests.csv](5_qbgf/results/5_reserved_confirmation/2_confirmation_paired_tests.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_PREFLIGHT=True; RUN_SMOKE=False; RUN_FULL=True; ALLOW_CONFIRMATION_LABEL_ACCESS=True; RUN_CONFIRMATION_ANALYSIS=True.

## 6_downstream_utility_attribution

### [9_attribution_setup.ipynb](6_downstream_utility_attribution/notebooks/9_attribution_setup.ipynb)

**Purpose:**  Week12 Attribution setup — frozen 150-query diagnostic

VALIDATION ONLY. No confirmation/TEST access. Default Run All uses clearly labelled synthetic fixtures. Real cached setup is allowed in J; real perturbations require explicit RUN_FULL in K. L reads saved results. Evidence attribution means context-dependent input ablation, not internal-model explanation. Optional attention/replacement/third-system studies remain disabled.

Order: H saved analysis → J (RUN_SMOKE=False, cached preparation) → K (RUN_FULL=True, real perturbations) → L (RUN_SM

**Methods:** downstream_utility_attribution; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; Frozen VAL selected source units/perturbation identities. **Outputs:** [2_helpful_neutral_harmful_summary.csv](6_downstream_utility_attribution/results/1_primary/2_helpful_neutral_harmful_summary.csv); [1_relevance_downstream_utility_correlations.csv](6_downstream_utility_attribution/results/3_statistics/1_relevance_downstream_utility_correlations.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** POST_FREEZE_DIAGNOSTIC.

**Saved switches:** RUN_SMOKE=True; RUN_FULL=True.

### [9_causal_evidence_ablation.ipynb](6_downstream_utility_attribution/notebooks/9_causal_evidence_ablation.ipynb)

**Purpose:**  Week12 Causal evidence ablation — manually enabled generation

VALIDATION ONLY. No confirmation/TEST access. Default Run All uses clearly labelled synthetic fixtures. Real cached setup is allowed in J; real perturbations require explicit RUN_FULL in K. L reads saved results. Evidence attribution means context-dependent input ablation, not internal-model explanation. Optional attention/replacement/third-system studies remain disabled.

Order: H saved analysis → J (RUN_SMOKE=False, cached preparation) → K (RUN_FULL=True, real perturbations) → L 

**Methods:** downstream_utility_attribution; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; Frozen VAL selected source units/perturbation identities. **Outputs:** [2_helpful_neutral_harmful_summary.csv](6_downstream_utility_attribution/results/1_primary/2_helpful_neutral_harmful_summary.csv); [1_relevance_downstream_utility_correlations.csv](6_downstream_utility_attribution/results/3_statistics/1_relevance_downstream_utility_correlations.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** VALIDATION_OR_PROTOCOL.

**Saved switches:** RUN_SMOKE=False; RUN_FULL=True.

### [9_attribution_analysis.ipynb](6_downstream_utility_attribution/notebooks/9_attribution_analysis.ipynb)

**Purpose:**  Week12 Attribution analysis — retrospective sensitivity, not internal reasoning

VALIDATION ONLY. No confirmation/TEST access. Default Run All uses clearly labelled synthetic fixtures. Real cached setup is allowed in J; real perturbations require explicit RUN_FULL in K. L reads saved results. Evidence attribution means context-dependent input ablation, not internal-model explanation. Optional attention/replacement/third-system studies remain disabled.

Order: H saved analysis → J (RUN_SMOKE=False, cached preparation) → K (RUN_FULL=True, real p

**Methods:** downstream_utility_attribution; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 5_qbgf/configs/1_protocol.yaml; Frozen VAL selected source units/perturbation identities. **Outputs:** [2_helpful_neutral_harmful_summary.csv](6_downstream_utility_attribution/results/1_primary/2_helpful_neutral_harmful_summary.csv); [1_relevance_downstream_utility_correlations.csv](6_downstream_utility_attribution/results/3_statistics/1_relevance_downstream_utility_correlations.csv).

**Execution:** Primarily saved-result analysis; may write plots/reports. **Status:** POST_FREEZE_DIAGNOSTIC.

**Saved switches:** RUN_SMOKE=True; RUN_FULL=False.

## 7_bea_v1

### [1_bea_v1_exploratory_pipeline.ipynb](7_bea_v1/notebooks/1_bea_v1_exploratory_pipeline.ipynb)

**Purpose:**  W12-POST — BEA-QBGF exploratory VAL pilot
Run All: tests → nine-query allocation-only calibration → final freeze → missing pilot rows. Calibration failure blocks generation.

Frozen Week12 remains SFR top-10 → FIXED_SENTENCE → Qwen3-8B BASE_FP16. This is a separate exploratory mechanism, not confirmation or a replacement final method.

Use the sara_env kernel. Wait until POST-W9/other GPU work finishes. The original 150 K/L VAL examples × 2 budgets × 3 methods yield 900 logical rows; absent caches can require up to 900 answer generations plus S

**Methods:** bea_v1; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 7_bea_v1/configs/1_config.json; 7_bea_v1/results/4_diagnostics/pilot_cohort.json. **Outputs:** [1_bea_v1_pilot_quality_results.csv](7_bea_v1/results/1_primary/1_bea_v1_pilot_quality_results.csv); [1_bea_v1_expanded_quality_results.csv](7_bea_v1/results/2_expanded/1_bea_v1_expanded_quality_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** POST_W12_EXPLORATORY.

**Saved switches:** RUN_PILOT=True; AUTO_RUN_MISSING=True; RUN_EXPANDED=False; RUN_ATTRIBUTION=False; RUN_TESTS=True; RUN_EXPANDED=True; RUN_ATTRIBUTION=True.

## 8_bea_v2

### [1_bea_v2_phelp_and_calibration.ipynb](8_bea_v2/notebooks/1_bea_v2_phelp_and_calibration.ipynb)

**Purpose:** BEA_V2 calibration terminated. The single final resolution sweep at 6e-5, 7e-5, 8e-5, 9e-5 found no globally qualifying threshold. The notebook stops before attribution audit, training, calibration or reader execution. See bea_v2_resolution_report.md. No pilot should be run.
  BEA_V2 — cross-fitted downstream-utility-aware allocation

POST_W12_EXPLORATORY_BEA_V2. This reused development cohort is NOT fresh validation. Run All audits exact historical labels, runs CPU tests, trains CPU cross-fit models, reports held-out diagnostics, calibrates on

**Methods:** bea_v2; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 8_bea_v2/configs/1_bea_v2_config.json; 8_bea_v2/results/1_phelp_model/protocol/training_sources.json; 8_bea_v2/results/1_phelp_model/protocol/crossfit_folds.json. **Outputs:** [1_group_crossfit_predictor_metrics.csv](8_bea_v2/results/1_phelp_model/1_group_crossfit_predictor_metrics.csv); [3_calibration_failed_terminated.json](8_bea_v2/results/2_calibration_failed/3_calibration_failed_terminated.json).

**Execution:** Training/calibration/reader capable in source; terminal failure guard stops original study. **Status:** POST_W12_EXPLORATORY.

**Saved switches:** RUN_PILOT=True; RUN_UNSEEN_EXPANSION=True; RUN_NEW_ATTRIBUTION=False; AUTO_RUN_MISSING=True; RUN_MISSING=True.

### [2_bea_v2_posthoc_tau8e5.ipynb](8_bea_v2/notebooks/2_bea_v2_posthoc_tau8e5.ipynb)

**Purpose:**  BEA_V2 — post-hoc exploratory engineering evaluation

POST_W12_BEA_V2_POSTHOC_EXPLORATORY

This is a post-hoc exploratory evaluation at a manually selected engineering operating point (tau_stop=8e-5) after the preregistered BEA_V2 calibration failed. It cannot be interpreted as confirmation or as evidence that the original calibration protocol succeeded.

The original terminated notebook and records stay unchanged. This is a separate notebook and output namespace. No search, refitting or expansion. Same 50 development queries per dataset, four

**Methods:** bea_v2; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 8_bea_v2/configs/1_bea_v2_config.json; 8_bea_v2/results/1_phelp_model/protocol/training_sources.json; 8_bea_v2/results/1_phelp_model/protocol/crossfit_folds.json; 8_bea_v2/configs/1_bea_v2_posthoc_config.json. **Outputs:** [1_bea_v2_posthoc_quality_results.csv](8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** POST_HOC_EXPLORATORY.

**Saved switches:** RUN_PREFLIGHT=True; RUN_FULL=True; AUTO_RUN_MISSING=True; ALLOW_MISSING_CONTROL_RESTORE=False.

## 9_minilm_reranker

### [1_minilm_baseline_comparison.ipynb](9_minilm_reranker/notebooks/1_minilm_baseline_comparison.ipynb)

**Purpose:**  MiniLM Cross-Encoder Sentence Reranker — final POST-W12 baseline

POST_W12_RERANKER_BASELINE_EXPLORATORY

This is a POST-W12 exploratory matched-cohort comparison, not part of frozen Week-12 method selection or confirmation. It uses the same previously analyzed 50-query-per dataset cohort as post-hoc BEA_V2. Existing historical answers, splits and the official FIXED_SENTENCE final policy remain unchanged. BEA_V2's preregistered calibration remains CALIBRATION_FAILED_TERMINATED.

To run: set only RUN_FULL=True, then Run All. All 150 MiniLM scor

**Methods:** minilm_reranker; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 11_shared_infrastructure/runtime/W12-POST/reranker_baseline/protocol.py; 8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv. **Outputs:** [1_quality_comparison.csv](10_final_method_comparison/results/1_quality_comparison.csv); [3_paired_statistical_comparisons.csv](10_final_method_comparison/results/3_paired_statistical_comparisons.csv).

**Execution:** Experiment/model-capable or operational notebook; inspect unchanged cells/flags before any execution. **Status:** POST_W12_RERANKER_BASELINE_EXPLORATORY.

**Saved switches:** RUN_PREFLIGHT=True; RUN_SMOKE=False; RUN_READER_SMOKE=False; RUN_FULL=True; ALLOW_MODEL_DOWNLOAD=True; RUN_INSTALL_DEPENDENCIES=True; RUN_ANALYSIS=True.

## 10_final_method_comparison

### [2_qualitative_case_analysis.ipynb](10_final_method_comparison/notebooks/2_qualitative_case_analysis.ipynb)

**Purpose:**  Final query-level qualitative failure-mode analysis

Saved-result analysis only — no allocation, training, model generation or tuning.

Compare FIXED_SENTENCE, QBGF_FULL, BEA_QBGF_V1 and the separately labelled post-hoc BEA_V2 at 256/1024. The original BEA_V2 calibration remains CALIBRATION_FAILED_TERMINATED.

Use the sara_env kernel and Run All. The existing post-hoc study must already have all 1,200 saved rows. Missing results stop this notebook; they are never regenerated. This notebook runs on CPU and uses only a local tokenizer, cached so

**Methods:** final_method_comparison; **datasets:** QASPER / HotpotQA / SciFact; **budgets:** 256/1024.

**Inputs:** 8_bea_v2/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv; 11_shared_infrastructure/data/matched_source_pools/. **Outputs:** [final_qualitative_case_study_report.md](10_final_method_comparison/docs/qualitative_cases/final_qualitative_case_study_report.md).

**Execution:** Primarily saved-result analysis; may write plots/reports. **Status:** POST_W12_EXPLORATORY.

**Saved switches:** RUN_ANALYSIS=True; ALLOW_GENERATION=False; ALLOW_ALLOCATION=False; ALLOW_TRAINING=False.

Machine-readable exact notebook hashes/source paths: [notebook_map.csv](11_shared_infrastructure/audit/notebook_map.csv). The final-comparison notebook alias points to the original MiniLM notebook, not a copied/rebuilt notebook.
