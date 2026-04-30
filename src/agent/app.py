import streamlit as st
import os
import random
from agent.database_utils import download_db_from_s3
from agent.model_utils import get_model_predictions
from agent.ui_components import render_header, render_footer, render_result_panel
from common.config_manager import ConfigManager

from agent.theme_manager import apply_theme, THEMES, THEME_SESSION_KEY
from agent.ui_components import render_header, render_footer
from database.db_generator import EPPDatabaseGenerator 

@st.cache_resource
def initialize_database():
    """
    Initialize DB once per Streamlit session.
    Forces regeneration using reset=True.
    """

    gen = EPPDatabaseGenerator()

    # IMPORTANT: regenerate DB every startup
    gen.initialize(reset=True)

    return gen.db_path

# 1. Apply theme immediately at startup
active_theme = apply_theme()

st.set_page_config(page_title="EPP SLA Reporter", layout="wide")
# --- DB INIT ---
db_path = initialize_database()


# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []
if "query_input" not in st.session_state:
    st.session_state.query_input = ""

# --- SIDEBAR ---
cfg = ConfigManager()
with st.sidebar:
    st.header("⚙️ Settings")
    
    # 2. Add the Theme Selector
    st.selectbox(
        "Dashboard Theme",
        options=list(THEMES.keys()),
        format_func=lambda key: THEMES[key].label,
        key=THEME_SESSION_KEY,
    )
    st.caption(active_theme.description)
    
    st.header("🛠️ System")
    
    # DB Status
    #db_path = cfg.get_versioned_db_path()
    if os.path.exists(db_path):
        st.success("Database: Ready")
    else:
        st.error("Database: Missing")
    
    if st.button("🔄 Sync Database from S3"):
        download_db_from_s3()

    if st.button("♻️ Regenerate Database"):
        st.cache_resource.clear()
        initialize_database()
        st.success("Database regenerated")

    st.divider()
    
    # Models Selection
    selected_models = st.multiselect(
        "Select Models to Compare",
        ["epp-sla-reporter-model", "openai", "huggingface"],
        default=["epp-sla-reporter-model"]
    )

# --- MAIN UI ---
render_header()

# Example Questions (Fuzzy search simulation)
examples = ["Trend of average latency for MOD-DOMAIN", "Top 5 clients last 7 days", "Failed releases count"]
suggested = [ex for ex in examples if st.session_state.query_input.lower() in ex.lower()]

# Define submission logic
def on_submit():
    user_q = st.session_state.user_query
    if user_q:
        # Get results for every selected model
        model_results = {}
        for m_name in selected_models:
            model_results[m_name] = get_model_predictions(m_name, user_q)
        
        # Save to history
        st.session_state.history.insert(0, {"question": user_q, "results": model_results})
        if len(st.session_state.history) > 10: st.session_state.history.pop()
        
        # Clear input for next user
        st.session_state.user_query = ""

# The Input Box
st.text_input("Enter your question:", key="user_query", on_change=on_submit)
st.caption(f"Suggestions: {', '.join(suggested[:5])}")

# --- RESULTS DISPLAY ---
if st.session_state.history:
    current = st.session_state.history[0]
    st.write(f"### Results for: *{current['question']}*")
    
    # Create sub-panels dynamically
    cols = st.columns(len(current['results']))
    for idx, (m_name, m_data) in enumerate(current['results'].items()):
        with cols[idx]:
            render_result_panel(m_name, m_data)

# --- HISTORY ---
if st.session_state.history:
    with st.expander("📜 Query History (Last 10)"):
        for h in st.session_state.history:
            st.text(f"Q: {h['question']}")

render_footer()