"""Comprehensive Streamlit AppTest test suite for Evidence Lab 2.0.

Tests all four primary workspaces, interactive walkthrough stages, method
comparisons, algorithm visualizers, and research tabs headlessly.
"""

import sys
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def start_app():
    """Launch the redesigned Evidence Lab Streamlit application."""
    at = AppTest.from_file(str(ROOT / "demo/app.py"), default_timeout=45).run()
    assert not at.exception, [e.message for e in at.exception]
    assert not at.error, [e.value for e in at.error]
    return at


def set_workspace(at, name):
    """Switch active workspace via the sidebar radio control."""
    radio = next(r for r in at.sidebar.radio if r.label == "Workspace Navigation")
    if name in ("Research & Live Lab", "Live Lab & Research") and "Live Lab" in radio.options:
        name = "Live Lab"
    radio.set_value(name).run()
    assert not at.exception, [e.message for e in at.exception]
    assert not at.error, [e.value for e in at.error]
    return at


def all_text(at):
    """Extract all text elements across markdown, subheaders, titles, and alert callouts."""
    texts = [m.value for m in at.markdown]
    texts += [s.value for s in at.subheader]
    texts += [t.value for t in at.title]
    texts += [s.value for s in at.success]
    texts += [w.value for w in at.warning]
    texts += [i.value for i in at.info]
    texts += [c.value for c in at.caption]
    return " ".join(texts)


# ==============================================================================
# Page 1: Start Here Tests
# ==============================================================================
def test_page1_start_here_defaults():
    at = start_app()
    txt = all_text(at)
    assert "Evidence Lab" in txt
    assert "Question" in txt
    assert "Answer" in txt
    
    # Verify 3 featured example cards exist
    assert any(b.label == "Explore Multi-Hop Case" for b in at.button)
    assert any(b.label == "Explore Starvation Case" for b in at.button)
    assert any(b.label == "Explore Microdomains Case" for b in at.button)
    
    # Default is Stage 1 of HotpotQA
    assert "Stage 1" in txt
    assert "Denis Villeneuve" in txt


def test_page1_walkthrough_navigation():
    at = start_app()
    # Click Next Stage -> Stage 2
    btn_next = next(b for b in at.button if "Next Stage" in b.label)
    btn_next.click().run()
    assert not at.exception
    assert "Stage 2" in all_text(at)
    
    # Click Next Stage -> Stage 3
    btn_next = next(b for b in at.button if "Next Stage" in b.label)
    btn_next.click().run()
    assert not at.exception
    assert "Stage 3" in all_text(at)
    assert "Evidence Budget Limit" in all_text(at)
    
    # Click Next Stage -> Stage 4
    btn_next = next(b for b in at.button if "Next Stage" in b.label)
    btn_next.click().run()
    assert not at.exception
    assert "Stage 4" in all_text(at)
    
    # Click Next Stage -> Stage 5
    btn_next = next(b for b in at.button if "Next Stage" in b.label)
    btn_next.click().run()
    assert not at.exception
    assert "Stage 5" in all_text(at)
    
    # Click Previous Stage -> Stage 4
    btn_prev = next(b for b in at.button if "Previous Stage" in b.label)
    btn_prev.click().run()
    assert not at.exception
    assert "Stage 4" in all_text(at)

    # Move back to Stage 5 and test Circular Restart
    btn_next = next(b for b in at.button if "Next Stage" in b.label)
    btn_next.click().run()
    assert "Stage 5" in all_text(at)
    btn_restart = next(b for b in at.button if "Restart Walkthrough" in b.label)
    btn_restart.click().run()
    assert not at.exception
    assert "Stage 1" in all_text(at)


def test_page1_example_switching():
    at = start_app()
    # Switch to QASPER Starvation Case
    btn_qasper = next(b for b in at.button if b.label == "Explore Starvation Case")
    btn_qasper.click().run()
    assert not at.exception
    assert "binary classification tasks" in all_text(at)
    
    # Switch to SciFact Matched Microdomains Case
    btn_scifact = next(b for b in at.button if b.label == "Explore Microdomains Case")
    btn_scifact.click().run()
    assert not at.exception
    assert "TCR/CD3" in all_text(at) or "microdomains" in all_text(at)


# ==============================================================================
# Page 2: Compare Methods Tests
# ==============================================================================
def test_page2_compare_methods():
    at = start_app()
    set_workspace(at, "Compare Methods")
    
    txt = all_text(at)
    assert "Compare Methods" in txt
    assert "CONTROLLED MATCHED COMPARISON" in txt
    
    # Verify side-by-side selection boxes exist
    m1_box = next(s for s in at.selectbox if s.label == "Left Method")
    m2_box = next(s for s in at.selectbox if s.label == "Center Method")
    assert m1_box.value is not None
    assert m2_box.value is not None
    
    # Switch left method to Whole Passages (RAW_SKIP)
    m1_box.set_value("RAW_SKIP").run()
    assert not at.exception
    
    # Verify evidence legend
    assert "Evidence Status Color Legend" in all_text(at)
    assert "Selected Evidence" in all_text(at)


def test_page2_direct_case_switching():
    at = start_app()
    set_workspace(at, "Compare Methods")
    
    # Verify direct example dropdown without Historical Curated Queries toolbar
    case_box = next(s for s in at.selectbox if s.label == "Choose an Example")
    assert any("HotpotQA" in opt for opt in case_box.options)
    assert any("QASPER" in opt for opt in case_box.options)
    assert any("SciFact" in opt for opt in case_box.options)
    
    # Switch to SciFact Matched Case
    scifact_opt = next(opt for opt in case_box.options if "TCR/CD3" in opt)
    case_box.set_value(scifact_opt).run()
    assert not at.exception
    assert "TCR/CD3" in all_text(at) or "microdomains" in all_text(at)
    
    # Switch to QASPER Starvation Case
    qasper_opt = next(opt for opt in case_box.options if "Binary Classification" in opt)
    case_box.set_value(qasper_opt).run()
    assert not at.exception
    assert "binary classification tasks" in all_text(at)


