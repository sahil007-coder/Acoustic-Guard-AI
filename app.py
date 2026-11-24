"""
AcousticGuard AI - Gradio Web Application
Native 100% Free deployment for Hugging Face Spaces (Gradio SDK).
Accessible real-time environmental sound classification and hazard alerts.
"""

import os
try:
    import spaces
except ImportError:
    class _SpacesMock:
        @staticmethod
        def GPU(func=None, **kwargs):
            if func is None:
                return lambda f: f
            return func
    spaces = _SpacesMock()

import gradio as gr
import numpy as np
import matplotlib.pyplot as plt

from audio_utils import (
    SAMPLE_RATE, DURATION, extract_log_mel_spectrogram, load_audio_from_file
)
from model import AcousticGuardModel, CLASSES, HAZARD_CLASSES
from alert_manager import AlertManager

# Initialize ML Singletons
model = AcousticGuardModel()
alert_manager = AlertManager()

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")

CUSTOM_CSS = """
.alert-box {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: #ffffff !important;
}
.alert-icon {
    font-size: 2.5rem;
}
.alert-text h2 {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 800;
    color: #ffffff !important;
}
.alert-text p {
    margin: 4px 0 0 0;
    font-size: 0.9rem;
    color: #f1f5f9 !important;
}
.hazard-alert {
    background: linear-gradient(135deg, #dc2626, #991b1b) !important;
    border: 2px solid #ef4444 !important;
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.6) !important;
    animation: pulse-hazard 1.2s infinite;
}
.warning-alert {
    background: linear-gradient(135deg, #d97706, #92400e) !important;
    border: 2px solid #f59e0b !important;
}
.normal-alert {
    background: linear-gradient(135deg, #16a34a, #166534) !important;
    border: 2px solid #22c55e !important;
}
.idle-alert {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
}
.strobe-pill {
    display: inline-block;
    background: #ffffff;
    color: #b91c1c;
    font-weight: 800;
    font-size: 0.75rem;
    padding: 3px 8px;
    border-radius: 4px;
    margin-top: 6px;
    text-transform: uppercase;
}
@keyframes pulse-hazard {
    0%, 100% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }
    50% { box-shadow: 0 0 35px rgba(239, 68, 68, 0.85); }
}
"""


@spaces.GPU
def classify_audio(audio_path, threshold):
    """Executes feature extraction, CNN inference, and prediction stabilization."""
    if not audio_path:
        return (
            """
            <div class='alert-box idle-alert'>
                <div class='alert-icon'>🎧</div>
                <div class='alert-text'>
                    <h2>Monitoring Ambient Environment</h2>
                    <p>Awaiting live microphone recording, uploaded file, or test sample below...</p>
                </div>
            </div>
            """,
            {},
            None,
            []
        )

    # Update threshold from user slider
    alert_manager.confidence_threshold = float(threshold)

    try:
        # 1. Preprocess & standardize audio
        y = load_audio_from_file(audio_path)

        # 2. Extract Log-Mel Spectrogram
        spec = extract_log_mel_spectrogram(y)

        # 3. Model forward inference
        raw_pred = model.predict(spec)

        # 4. Stabilization evaluation
        result = alert_manager.process_prediction(raw_pred)

        pred_class = result["predicted_class"]
        confidence = result["confidence"]
        is_hazard = result["is_hazard"]
        alert_triggered = result["alert_triggered"]
        status = result["status"]
        reason = result["reason"]

        # Build dynamic accessible HTML banner
        if alert_triggered:
            banner_html = f"""
            <div class="alert-box hazard-alert">
                <div class="alert-icon">🚨</div>
                <div class="alert-text">
                    <h2>HAZARD DETECTED: {pred_class.upper()}</h2>
                    <p><strong>Confidence:</strong> {confidence * 100:.1f}% &bull; <strong>Trigger:</strong> {reason}</p>
                    <span class="strobe-pill">⚠️ High-Priority Visual Alert Active</span>
                </div>
            </div>
            """
        elif is_hazard:
            banner_html = f"""
            <div class="alert-box warning-alert">
                <div class="alert-icon">⚠️</div>
                <div class="alert-text">
                    <h2>POTENTIAL HAZARD: {pred_class}</h2>
                    <p><strong>Confidence:</strong> {confidence * 100:.1f}% &bull; <strong>Status:</strong> {status} ({reason})</p>
                </div>
            </div>
            """
        else:
            banner_html = f"""
            <div class="alert-box normal-alert">
                <div class="alert-icon">🌿</div>
                <div class="alert-text">
                    <h2>NORMAL SOUND: {pred_class}</h2>
                    <p><strong>Confidence:</strong> {confidence * 100:.1f}% &bull; Safe ambient baseline</p>
                </div>
            </div>
            """

        # Generate Spectrogram Figure
        fig, ax = plt.subplots(figsize=(6, 2.4), facecolor='#0f172a')
        ax.set_facecolor('#0f172a')
        im = ax.imshow(spec[:, :, 0], aspect='auto', origin='lower', cmap='inferno')
        ax.set_title("Log-Mel Energy Spectrogram (128 Bands × 94 Frames)", color='#f8fafc', fontsize=9, pad=8)
        ax.tick_params(colors='#94a3b8', labelsize=8)
        for spine in ax.spines.values():
            spine.set_color('#334155')
        plt.tight_layout()

        # Audit History
        history = alert_manager.get_audit_log()
        history_rows = [
            [h["id"], h["timestamp"], h["hazard"], h["confidence"], h["status"]]
            for h in history
        ]

        return banner_html, raw_pred["all_probabilities"], fig, history_rows

    except Exception as e:
        err_banner = f"""
        <div class="alert-box hazard-alert">
            <div class="alert-icon">❌</div>
            <div class="alert-text">
                <h2>Audio Processing Error</h2>
                <p>{str(e)}</p>
            </div>
        </div>
        """
        return err_banner, {}, None, []


