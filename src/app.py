"""
Mood Driven Personalized Recommendation System — Main Application Entry Point

This file handles ONLY:
  - Page configuration
  - Session state initialization
  - Model loading
  - Mode routing (single vs multimodal)
  - Footer / history display

All detection logic lives in core/emotion_engine.py.
All UI rendering lives in ui/ modules.
"""

import sys
from pathlib import Path

import streamlit as st
import pandas as pd

# ===============================
# Path Configuration
# ===============================
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ===============================
# Load Environment Variables
# ===============================
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

# ===============================
# Application Modules
# ===============================
from src.state.session_state import init_session_state
from src.core.model_manager import load_models
from src.ui.enhanced_ui import (
    apply_enhanced_styling,
    create_enhanced_header,
    create_enhanced_footer,
)
from src.ui.compact_sidebar import create_compact_sidebar
from src.ui.resources_section import create_resources_section
from src.ui.single_mode_ui import render_single_mode_ui
from src.ui.multimodal_ui import render_multimodal_mode_ui
from src.ui.professional_music_player import create_current_player

# ===============================
# Page Configuration
# ===============================
st.set_page_config(
    page_title="🧠 MOOD DRIVEN PERSONALIZED RECOMMENDATION SYSTEM",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===============================
# Initialize Session State (once)
# ===============================
init_session_state()


# ===============================
# Main Application
# ===============================
def main():
    apply_enhanced_styling()
    create_enhanced_header()
    create_compact_sidebar()

    # --- Mode Selector ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Input Mode")
    mode_options = ["Single", "Multimodal"]
    current_mode_index = 0 if st.session_state.input_mode == "single" else 1
    mode_label = st.sidebar.radio(
        "Select analysis mode:", mode_options, index=current_mode_index
    )

    if st.session_state.input_mode != mode_label.lower():
        st.session_state.input_mode = mode_label.lower()
        st.session_state.multimodal_results = []

    # --- Model Loading ---
    if not st.session_state.get("models_loaded", False):
        if st.sidebar.button(
            "🚀 Load AI Models", type="primary", use_container_width=True
        ):
            try:
                with st.spinner("Loading AI models..."):
                    models = load_models()
                st.session_state.device = models["device"]
                st.session_state.face_model = models["face_model"]
                st.session_state.fer_detector = models["fer"]
                st.session_state.advanced_detector = models.get("advanced_detector")
                st.session_state.emotion_smoother = models.get("emotion_smoother")
                st.session_state.models_loaded = True
                st.rerun()
            except Exception as e:
                st.error(f"Model load error: {e}")
        st.warning(
            "Please load the AI models using the button in the sidebar to begin."
        )
        return

    # --- Global Music Player ---
    if st.session_state.get("current_track"):
        create_current_player(st.session_state.current_track)

    # --- Route to Mode UI ---
    if st.session_state.input_mode == "single":
        render_single_mode_ui()
    else:
        render_multimodal_mode_ui()

    st.markdown("---")

    # --- Emotion History ---
    if st.session_state.emotion_history:
        with st.expander("📈 Your Emotional Journey History"):
            hist_df = pd.DataFrame(st.session_state.emotion_history)
            hist_df["timestamp"] = pd.to_datetime(
                hist_df["timestamp"]
            ).dt.strftime("%Y-%m-%d %H:%M:%S")
            st.dataframe(hist_df, use_container_width=True)

    # --- Footer ---
    create_resources_section()
    create_enhanced_footer()


if __name__ == "__main__":
    main()
