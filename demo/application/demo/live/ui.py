"""Presentation UI for Evidence Lab 2.0 Live Lab.

Provides two distinct experimental actions:
- Action 1: Compare Four Methods (Best Sentences, QBGF, BEA-V1, BEA-V2)
- Action 2: Analyze Evidence Impact (Fresh Leave-One-Out deletions without refilling)

Preserves single-pipeline diagnostics and helper functions for regression compatibility.
"""

from html import escape
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import streamlit as st
from src.week12.protocol import digest

from demo.components import unit_card, budget_meter
from demo.constants import calculate_utilization
from .engine import METHODS, STAGES, parse_passages, validate, input_key, run, MAX_PASSAGES
from .resources import LiveResources, inventory
from .segmentation import MODES, ADAPTED, FROZEN
from .protocol import NATIVE, CONTROLLED, SCORING_MODES, assert_controlled_pair, validity, archive_obsolete
from .preset import load_preset, is_preset, passage_status, preset_cards
from .presentation import reader_answer_pair
from .history import remember, rows, differences
from .reference import evaluate as evaluate_reference, metrics_text
from .impact import (
    compare_four_methods,
    analyze_evidence_impact,
    rescore_existing_impact,
    score_answer,
    QA_LOO_EPSILON, comparison_input_id,
    CANONICAL_METHODS,
    METHOD_NAMES,
    METHOD_EXPLANATIONS
)

METHOD_LABELS = {
    'NONE': 'No Evidence',
    'RAW_SKIP': 'Whole passages · RAW_SKIP',
    'FIXED_SENTENCE': 'Best Sentences · FIXED_SENTENCE',
    'QBGF_FULL': 'Adaptive fidelity · QBGF',
    'BEA_V1': 'BEA-V1 · Dynamic Marginal',
    'BEA_V2': 'BEA-V2'
}

WHY = {
    'NONE': 'No retrieval or evidence allocation occurs. The reader answers from the query alone.',
    'RAW_SKIP': 'Entire passages are preserved, but a passage can only be included if it fits within the remaining evidence budget.',
    'FIXED_SENTENCE': 'Retrieved passages are decomposed into source-linked evidence units. Fitting relevant units are selected up to budget.',
    'QBGF_FULL': 'Each retrieved passage can be dropped, represented by selected sentences, or preserved in full, optimized jointly under one shared token budget.',
    'BEA_V1': 'Bottom-up marginal allocation halts when marginal utility per token drops below stopping threshold tau.',
    'BEA_V2': 'Learned helpfulness predictions (P_help) weight candidate gains, guiding incremental additions toward downstream utility.'
}

SAMPLE = [
    'The Helios laboratory compared three temperature sensors. Sensor A recorded measurements once every second. Its battery lasted twelve hours.',
    'Sensor B recorded a measurement every ten seconds. It had a battery life of forty-eight hours. The team selected it for remote deployments where replacing batteries was difficult.',
    'Sensor C sampled twice per second. It was used for short experiments where rapid changes mattered more than battery life.',
    'The remote field campaign lasted thirty-six hours. Its primary requirement was unattended operation for the entire campaign.',
    'The laboratory report also measured enclosure mass and calibration time. These were secondary requirements for the remote campaign.'
]

DEFAULT_SAMPLE_QUERY = "Which sensor was selected for remote deployment, and why?"


@st.cache_resource(show_spinner=False)
def resources():
    # A new manager is required after the strict reader-contract migration.
    manager = LiveResources()
    return manager


@st.cache_data(ttl=5, show_spinner=False)
def available():
    return inventory()


def pipeline_html(states):
    icons = {'pending': '○', 'processing': '◌', 'completed': '✓', 'failed': '!', 'skipped': '–'}
    return '<div class="live-pipeline">' + ''.join(
        '<div class="live-stage ' + states[s]['state'] + '"><b>' + icons[states[s]['state']] + '</b><span>' + s + '</span><small>' + escape(states[s]['state']) + '</small></div>'
        for s in STAGES
    ) + '</div>'


def candidate_table(r):
    selected = {u['passage_id'] for u in r['selection']['units']}
    return pd.DataFrame([
        dict(
            Rank=x['rank'],
            Passage=x['unit']['document_id'],
            Relevance=round(x['score'], 5),
            Tokens=x['unit']['token_count'],
            Status='Exposed' if x['unit']['unit_id'] in selected else 'Candidate — not exposed' if x['in_pool'] else 'Outside top-10 pool'
        )
        for x in r['ranking']
    ])


def evidence_card(r, technical=False):
    st.caption('LIVE CUSTOM RUN')
    st.markdown('#### Model Answer')
    if r['answer'] is None:
        st.info('Reader generation unavailable in this environment. The evidence pipeline completed and the exact context is available below.')
    else:
        st.write(r['answer'])
    if is_preset(r['query'], r['passages']):
        st.caption('Preset Reference Answer comparison · user-supplied demonstration reference, not official gold.')
        st.caption(metrics_text(r))
        with st.expander('Preset Reference Answer and required-facts checklist'):
            st.write(load_preset()['reference']['answer'])
            metrics = evaluate_reference(r)
            if metrics is not None:
                st.dataframe(pd.DataFrame(metrics['checklist']), hide_index=True, width='stretch')
            else:
                st.write([f['text'] for f in load_preset()['reference']['required_facts']])
    else:
        st.caption('No gold-reference evaluation is available for custom LiveDemo queries.')
    st.markdown('#### Evidence Budget')
    budget_meter(r['selection']['evidence_tokens'], r['budget'])
    c = st.columns(4)
    for col, label, value in zip(c, ['Source tokens', 'Evidence units', 'Prompt tokens', 'Generated tokens'], [r['source_tokens'], len(r['selection']['units']), r['prompt_tokens'], r['generated_tokens'] if r['generated_tokens'] is not None else '—']):
        col.metric(label, value)
    st.markdown('#### Exact Evidence Sent to the Reader' if r['answer'] is not None else '#### Exact Evidence Prepared for the Reader')
    if r['method'] == 'NONE':
        st.info('No external evidence was supplied. The reader is configured to use only the query and its pretrained knowledge.')
    elif not r['selection']['units']:
        st.info('No evidence unit fit this allocation; the prepared reader context is empty.')
    else:
        st.code(r['selection']['text'], language=None)
        for u in r['selection']['units']:
            unit_card(u)


