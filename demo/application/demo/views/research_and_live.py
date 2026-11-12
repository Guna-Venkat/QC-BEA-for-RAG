"""View 4 — Research & Live Lab: Comprehensive Research Synthesis & Live Runner.

Contains three distinct tabs with Live Experiment as the default active section:
- Tab 1: Live Experiment (Interactive custom inference and impact runner)
- Tab 2: Research Journey (8 stages answering 4 core scientific questions per stage)
- Tab 3: Key Findings (7 visual takeaways, data tables, and plain-language statistics)
"""

from html import escape
from typing import Dict, Any, List
import streamlit as st
import pandas as pd
from demo.result_registry import findings
from demo.components import source, note
from demo.plots import bars, deltas, attribution
from demo.live.ui import render as render_live_demo


JOURNEY_STAGES = [
    {
        "stage": "Stage 1 · SARA Latent Compression",
        "title": "Investigating Adaptive Context Quantity",
        "solve": "Can we compress retrieved passages into continuous latent vectors to fit more information into the model's limited context?",
        "tried": "Evaluated the SARA architecture (Mistral-7B with a trained MLP projector mapping SFR embeddings to <COMPRESS> tokens) across fixed context depths k = 0, 2, 4, 5, 6, 8, 10.",
        "observed": "A theoretical retrospective oracle that selects the best k per query achieved +26.78% F1 over fixed k=5. Different questions exhibited radically different context requirements (e.g. Q1001 needed k=6 to expose decisive features, while Q897 peaked at k=0).",
        "next": "Motivated training a classifier to predict each question's optimal context quantity before generation."
    },
    {
        "stage": "Stage 2 · QCCA Context Prediction",
        "title": "Attempting to Predict Evidence Quantity",
        "solve": "Can a pre-generation controller predict how much context a question needs using lexical, semantic, and syntactic features?",
        "tried": "Built 64 query features across 6 families and trained 12 classification models (Balanced Logistic Regression, XGBoost, Random Forest, MLP, LightGBM) to predict expansion steps (e.g. 2 -> 4 -> 6 -> 8).",
        "observed": "Predicting exact context size proved unreliable. Classifiers suffered high false expansion rates (~20-28%) and asymmetric loss: missing decisive evidence (false stop) cost up to 1.0 F1, while carrying mild excess context only reduced F1 by ~0.05.",
        "next": "Revealed that context size alone is insufficient—which specific passages enter the budget matters just as much."
    },
    {
        "stage": "Stage 3 · Passage Identity",
        "title": "The Decisive Role of Specific Documents",
        "solve": "Does varying which passages enter the context matter when the total passage count is strictly fixed?",
        "tried": "Evaluated fixed k=4 on QASPER while varying the selection policy: lexical BM25 prefix [1,2,3,4], dense semantic cosine [2,3,4,5], and learned passage ranker [1,2,6,8].",
        "observed": "Semantic routing gained +0.03173 F1 over BM25 prefix at identical passage budget k=4. On Question 917, only the learned route pulled in the decisive Rank-8 passage (ParCorFull English-German corpus), boosting F1 from 0.50 to 1.00.",
        "next": "Proved that passage selection identity is critical, leading to the study of finer representation units than whole passages."
    },
    {
        "stage": "Stage 4 · Evidence Granularity",
        "title": "Passages vs Sentences vs Spans",
        "solve": "Should evidence be packed as whole passages, individual sentences, or fine-grained spans under tight token budgets?",
        "tried": "Controlled three-way granularity pilot on HotpotQA across budgets B in {256, 512, 1024} tokens.",
        "observed": "Under tight budgets (256 tokens), sentence selection outperformed whole passages by +0.0838 F1 (+24.8% relative gain) by distributing limited space across multiple sources. At 1024 tokens, whole passages regained competitiveness (0.4803 vs 0.4721).",
        "next": "Formulated the hypothesis: rather than choosing one granularity globally, adapt representation fidelity per passage under a shared token budget."
    },
    {
        "stage": "Stage 5 · QBGF Formulation",
        "title": "Query-Conditioned Budgeted Granularity Fusion",
        "solve": "Can we jointly optimize evidence representations across all retrieved passages under a hard token budget?",
        "tried": "Formulated QBGF as a Multiple-Choice Knapsack Problem (MCKP), selecting one of {DROP, SENT_1, SENT_2, SENT_4, SENT_8, FULL} per passage using exact branch-and-bound dynamic programming.",
        "observed": "Query conditioning improved validation quality (+0.015 to +0.043 across datasets). However, fusion (mixing sentences and passages) did not consistently beat the simple sentence baseline. A noninferiority audit confirmed the sentence baseline is noninferior to QBGF with 95% confidence.",
        "next": "Led to freezing SFR -> FIXED_SENTENCE -> Qwen as the production policy, and prompted investigation into why relevance-based allocation plateaued."
    },
    {
        "stage": "Stage 6 · Leave-One-Out (LOO) Analysis",
        "title": "Empirical Downstream Evidence Utility",
        "solve": "Does retrieved and selected evidence actually help the language model generate better answers?",
        "tried": "Conducted exhaustive Leave-One-Out (LOO) deletions on 1,489 passages and 5,165 sentences, regenerating reader outputs after removing each unit without refilling freed budget.",
        "observed": "Semantic relevance is an imperfect proxy for downstream utility. Rank correlation between dense similarity and LOO delta was near zero (rho in [-0.021, +0.082]). 69.5%–98.9% of units were neutral, and 0.6%–13.5% were harmful (SciFact: 4.9% at 256, 0.6% at 1024; QASPER: 13.5% at 256).",
        "next": "Motivated designing budget-aware allocators that actively model downstream evidence utility rather than relying solely on query relevance."
    },
    {
        "stage": "Stage 7 · BEA-V1 Dynamic Stopping",
        "title": "Bottom-Up Incremental Allocation",
        "solve": "Can we incrementally add evidence sentences based on marginal utility gain and stop early to avoid context dilution?",
        "tried": "Implemented BEA-V1, sequentially adding evidence while tracking multi-aspect coverage and diversity, terminating when marginal gain per token fell below a threshold.",
        "observed": "Heuristic stopping rules suffered severe context starvation. On QASPER, BEA-V1 stopped at 245/1024 tokens (76.1% budget unused; operational tau=0.010 vs base tau=0.001), missing the decisive task list and dropping accuracy.",
        "next": "Showed that heuristic stopping rules must be guided by calibrated predictions of downstream evidence helpfulness."
    },
    {
        "stage": "Stage 8 · BEA-V2 Learned Helpfulness",
        "title": "Guiding Context with P_help",
        "solve": "Can a learned classifier predict which evidence units will measurably help the reader before generation?",
        "tried": "Trained GroupKFold cross-fitted logistic regression models to predict P_help, weighting marginal transition gains by estimated helpfulness.",
        "observed": "Successfully rescued the missing screenwriter bridge fact on HotpotQA (P_help = 0.1259 promoted at Step 1, F1 flipped 0.0 -> 1.0) and avoided QASPER starvation. However, global calibration remained challenging and zero paired contrasts survived Holm-Bonferroni correction.",
        "next": "Established that while learned helpfulness can repair specific multi-hop gaps, simple sentence selection remains a robust, transparent baseline."
    }
]


