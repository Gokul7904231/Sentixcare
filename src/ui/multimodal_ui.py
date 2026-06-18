"""
Multimodal Mode UI
Handles collecting emotion inputs from multiple sources and fusing them.
Extracted from app.py to separate UI from routing logic.
"""

import cv2
import streamlit as st
from datetime import datetime
from PIL import Image

from src.core.emotion_engine import (
    detect_faces_and_emotions,
    fuse_emotions,
    standardize_emotion_result,
    detect_emotion_from_text_simple,
)
from src.ui.enhanced_ui import create_soothing_section
from src.ui.recommendation_panel import display_unified_recommendation_panel
from src.utils.constants import EMOTION_EMOJIS


def _process_emotion_result_multimodal(emotion, confidence, source):
    """Handle the final emotion result for multimodal mode (append to list)."""
    result = standardize_emotion_result(emotion, confidence, source)
    st.session_state.emotion_history.append({
        'timestamp': datetime.now(),
        'emotion': emotion,
        'confidence': confidence,
        'source': source,
    })
    st.session_state.multimodal_results.append(result)
    st.success(
        f"✅ Added **{result['emotion'].title()}** ({result['confidence']:.1f}%) "
        f"from {source.title()}"
    )


def render_multimodal_mode_ui():
    """Renders the UI for collecting multiple inputs and fusing them."""
    create_soothing_section(
        "Multimodal Emotion Fusion",
        "Combine inputs from different sources for a more holistic analysis.",
        "pastel-purple",
    )
    st.info(
        "ℹ️ **Multimodal Mode Active:** Add emotion data from multiple sources below. "
        "When you're ready, click 'Get Final Recommendations' at the bottom."
    )

    conf_thres = st.sidebar.slider("Face Confidence Threshold", 0.1, 1.0, 0.5, 0.05)
    iou_thres = st.sidebar.slider("IoU Threshold", 0.1, 1.0, 0.45, 0.05)

    # --- Input Sections ---
    with st.expander("📸 Add from Photo", expanded=True):
        uploaded_file = st.file_uploader(
            "Upload an image", type=['jpg', 'jpeg', 'png'], key="multi_photo"
        )
        if uploaded_file:
            if st.button("Add Photo Emotion", use_container_width=True):
                image = Image.open(uploaded_file)
                with st.spinner("Analyzing photo..."):
                    results, error = detect_faces_and_emotions(image, conf_thres, iou_thres)
                    if error:
                        st.error(error)
                    elif results:
                        for res in results:
                            _process_emotion_result_multimodal(
                                res['emotion'], res['confidence'], "photo"
                            )
                    else:
                        st.warning("No faces detected.")

    with st.expander("💬 Add from Text", expanded=True):
        mood_text = st.text_area(
            "Describe your mood:",
            placeholder="e.g., I'm feeling overwhelmed today after a long meeting...",
            height=120,
            help="Our AI will automatically detect your emotion from the text.",
            key="multi_mood_text"
        )
        intensity_multi = st.slider("Mood Intensity", 1, 10, 5, key="multi_intensity_slider")

        if st.button("Add Text Emotion", use_container_width=True):
            if not mood_text.strip():
                st.warning("Please describe your mood before adding.")
            else:
                emotion = detect_emotion_from_text_simple(mood_text)
                conf_multi = 70.0 + (intensity_multi * 2)
                conf_multi = min(100.0, conf_multi)
                _process_emotion_result_multimodal(emotion, conf_multi, "text")
                st.toast(f"Detected and added **{emotion.title()}** from your description!")

    with st.expander("📹 Add from Webcam", expanded=True):
        st.info("Captures a single frame for quick analysis.")
        if st.button("Add Webcam Emotion", use_container_width=True):
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error(
                    "Error: Could not access webcam. "
                    "Please ensure it is connected and not in use by another application."
                )
            else:
                ret, frame = cap.read()
                cap.release()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    st.info("🧪 Debug Mode: Analyzing webcam frame step by step...")
                    col1, col2 = st.columns(2)
                    col1.image(frame_rgb, caption="STEP 1: Raw Webcam Frame")
                    results, error = detect_faces_and_emotions(
                        frame_rgb, conf_thres, iou_thres
                    )
                    if error:
                        st.error(f"STEP 2 Error: {error}")
                        col2.image(frame_rgb, caption="No Detection")
                    else:
                        bbox_img = draw_results(frame_rgb, results) if results else frame_rgb
                        col2.image(bbox_img, caption="STEP 2: Face Detection (bboxes)")
                        if results:
                            st.metric("STEP 2: Faces Detected", len(results))
                            for i, res in enumerate(results):
                                with st.expander(f"STEP 3-5: Face {i+1} Debug"):
                                    bbox = res['bbox']
                                    x1,y1,x2,y2 = map(int, bbox)
                                    crop = frame_rgb[y1:y2, x1:x2]
                                    crop_resized = cv2.resize(crop, (224,224))
                                    st.image(Image.fromarray(crop_resized), caption="STEP 3: Face Crop")
                                    st.json({
                                        "STEP 4 Preprocessing": {
                                            "shape": list(crop.shape),
                                            "pixel_min": float(crop.min()),
                                            "pixel_max": float(crop.max()),
                                        },
                                        "STEP 5 Model Output": {
                                            "emotion": res['emotion'],
                                            "confidence": f"{res['confidence']:.1f}%",
                                            "face_conf": f"{res['face_conf']:.1f}%"
                                        }
                                    })
                            # Process as before
                            for res in results:
                                _process_emotion_result_multimodal(
                                    res['emotion'], res['confidence'], "webcam"
                                )
                            st.success("✅ Debug complete. Emotion added to multimodal results!")
                        else:
                            st.warning("STEP 2: No faces detected.")
                else:
                    st.error("Failed to capture frame from webcam.")

    st.markdown("---")

    # --- Collected Inputs & Final Analysis ---
    if st.session_state.multimodal_results:
        st.subheader("📊 Collected Inputs")
        for i, res in enumerate(st.session_state.multimodal_results):
            emoji = EMOTION_EMOJIS.get(res['emotion'], '😐')
            st.markdown(
                f"- **{res['source'].title()}**: {emoji} "
                f"{res['emotion'].title()} ({res['confidence']:.1f}%)"
            )

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(
                "Get Final Recommendations",
                type="primary",
                use_container_width=True,
            ):
                final_emo, final_conf = fuse_emotions(st.session_state.multimodal_results)
                st.session_state.final_emotion = final_emo
                st.session_state.final_confidence = final_conf
                st.session_state.show_multimodal_recommendations = True

        with col2:
            if st.button("Clear Inputs", use_container_width=True):
                st.session_state.multimodal_results = []
                st.session_state.show_multimodal_recommendations = False
                st.session_state.final_emotion = None
                st.session_state.final_confidence = None
    else:
        st.write("No inputs collected yet. Use the sections above to add data.")

    # Conditionally display the recommendations panel
    if st.session_state.show_multimodal_recommendations:
        st.markdown("---")
        st.header("Fusion Analysis & Recommendations")
        display_unified_recommendation_panel(
            st.session_state.final_emotion,
            st.session_state.final_confidence,
        )