def show_result(r, technical=False):
    st.subheader('User Query'); st.write(r['query'])
    st.caption('LIVE CUSTOM RUN · Segmentation: ' + ('Citation/Markdown-aware Live' if r.get('segmentation') == ADAPTED else 'Frozen research splitter'))
    st.caption('CONTROLLED RETRIEVER EFFECT · Only candidate retrieval differs.' if r.get('scoring_mode') == CONTROLLED else 'Pipeline-native comparison · Retriever and downstream relevance scoring may both differ.')
    st.caption(f"{METHOD_LABELS.get(r['method'], r['method'])} · {r['retriever'] if r['method'] != 'NONE' else 'Retrieval skipped'} · {r['budget']} evidence-token budget")
    if r.get('ranking'):
        st.subheader('Retrieved Candidate Pool')
        st.dataframe(candidate_table(r), hide_index=True, width='stretch')
        for x in r['ranking']:
            with st.expander(f"#{x['rank']} · {x['unit']['document_id']} · {'candidate' if x['in_pool'] else 'outside top-10'}"):
                st.caption(f"Relevance {x['score']:.4f} · {x['unit']['token_count']} source tokens")
                st.write(x['unit']['source_text'])
    evidence_card(r, technical)
    if r.get('allocation_trace'):
        with st.expander('How the budget was allocated', expanded=r['method'] in ('RAW_SKIP', 'QBGF_FULL')):
            st.dataframe(pd.DataFrame(r['allocation_trace']), hide_index=True, width='stretch')
    st.subheader('What happened in this run?')
    for line in r.get('explanation', []):
        st.write(line)
    if r['method'] in WHY:
        with st.expander('Why does this method behave this way?', expanded=True):
            st.write(WHY[r['method']])


def render_history(history, technical=False):
    """Render saved pairs with the existing evidence cards; no execution path."""
    st.divider()
    st.subheader('Run History / Comparison Tray')
    st.caption('Last 30 distinct runs in this browser session. Select any two to inspect saved results without new model calls. Context-only runs are marked explicitly.')
    summary = rows(history)
    if not summary:
        st.info('Complete a live pipeline run to start your history.')
        return
    st.dataframe(pd.DataFrame(summary), hide_index=True, width='stretch', row_height=90,
                 column_config={'Answer': st.column_config.TextColumn('Saved answer', width='large'),
                                'Metrics': st.column_config.TextColumn('Reference metrics', width='large')})
    if any(row['Run'] == 0 for row in summary):
        st.caption('Row 0 is the Preset Reference Answer, not a generated run. Metrics apply only to runs with the exact frozen preset query and passages. Other inputs remain unscored.')
        with st.expander('Preset reference · metric definitions and required facts'):
            st.write(load_preset()['reference']['answer'])
            for fact in load_preset()['reference']['required_facts']:
                st.write('• ' + fact['text'])
    entries = {e['number']: e for e in history if validity(e['result']) is None}
    if len(entries) < 2:
        st.caption('Run another method, budget or retriever to compare two saved runs.')
        return
    def label(n):
        r = entries[n]['result']
        return f"Run {n} · {r['retriever']} · {r['method']} · {r['budget']}"
    picked = st.multiselect('Select two saved runs', list(entries), format_func=label,
                            max_selections=2, key='live_history_picked')
    if st.button('Compare Selected Runs', disabled=len(picked) != 2):
        st.session_state['live_history_pair'] = tuple(picked)
    pair = st.session_state.get('live_history_pair', ())
    if len(pair) != 2 or any(n not in entries for n in pair):
        return
    a, b = [entries[n]['result'] for n in pair]
    changed = differences(a, b)
    st.caption('Changed: ' + (', '.join(changed) if changed else 'no recorded configuration fields') + '.')
    for col, n, r in zip(st.columns(2), pair, [a, b]):
        with col:
            st.markdown('### ' + label(n))
            st.write(r['query'])
            st.caption('Segmentation: ' + r['segmentation'] + ' · Scoring: ' + r['scoring_mode'])
            evidence_card(r, technical)


def same_custom_inputs(a, b):
    return all(a.get(k) == b.get(k) for k in ('query', 'passages', 'budget', 'segmentation', 'device'))