def render():
    st.markdown("## Live Lab & Research")
    st.caption("Interactive live experiment workspace, complete research progression, and audited empirical findings.")
    
    # Live Experiment is placed first as requested
    tab_live, tab_journey, tab_findings = st.tabs([
        "◈ Live Experiment",
        "◈ Research Journey (8 Stages)",
        "◈ Audited Key Findings"
    ])
    
    with tab_live:
        render_live_experiment()
        
    with tab_journey:
        render_research_journey()
        
    with tab_findings:
        render_key_findings()


def render_live_experiment():
    st.subheader("Live Custom Experiment Runner")
    st.caption(
        "Test custom questions and passages with working token allocation and reader inference. "
        "Models load only when explicitly requested; CPU fallback and GPU memory safeguards are active."
    )
    
    st.warning("LIVE CUSTOM RUN MODE: Evaluated on user-supplied text. Does not compute benchmark scores.")
    
    # Delegate to LiveDemo engine
    render_live_demo(technical=False, presentation=True)


def render_research_journey():
    st.subheader("The Research Progression: From Context Size to Evidence Utility")
    st.markdown(
        "Our investigation progressed through 8 distinct scientific stages. "
        "Each stage was directly motivated by an empirical finding or failure mode in the previous stage."
    )
    
    for item in JOURNEY_STAGES:
        with st.container(border=True):
            st.markdown(f"#### {item['stage']}: {item['title']}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**What were we trying to solve?**\n\n{item['solve']}")
                st.markdown(f"**What did we try?**\n\n{item['tried']}")
            with c2:
                st.markdown(f"**What did we observe?**\n\n{item['observed']}")
                st.markdown(f"**Why did that lead to the next stage?**\n\n{item['next']}")
                
    source('w10_runner', 'w11_runner', 'code', 'validation', 'confirmation')


