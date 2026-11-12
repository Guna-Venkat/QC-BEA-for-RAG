"""View 2 — Compare Methods: Controlled Side-by-Side Experimental Interface.

Allows users to compare evidence selection, token utilization, and downstream
reader answers across Whole Passages, Best Sentences, QBGF, BEA-V1, and BEA-V2
using native Streamlit components.
"""

from html import escape
from typing import Dict, Any, List, Optional
import streamlit as st
from demo.constants import LABELS, EXPLANATIONS, COLORS, calculate_utilization
from demo.components import controlled_comparison_badge, budget_meter, unit_card
from demo.curated_examples import (
    HOTPOT_BRIDGE_EXAMPLE,
    QASPER_STARVATION_EXAMPLE,
    SCIFACT_MATCHED_EXAMPLE,
    SCIFACT_HARMFUL_LOO_EXAMPLE,
    QASPER_REI_EXAMPLE
)


FEATURED_CASES = {
    "hotpot_bridge": {
        "title": "HotpotQA · Multi-Hop Screenwriter & Movie Bridge (256 tok)",
        "dataset": "HotpotQA",
        "data": HOTPOT_BRIDGE_EXAMPLE
    },
    "qasper_starve": {
        "title": "QASPER · Binary Classification Tasks & Context Starvation (1024 tok)",
        "dataset": "QASPER",
        "data": QASPER_STARVATION_EXAMPLE
    },
    "scifact_matched": {
        "title": "SciFact · TCR/CD3 Microdomains Claim Verification (256 tok)",
        "dataset": "SciFact",
        "data": SCIFACT_MATCHED_EXAMPLE
    },
    "scifact_loo": {
        "title": "SciFact · Claim 343 Harmful Evidence LOO Ablation (256 tok)",
        "dataset": "SciFact",
        "data": SCIFACT_HARMFUL_LOO_EXAMPLE
    },
    "qasper_rei": {
        "title": "QASPER · Rei (2016) Model vs Manual Annotation Baseline (256 tok)",
        "dataset": "QASPER",
        "data": QASPER_REI_EXAMPLE
    }
}


def render():
    st.markdown("## Compare Methods")
    st.caption(
        "Side-by-side empirical comparison: What evidence did each method select, "
        "what did the language model actually see, and how did that change the generated answer?"
    )
    
    # Direct case selector — No historical queries toggle
    c1, c2 = st.columns([3, 1])
    with c1:
        case_key = st.selectbox(
            "Choose an Example",
            list(FEATURED_CASES.keys()),
            format_func=lambda k: FEATURED_CASES[k]["title"],
            key="featured_case_select"
        )
    
    case_info = FEATURED_CASES[case_key]
    case_data = case_info["data"]
    budget = case_data.get("budget", 256)
    
    with c2:
        st.markdown(f"**Budget Limit:** `{budget}` tokens")
        
    render_featured_case_comparison(case_data, budget)


def render_featured_case_comparison(data: Dict[str, Any], budget: int):
    # Question Header
    with st.container(border=True):
        st.caption(f"QUESTION UNDER STUDY ({data['dataset'].upper()})")
        st.markdown(f"### \"{data['question']}\"")
        st.markdown(f"**Verified Reference:** `{data['gold_reference']}`")
        
    meta = data.get("controlled_metadata")
    controlled_comparison_badge(is_controlled=bool(meta), metadata=meta)
    
    # Handle dedicated LOO ablation study
    if "methods" not in data and "loo_experiment" in data:
        render_scifact_loo_detail(data)
        return
        
    available_methods = list(data.get("methods", {}).keys())
    
    st.markdown("#### Choose Methods to Compare Side-by-Side")
    m_cols = st.columns(3)
    
    # Default selections
    def_m1 = "FIXED_SENTENCE" if "FIXED_SENTENCE" in available_methods else available_methods[0]
    def_m2 = "QBGF_FULL" if "QBGF_FULL" in available_methods else available_methods[min(1, len(available_methods)-1)]
    def_m3 = "BEA_V2" if "BEA_V2" in available_methods else ("BEA_QBGF_V1" if "BEA_QBGF_V1" in available_methods else "None")
    
    with m_cols[0]:
        m1 = st.selectbox("Left Method", available_methods, index=available_methods.index(def_m1), format_func=lambda m: LABELS.get(m, m), key="cmp_m1")
    with m_cols[1]:
        m2 = st.selectbox("Center Method", available_methods, index=available_methods.index(def_m2), format_func=lambda m: LABELS.get(m, m), key="cmp_m2")
    with m_cols[2]:
        options_m3 = ["None"] + available_methods
        idx3 = options_m3.index(def_m3) if def_m3 in options_m3 else 0
        m3 = st.selectbox("Right Method (Optional)", options_m3, index=idx3, format_func=lambda m: "None" if m == "None" else LABELS.get(m, m), key="cmp_m3")
        
    selected_methods = [m1, m2] + ([m3] if m3 != "None" else [])
    
    # Side-by-side comparison cards
    cards = st.columns(len(selected_methods))
    for col, mkey in zip(cards, selected_methods):
        m = data["methods"][mkey]
        with col:
            render_method_comparison_card(m, data, budget)
            
    # Evidence Visualization Legend
    st.markdown("---")
    render_evidence_legend()
    
    # Visual Evidence Inspector
    render_evidence_inspector(data, selected_methods)