def render(technical=False, presentation=True):
    """Evidence Lab 2.0 Live Lab Interface."""
    st.markdown("### Live Lab: Interactive Evidence Allocation & Impact Analysis")
    st.caption(
        "Bring your own questions and passages. Compare available research evidence policies under a strict SFR scoring contract, "
        "and experimentally test how removing evidence changes the language model's answer."
    )
    
    pool = resources()
    inv = available()
    
    # -------------------------------------------------------------
    # Session State Initialization for Dynamic Passages
    # -------------------------------------------------------------
    if "live_passages_data" not in st.session_state:
        previous_ids = st.session_state.get("live_passage_ids", [])
        if previous_ids and all(f"live_passage_{i}" in st.session_state for i in previous_ids):
            st.session_state["live_passages_data"] = [
                {"id": i, "title": f"Passage {n+1}", "text": st.session_state[f"live_passage_{i}"]}
                for n,i in enumerate(previous_ids)]
        else:
            preset = load_preset()
            st.session_state["live_passages_data"] = preset_cards(preset)
            st.session_state.setdefault("live_query", preset["query"])
    st.session_state.setdefault("live_query", "")
    st.session_state.setdefault("live_user_query", st.session_state["live_query"])
    for i,item in enumerate(st.session_state["live_passages_data"]):
        item.setdefault("id", i)
        st.session_state.setdefault(f"live_passage_{item['id']}", item["text"])
    st.session_state["live_passage_ids"] = [p["id"] for p in st.session_state["live_passages_data"]]
    st.session_state["live_next_id"] = max(st.session_state.get("live_next_id",0),
        max(st.session_state["live_passage_ids"],default=-1)+1)

    # Callback handlers for preset loading
    def _on_load_preset():
        preset = load_preset()
        st.session_state["live_passages_data"] = preset_cards(preset)
        st.session_state["live_query"] = preset["query"]
        st.session_state["live_user_ref_text"] = preset["reference"]["answer"]
        st.session_state["live_passage_ids"] = list(range(len(preset["passages"])))
        st.session_state["live_next_id"] = len(preset["passages"])
        for i, p in enumerate(preset["passages"]):
            st.session_state[f"live_passage_{i}"] = p
        st.session_state.pop("live_four_results", None)
        st.session_state.pop("live_impact_results", None)

    # -------------------------------------------------------------
    # SECTION 1: Enter Your Question
    # -------------------------------------------------------------
    st.markdown("#### 1. Ask a Question")
    user_query = st.text_area(
        "Your query",
        height=75,
        max_chars=2000,
        key="live_query",
        help="Natural language question or claim to investigate."
    )
    st.session_state["live_user_query"] = user_query
    
    # -------------------------------------------------------------
    # SECTION 2: Source Passages
    # -------------------------------------------------------------
    st.markdown("#### 2. Source Passages")
    st.caption("Add, edit, or remove passages. Stable identifiers are assigned automatically.")
    
    passages_list = st.session_state["live_passages_data"]
    
    # Preset loaders
    st.button("Budget-sensitive multi-aspect question", on_click=_on_load_preset, key="live_world_cup_preset", help="Load the original World Cup example with 15 source passages.")
            
    # Compact editable cards; titles do not enter retrieval/reader evidence.
    try:
        source_tokenizer=pool.tokenizer()
    except Exception:
        source_tokenizer=None
    for idx,p_item in enumerate(passages_list):
        key=f"live_passage_{p_item['id']}"
        current=st.session_state.get(key,p_item.get('text',''))
        n=len(source_tokenizer.encode(current,add_special_tokens=False)) if source_tokenizer else None
        label=f"P{idx+1} — {p_item.get('title',f'Passage {idx+1}')} · {n if n is not None else 'Unknown'} tokens"
        with st.expander(label,expanded=False):
            st.caption("Source text · edit below. Passage title is a display label only.")
            p_item['text']=st.text_area(f"Passage {idx+1}",height=180,key=key,max_chars=8000)
            if len(passages_list)>1 and st.button('Remove',key=f"btn_remove_passage_{p_item['id']}"):
                passages_list.pop(idx)
                st.session_state['live_passages_data']=passages_list
                st.session_state['live_passage_ids']=[p['id'] for p in passages_list]
                st.rerun()

    if st.button("+ Add Passage", key="btn_add_passage", disabled=len(passages_list) >= MAX_PASSAGES):
        passages_list.append({"id": st.session_state["live_next_id"], "title": f"Passage {len(passages_list)+1}", "text": ""})
        st.session_state["live_passages_data"] = passages_list
        st.session_state["live_passage_ids"] = [p["id"] for p in passages_list]
        st.session_state["live_next_id"] += 1
        st.rerun()
        
    usable_passages = [p["text"].strip() for p in passages_list if p.get("text", "").strip()]
    tot_chars = sum(len(p) for p in usable_passages)
    st.caption(f"{len(usable_passages)} active passages loaded ({tot_chars:,} characters total).")
    
    # -------------------------------------------------------------
    # SECTION 3: Optional Reference Answer & Task Selector
    # -------------------------------------------------------------
    st.markdown("#### 3. Expected Answer (Optional)")
    r_cols = st.columns([2, 3])
    with r_cols[0]:
        task_format = st.selectbox(
            "Task Format",
            ["Question Answering (Token-F1)", "Scientific Claim Verification (Categorical)"],
            index=0,
            key="live_task_format"
        )
        task_key = "verification" if "Claim" in task_format else "qa"
        
    with r_cols[1]:
        ref_placeholder = "e.g. 12 groups of 4 teams, 104 matches, collusion risk." if task_key == "qa" else "SUPPORT, REFUTE, or NOT_ENOUGH_INFO"
        user_reference = st.text_area(
            "User-Provided Reference Answer (Optional)",
            height=70,
            placeholder=ref_placeholder,
            key="live_user_ref_text",
            help="If provided, model answers are evaluated against it, and Leave-One-Out deletions test if evidence helped or hurt."
        )
    st.caption(
        "User-Provided Reference Answer: If you provide an expected answer, the application evaluates agreement and tests whether "
        "removing specific evidence improves or hurts the response. Comparison works without a reference answer."
    )
    
    # -------------------------------------------------------------
    # Operational Settings & Safeties
    # -------------------------------------------------------------
    st.markdown("#### Operational Controls")
    ctl_cols = st.columns(4)
    with ctl_cols[0]:
        budget = st.selectbox("Evidence Token Budget", [256, 1024], index=0, key="live_budget")
    with ctl_cols[1]:
        try:
            import torch
        except ImportError:
            torch = None
        default_dev_idx = 1 if torch is not None and torch.cuda.is_available() and inv.get("gpu_free_mib") is not None else 0
        if torch is None:
            st.caption("Install requirements-live.txt for model execution; saved examples remain available.")
        device = st.selectbox(
            "Execution Device",
            ["cpu", "cuda"],
            index=default_dev_idx,
            format_func=lambda d: "CPU (Sequential FP16)" if d == "cpu" else "GPU (CUDA FP16)",
            key="live_device"
        )
        if hasattr(pool, "set_device"):
            pool.set_device(device)
    with ctl_cols[2]:
        enable_models = st.toggle(
            "Enable Live Models",
            value=st.session_state.get("live_models_enabled", False),
            key="live_models_enabled",
            help="Opt in to local SFR/Qwen inference. When disabled, displays exact prepared evidence contexts."
        )
    with ctl_cols[3]:
        loo_depth = st.slider("LOO Depth (Units tested)", min_value=1, max_value=3, value=1, key="live_loo_depth")

    # -------------------------------------------------------------
    # SECTION 4: Two Action Buttons
    # -------------------------------------------------------------
    st.markdown("---")
    act_c1, act_c2 = st.columns(2)
    
    with act_c1:
        run_compare_btn = st.button(
            "◈ Compare Four Methods",
            type="primary",
            width="stretch",
            help="Run qualified methods with canonical SFR scores. Unqualified methods are explicitly unavailable."
        )
    with act_c2:
        run_impact_btn = st.button(
            "◈ Analyze Evidence Impact",
            width="stretch",
            help="Perform fresh Leave-One-Out evidence removals without refilling budget."
        )
        
    # Execute Action 1: Four-Method Comparison
    if run_compare_btn:
        if not user_query.strip():
            st.error("Please enter a question before running.")
            return
        if not usable_passages or any(not p.get("text", "").strip() for p in passages_list):
            st.error("Fill every source passage or remove empty passage cards.")
            return
            
        with st.spinner("Executing 4-method comparison under shared budget..."):
            try:
                cmp_res = compare_four_methods(
                    query=user_query,
                    passages=usable_passages,
                    budget=budget,
                    task_format=task_key,
                    user_reference=user_reference,
                    resources=pool,
                    enable_models=enable_models,
                    cache=st.session_state.setdefault("live_generation_cache", {})
                )
                st.session_state["live_four_results"] = cmp_res
                st.session_state.pop("live_impact_results", None)
            except Exception as exc:
                st.error(f"Method comparison failed: {exc}")
                
    # Bind intervention analysis to the exact saved run and active reader contract.
    saved = st.session_state.get("live_four_results")
    stale = bool(saved and "version" not in saved)
    if saved and saved.get("run_id"):
        try:
            current_id = comparison_input_id(user_query, usable_passages, budget, task_key, pool)
            stale = saved.get("run_id") != current_id
        except Exception:
            stale = True
        if stale:
            st.warning("Inputs or reader configuration changed. Rerun Compare Four Methods before analyzing evidence impact.")

    # Execute Action 2: Evidence Impact Analysis
    if run_impact_btn:
        cmp_res = st.session_state.get("live_four_results")
        if stale:
            st.error("Analysis blocked: the saved comparison does not match the current inputs/reader.")
        elif not cmp_res:
            st.warning("Please click 'Compare Four Methods' first before analyzing evidence impact.")
        elif not user_reference or not user_reference.strip():
            st.warning("Reference answer required: Please provide a reference answer to evaluate whether removing evidence improves or worsens the generated response. Evidence impact analysis (Leave-One-Out) calculates the change in answer quality: Δi = S(y_-i) - S(y_full). Without a reference answer, downstream quality cannot be scored.")
        elif not any(m.get("answer") for m in cmp_res.get("methods", {}).values() if isinstance(m, dict)):
            st.warning("Reader inference required: Evidence selection has completed, but the language model has not generated answers for the candidate configurations. Leave-One-Out evidence impact analysis measures the change in reader answer quality (Δi = S(y_-i) - S(y_full)). Enable Live Model Inference in the sidebar or evaluate a configuration with generated reader outputs before analyzing evidence impact.")
        else:
            with st.spinner(f"Performing Leave-One-Out interventions on top {loo_depth} unit(s) per method..."):
                try:
                    impact_cache = st.session_state.setdefault("live_loo_cache", {})
                    impact_res = analyze_evidence_impact(
                        comparison_results=cmp_res,
                        user_reference=user_reference.strip(),
                        top_n_units=loo_depth,
                        resources=pool,
                        enable_models=enable_models,
                        cache=impact_cache
                    )
                    st.session_state["live_impact_results"] = impact_res
                    st.rerun()
                except Exception as exc:
                    st.error(f"Evidence impact analysis failed: {exc}")

    # -------------------------------------------------------------
    # SECTION 5: Results Display — Four Method Cards
    # -------------------------------------------------------------
    cmp_res = st.session_state.get("live_four_results")
    if cmp_res:
        st.markdown("### Four-Method Evidence Allocation Comparison")
        st.caption(
            f"Query: \"{escape(cmp_res['query'])}\" · Budget: {cmp_res['budget']} tokens · "
            f"Shared Candidates: {len(cmp_res['pool'])} passages · Task: {cmp_res['task_format'].upper()}"
        )
        
        current_ref = user_reference.strip()
        last_ref = (cmp_res.get("user_reference") or "").strip()
        if current_ref and current_ref != last_ref and not stale:
            if st.button("↻ Rescore Answers with Updated Reference", key="btn_rescore_methods"):
                for mdata in cmp_res.get("methods", {}).values():
                    if mdata.get("answer"):
                        mdata["evaluation"] = score_answer(mdata["answer"], current_ref, task_key)
                cmp_res["user_reference"] = current_ref
                if "live_impact_results" in st.session_state:
                    st.session_state["live_impact_results"] = rescore_existing_impact(
                        st.session_state["live_impact_results"], current_ref, task_key
                    )
                st.rerun()

        method_keys = ["FIXED_SENTENCE", "QBGF", "BEA_V1", "BEA_V2"]
        cols = st.columns(4)
        for col, mkey in zip(cols, method_keys):
            mdata = cmp_res.get("methods", {}).get(mkey, {})
            with col:
                render_live_method_card(mdata, cmp_res)
                
    # -------------------------------------------------------------
    # SECTION 6: Results Display — LOO Evidence Impact Analysis
    # -------------------------------------------------------------
    impact_res = st.session_state.get("live_impact_results")
    if impact_res:
        st.markdown("---")
        render_live_impact_results(impact_res)
        
    # -------------------------------------------------------------
    # Single-Pipeline Diagnostics (Preserved for compatibility)
    # -------------------------------------------------------------
    with st.expander("Single-Method Diagnostics & Advanced Pipeline Controls", expanded=False):
        render_single_pipeline_diagnostic(pool, inv, device, enable_models, technical)


