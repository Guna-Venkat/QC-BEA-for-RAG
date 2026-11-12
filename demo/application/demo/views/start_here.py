"""View 1 — Start Here: Guided Research Walkthrough for Evidence Lab 2.0.

Introduces the problem and guides the viewer through three real, frozen
experimental cases illustrating core scientific findings with circular stage navigation.
"""

from html import escape
import streamlit as st
from demo.components import hero, pipeline_flow, walkthrough_stepper, controlled_comparison_badge, unit_card
from demo.constants import calculate_utilization
from demo.curated_examples import (
    HOTPOT_BRIDGE_EXAMPLE,
    QASPER_STARVATION_EXAMPLE,
    SCIFACT_MATCHED_EXAMPLE
)


def _open_live_lab():
    # Button callbacks execute before the next run creates the sidebar radio.
    # Keep its widget value synchronized so it cannot route back to Start Here.
    st.session_state["workspace"] = "Live Lab"
    st.session_state["nav_workspace_radio"] = "Live Lab"
    st.query_params["workspace"] = "Live Lab"


def render():
    hero(compact=False)
    pipeline_flow()
    
    st.markdown("---")
    st.subheader("Interactive Research Examples")
    st.caption(
        "Select one of the three real research cases below to explore how evidence selection directly influences the model's answer."
    )
    
    # Initialize session state
    if "guided_example_id" not in st.session_state:
        st.session_state["guided_example_id"] = "hotpot"
    if "walkthrough_stage" not in st.session_state:
        st.session_state["walkthrough_stage"] = 1
        
    cols = st.columns(3)
    
    with cols[0]:
        with st.container(border=True):
            is_selected = (st.session_state["guided_example_id"] == "hotpot")
            st.caption("CASE 1 · MULTI-HOP REASONING")
            st.markdown("#### The Movie & Screenwriter Bridge")
            st.markdown(
                "Connecting *Enemy* to screenwriter Javier Gullón, and Gullón to his Goya nomination for *Invader (Invasor)*."
            )
            st.caption("Dataset: HotpotQA · Budget: 256 tokens")
            btn_label = "Explore Multi-Hop Case"
            if st.button(btn_label, key="btn_hotpot", width="stretch", type="primary" if is_selected else "secondary"):
                st.session_state["guided_example_id"] = "hotpot"
                st.session_state["walkthrough_stage"] = 1
                st.rerun()

    with cols[1]:
        with st.container(border=True):
            is_selected = (st.session_state["guided_example_id"] == "qasper")
            st.caption("CASE 2 · RESEARCH PAPER QA")
            st.markdown("#### The Five Binary Tasks")
            st.markdown(
                "Finding a decisive classification list inside a paper, and how an uncalibrated stopping rule starves the reader."
            )
            st.caption("Dataset: QASPER · Budget: 1024 tokens")
            btn_label = "Explore Starvation Case"
            if st.button(btn_label, key="btn_qasper", width="stretch", type="primary" if is_selected else "secondary"):
                st.session_state["guided_example_id"] = "qasper"
                st.session_state["walkthrough_stage"] = 1
                st.rerun()

    with cols[2]:
        with st.container(border=True):
            is_selected = (st.session_state["guided_example_id"] == "scifact")
            st.caption("CASE 3 · SCIENTIFIC VERIFICATION")
            st.markdown("#### TCR/CD3 Microdomains")
            st.markdown(
                "Verifying a biomedical claim where coarse allocation squeezes out decisive sentences under tight budgets."
            )
            st.caption("Dataset: SciFact · Budget: 256 tokens")
            btn_label = "Explore Microdomains Case"
            if st.button(btn_label, key="btn_scifact", width="stretch", type="primary" if is_selected else "secondary"):
                st.session_state["guided_example_id"] = "scifact"
                st.session_state["walkthrough_stage"] = 1
                st.rerun()

    st.markdown("---")
    
    # Load selected example data
    example_id = st.session_state["guided_example_id"]
    if example_id == "hotpot":
        data = HOTPOT_BRIDGE_EXAMPLE
    elif example_id == "qasper":
        data = QASPER_STARVATION_EXAMPLE
    else:
        data = SCIFACT_MATCHED_EXAMPLE
        
    stage = st.session_state["walkthrough_stage"]
    walkthrough_stepper(current_stage=stage, total_stages=5)
    
    # Render Stage Content
    st.markdown(f"### Stage {stage} · {get_stage_title(stage)}")
    
    if stage == 1:
        render_stage_1_question(data)
    elif stage == 2:
        render_stage_2_candidates(data)
    elif stage == 3:
        render_stage_3_budget(data)
    elif stage == 4:
        render_stage_4_selection(data)
    elif stage == 5:
        render_stage_5_answer(data)
        
    st.markdown("---")
    
    # Circular Navigation controls (Next / Previous / Restart)
    nav_left, _, nav_right = st.columns([1, 2, 1])
    with nav_left:
        if stage > 1:
            if st.button("← Previous Stage", width="stretch"):
                st.session_state["walkthrough_stage"] -= 1
                st.rerun()
    with nav_right:
        if stage < 5:
            if st.button("Next Stage →", type="primary", width="stretch"):
                st.session_state["walkthrough_stage"] += 1
                st.rerun()
        else:
            # Stage 5 circular loop back to Stage 1
            if st.button("↻ Restart Walkthrough", width="stretch"):
                st.session_state["walkthrough_stage"] = 1
                st.rerun()
                
    if stage == 5:
        st.markdown("---")
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown("#### Ready to test custom questions?")
            st.caption("Jump directly into the **Live Lab** to experiment with custom queries, passages, and evidence impact analysis.")
        with c2:
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.button("Open Live Lab →", type="primary", key="btn_go_to_live_lab",
                      on_click=_open_live_lab)


