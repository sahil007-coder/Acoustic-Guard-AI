"""
AcousticGuard AI - Streamlit Web Dashboard
Alternative 1-Click Interface tailored for Hugging Face Spaces (Streamlit SDK).
"""

import os
import sys
import warnings
import tempfile

# Complete suppression of backend stderr warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib")
warnings.filterwarnings("ignore")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from audio_utils import (
    SAMPLE_RATE, DURATION, extract_log_mel_spectrogram, load_audio_from_bytes,
    load_audio_from_file
)
from model import AcousticGuardModel, CLASSES, HAZARD_CLASSES
from alert_manager import AlertManager

# Page Configuration
st.set_page_config(
    page_title="AcousticGuard AI - Accessible Hazard Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "model" not in st.session_state:
    st.session_state.model = AcousticGuardModel()
if "alert_manager" not in st.session_state:
    st.session_state.alert_manager = AlertManager()

# App Header
st.title("🛡️ AcousticGuard AI")
st.markdown("**Real-Time Environmental Sound Recognition & Accessible Alert System**")
st.caption("College Mini-Project by Group 17 • Medi-Caps University")

# Sidebar Controls
st.sidebar.header("⚙️ Configuration")
threshold = st.sidebar.slider("Confidence Gate Threshold (%)", min_value=50, max_value=95, value=70, step=5) / 100.0
st.session_state.alert_manager.confidence_threshold = threshold

enable_strobe = st.sidebar.checkbox("Visual High-Contrast Alert", value=True)
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Monitored Sound Classes")
for cls in CLASSES:
    icon = "🚨" if cls in HAZARD_CLASSES else "🔊"
    st.sidebar.write(f"{icon} {cls}")

# Input Tabs
tab1, tab2 = st.tabs(["📁 Upload Audio File", "⚡ 1-Click Test Samples"])

audio_array = None

with tab1:
    uploaded_file = st.file_uploader("Upload an environmental audio clip (WAV, MP3, OGG):", type=["wav", "mp3", "ogg"])
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes)
        if st.button("🔍 Analyze Uploaded Audio", key="btn_upload"):
            with st.spinner("Extracting Log-Mel Spectrogram & Inferring..."):
                audio_array = load_audio_from_bytes(audio_bytes)

with tab2:
    st.write("Click any sample below to evaluate immediate detection response:")
    col1, col2, col3, col4 = st.columns(4)
    samples_dir = os.path.join(os.path.dirname(__file__), "samples")

    sample_choice = None
    if col1.button("🚨 Siren (Hazard)"):
        sample_choice = "sample_siren.wav"
    if col2.button("🚗 Car Horn (Hazard)"):
        sample_choice = "sample_car_horn.wav"
    if col3.button("🔥 Fire Alarm (Hazard)"):
        sample_choice = "sample_fire_alarm.wav"
    if col4.button("🌿 Ambient (Normal)"):
        sample_choice = "sample_ambient.wav"

    if sample_choice and os.path.exists(os.path.join(samples_dir, sample_choice)):
        sample_path = os.path.join(samples_dir, sample_choice)
        st.audio(sample_path)
        audio_array = load_audio_from_file(sample_path)

# Prediction Pipeline & Visual Dispatch
if audio_array is not None:
    # 1. Feature Extraction
    spectrogram = extract_log_mel_spectrogram(audio_array)

    # 2. CNN Inference
    raw_pred = st.session_state.model.predict(spectrogram)

    # 3. Stabilization
    result = st.session_state.alert_manager.process_prediction(raw_pred)

    pred_class = result["predicted_class"]
    confidence = result["confidence"]
    is_hazard = result["is_hazard"]
    alert_triggered = result["alert_triggered"]
    status = result["status"]
    reason = result["reason"]

    st.markdown("---")
    # Alert Banner
    if alert_triggered:
        st.error(f"### 🚨 HAZARD DETECTED: {pred_class.upper()} ({confidence * 100:.1f}%)")
        st.warning(f"**Alert Engine Dispatch:** {reason}")
    elif is_hazard:
        st.warning(f"### ⚠️ POTENTIAL HAZARD: {pred_class} ({confidence * 100:.1f}%) — {status}")
    else:
        st.success(f"### 🌿 NORMAL SOUND: {pred_class} ({confidence * 100:.1f}%)")

    # Main Visual Grid
    c_left, c_right = st.columns([1, 1])

    with c_left:
        st.subheader("📊 Class Posterior Probabilities")
        probs = raw_pred["all_probabilities"]
        for cls, p in probs.items():
            st.write(f"**{cls}**: `{p * 100:.1f}%`")
            st.progress(float(p))

    with c_right:
        st.subheader("🎼 Extracted Log-Mel Spectrogram")
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.imshow(spectrogram[:, :, 0], aspect='auto', origin='lower', cmap='inferno')
        ax.set_title("Log-Mel Energy Matrix (128 Bands × 94 Frames)")
        ax.set_xlabel("Time Frames")
        ax.set_ylabel("Mel Frequency Bands")
        st.pyplot(fig)

# Audit Log Table
st.markdown("---")
st.subheader("📋 Incident Audit Trail")
history = st.session_state.alert_manager.get_audit_log()
if history:
    st.table(history)
else:
    st.info("No hazard incidents recorded yet.")