def render_live_method_card(mdata: Dict[str, Any], cmp_res: Dict[str, Any]):
    """Render a clean card for one of the four canonical methods using native components."""
    mname = mdata.get("name", "Method")
    tokens_used = mdata.get("evidence_tokens", 0)
    budget = cmp_res.get("budget", 256)
    pct = calculate_utilization(tokens_used, budget)
    units = mdata.get("units", [])
    stopped_early = mdata.get("stopped_early", False)
    answer = mdata.get("answer")
    eval_info = mdata.get("evaluation")
    
    with st.container(border=True):
        if mdata.get("error"):
            st.markdown(f"#### {mname}")
            st.warning("Method unavailable: " + mdata["error"])
            return
        c_title, c_badge = st.columns([2, 1])
        with c_title:
            st.markdown(f"#### {mname}")
        with c_badge:
            if stopped_early:
                st.warning("Early Stop")
            else:
                st.success("Within Token Budget")
                
        st.caption(f"Evidence used: **{tokens_used} / {budget} tokens** ({pct:.1f}% utilized)")
        st.progress(min(1.0, max(0.0, tokens_used / budget)) if budget > 0 else 0.0)
        
        if answer:
            st.caption("READER ANSWER:")
            st.info(f"\"{answer}\"")
            if eval_info:
                st.caption(f"**Evaluation ({eval_info.get('metric', 'Score')}):** {eval_info.get('score', 0.0):.4f}")
        else:
            st.caption("READER OUTPUT UNAVAILABLE:")
            if mdata.get("reader_error"): st.warning(mdata["reader_error"])
            st.markdown("*Evidence selection completed. Enable live model inference and run the reader to generate an answer.*")
            st.caption("Evaluation: *Inference not executed; answer quality has not been evaluated.*")
            
        if mdata.get("method") == "BEA_V2" and mdata.get("execution_metadata"):
            with st.expander("Advanced details · BEA-V2 execution"):
                meta=mdata['execution_metadata']
                st.json({k:meta[k] for k in ['threshold','models','policy','parameters','manifest_sha256','calibration_status'] if k in meta})
        if mdata.get("receipt"):
            with st.expander(f"{mname} inference receipt"):
                st.caption("Session-only request; cached" if mdata["receipt"].get("cache_hit") else "Fresh reader request; session-only receipt")
                st.json(mdata["receipt"])
        st.caption(f"Evidence Selection: **{len(units)} units** from **{len({u.get('document_id', u.get('passage_id')) for u in units})} sources**")
        
        with st.expander(f"Inspect {mname} Evidence ({len(units)} units)", expanded=False):
            st.caption(mdata.get("explanation", ""))
            for u in units:
                unit_card(u, selected=True)