def render_key_findings():
    st.subheader("What Survived the Experiments? (Audited Findings)")
    st.caption("Frozen experimental results. QA F1 and SciFact macro-F1 are never pooled.")
    
    data = findings()
    
    # 7 Visual Key Takeaways Cards using native containers
    st.markdown("#### Seven Core Scientific Takeaways")
    
    kcols = st.columns(3)
    with kcols[0]:
        with st.container(border=True):
            st.markdown("**1. Questions Need Different Context**")
            st.caption("An oracle that chooses the best k context depth per query gains +26.78% F1. Some questions peak at k=0; others require deep retrieval.")
            
    with kcols[1]:
        with st.container(border=True):
            st.markdown("**2. Passage Identity Matters**")
            st.caption("At fixed k=4 passages, semantic routing gained +0.03173 F1 over BM25 prefix. Selecting the decisive passage is critical.")
            
    with kcols[2]:
        with st.container(border=True):
            st.markdown("**3. Sentences Win Under Tight Budgets**")
            st.caption("At 256 tokens, sentence selection gained +0.0838 F1 (+24.8%) over whole passages by spreading limited tokens across sources.")
            
    kcols2 = st.columns(4)
    with kcols2[0]:
        with st.container(border=True):
            st.markdown("**4. QBGF Query Conditioning**")
            st.caption("Query conditioning improved all 6 validation cells, but multi-granularity fusion did not beat simple sentences.")
            
    with kcols2[1]:
        with st.container(border=True):
            st.markdown("**5. Relevance ≠ Utility**")
            st.caption("LOO rank correlations were near zero (rho in [-0.021, +0.082]). 69.5%–98.9% of units are neutral; 0.6%–13.5% are harmful (e.g. 4.9% on SciFact 256, 13.5% on QASPER 256).")
            
    with kcols2[2]:
        with st.container(border=True):
            st.markdown("**6. Stopping Rules Can Starve**")
            st.caption("BEA-V1 stopped at 245/1024 tokens on QASPER (operational tau=0.010), leaving 76.1% of budget unused and failing to expose the decisive task list.")
            
    with kcols2[3]:
        with st.container(border=True):
            st.markdown("**7. Learned Helpfulness (P_help)**")
            st.caption("BEA-V2 recovered missing bridge facts on HotpotQA, though 24 paired tests showed no universal Holm-corrected advantage.")
            
    st.markdown("---")
    
    # Expandable Audited Tables
    with st.expander("Audited Experimental Results Table (Validation Surface)", expanded=False):
        st.markdown("**Main Validation Surface (N=7,155 HotpotQA, N=1,005 QASPER, N=177 SciFact):**")
        df_val = pd.DataFrame(data['validation'])
        st.dataframe(df_val, hide_index=True, width="stretch")
        source('validation')
        
    with st.expander("Reserved Confirmation Surface & Noninferiority Audit", expanded=False):
        st.markdown("**Reserved Two-Task Confirmation Surface (N=200 HotpotQA, N=50 SciFact):**")
        df_conf = pd.DataFrame(data['confirmation'])
        st.dataframe(df_conf, hide_index=True, width="stretch")
        st.caption("Plain-language summary: FIXED_SENTENCE significantly outperformed NONE across all 4 cells. Against whole passages, sentence selection gained +0.2876 on SciFact 256 (p_Holm = 0.0356).")
        source('confirmation', 'contrasts')
        
    with st.expander("Leave-One-Out (LOO) Attribution Distributions", expanded=False):
        counts = data.get('unit_counts', {})
        total = sum(counts.values()) or 1
        c1, c2, c3 = st.columns(3)
        c1.metric("Helpful Units", f"{counts.get('HELPFUL', 0):,} ({100*counts.get('HELPFUL', 0)/total:.1f}%)")
        c2.metric("Neutral Units", f"{counts.get('NEUTRAL', 0):,} ({100*counts.get('NEUTRAL', 0)/total:.1f}%)")
        c3.metric("Harmful Units", f"{counts.get('HARMFUL', 0):,} ({100*counts.get('HARMFUL', 0)/total:.1f}%)")
        st.caption("A neutral deletion means deleting that sentence caused zero observed score change in the reader output.")
        source('units', 'correlations')