def render_method_comparison_card(m: Dict[str, Any], data: Dict[str, Any], default_budget: int = 256):
    score = m.get("score", 0.0)
    is_correct = score > 0.5
    is_starved = m.get("status") == "CONTEXT_STARVATION"
    tokens_used = m.get("tokens_used", 0)
    budget = m.get("budget", default_budget)
    pct = calculate_utilization(tokens_used, budget)
    metric_label = m.get("metric", "Score")
    
    with st.container(border=True):
        c_title, c_score = st.columns([2, 1])
        with c_title:
            st.markdown(f"#### {m.get('name', 'Method')}")
        with c_score:
            if is_correct:
                st.success(f"{metric_label}: {score:.4f}")
            else:
                st.error(f"{metric_label}: {score:.4f}")
                
        # Token Meter
        ratio = min(1.0, max(0.0, tokens_used / budget)) if budget > 0 else 0.0
        st.progress(ratio, text=f"Evidence tokens: {tokens_used:,} / {budget:,} ({pct:.1f}% utilized)")
        if is_starved:
            st.warning(f"⚠ Early stop starved context: {budget - tokens_used:,} tokens ({100.0 - pct:.1f}%) unused.")
            
        st.caption("WHAT THE MODEL ANSWERED:")
        st.info(f"\"{m['reader_output']}\"")
        
        st.caption("WHY THE RESULT DIFFERED:")
        st.write(m.get("why", ""))
        
        st.caption(f"Outcome: **{m.get('outcome', 'Executed')}**")
        
        # Expandable inspection of selected evidence
        sel_units = m.get("selected_units", [])
        if sel_units:
            with st.expander(f"Inspect Selected Evidence ({len(sel_units)} units)", expanded=False):
                for u in sel_units:
                    unit_card(u, selected=True)
                    
        omit_units = m.get("omitted_units", [])
        if omit_units:
            with st.expander(f"Inspect Omitted Evidence ({len(omit_units)} units)", expanded=False):
                for u in omit_units:
                    unit_card(u, selected=False)


def render_evidence_legend():
    with st.container(border=True):
        st.markdown("**Evidence Status Color Legend:**")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown("🟢 **Selected Evidence**\n\nPacked into reader prompt")
        with c2:
            st.markdown("⚪ **Omitted Evidence**\n\nDropped / skipped by budget")
        with c3:
            st.markdown("🔵 **Decisive Evidence**\n\nContains ground-truth answer")
        with c4:
            st.markdown("🟠 **Warning**\n\nStarvation / threshold alert")
        with c5:
            st.markdown("🔴 **Harmful Unit**\n\nHurt score under LOO deletion")


def render_evidence_inspector(data: Dict[str, Any], selected_methods: List[str]):
    with st.expander("Evidence Inspector · Inspect Candidate Passages & Allocations", expanded=True):
        passages = data.get("retrieved_passages", [])
        if not passages:
            st.info("No raw passages stored for this example.")
            return
            
        for p in passages:
            is_decisive = p.get("has_decisive", False) or "Hop 2" in p.get("role", "")
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    badge_str = "🔵 DECISIVE PASSAGE" if is_decisive else f"RANK {p.get('rank', '?')}"
                    title_str = p.get("title", p.get("document_id", "Passage"))
                    st.markdown(f"**{badge_str} · {title_str}**")
                with c2:
                    sim = p.get("similarity")
                    sim_str = f"Relevance: {sim:.4f}" if sim else ""
                    st.caption(f"{sim_str} · {p.get('tokens', 0)} tokens")
                    
                st.markdown(f'"{p["text"]}"')
                if p.get("role"):
                    st.caption(f"Role: {p['role']}")


def render_scifact_loo_detail(data: Dict[str, Any]):
    loo = data["loo_experiment"]
    harmful = data["harmful_unit"]
    decisive = data["decisive_gold_unit"]
    
    st.markdown("### SciFact Claim 343 · Leave-One-Out (LOO) Attribution Case")
    st.caption(
        "This experiment measures what happens to the model's answer when we delete a single retrieved evidence sentence, "
        "without refilling the freed budget tokens (E \\ {u})."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.error("Pre-Ablation Context (165 Tokens) — 5 Units")
            st.caption("Contains 5 units including Harmful Unit #4074 (Relevance: 0.7882):")
            st.markdown(f'"{harmful["text"]}"')
            st.caption(f"Why Harmful: {harmful.get('why_harmful', '')}")
            st.markdown(f"**Reader Output:** `{loo['baseline_pre_ablation']['reader_output']}`")
            st.caption("Evaluation Correctness: **0.0000 (INCORRECT)**")
            
    with c2:
        with st.container(border=True):
            st.success("Post-Ablation Context (125 Tokens) — 4 Units")
            st.caption("Unit #4074 ablated without refilling freed budget:")
            st.markdown(f'"{decisive["text"]}"')
            st.caption("Retained Decisive Sentence (Relevance: 0.7610) directly supports the claim.")
            st.markdown(f"**Reader Output:** `{loo['ablated_post_ablation']['reader_output']}`")
            st.caption("Evaluation Correctness: **1.0000 (CORRECT)** · LOO Delta: **+1.0000 (HARMFUL UNIT)**")
            
    st.info(data.get("lesson", ""))