def render_live_impact_results(impact_res: Dict[str, Any]):
    """Render Section 6: Leave-One-Out Evidence-Impact Results."""
    st.markdown("### Evidence Impact Analysis: Leave-One-Out Interventions")
    st.caption(
        "Each tested evidence unit was deleted from the prompt context WITHOUT refilling freed tokens (E \\ {u}). "
        "The reader regenerated its answer, and the score change Δ = Score(E \\ {u}) - Score(E) reveals whether that evidence helped, hurt, or had no effect. "
        f"Live LOO threshold: {0.0 if impact_res.get('task_format') == 'verification' else QA_LOO_EPSILON:g} score units (strict inequality). "
        "Historical W12 attribution used zero tolerance and the reverse importance sign. "
        "Only the first selected source-order units are tested; this is not exhaustive LOO."
    )
    
    impact_by_method = impact_res.get("impact_by_method", {})
    all_tested = []
    
    for mkey, mres in impact_by_method.items():
        if mres.get("error"): st.warning(f"{METHOD_NAMES.get(mkey,mkey)}: {mres['error']}")
        mname = METHOD_NAMES.get(mkey, mkey)
        for uinfo in mres.get("units_analyzed", []):
            all_tested.append(dict(mname=mname, **uinfo))
            
    if not all_tested:
        st.info("No evidence units were eligible for deletion analysis.")
        return
        
    helpful_count = sum(1 for x in all_tested if x.get("effect") == "HELPFUL")
    harmful_count = sum(1 for x in all_tested if x.get("effect") == "HARMFUL")
    neutral_count = sum(1 for x in all_tested if x.get("effect") == "NO_MEASURABLE_CHANGE")
    
    failed_count = sum(1 for x in all_tested if x.get("effect") == "UNAVAILABLE")
    s_cols = st.columns(5)
    s_cols[0].metric("Total Deletions Attempted", len(all_tested))
    s_cols[1].metric("Helpful Units", helpful_count, help="Removing them reduced answer score (presence was helpful)")
    s_cols[2].metric("Harmful Units", harmful_count, help="Removing them improved answer score (presence was harmful)")
    s_cols[3].metric("Neutral Units", neutral_count, help="Removing them produced no measurable score change")
    s_cols[4].metric("Failed / Unavailable", failed_count)
    
    rows_data = []
    for x in all_tested:
        rows_data.append({
            "Method": x["mname"],
            "Source": x.get("passage_id", "P?"),
            "Removed Unit Text": (x.get("text", "")[:75] + "…") if len(x.get("text", "")) > 75 else x.get("text", ""),
            "Original Score": f"{x['original_score']:.3f}" if x.get("original_score") is not None else "Unavailable",
            "Score After Removal": f"{x['ablated_score']:.3f}" if x.get("ablated_score") is not None else "Unavailable",
            "Delta (Δ)": f"{x['loo_delta']:+.3f}" if x.get("loo_delta") is not None else "Unavailable",
            "Observed Effect": x["effect"]
        })
    st.dataframe(pd.DataFrame(rows_data), hide_index=True, width="stretch")
    
    all_tested = [x for x in all_tested if x.get("status") == "COMPLETE"]
    if not all_tested:
        st.warning("No valid intervention pair is available. Technical failures are not evidence effects.")
        return
    st.markdown("#### Before / After Answer Comparison")
    st.caption("Select a tested evidence unit to inspect the exact context change and reader response difference.")
    
    def format_unit_label(u: Dict[str, Any]) -> str:
        doc_id = u.get("document_id") or u.get("passage_id") or "P?"
        kind = u.get("unit_type", "SENTENCE")
        order = u.get("document_order")
        if kind == "PASSAGE":
            return f"{doc_id} — Full Passage"
        elif isinstance(order, (list, tuple)) and len(order) >= 3:
            sent_num = order[2] + 1
            return f"{doc_id} — Sentence {sent_num}"
        else:
            return f"{doc_id} — Sentence"
    
    unit_labels = [
        f"[{x.get('method_name', x.get('mname'))}] {format_unit_label(x.get('unit') or x)}: {x.get('text', '')[:60]}…"
        for x in all_tested
    ]
    sel_idx = st.selectbox(
        "Select Evidence Intervention to Inspect",
        range(len(all_tested)),
        format_func=lambda i: unit_labels[i],
        key="loo_selected_unit_idx"
    )
    
    chosen = all_tested[sel_idx]
    with st.expander("Exact original and ablated inference receipts"):
        st.json({"original": chosen.get("original_receipt"), "ablated": chosen.get("receipt")})
    method_name = chosen.get("method_name") or chosen.get("mname") or "Method"
    removed_unit = chosen.get("unit") or chosen
    p_id = chosen.get("passage_id") or removed_unit.get("document_id") or "Passage"
    budget = chosen.get("budget", 256)
    orig_tokens = chosen.get("original_tokens", 0)
    rem_tokens = chosen.get("remaining_tokens", chosen.get("ablated_tokens", 0))
    freed_tokens = chosen.get("freed_tokens", max(0, orig_tokens - rem_tokens))

    st.markdown(f"## Selected Method: {method_name}")
    st.markdown(f"**Evidence removed from:** {p_id}")

    # -------------------------------------------------------------
    # ① Original Evidence Sent to Reader
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown("### ① Original Evidence Sent to Reader")
        pct_orig = (orig_tokens / budget * 100) if budget else 0.0
        st.caption(f"Evidence tokens: **{orig_tokens} / {budget}** ({pct_orig:.1f}% utilized)")
        
        orig_units = chosen.get("original_units") or []
        if orig_units:
            for u in orig_units:
                u_lbl = format_unit_label(u)
                u_tok = u.get("token_count", 0)
                is_target = (u.get("unit_id") == chosen.get("unit_id"))
                if is_target:
                    st.markdown(f"**{u_lbl}** ({u_tok} tokens) · *[Target for LOO removal]*")
                    st.info(f"\"{u.get('source_text', '')}\"")
                else:
                    st.markdown(f"**{u_lbl}** ({u_tok} tokens)")
                    st.markdown(f"> {u.get('source_text', '')}")
                    
            with st.expander("View Exact Serialized Evidence (Original)", expanded=False):
                st.caption("Exact serialized text supplied to the reader prompt before LOO removal:")
                st.code(chosen.get("original_serialized_text") or "\n\n".join(u.get("source_text", "") for u in orig_units), language=None)
        else:
            st.info("Original evidence context not recorded.")

    # -------------------------------------------------------------
    # ② Removed Evidence
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown("### ② Removed Evidence")
        u_lbl = format_unit_label(removed_unit)
        u_tok = chosen.get("token_count", 0)
        uid = chosen.get("unit_id", "")
        
        st.markdown(f"**REMOVED — {u_lbl}**")
        st.caption(f"Source: **{p_id}** · Unit Token Cost: **{u_tok} tokens** · Unit ID: `{uid}`")
        st.warning(f"\"{chosen.get('text', '')}\"")
        st.caption("This unit was deleted from the evidence context (E \\ {u}). No replacement evidence was added, and freed budget was not refilled.")

    # -------------------------------------------------------------
    # ③ Evidence Sent to Reader After Removal
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown("### ③ Evidence Sent to Reader After Removal")
        pct_rem = (rem_tokens / budget * 100) if budget else 0.0
        st.markdown(f"**Remaining evidence tokens: {rem_tokens} / {budget}** ({pct_rem:.1f}% utilized · {freed_tokens} tokens freed)")
        st.caption("The removed evidence unit does not appear below. This exact context was supplied to the reader to generate the ablated response.")
        
        target_uid = chosen.get("unit_id")
        rem_units = [u for u in (chosen.get("remaining_units") or []) if u.get("unit_id") != target_uid]
        
        if rem_units:
            for u in rem_units:
                u_lbl = format_unit_label(u)
                u_tok = u.get("token_count", 0)
                st.markdown(f"**{u_lbl}** ({u_tok} tokens)")
                st.markdown(f"> {u.get('source_text', '')}")
                
            with st.expander("View Complete Remaining Evidence", expanded=False):
                st.caption("Complete untruncated remaining evidence context:")
                for u in rem_units:
                    st.markdown(f"**{format_unit_label(u)}:** {u.get('source_text', '')}")
                    
            with st.expander("View Exact Serialized Evidence", expanded=False):
                st.caption("Exact serialized string supplied to the reader's evidence input field after removal:")
                st.code(chosen.get("remaining_serialized_text") or "\n\n".join(u.get("source_text", "") for u in rem_units), language=None)
        else:
            st.info("No remaining evidence units (context empty after removal).")

    # -------------------------------------------------------------
    # ④ Reader Answers
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown("### ④ Reader Answers")
        st.markdown(reader_answer_pair(chosen.get('original_answer'),chosen.get('ablated_answer'),
                       chosen.get('original_score'),chosen.get('ablated_score')),unsafe_allow_html=True)

    # -------------------------------------------------------------
    # ⑤ Evidence Impact
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown("### ⑤ Evidence Impact")
        eff = chosen.get("effect", "NO_MEASURABLE_CHANGE")
        delta = chosen.get("loo_delta", 0.0)
        orig_s = chosen.get("original_score", 0.0)
        abl_s = chosen.get("ablated_score", 0.0)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Original Score", f"{orig_s:.3f}")
        m2.metric("Score After Removal", f"{abl_s:.3f}")
        m3.metric("Score Difference (Δ)", f"{delta:+.3f}")
        m4.metric("Observed Effect", eff)
        
        if eff == "HELPFUL":
            st.success(f"**HELPFUL EVIDENCE:** {chosen['explanation']}")
        elif eff == "HARMFUL":
            st.error(f"**HARMFUL EVIDENCE:** {chosen['explanation']}")
        else:
            st.info(f"**NEUTRAL EVIDENCE:** {chosen['explanation']}")


