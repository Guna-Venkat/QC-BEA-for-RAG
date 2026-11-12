"""View 3 — How the Algorithms Work: Interactive Algorithm Explorer.

Provides deep visualizers and mathematical formulations for:
- QBGF (Multiple-Choice Knapsack dynamic programming)
- BEA-V1 (Incremental bottom-up heuristic stopping rule & starvation trace)
- BEA-V2 (Helpfulness-weighted allocation & multi-hop bridge rescue)
"""

from html import escape
import streamlit as st
import pandas as pd
from demo.components import source
from demo.curated_examples import QASPER_STARVATION_EXAMPLE, HOTPOT_BRIDGE_EXAMPLE


def render():
    st.markdown("## How the Algorithms Work")
    st.caption("Visual interactive explorers for the project's three novel evidence allocation algorithms.")
    
    # Algorithm Selector
    selected_algo = st.radio(
        "Choose Algorithm to Explore",
        ["QBGF (Knapsack Optimization)", "BEA-V1 (Dynamic Marginal Stopping)", "BEA-V2 (Learned Helpfulness Guidance)"],
        horizontal=True,
        key="algo_explorer_radio"
    )
    
    st.markdown("---")
    
    if "QBGF" in selected_algo:
        render_qbgf_explorer()
    elif "BEA-V1" in selected_algo:
        render_beav1_explorer()
    else:
        render_beav2_explorer()


# ==============================================================================
# 1. QBGF Explorer
# ==============================================================================
def render_qbgf_explorer():
    st.subheader("QBGF: Query-Conditioned Budgeted Granularity Fusion")
    
    with st.container(border=True):
        st.markdown("**The Core Intuition:**")
        st.caption(
            "Instead of treating every retrieved passage the same way, QBGF chooses how much information to retain "
            "from each passage (a full passage, 1 sentence, 2 sentences, 4 sentences, or nothing) "
            "while respecting a single shared token budget."
        )
    
    # Workflow Pipeline
    st.markdown("#### The QBGF Pipeline")
    pcols = st.columns(5)
    pcols[0].info("**1. Query & Retrieval**\n\nRetrieve top-10 candidate passages using SFR bi-encoder.")
    pcols[1].info("**2. Fidelity Menu**\n\nConstruct representation options for each passage.")
    pcols[2].info("**3. Query Utility**\n\nCompute relevance masses from sentence embeddings.")
    pcols[3].info("**4. Knapsack Solver**\n\nExact dynamic programming solves budget packing.")
    pcols[4].info("**5. Reader Prompt**\n\nAssemble selected text into frozen reader.")
    
    st.markdown("---")
    st.subheader("Interactive Demonstration: The Discrete Fidelity Menu")
    st.caption(
        "For each retrieved passage i, QBGF builds a discrete menu of mutually exclusive options. "
        "Here is how representation fidelity changes token cost and query utility:"
    )
    
    # Illustrative Passage Example
    menu_options = [
        {"option": "DROP", "tokens": 0, "utility": 0.00, "desc": "Do not include any text from this passage."},
        {"option": "SENT_1", "tokens": 28, "utility": 0.38, "desc": "Extract the single most query-relevant sentence."},
        {"option": "SENT_2", "tokens": 54, "utility": 0.59, "desc": "Extract the top-two query-relevant sentences."},
        {"option": "SENT_4", "tokens": 98, "utility": 0.81, "desc": "Extract the top-four query-relevant sentences."},
        {"option": "SENT_8", "tokens": 165, "utility": 0.92, "desc": "Extract the top-eight query-relevant sentences."},
        {"option": "FULL", "tokens": 210, "utility": 1.00, "desc": "Include the complete, contiguous whole passage."}
    ]
    
    mcols = st.columns(6)
    for col, opt in zip(mcols, menu_options):
        with col:
            with st.container(border=True):
                st.markdown(f"**{opt['option']}**")
                st.caption(f"{opt['tokens']} tok · Util: {opt['utility']:.2f}")
                st.caption(opt['desc'])
                
    st.caption("Note: Utilities are calculated from dense sentence embedding similarities in real execution.")
    
    # Advanced Details Expander
    with st.expander("Advanced Details · Exact MCKP Mathematical Formulation"):
        st.markdown(
            r'''
            QBGF formalizes evidence allocation as a **Multiple-Choice Knapsack Problem (MCKP)**:
            
            $$\max \sum_{i=1}^m \sum_{j \in M_i} u_{ij} x_{ij} \quad \text{s.t.} \quad \sum_{i=1}^m \sum_{j \in M_i} c_{ij} x_{ij} \le B, \quad \sum_{j \in M_i} x_{ij} = 1, \quad x_{ij} \in \{0, 1\}$$
            
            Where:
            - $m$ is the number of candidate retrieved passages.
            - $M_i = \{\text{DROP}, \text{SENT\_1}, \text{SENT\_2}, \text{SENT\_4}, \text{SENT\_8}, \text{FULL}\}$ is the fidelity menu for passage $i$.
            - $u_{ij}$ is the query-conditioned utility of option $j$ for passage $i$.
            - $c_{ij}$ is the exact tokenizer cost of option $j$.
            - $B \in \{256, 1024\}$ is the hard token budget constraint.
            
            The problem is solved using exact branch-and-bound dynamic programming with dominated-option pruning.
            '''
        )
        source('code', 'validation')


