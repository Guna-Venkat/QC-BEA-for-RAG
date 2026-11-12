# Evidence Lab 2.0 — Complete Application and Demonstration Guide

**CS787 · Generative Artificial Intelligence · IIT Kanpur**  
**Project Title:** Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation  
**Documented Release:** November 2026 (Evidence Lab 2.0)

---

## 1. Executive Overview

**Evidence Lab 2.0** is an interactive research demonstrator for investigating a fundamental question in Retrieval-Augmented Generation (RAG):

> **When a language model has limited space to read retrieved documents, which evidence should we select, how much should we include, and how should we represent it?**

The redesigned application prioritizes clarity, progressive disclosure, and scientific rigor. It is designed for three audiences:
1. **Beginners:** Understand the problem and RAG evidence pipeline within 1 minute.
2. **Faculty / TAs (Professor Arnab Bhattacharya):** Understand the algorithms (QBGF, BEA-V1, BEA-V2), compare them on real empirical cases, inspect why results differed, and review audited findings.
3. **Developers / Researchers:** Inspect raw candidate pools, dense relevance scores, token budgets, execution traces, and mathematical formulations in expandable **Advanced Details** containers.

---

## 2. Information Architecture: The Four Workspaces

The application is structured into four primary workspaces selectable from the sidebar:

| Workspace | Purpose | Key Content & Interactivity |
|---|---|---|
| **1. Start Here** | Default beginner-friendly landing page | 5-stage RAG pipeline flow, 3 interactive real research cases, and a 5-stage guided walkthrough (Question → Retrieval → Budget → Selection → Answer). |
| **2. Live Lab** | Live custom runner & research synthesis | **Tab 1:** Live Experiment Runner for user-supplied queries and passages (default view).<br>**Tab 2:** 8-stage Research Journey answering 4 questions per stage.<br>**Tab 3:** 7 Audited Key Findings with expandable validation/confirmation tables. |
| **3. Compare Methods** | Central experimental comparison interface | Side-by-side controlled comparison across Whole Passages (`RAW_SKIP`), Best Sentences (`FIXED_SENTENCE`), `QBGF`, `BEA-V1`, and `BEA-V2`. Includes the Visual Evidence Inspector and status color legend. |
| **4. How the Algorithms Work** | Interactive visual Algorithm Explorer | Dedicated visualizers for **QBGF** (MCKP global knapsack), **BEA-V1** (bottom-up heuristic stopping and starvation trace), and **BEA-V2** (learned helpfulness $P_{\mathrm{help}}$ and multi-hop bridge rescue). |

---

## 3. The 3-Minute Professor-Facing Demonstration Guide

Follow this streamlined script when demonstrating Evidence Lab to Professor Arnab Bhattacharya:

### Minute 1: The Core Problem & Start Here (Workspace 1)
1. **Open Workspace 1 ("Start Here"):** Point to the subtitle: *"Understanding how language models select useful information under limited context budgets."*
2. **Explain the 5-Stage Pipeline:** Explain that RAG involves *Question → Retrieved Candidates → Evidence Selection → Language Model → Answer*.
3. **Show Case 1 (Multi-Hop Reasoning):**
   - Click **"Explore Multi-Hop Case"** (HotpotQA, *Enemy* $\rightarrow$ Javier Gullón $\rightarrow$ *Invader (Invasor)*).
   - Step through the 5 stages using **Next Stage →**:
     - *Stage 1:* The question asks which movie Denis Villeneuve's screenwriter got a Goya nomination for.
     - *Stage 2:* The retrieved candidates contain both *Enemy* and Javier Gullón's bio mentioning *Invader (Invasor)*.
     - *Stage 3:* The budget is restricted to 256 tokens.
     - *Stage 4:* Whole Passages and Best Sentences fit the bridge sentence; BEA-V1 drops it!
     - *Stage 5:* Show the reader output: BEA-V1 hallucinates *"Enemy"*, while BEA-V2 rescues the bridge fact and outputs *"Invader (Invasor)"* (Score 1.0).

### Minute 2: Comparing Methods & Visualizing Evidence (Workspace 2)
1. **Switch to Workspace 2 ("Compare Methods"):**
   - Note the **✓ CONTROLLED MATCHED COMPARISON** badge: query, retriever, reader (Qwen), and prompt contract are identical.
2. **Side-by-Side Comparison:**
   - Display **Best Sentences** vs **QBGF** vs **BEA-V1**.
   - Show how BEA-V1 used only 168 tokens, stopped early, and produced an incorrect answer, while Best Sentences and QBGF used ~243 tokens and answered correctly.