def render_single_pipeline_diagnostic(pool, inv, device, enable, technical=False):
    """Preserved legacy single-pipeline runner for detailed step-by-step diagnostic audits."""
    st.subheader('Single-Method Pipeline Inspector')
    st.caption('Run a single algorithm step-by-step through retrieval, segmentation, allocation, and generation.')
    
    segmentation = st.selectbox(
        'Source segmentation',
        MODES if technical else (ADAPTED,),
        format_func=lambda m: 'Citation/Markdown-aware Live segmentation' if m == ADAPTED else 'Frozen research splitter · exact historical behavior',
        key='live_segmentation'
    )
    scoring_mode = st.selectbox(
        'Comparison protocol',
        (CONTROLLED, NATIVE) if technical else (CONTROLLED,),
        format_func=lambda m: 'Controlled retriever-only comparison' if m == CONTROLLED else 'Pipeline-native comparison',
        key='live_scoring_mode'
    )
    if scoring_mode == CONTROLLED:
        st.info('CONTROLLED RETRIEVER EFFECT · Only candidate retrieval differs. Both pools use the same SFR passage/unit scorer and frozen downstream settings.')
    else:
        st.caption('Retriever and its associated downstream relevance scoring may both differ. This compares complete pipeline variants, not retrieval alone. BM25-native QBGF is disabled because of score-scale incompatibility.')
    method = st.selectbox('Method', METHODS, index=2, format_func=lambda m: METHOD_LABELS.get(m, m), key='live_method')
    budget = st.session_state.get('live_budget', 256)
    
    enable_cur = st.session_state.get('live_models_enabled', enable)
    capacity = pool.available_memory_mib() if enable_cur and device == 'cuda' else inv['gpu_free_mib']
    sfr_usable = enable_cur and inv['sfr_local'] and (device == 'cpu' or (capacity is not None and (capacity >= 16000 or pool.encoder is not None or pool.reader is not None)))
    opts = ['BM25'] + (['SFR'] if sfr_usable else [])
    if st.session_state.get('live_retriever') not in opts:
        st.session_state['live_retriever'] = 'BM25'
    retriever = st.selectbox('Retriever', opts, key='live_retriever')
    
    preset_fallback = load_preset()
    query = st.session_state.get('live_query', preset_fallback['query'])
    passages = [st.session_state.get(f'live_passage_{i}', '') for i in st.session_state.get('live_passage_ids', list(range(len(preset_fallback['passages']))))]
    passages = [p for p in passages if p.strip()] or preset_fallback['passages'][:3]
    
    blocked = method == 'QBGF_FULL' and retriever == 'BM25' and scoring_mode == NATIVE
    pressed = st.button('Run Evidence Pipeline', type='primary', key='btn_run_single_pipeline', disabled=blocked or (scoring_mode == CONTROLLED and not enable and method != 'NONE'))
    
    states = {s: dict(state='pending', detail='') for s in STAGES}
    progress = st.empty()
    progress.markdown(pipeline_html(states), unsafe_allow_html=True)
    
    results = st.session_state.setdefault('live_results', {})
    history = st.session_state.setdefault('live_history', [])
    cache = st.session_state.setdefault('live_prepared', {})
    
    def notify(stage, state, detail, stts):
        progress.markdown(pipeline_html(stts), unsafe_allow_html=True)
        
    def execute(q, ps, m, b, rt, reader=True, score_mode=None, segment_mode=None):
        sm = score_mode or scoring_mode
        seg = segment_mode or segmentation
        k = (input_key(q.strip(), [p.strip() for p in ps], b, rt, seg, sm), m, device)
        old = results.get(k)
        identity = digest(pool.inference_identity()) if hasattr(pool, 'inference_identity') else None
        if reader and identity is not None and old is not None and old.get('reader_identity_hash') == identity and validity(old) is None and (old['answer'] is not None or not enable):
            remember(history, old)
            return old
        with st.spinner('Running evidence operations…'):
            with pool.lock:
                if hasattr(pool, 'set_device'):
                    pool.set_device(device)
                value = run(q, ps, m, b, rt, pool, enable, notify, cache, generate_answer=reader, segmentation=seg, scoring_mode=sm)
        if reader:
            value["reader_identity_hash"] = identity
            results[k] = value
            remember(history, value)
        return value

    if pressed:
        try:
            validate(query, passages, method, budget, retriever)
            value = execute(query, passages, method, budget, retriever)
            st.session_state['live_active'] = (value['input_key'], method, device)
            st.session_state.pop('live_compare', None)
        except Exception as exc:
            st.error(str(exc))
            
    active = st.session_state.get('live_active')
    value = results.get(active) if active else None
    if value and validity(value) is None and value.get('device', device) == device:
        progress.markdown(pipeline_html(value['stages']), unsafe_allow_html=True)
        st.divider()
        show_result(value, technical)
        
        st.subheader('Compare with another method')
        other = st.selectbox('Comparison method', [m for m in METHODS if m != value['method']], format_func=lambda m: METHOD_LABELS.get(m, m), key='live_compare_method_' + value['method'])
        if st.button('Run comparison', disabled=other == 'QBGF_FULL' and value['retriever'] == 'BM25' and value['scoring_mode'] == NATIVE):
            try:
                second = execute(value['query'], value['passages'], other, value['budget'], value['retriever'], score_mode=value['scoring_mode'], segment_mode=value['segmentation'])
                st.session_state['live_compare'] = (second['input_key'], other, device)
            except Exception as exc:
                st.error(str(exc))
        compared = results.get(st.session_state.get('live_compare'))
        if compared and compared['input_key'] == value['input_key'] and compared.get('device', device) == device:
            c = st.columns(2)
            for col, r in zip(c, [value, compared]):
                with col:
                    st.markdown('### ' + METHOD_LABELS.get(r['method'], r['method']))
                    evidence_card(r, technical)
                    
        if sfr_usable:
            if st.button('Compare Retrievers End-to-End', disabled=value['method'] == 'NONE'):
                try:
                    pair = [execute(value['query'], value['passages'], value['method'], value['budget'], rt, score_mode=CONTROLLED, segment_mode=value['segmentation']) for rt in ('BM25', 'SFR')]
                    assert_controlled_pair(*pair)
                    st.session_state['live_e2e'] = pair
                except Exception as exc:
                    st.error(str(exc))
            pair = st.session_state.get('live_e2e')
            if pair and same_custom_inputs(pair[0], value) and pair[0]['method'] == value['method']:
                assert_controlled_pair(*pair)
                st.subheader('CONTROLLED RETRIEVER EFFECT')
                st.info('Only the candidate retriever differs in this comparison.')
                with st.expander('Pipeline invariants', expanded=True):
                    st.write('Held constant: source passages, query, segmentation, common SFR downstream scorer, allocation method, evidence budget, Qwen reader, prompt template/parser, decoding and device. Changed: candidate retriever only.')
                    if technical:
                        st.json(pair[0]['invariants'])
                columns = st.columns(2)
                for col, r in zip(columns, pair):
                    with col:
                        st.markdown('### ' + r['retriever'])
                        st.dataframe(candidate_table(r), hide_index=True, width='stretch')
                        evidence_card(r, technical)

    render_history(history, technical)