# ==============================================================================
# 2. BEA-V1 Explorer
# ==============================================================================
def render_beav1_explorer():
    st.subheader("BEA-V1: Dynamic Marginal Allocation & Context Starvation")
    
    with st.container(border=True):
        st.markdown("**The Core Intuition:**")
        st.caption(
            "Unlike top-down budget packing, BEA-V1 builds the selected context gradually from the bottom up. "
            "At each step, it calculates the marginal gain of adding another sentence (relevance + new query coverage − redundancy) "
            "divided by its token cost, and stops early when the best gain-to-cost ratio drops below a threshold tau."
        )
    
    st.markdown("#### The Context Starvation Pathology (Real QASPER Trace)")
    st.caption(
        "Here is the actual recorded execution trace on QASPER Question deb89bca... (Budget B = 1024 tokens). "
        "Watch how the allocator prematurely halts at Step 15, leaving 779 tokens (76% of budget) completely empty:"
    )
    
    trace_data = QASPER_STARVATION_EXAMPLE["transition_trace"]
    df_trace = pd.DataFrame(trace_data)
    
    # Interactive Step Slider
    step = st.slider("Inspect Trace Step-by-Step", min_value=1, max_value=len(trace_data), value=len(trace_data), key="beav1_step_slider")
    
    current_row = trace_data[step - 1]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Step", f"{current_row['step']} / {len(trace_data)}")
    c2.metric("Cumulative Tokens", f"{current_row['cum_tokens']} / 1024", delta=f"{1024 - current_row['cum_tokens']} unused", delta_color="inverse")
    c3.metric("Marginal Gain/Token", f"{current_row['ratio']:.6f}")
    c4.metric("Allocator Decision", current_row["decision"], delta_color="off")
    
    if step == 16:
        st.error(
            f"⛔ STOPPING RULE TRIGGERED: Step 16 marginal ratio ({current_row['ratio']:.6f}) fell below threshold "
            f"tau = 0.010000. Selection halted! Decisive Sentence S005 was never reached."
        )
    else:
        st.success(f"✓ Step {step}: Sentence accepted ({current_row['cost']} tokens added). Selection continues.")
        
    st.markdown("##### Complete Transition Table:")
    st.dataframe(df_trace, hide_index=True, width="stretch")
    
    # Advanced Details Expander
    with st.expander("Advanced Details · Heuristic Scoring Formulation"):
        st.markdown(
            r'''
            At step $t$, candidate transition $a$ is scored by:
            
            $$g_t(a) = \mathrm{Rel}_t(a) + 0.5 \Delta\mathrm{Cov}_t(a) - 0.5 \mathrm{Red}_t(a)$$
            
            The marginal efficiency ratio divides gain by exact incremental token cost:
            
            $$d_t(a) = \frac{g_t(a)}{\Delta c_t(a)}$$
            
            BEA-V1 selects $a_t^* = \arg\max_a d_t(a)$. It halts if $d_t(a_t^*) < \tau$ (with default $\tau = 0.01$).
            
            **Why Context Starvation Happens:**
            Once early sentences cover general keywords, the marginal gain $g_t(a)$ of newly candidate sentences diminishes. 
            Because cost $\Delta c$ remains positive, the ratio $d_t(a)$ falls below $\tau$ even when complementary, answer-bearing 
            evidence remains in the candidate pool and hundreds of budget tokens sit empty.
            '''
        )
        source('code')