def get_stage_title(stage: int) -> str:
    titles = {
        1: "The Question & Reference Goal",
        2: "Retrieved Candidate Information",
        3: "The Evidence Budget Limit",
        4: "What the Algorithms Selected vs Omitted",
        5: "The Reader's Answer & Observed Outcome"
    }
    return titles.get(stage, "")


def render_stage_1_question(data):
    with st.container(border=True):
        st.caption(f"QUESTION / CLAIM UNDER INVESTIGATION ({data['dataset'].upper()})")
        st.markdown(f"### \"{data['question']}\"")
        st.markdown(f"**Verified Reference (Gold):** `{data['gold_reference']}`")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Dataset:** `{data['dataset']}`")
        st.markdown(f"**Query ID:** `{data['query_id']}`")
        st.markdown(f"**Target Budget:** `{data.get('budget', 256)}` tokens")
    with c2:
        st.markdown(f"**Controlled Reader:** `{data.get('reader', 'Qwen2.5-7B-Instruct')}`")
        st.caption("Reader decodes greedily (temperature = 0.0) under a strict task prompt contract.")
        
    st.markdown("#### The Reasoning Challenge:")
    st.info(data["challenge"])


def render_stage_2_candidates(data):
    passages = data.get("retrieved_passages", [])
    st.markdown(
        f"The retriever surfaced **{len(passages)} candidate documents**. "
        "Notice that some passages contain the decisive answer, while others contain topical distractors or general background:"
    )
    
    for p in passages:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                title_str = p.get("title", p.get("document_id", "Document"))
                st.markdown(f"**Rank {p['rank']}: {title_str}**")
            with c2:
                sim = p.get("similarity")
                sim_str = f"Similarity: {sim:.4f}" if sim else ""
                st.caption(f"{sim_str} · {p.get('tokens', 0)} tokens")
                
            st.markdown(f'"{p["text"]}"')
            if p.get("role"):
                st.caption(f"Role in Query: {p['role']}")


def render_stage_3_budget(data):
    budget = data["budget"]
    with st.container(border=True):
        st.markdown(f"#### Evidence Budget Limit: {budget} Tokens")
        st.markdown(
            "**What is a token?** A token is a subword piece of text (roughly 4 characters or 0.75 words).<br>"
            "**What does the budget limit?** The evidence budget limits how much retrieved text can be packed into the model's prompt. "
            "It does *not* restrict the length of the model's generated response.",
            unsafe_allow_html=True
        )
    
    st.markdown("#### The Evidence Allocation Dilemma:")
    st.markdown(
        f"The candidate pool contains more text than can fit into **{budget} tokens**. "
        "The system cannot simply dump all retrieved text into the prompt. It must select which evidence to keep:"
    )
    
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**Best Sentences**")
            st.caption("Extracts individual sentences from across candidates, ranks by query similarity, and packs fitting sentences.")
    with c2:
        with st.container(border=True):
            st.markdown("**QBGF (Knapsack)**")
            st.caption("Solves a Multiple-Choice Knapsack Problem, choosing representation fidelity (DROP, 1/2/4/8 sentences, FULL) per passage.")
    with c3:
        with st.container(border=True):
            st.markdown("**BEA-V1 & BEA-V2**")
            st.caption("Incrementally adds evidence with stopping rules (V1: marginal gain/cost ratio; V2: learned LOO helpfulness P_help).")


