"""
AcousticGuard AI - Main Flask Web Application & REST API
Provides web interface and real-time inference endpoints for environmental sound recognition.
"""

import os
import sys
import warnings
import tempfile

# Suppress all backend stderr warnings before loading dependencies
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib")
warnings.filterwarnings("ignore")

import base64
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

from audio_utils import (
    load_audio_from_bytes, load_audio_from_file, extract_log_mel_spectrogram
)
from model import AcousticGuardModel, CLASSES, HAZARD_CLASSES
from alert_manager import AlertManager

app = Flask(__name__)
CORS(app)

# Initialize Model and Alert Manager Singletons
model = AcousticGuardModel()
alert_manager = AlertManager()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")


@app.route("/")
def index():
    """Renders the primary Accessible Alert Dashboard."""
    return render_template("index.html", classes=CLASSES, hazards=list(HAZARD_CLASSES))


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Inference endpoint supporting:
    1. Direct audio file upload (multipart/form-data: 'audio')
    2. Base64 audio string (JSON: {'audio_base64': '...'})
    3. Built-in sample trigger (JSON: {'sample_name': 'sample_siren.wav'})
    """
    try:
        audio_array = None

        # Case 1: Sample name provided in JSON
        if request.is_json and request.json and "sample_name" in request.json:
            sample_name = request.json["sample_name"]
            sample_path = os.path.join(SAMPLES_DIR, sample_name)
            if not os.path.exists(sample_path):
                return jsonify({"error": f"Sample '{sample_name}' not found"}), 404
            audio_array = load_audio_from_file(sample_path)

        # Case 2: Base64 audio provided in JSON
        elif request.is_json and request.json and "audio_base64" in request.json:
            b64_data = request.json["audio_base64"]
            if "," in b64_data:
                b64_data = b64_data.split(",")[1]
            audio_bytes = base64.b64decode(b64_data)
            audio_array = load_audio_from_bytes(audio_bytes)

        # Case 3: File upload via multipart/form-data
        elif "audio" in request.files:
            file = request.files["audio"]
            audio_bytes = file.read()
            audio_array = load_audio_from_bytes(audio_bytes)

        if audio_array is None:
            return jsonify({"error": "No valid audio payload provided"}), 400

        # Feature Extraction: Log-Mel Spectrogram (128, 94, 1)
        spectrogram = extract_log_mel_spectrogram(audio_array)

        # CNN Model Inference
        raw_pred = model.predict(spectrogram)

        # Prediction Stabilization & Alert Assessment
        stabilized_result = alert_manager.process_prediction(raw_pred)

        return jsonify({
            "success": True,
            **stabilized_result
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/samples", methods=["GET"])
def get_samples():
    """Returns available built-in test audio samples."""
    samples = []
    if os.path.exists(SAMPLES_DIR):
        for f in sorted(os.listdir(SAMPLES_DIR)):
            if f.endswith(".wav"):
                samples.append({
                    "filename": f,
                    "label": f.replace("sample_", "").replace(".wav", "").replace("_", " ").title()
                })
    return jsonify({"samples": samples})


@app.route("/api/sample/<filename>", methods=["GET"])
def serve_sample(filename):
    """Serves sample audio files for in-browser playback."""
    return send_from_directory(SAMPLES_DIR, filename)


@app.route("/api/history", methods=["GET"])
def get_history():
    """Returns detection event audit log."""
    return jsonify({"history": alert_manager.get_audit_log()})


@app.route("/api/clear_history", methods=["POST"])
def clear_history():
    """Clears detection event history."""
    alert_manager.clear_audit_log()
    return jsonify({"success": True, "message": "History cleared"})


@app.route("/api/health", methods=["GET"])
def health():
    """Healthcheck endpoint for local monitoring and Hugging Face Spaces."""
    return jsonify({
        "status": "healthy",
        "service": "AcousticGuard AI",
        "model_loaded": model.model is not None,
        "classes_count": len(CLASSES)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f"🚀 AcousticGuard AI Web App Running on http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