# ==============================================================================
# 3. BEA-V2 Explorer
# ==============================================================================
def render_beav2_explorer():
    st.subheader("BEA-V2: Usefulness-Weighted Allocation & Bridge Rescue")
    
    with st.container(border=True):
        st.markdown("**The Core Intuition:**")
        st.caption(
            "BEA-V2 learns from previous Leave-One-Out (LOO) deletion experiments. "
            "Instead of relying solely on heuristic similarity, it predicts P_help: "
            "the probability that including this evidence will measurably improve the reader's downstream answer."
        )
    
    # The Learning Pipeline
    st.markdown("#### The BEA-V2 Learning & Selection Workflow")
    wcols = st.columns(4)
    wcols[0].info("**1. LOO Perturbations**\n\nRun leave-one-out deletions across hundreds of training contexts.")
    wcols[1].info("**2. Utility Supervision**\n\nRecord empirical helpful (score increase) vs neutral/harmful labels.")
    wcols[2].info("**3. Cross-Fitted Model**\n\nTrain GroupKFold logistic regression to predict P_help.")
    wcols[3].info("**4. Helpfulness Guidance**\n\nWeight marginal incremental candidate values by P_help.")
    
    st.markdown("---")
    st.subheader("Real Case Study: Rescuing the Screenwriter Bridge Fact")
    st.caption(
        "On HotpotQA question 5a7df25a..., BEA-V1 starved at 168 tokens and dropped the bridge sentence, "
        "causing the reader to fail. Watch how BEA-V2's learned helpfulness signal rescues the bridge:"
    )
    
    hb = HOTPOT_BRIDGE_EXAMPLE
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.error("BEA-V1 Heuristic Decision")
            st.caption("Evaluated the bridge sentence late under generic keyword overlap:")
            st.markdown(
                "The bridge sentence received a low marginal ratio because *Enemy* had already been introduced. "
                "BEA-V1 rejected the sentence, used only 168 tokens, and the reader output:"
            )
            st.info("\"nomination for Best Adapted Screenplay ... for Enemy.\" (F1 = 0.0)")
    with c2:
        with st.container(border=True):
            st.success("BEA-V2 Helpfulness Guidance")
            st.caption("P_help model recognized high multi-hop utility (P_help = 0.1259):")
            st.markdown(
                "The bridge sentence was prioritized and accepted at Step 1 with value 0.1521, "
                "packing 243 tokens and correctly yielding:"
            )
            st.info("\"...at the 27th Goya Awards for Invader (Invasor).\" (F1 = 1.0)")
            
    st.caption("Scientific qualification: BEA-V2's threshold was evaluated in an exploratory matched comparison. While it successfully rescued this bridge fact and led HotpotQA cells, zero comparisons survived Holm correction across the 24 paired tests.")
    
    # Advanced Details Expander
    with st.expander("Advanced Details · Mathematical Formulation & Logistic Model"):
        st.markdown(
            r'''
            BEA-V2 replaces heuristic relevance with a **Helpfulness-Weighted Transition Value**:
            
            $$v_t(a) = P_{\mathrm{help}}(a) \cdot \max(0, \mathrm{Rel}_t(a) + 0.5 \Delta\mathrm{Cov}_t(a) - 0.5 \mathrm{Red}_t(a))$$
            
            $$d_t(a) = \frac{v_t(a)}{\Delta c_t(a)}$$
            
            **The Helpfulness Model:**
            $P_{\mathrm{help}}(a) = \sigma(w_h^\top x_a + b_h)$ is an $L_2$-regularized logistic regression model ($C=1.0$, `lbfgs`) 
            trained with 5-fold `GroupKFold` cross-fitting on Leave-One-Out downstream utility labels.
            Features include:
            - Dense query-sentence similarity
            - Parent document retrieval rank and score
            - Normalized token length
            - Query aspect coverage gain
            '''
        )
        source('code')