# ==============================================================================
# Page 3: How the Algorithms Work Tests
# ==============================================================================
def test_page3_qbgf_explorer():
    at = start_app()
    set_workspace(at, "How the Algorithms Work")
    
    txt = all_text(at)
    assert "QBGF" in txt
    assert "Knapsack" in txt or "MCKP" in txt
    assert "SENT_1" in txt
    assert "FULL" in txt


def test_page3_beav1_explorer():
    at = start_app()
    set_workspace(at, "How the Algorithms Work")
    
    # Switch radio to BEA-V1
    algo_radio = next(r for r in at.radio if r.label == "Choose Algorithm to Explore")
    algo_radio.set_value("BEA-V1 (Dynamic Marginal Stopping)").run()
    assert not at.exception
    
    txt = all_text(at)
    assert "BEA-V1" in txt
    assert "Context Starvation" in txt
    
    # Verify interactive trace slider
    slider = next(s for s in at.slider if "Trace" in s.label)
    assert slider.max >= 15
    slider.set_value(5).run()
    assert not at.exception


def test_page3_beav2_explorer():
    at = start_app()
    set_workspace(at, "How the Algorithms Work")
    
    # Switch radio to BEA-V2
    algo_radio = next(r for r in at.radio if r.label == "Choose Algorithm to Explore")
    algo_radio.set_value("BEA-V2 (Learned Helpfulness Guidance)").run()
    assert not at.exception
    
    txt = all_text(at)
    assert "BEA-V2" in txt
    assert "P_help" in txt
    assert "Gull" in txt or "Enemy" in txt or "Invader" in txt


# ==============================================================================
# Page 4: Research & Live Lab Tests
# ==============================================================================
def test_page4_research_journey_and_findings():
    at = start_app()
    set_workspace(at, "Research & Live Lab")
    
    txt = all_text(at)
    assert "Research Progression" in txt or "Research Journey" in txt
    assert "SARA" in txt
    assert "BEA-V2" in txt
    
    # Verify core scientific questions are addressed
    assert "What were we trying to solve?" in txt
    assert "What did we observe?" in txt


def test_page4_advanced_mode_toggle():
    at = start_app()
    toggle = next(t for t in at.sidebar.toggle if t.label == "Advanced Details")
    toggle.set_value(True).run()
    assert not at.exception
    assert at.session_state["advanced_mode"] is True


def test_page4_live_lab_two_actions():
    at = start_app()
    set_workspace(at, "Research & Live Lab")
    
    # Switch to Live tab in Research & Live Lab
    txt = all_text(at)
    assert "Live Lab" in txt
    
    # Check that input sections and action buttons exist
    assert any("Passage " in a.label for a in at.text_area)
    assert any(b.label == "+ Add Passage" for b in at.button)
    assert any("Compare Four Methods" in b.label for b in at.button)
    assert any("Analyze Evidence Impact" in b.label for b in at.button)
    
    # Action 1: Click Compare Four Methods
    btn_cmp = next(b for b in at.button if "Compare Four Methods" in b.label)
    btn_cmp.click().run()
    assert not at.exception
    
    txt_after_cmp = all_text(at)
    assert "Best Sentences" in txt_after_cmp
    assert "QBGF" in txt_after_cmp
    assert "BEA-V1" in txt_after_cmp
    assert "BEA-V2" in txt_after_cmp
    
    # Action 2 Guard Case A: Click Analyze Evidence Impact WITHOUT reference answer
    btn_impact = next(b for b in at.button if "Analyze Evidence Impact" in b.label)
    btn_impact.click().run()
    assert not at.exception
    assert "Reference answer required" in all_text(at)

    # Action 2 Guard Case B: Provide reference answer, but reader inference not executed
    ref_area = next(a for a in at.text_area if "Reference Answer" in a.label)
    ref_area.set_value("Sensor B forty-eight hours").run()
    btn_impact = next(b for b in at.button if "Analyze Evidence Impact" in b.label)
    btn_impact.click().run()
    assert not at.exception
    assert "Reader inference required" in all_text(at)

    # Injecting an answer string cannot manufacture a valid baseline receipt.
    for m in at.session_state["live_four_results"]["methods"].values():
        m["answer"] = "Sensor B had forty-eight hours of battery life."
    btn_impact.click().run()
    assert not at.exception
    assert "No evidence units were eligible" in all_text(at)


def test_start_here_open_live_lab_button_syncs_sidebar():
    at=start_app()
    for _ in range(4):
        next(b for b in at.button if b.label=='Next Stage →').click().run()
        assert not at.exception
    next(b for b in at.button if b.label=='Open Live Lab →').click().run()
    assert not at.exception
    assert at.session_state['workspace']=='Live Lab'
    assert next(r for r in at.sidebar.radio if r.label=='Workspace Navigation').value=='Live Lab'
    assert at.query_params['workspace']=='Live Lab'
    at.run()
    assert at.session_state['workspace']=='Live Lab'
    next(r for r in at.sidebar.radio if r.label=='Workspace Navigation').set_value('Start Here').run()
    assert not at.exception
    assert at.session_state['workspace']=='Start Here'