3. **Evidence Status Legend:**
   - Highlight the color semantics:
     - 🟢 **Selected Evidence:** Sent to the reader.
     - ⚪ **Omitted Evidence:** Dropped due to budget.
     - 🔵 **Decisive Evidence:** Contains the verified ground-truth answer.
     - 🟠 **Warning:** Stopping threshold / budget starvation.
     - 🔴 **Harmful Unit:** Proved to degrade performance under LOO.

### Minute 3: Explaining the Algorithms & Why Relevance ≠ Utility (Workspaces 3 & 4)
1. **Switch to Workspace 3 ("How the Algorithms Work"):**
   - **QBGF:** Show the discrete fidelity menu per passage (`DROP`, `SENT_1`, `SENT_2`, `SENT_4`, `SENT_8`, `FULL`). Explain that it optimizes a knapsack problem across representation choices under a shared budget.
   - **BEA-V1:** Show the interactive transition slider on QASPER: at Step 15, the allocator halts at 245/1024 tokens because marginal gain/cost falls below $\tau = 0.010000$, starving the context and hallucinating stimulus words.
   - **BEA-V2:** Explain $P_{\mathrm{help}}$: *"the probability that this evidence will measurably improve the reader's downstream answer."*
2. **Switch to Workspace 4 ("Research & Live Lab"):**
   - Point to **Key Finding 5:** Relevance is an imperfect proxy for utility ($\rho \in [-0.021, +0.082]$, 69.5%–98.9% neutral, 0.6%–13.5% harmful; SciFact: 4.9% at 256, 0.6% at 1024; QASPER: 13.5% at 256).
   - Open **Audited Experimental Results Table** to show the 7,155-query HotpotQA and 1,005-query QASPER validation surface.

---

### Navigation and theme compatibility

At the final Start Here walkthrough stage, **Open Live Lab →** switches to Live Lab and updates the sidebar selection and URL together. You can return with the sidebar. Reader-answer cards inherit the active theme's text color and use a translucent background, keeping original/removal answers and scores readable in both light and dark modes without text selection.

### Original World Cup preset and compact reader answers

The default **Budget-sensitive multi-aspect question** loads the original **15 source passages**, restored at the user's request. The original question and Preset Reference Answer are unchanged. If your browser still holds the grouped five-passage version, click the preset button to restore all original passages and clear stale comparison/impact outputs. Custom edits remain supported.

The grouped preset is retained as an inactive demo asset; it is not the default. No research artifacts or algorithms were changed by this restoration.

The main method title is simply **BEA-V2**. Its runtime threshold, predictor identity and calibration notes are available in the collapsed **Advanced details · BEA-V2 execution** panel. The actual threshold and saved predictor execution have not changed.

**Reader Answers** shows original and removal answers in two wrapped HTML cards, each with its score. Narrow screens stack the cards. Long text has optional internal vertical scrolling; there is no code-block horizontal scrolling. Scores, LOO subtraction, prompts and generations are unchanged.

### 3.1 Live Lab: corrected comparison and LOO workflow

1. Open **Live Lab → Live Experiment**. Enter a query and source passages or load **Budget-sensitive multi-aspect question**. Passage cards retain stable IDs when another card is removed.
2. Select **256 or 1024 evidence tokens** (input evidence allowance, not output length), CPU or CUDA, and **Enable Live Models**. Checkpoints are local-only; nothing downloads automatically. CPU loads SFR and Qwen sequentially. Genuine qualification of these repairs used CUDA; CPU dispatch is also covered by synthetic tests.
3. Optionally supply an evaluation reference. For claim verification it must be exactly `SUPPORT`, `REFUTE` or `NOT_ENOUGH_INFO`. A custom reference is user supplied, not official benchmark gold. It is never sent to the reader or selector.
4. Click **Compare Four Methods**. Every available method uses actual SFR query/passage/sentence scores and the canonical research selector. A failed component makes its method unavailable; there is no BM25 substitution or invented embedding/probability.

| Method | Current custom-input execution |
|---|---|
| Best Sentences / FIXED_SENTENCE | Canonical SFR sentence ranking, exact source evidence and budget packing |
| QBGF | Canonical fidelity options and exact cost-state multiple-choice DP; no lexical score rescaling |
| BEA-V1 | Canonical marginal relevance/coverage/redundancy transitions; reviewed frozen `tau_stop=tau_expand=.01`, `tau_context=.05`, `eta_cov=lambda_red=.5` |
| BEA-V2 | **Enabled at τ = 0.00008**, as requested. Canonical helpfulness-weighted allocator and canonical features use all 15 checksum-verified saved predictors: five folds per dataset, averaged within dataset and then equally across datasets. No new training or synthetic probabilities. This custom-input ensemble is exploratory; historical calibration results and saved examples remain unchanged. |