def render_stage_4_selection(data):
    st.markdown(
        "Here is the **actual evidence selected** by each allocation method from the saved execution records:"
    )
    
    methods = data.get("methods", {})
    method_keys = ["FIXED_SENTENCE", "QBGF_FULL", "BEA_QBGF_V1", "BEA_V2"]
    active_keys = [k for k in method_keys if k in methods]
    
    cols = st.columns(len(active_keys))
    for col, mkey in zip(cols, active_keys):
        m = methods[mkey]
        tokens_used = m["tokens_used"]
        budget = m["budget"]
        pct = calculate_utilization(tokens_used, budget)
        is_starved = m.get("status") == "CONTEXT_STARVATION"
        
        with col:
            with st.container(border=True):
                st.markdown(f"#### {m['name']}")
                st.caption(f"Evidence used: **{tokens_used} / {budget} tokens** ({pct:.1f}% utilized)")
                st.progress(min(1.0, tokens_used / budget))
                
                if is_starved:
                    st.warning("⚠ CONTEXT STARVATION (Early Stop)")
                elif m.get("score", 0) > 0:
                    st.success("✓ Decisive Evidence Included")
                else:
                    st.error("✗ Decisive Evidence Omitted")
                    
                st.caption(m["why"])
                
                # Expandable Selected Units
                sel_units = m.get("selected_units", [])
                with st.expander(f"View Selected Evidence ({len(sel_units)} units)", expanded=True):
                    for u in sel_units:
                        unit_card(u, selected=True)
                        
                # Expandable Omitted Units
                omit_units = m.get("omitted_units", [])
                if omit_units:
                    with st.expander(f"View Omitted Evidence ({len(omit_units)} units)", expanded=False):
                        for u in omit_units:
                            unit_card(u, selected=False)
                            
                # Exact Reconstructed / Serialized Context
                ser_context = m.get("serialized_context")
                if ser_context:
                    with st.expander("View Exact Evidence Sent to Reader", expanded=False):
                        st.caption("Exact serialized text packed into the reader prompt:")
                        st.text(ser_context)


def render_stage_5_answer(data):
    st.markdown("Here is what the language model answered after reading the selected evidence:")
    
    methods = data.get("methods", {})
    method_keys = ["FIXED_SENTENCE", "QBGF_FULL", "BEA_QBGF_V1", "BEA_V2"]
    active_keys = [k for k in method_keys if k in methods]
    
    cols = st.columns(len(active_keys))
    for col, mkey in zip(cols, active_keys):
        m = methods[mkey]
        score = m.get("score", 0.0)
        is_correct = score > 0.5
        
        with col:
            with st.container(border=True):
                st.markdown(f"#### {m['name']}")
                metric_name = m.get("metric", "Score")
                if is_correct:
                    st.success(f"**Score:** {score:.4f} ({metric_name})")
                else:
                    st.error(f"**Score:** {score:.4f} ({metric_name})")
                    
                st.caption("READER ANSWER:")
                st.info(f"\"{m['reader_output']}\"")
                
                st.caption(f"Outcome: **{m.get('outcome', 'Executed')}**")
                st.markdown(f"*{m['why']}*")
                
    with st.container(border=True):
        st.markdown("#### Scientific Takeaway:")
        if data["dataset"] == "HotpotQA":
            st.markdown(
                "In multi-hop reasoning, an allocator that omits a bridge sentence leaves the language model without "
                "the connecting logic, resulting in an incorrect answer (e.g. *Enemy* instead of *Invader (Invasor)*). "
                "BEA-V2's learned helpfulness model ($P_{\\mathrm{help}}$) promoted the bridge sentence at Step 1, rescuing the correct answer."
            )
        elif data["dataset"] == "QASPER":
            st.markdown(
                "Aggressive early stopping rules can cause **context starvation**: BEA-V1 halted at 245/1024 tokens "
                "because marginal relevance gain dropped below $\\tau = 0.010$, leaving 76.1% of the budget unused and missing the decisive classification list. "
                "The reader hallucinated stimulus words instead."
            )
        else:
            st.markdown(
                "In scientific claim verification, coarse whole-passage allocations upgrade surrounding background context "
                "to FULL, consuming the budget and squeezing out the single decisive sentence. Sentence selection and BEA-V2 "
                "preserved the decisive microdomain finding within 256 tokens, verifying the claim as SUPPORT."
            )