# Reference Sample Audio Files for 1-Click Evaluation
sample_files = []
for f in ["sample_siren.wav", "sample_car_horn.wav", "sample_fire_alarm.wav", "sample_glass_break.wav",
          "sample_dog_bark.wav", "sample_door_knock.wav", "sample_baby_cry.wav", "sample_ambient.wav"]:
    full_p = os.path.join(SAMPLES_DIR, f)
    if os.path.exists(full_p):
        sample_files.append([full_p, 0.70])

# Construct Gradio Interface
with gr.Blocks(title="AcousticGuard AI - Accessible Hazard Detection", css=CUSTOM_CSS, theme=gr.themes.Base()) as demo:
    gr.Markdown(
        """
        # 🛡️ AcousticGuard AI
        ### Real-Time Environmental Sound Classification & Accessible Alert System
        *Designed for individuals with hearing impairments &bull; Group 17, Medi-Caps University*
        """
    )

    # Main Alert Banner
    alert_output = gr.HTML(
        value="""
        <div class='alert-box idle-alert'>
            <div class='alert-icon'>🎧</div>
            <div class='alert-text'>
                <h2>Monitoring Ambient Environment</h2>
                <p>Record from microphone, upload audio, or choose a test sample below...</p>
            </div>
        </div>
        """
    )

    with gr.Row():
        # Left: Audio Input & Settings
        with gr.Column(scale=1):
            gr.Markdown("### 🎙️ Audio Input")
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="Record via Mic or Upload Audio (WAV, MP3, OGG)"
            )
            threshold_slider = gr.Slider(
                minimum=0.50,
                maximum=0.95,
                value=0.70,
                step=0.05,
                label="Confidence Threshold Gate (Default: 70%)"
            )
            analyze_btn = gr.Button("🔍 Analyze Environmental Sound", variant="primary")

            if sample_files:
                gr.Markdown("### ⚡ 1-Click Test Samples")
                gr.Examples(
                    examples=sample_files,
                    inputs=[audio_input, threshold_slider],
                    label="Click any sound clip to evaluate instantly:"
                )

        # Right: Probability Breakdown & Spectrogram
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Posterior Probabilities")
            label_output = gr.Label(num_top_classes=8, label="Class Confidence Distribution")
            spectrogram_plot = gr.Plot(label="🎼 Extracted Feature Spectrogram")

    # Bottom: Incident History
    gr.Markdown("### 📋 Recent Hazard Incident Trail")
    history_table = gr.Dataframe(
        headers=["#", "Timestamp", "Detected Hazard", "Confidence", "Dispatch Status"],
        datatype=["number", "str", "str", "str", "str"],
        interactive=False,
        label="Stabilized Incident Log"
    )

    # Event Wiring
    analyze_btn.click(
        fn=classify_audio,
        inputs=[audio_input, threshold_slider],
        outputs=[alert_output, label_output, spectrogram_plot, history_table]
    )

    audio_input.change(
        fn=classify_audio,
        inputs=[audio_input, threshold_slider],
        outputs=[alert_output, label_output, spectrogram_plot, history_table]
    )


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Base())