With Live Models disabled, this strict four-method comparison shows unavailable methods. The expandable **Single-Method Diagnostics & Advanced Pipeline Controls** still supports labelled CPU-only BM25 context inspection; that educational mode is not a canonical SFR method comparison.

5. Inspect exact evidence and each **inference receipt**. Receipts are session-only and include final prompt token IDs/text/hash, evidence hash and IDs, pinned reader identity, tokenizer/template/code identity, task, generation settings and cache provenance. Identical reader requests may reuse an answer even across methods if the context and complete generation contract are identical. Old-format caches are never eligible.
6. Click **Analyze Evidence Impact** only after a valid comparison and a reference. It tests the first **1–3 selected units in source order**, not all units and not necessarily the most relevant ones. Each unit is removed without retrieval, allocator rerun, replacement or budget refill. A FULL-passage representation is one atomic deletion unit. Duplicate facts elsewhere can legitimately remain.

The live convention is:

`delta = score(after deletion) - score(original)`

- QA **HELPFUL:** delta < −0.01.
- QA **HARMFUL:** delta > +0.01.
- QA **NEUTRAL:** |delta| ≤ 0.01.
- Claim verification uses zero tolerance with the exact-label parser. Other nonempty outputs are `INVALID_OUTPUT` and incorrect; invalid prose does not become NEI.
- If either required generation is missing, failed or has an incompatible receipt, there is **no quality delta or helpful/harmful label**. Failures are shown separately.

These are reference-agreement effects of an input deletion, not proof that the reader internally reasoned from the unit, was confused by it, or required it universally. Token F1 can be low for a correct but verbose/synonymous answer. Frozen W12 attribution used zero tolerance and the opposite importance sign; those research outputs are unchanged.

7. Use the Before/After inspector to view both contexts, answers and exact request receipts. Changing query, passages, budget, task, scoring model or reader configuration requires a fresh comparison before analysis. Failed comparisons cannot manufacture usable baselines.
8. A reference-only change can use **Rescore Answers with Updated Reference** without inference. A task change cannot: it changes the prompt/parser contract and requires a new comparison.

The LOO cache key binds final prompt IDs, model revision, tokenizer/template, device/precision, decoding/seed, task and reader protocol/code. Cache hits are explicit; failures are never stored as successful answers. Live data remains session-only and never enters benchmark, validation or confirmation results.

### 3.2 Qualification of the repairs (11 November 2026)

The regression suite includes controlled prompt/reference isolation, exact no-refill deletion, cache invalidation, failed-inference handling, strict labels, stale-input blocking and passage removal. See [the corrective implementation report](audit/LIVE_LAB_CORRECTNESS_REPAIR.md) for exact counts and limitations.

A tiny fictional-vessel CUDA test used real pinned SFR and Qwen3-8B, including full evidence, LOO, query-only, contradictory evidence, verification, repeated cache reuse and reference-only rescoring. This is a technical qualification, not a new study or a method-quality comparison. No historical research scores were changed.

---

## 4. Quick Start & Launch Instructions

### Launching the Streamlit Application
From the repository root:
```bash
demo/.venv/bin/python -m streamlit run demo/app.py
```
Or specify a custom port:
```bash
demo/.venv/bin/python -m streamlit run demo/app.py --server.port 8501
```

### Running the Test Suite
The demo includes a comprehensive regression suite covering all components, freeze hashes, segmentation adapters, live impact interventions, and Streamlit AppTest screens:
```bash
demo/.venv/bin/python -m pytest demo/tests/ -v
```

---

## 5. Scientific Guardrails & Data Provenance

1. **Strictly Read-Only Research Results:** All benchmark tables, validation figures, and qualitative cases are read directly from canonical frozen artifacts in `FINAL_PROJECT_MAIN/` and `results/`.
2. **Fail-Closed Artifact Verification:** On startup, `demo/app.py` runs `freeze_check()` and `verify_manifest()`. If primary SHA256 checksums disagree, the application stops immediately.
3. **No Fabricated Model Generations:** Every reader output displayed in Curated and Compare views is the exact string generated during controlled frozen execution.
4. **Controlled vs Live Distinction:**
   - **CONTROLLED MATCHED COMPARISON:** Strictly identical candidate pool, budget, reader, and decoding parameters.
   - **LIVE CUSTOM RUN:** User-supplied text and queries. Clearly labelled as a demonstration without benchmark ground truth.

---

## 6. Directory Structure of `demo/`

