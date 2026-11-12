"""Visual UI components for Evidence Lab 2.0.

Provides consistent typography, cards, budget meters, and evidence visualizers
using native Streamlit components to prevent raw HTML leaking.
"""

from html import escape
from pathlib import Path
from typing import Optional, Dict, Any, List
import streamlit as st
from demo.constants import ROOT, COLORS, SOURCES, EXPLANATIONS, LABELS, calculate_utilization
from demo.data_loader import provenance


def source(*names):
    """Render provenance artifact links in an expandable container."""
    with st.expander('Research Provenance · Primary Frozen Artifacts', expanded=False):
        for name in names:
            try:
                info = provenance(name)
                st.code(info['path'], language=None)
                st.caption(f"SHA256 {info['sha256'][:16]}… · frozen research record")
            except (ValueError, FileNotFoundError, KeyError):
                st.caption(f"Source: {SOURCES.get(name, name)}")


def hero(compact=False):
    """Main application hero banner rendered using native Streamlit typography."""
    if compact:
        st.caption("CS787 · Generative AI · IIT Kanpur")
        st.subheader("Evidence Lab")
        st.markdown("*Understanding how language models select useful information under limited context budgets.*")
        return

    st.caption("CS787 Course Project · Generative AI · IIT Kanpur")
    st.title("Evidence Lab 2.0")
    st.markdown(
        "**When a language model has limited space to read retrieved documents, "
        "which evidence should we select, how much should we include, and how should we represent it?**"
    )
    st.markdown(
        "An interactive research demonstrator investigating Query-Conditioned Budget-Aware Evidence Allocation "
        "across Multi-Hop QA (HotpotQA), Long-Form Scientific QA (QASPER), and Scientific Claim Verification (SciFact)."
    )


def pipeline_flow():
    """Five-stage beginner-friendly RAG pipeline display using native container cards."""
    stages = [
        ("1. Question", "The user query or claim to be verified."),
        ("2. Retrieval", "Candidate documents surfaced by dense/BM25 retrieval."),
        ("3. Allocation", "Policy decides which pieces of text fit the budget limit."),
        ("4. Language Model", "Reader receives packed evidence in its prompt context."),
        ("5. Final Answer", "Reader model generates the response or categorical verdict.")
    ]
    
    st.markdown("#### The Evidence Allocation Pipeline")
    cols = st.columns(5)
    for col, (title, desc) in zip(cols, stages):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(desc)


def walkthrough_stepper(current_stage: int, total_stages: int = 5, labels: Optional[List[str]] = None):
    """Render a clean progress stepper for the guided walkthrough."""
    default_labels = [
        "1. Question",
        "2. Retrieved Info",
        "3. Evidence Budget",
        "4. Selected Evidence",
        "5. Generated Answer"
    ]
    labels = labels or default_labels
    
    cols = st.columns(len(labels))
    for i, (col, label) in enumerate(zip(cols, labels), 1):
        with col:
            with st.container(border=True):
                if i == current_stage:
                    st.markdown(f"**▶ {label}**")
                elif i < current_stage:
                    st.caption(f"✓ {label}")
                else:
                    st.caption(f"○ {label}")


def controlled_comparison_badge(is_controlled: bool = True, note_text: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
    """Display an explicit scientific validity badge using native callouts."""
    if is_controlled:
        st.success(
            "✓ **CONTROLLED MATCHED COMPARISON** — Identical Query, Candidate Retrieval Pool, Budget, Reader Model, Prompt Contract, and Decoding Configuration."
        )
        if metadata:
            with st.expander("Controlled Invariants Audit · Matched Experimental Parameters", expanded=False):
                st.json(metadata)
    else:
        note_str = f" — {note_text}" if note_text else " — Comparison differs across candidate retrieval pools, readers, or prompt configurations."
        st.warning(f"⚠ **HISTORICAL / EXPLORATORY COMPARISON**{note_str}")


def budget_meter(evidence, budget):
    """Visual progress meter for evidence token consumption with mathematically verified utilization."""
    evidence = int(evidence)
    budget = int(budget)
    pct = calculate_utilization(evidence, budget)
    ratio = min(1.0, max(0.0, evidence / budget)) if budget > 0 else 0.0
    is_starved = (pct < 35.0 and budget >= 512)
    
    st.progress(ratio, text=f"Evidence tokens: {evidence:,} / {budget:,} ({pct:.1f}% utilized)")
    if is_starved:
        st.caption(f"⚠ Context Starvation Alert: {budget - evidence:,} tokens ({100.0 - pct:.1f}%) left unused.")
    else:
        st.caption(f"Budget utilization: {pct:.1f}%. Tokens measure evidence content fed to reader.")


def note(text: str):
    """Callout box for explanations."""
    st.info(text)


def explanation(method: str):
    """Expandable explanation of how an algorithm selects evidence."""
    human_name = LABELS.get(method, method)
    with st.expander(f"How {human_name} allocates evidence"):
        st.write(EXPLANATIONS.get(method, 'Refer to official research algorithm specification.'))
        source('code')


def unit_card(u: Dict[str, Any], selected: bool = True, focus: bool = False):
    """Display an evidence unit with its status, metrics, and text using native components."""
    kind = u.get('display_kind') or u.get('granularity') or (u.get('source') or {}).get('unit_type') or u.get('unit_type', 'SENTENCE')
    text = u.get('text') or u.get('source_text') or 'Exact source text unavailable in retained artifacts.'
    if kind == 'PROPOSITION':
        kind = 'FINE-GRAINED SPAN'
        
    tokens = u.get('tokens') or u.get('token_count')
    rel = u.get('relevance') or u.get('score')
    doc_title = u.get('source_title') or u.get('document_id') or u.get('passage_id')
    is_decisive = u.get('is_decisive', False)
    
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            if is_decisive:
                status_str = "🔵 DECISIVE EVIDENCE"
            elif selected:
                status_str = "🟢 SELECTED"
            else:
                status_str = "⚪ OMITTED"
            st.markdown(f"**{status_str} · {kind.upper()}**" + (f" · *{doc_title}*" if doc_title else ""))
        with c2:
            st.caption(f"{int(tokens)} tokens" if tokens is not None else "")
            
        st.markdown(f'"{escape(text)}"')
        
        meta = []
        if rel is not None:
            meta.append(f"Relevance: {float(rel):.4f}")
        if u.get('reason'):
            meta.append(f"Reason: {u['reason']}")
        if meta:
            st.caption(" · ".join(meta))
