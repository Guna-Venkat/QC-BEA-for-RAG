"""Evidence Lab 2.0: Interactive Research Demonstrator.

CS787 Course Project · Generative AI · IIT Kanpur
Query-Conditioned Budget-Aware Evidence Allocation for Retrieval-Augmented Generation.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from demo.data_loader import freeze_check, verify_manifest, DataError
from demo.views import start_here, compare_methods, algorithm_explorer, research_and_live

# Configure Streamlit page layout and branding
st.set_page_config(
    page_title="Evidence Lab · CS787",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom styles
css_file = ROOT / "demo/assets/styles.css"
if css_file.exists():
    st.markdown(f"<style>{css_file.read_text()}</style>", unsafe_allow_html=True)

# Verify research artifact integrity (fail-closed)
try:
    freeze_check()
    verify_manifest()
except (DataError, FileNotFoundError, ValueError) as exc:
    st.error(f"Primary research artifact verification failed. Application stopped to prevent unverified results: {exc}")
    st.stop()

# Initialize session state for workspace navigation
WORKSPACES = [
    "Start Here",
    "Live Lab",
    "Compare Methods",
    "How the Algorithms Work"
]

# Support workspace synchronization with query parameters for clean refresh/bookmarking
param_ws = st.query_params.get("workspace")
if param_ws in ("Research & Live Lab", "Live Lab & Research"):
    param_ws = "Live Lab"
if param_ws in WORKSPACES and "workspace" not in st.session_state:
    st.session_state["workspace"] = param_ws
elif "workspace" not in st.session_state or st.session_state["workspace"] not in WORKSPACES:
    st.session_state["workspace"] = "Start Here"

# Keep query params in sync
st.query_params["workspace"] = st.session_state["workspace"]

# Sidebar Navigation and Configuration
with st.sidebar:
    st.markdown("### ◈ EVIDENCE LAB")
    st.caption("CS787 · Generative AI · IIT Kanpur")
    
    st.markdown("---")
    
    st.session_state.setdefault("nav_workspace_radio", st.session_state["workspace"])
    selected_mode = st.radio(
        "Workspace Navigation",
        WORKSPACES,
        index=None,
        key="nav_workspace_radio"
    )
    if selected_mode != st.session_state["workspace"]:
        st.session_state["workspace"] = selected_mode
        st.query_params["workspace"] = selected_mode
        st.rerun()

    st.markdown("---")
    
    st.markdown(
        '''
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; margin-bottom: 12px;">
            <div style="font-size: 0.72rem; font-weight: 700; color: #0f766e; text-transform: uppercase;">Frozen Production Policy</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: #1e293b; margin: 2px 0;">SFR → FIXED_SENTENCE → Qwen3-8B</div>
            <div style="font-size: 0.72rem; color: #64748b;">Top-10 Candidates · Greedy FP16 · 256 / 1024 Tokens</div>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    st.session_state["advanced_mode"] = st.toggle("Advanced Details", value=st.session_state.get("advanced_mode", False), help="Enables raw candidate pools, execution traces, and mathematical formulations across panels.")
    
    st.caption(
        "Scientific constraints:\n"
        "• Research findings remain strictly read-only.\n"
        "• Semantic relevance ≠ downstream utility.\n"
        "• Custom live runs are separate demonstrations without gold evaluation."
    )

# Main Workspace Router
current_ws = st.session_state["workspace"]

if current_ws == "Start Here":
    start_here.render()
elif current_ws in ("Live Lab", "Research & Live Lab", "Live Lab & Research"):
    research_and_live.render()
elif current_ws == "Compare Methods":
    compare_methods.render()
elif current_ws == "How the Algorithms Work":
    algorithm_explorer.render()

st.markdown("---")
st.markdown(
    '<div style="text-align: center; font-size: 0.78rem; color: #94a3b8; padding: 10px 0;">'
    'Evidence Lab 2.0 · CS787 Course Project · Generative AI · IIT Kanpur<br>'
    'Query-Conditioned Budget-Aware Evidence Allocation in Retrieval-Augmented Generation'
    '</div>',
    unsafe_allow_html=True
)