```text
demo/
├── app.py                     # Main coordinator and 4-workspace router
├── constants.py               # Human-readable labels, color semantics, sources
├── data_loader.py             # Fail-closed artifact loader and SHA256 verifier
├── curated_examples.py        # Frozen data for the 4 real research case studies
├── components.py              # Visual components (hero, pipeline, badges, meters)
├── plots.py                   # Plotly visualization routines (bars, deltas, attribution)
├── result_registry.py         # Query and profile registry from the published bundle
├── evidence_registry.py       # Candidate pools and retrieval scopes
├── views/                     # Internal views (avoiding Streamlit automatic page routing)
│   ├── __init__.py
│   ├── start_here.py          # Workspace 1: Guided circular 5-stage walkthrough
│   ├── compare_methods.py     # Workspace 2: Side-by-side experimental comparison (Featured Cases only)
│   ├── algorithm_explorer.py  # Workspace 3: Interactive QBGF, BEA-V1, BEA-V2 visualizers
│   └── research_and_live.py   # Workspace 4: Live Experiment (Tab 1), Journey (Tab 2), Key Findings (Tab 3)
├── replay_data/v1/            # Preserved published replay bundle and manifest
├── live/                      # Live inference engine and safeguards
│   ├── allocator.py           # Core heuristic and fallback allocators
│   ├── bea_adapter.py         # Canonical BEA-V1 & BEA-V2 integration (12-feature utility model)
│   ├── impact.py              # 4-Method comparison & Leave-One-Out impact interventions
│   ├── ui.py                  # Live Lab interactive interface with native Streamlit components
│   └── resources.py           # Device detection, GPU memory allocation, CPU fallback
├── artifacts/
│   └── redesigned_ui/         # Verified browser screenshots across all workspaces & live runs
├── run_playwright_verification.py # Automated end-to-end browser verification script
└── tests/                     # 165-test regression suite passing 100%

---

## 7. Critical UI, Navigation, and Evidence Display Fixes (Audit Summary)

The following 9 functional and usability defects were audited and resolved:

1. **Eliminated Broken Automatic Navigation Links (Issue 1):** Moved internal page modules from `demo/pages/` to `demo/views/` and added query parameter synchronization (`?workspace=...`), permanently eliminating duplicate blank-page routes (`/start_here`, `/algorithm_explorer`, etc.).
2. **Detailed Selected Evidence Display in Start Here (Issue 2):** Stage 4 now displays actual selected evidence units with status badges (`🟢 SELECTED`, `🔵 DECISIVE`), token counts, document titles, expandable omitted evidence, and expandable exact reader serialized contexts.
3. **Consistent Matched SciFact Walkthrough (Issue 3):** Replaced the isolated SciFact LOO ablation with a genuine matched 4-method comparison (`SCIFACT_MATCHED_EXAMPLE`, Claim 1132 on TCR/CD3 microdomains) across `FIXED_SENTENCE`, `QBGF`, `BEA-V1`, and `BEA-V2`. Preserved Claim 343 for dedicated LOO ablation study.
4. **Circular Start Here Navigation (Issue 4):** Implemented clean circular navigation ($1 \rightarrow 2 \rightarrow 3 \rightarrow 4 \rightarrow 5 \rightarrow 1$) with `↻ Restart Walkthrough` on Stage 5 and `← Previous Stage` buttons, with automatic reset to Stage 1 on dataset switch.
5. **Removed Historical Curated Queries Toolbar (Issue 5):** Streamlined Compare Methods to default directly to the Featured Research Cases selectbox.
6. **Eliminated Leaked Raw HTML and Fixed Token Math (Issue 6):** Converted hand-built indented HTML cards in Compare Methods to native `st.container(border=True)` components. Implemented centralized `calculate_utilization(tokens_used, budget)` fixing the `0.0%` math error ($245/256 \rightarrow 95.7\%$, $251/256 \rightarrow 98.0\%$, $255/256 \rightarrow 99.6\%$, $242/256 \rightarrow 94.5\%$).
7. **Default Live Experiment Tab (Issue 7):** Reordered tabs in Research & Live Lab so **Tab 1: Live Experiment** is selected by default while preserving inputs across tabs.
8. **Native Containers in Live Experiment & Clear Status Labels (Issue 8):** Replaced raw HTML strings in method cards with native Streamlit components, verified status badges (`Within Token Budget`), and explicit `"Reader inference not executed"` notices when reader models are disabled.
9. **Fully Guarded & Functional Evidence Impact Analysis (Issue 9):**
   - *Case A (No reference answer):* Displays informative warning: `"Reference answer required: Please provide a reference answer to evaluate whether removing evidence improves or worsens the generated response..."`.
   - *Case B (Context-only mode):* Displays educational warning: `"Reader inference required: Evidence selection has completed, but the language model has not generated answers..."`.
   - *Case C (Valid reference and completed outputs):* Executes real Leave-One-Out deletions without refilling budget ($E \setminus \{u\}$), scores ablated reader answers, computes $\Delta_i$, classifies effects into Helpful / Harmful / Neutral, and renders the interactive Before / After Answer Inspector.
```
