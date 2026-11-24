# AcousticGuard AI 🛡️
> **Real-Time Environmental Sound Classification & Accessible Alert System**

AcousticGuard AI is an AI-powered accessibility solution designed to help individuals with hearing impairments remain aware of critical environmental hazard sounds (such as sirens, vehicle horns, alarms, and glass breaking).

The system captures ambient audio, standardizes it to 16 kHz mono, extracts 128-band Log-Mel Spectrogram features, and classifies sounds in real time using a 2D Convolutional Neural Network (CNN). Upon detecting a confirmed hazard, it fires multi-modal alerts: high-contrast visual strobes, device tactile vibration, and persistent telemetry audit logging.

Developed as a college mini-project by **Group 17** &bull; Department of Computer Science and Engineering, Medi-Caps University.

---

## 🌟 Key Features

* **Real-Time Audio Ingestion:** Captures live microphone audio in continuous 3-second buffer windows at 16 kHz mono.
* **Log-Mel Feature Extraction:** Computes Short-Time Fourier Transform (STFT, $N_{\text{fft}}=2048$, $\text{hop}=512$) with a 128-band Mel filterbank and logarithmic energy scaling ($128 \times 94 \times 1$).
* **Deep Learning CNN Classifier:** 2D Convolutional Neural Network trained to distinguish target environmental sounds with high posterior probability.
* **Multi-Stage Prediction Stabilization:**
  * **Confidence Gating:** Rejects background indeterminate noise where confidence $< 70\%$.
  * **Temporal Majority Queue:** Circular buffer ($W = 3$ frames) requiring consecutive frame agreement before alert dispatch.
  * **Cooldown Debounce:** Suppresses duplicate notifications for continuous events ($t_{\text{cooldown}} = 3.0\text{s}$).
* **Accessible Multi-Modal Delivery:**
  * 🚨 **High-Contrast Visual Strobe:** Bold full-screen and banner flash animations for deaf and hard-of-hearing users.
  * 📳 **Haptic Vibration API:** Drives device vibration motors on mobile and supporting browsers (`[300, 100, 300, 100, 500]` ms).
  * 📊 **Live Visualizer & Posterior Meters:** Real-time HTML5 Canvas audio waveform visualizer and live probability distribution across all 8 classes.
  * 📋 **Audit Log:** Incident history tracking with timestamps, hazard class, confidence, and status.

---

## 🎯 Target Sound Classes

| Class | Category | Severity | Response Action |
|---|---|---|---|
| 🚨 **Siren (Emergency Vehicle)** | Hazard | High | Visual Strobe + Haptic Vibration + Incident Log |
| 🚗 **Car Horn (Traffic)** | Hazard | High | Visual Strobe + Haptic Vibration + Incident Log |
| 🔥 **Fire / Smoke Alarm** | Hazard | Critical | Visual Strobe + Haptic Vibration + Incident Log |
| 🪟 **Glass Breaking** | Hazard | High | Visual Strobe + Haptic Vibration + Incident Log |
| 🐕 **Dog Barking** | Awareness | Medium | Status Banner Notification |
| 🚪 **Door Knock / Bell** | Awareness | Medium | Status Banner Notification |
| 👶 **Crying Baby** | Awareness | Medium | Status Banner Notification |
| 🌿 **Normal Ambient** | Baseline | Low | Monitoring Active |

---

## 📁 Repository Structure

```text
AcousticGuard AI/
├── app.py                     # Main Flask Web Application & REST API
├── streamlit_app.py           # Alternative Streamlit App (for 1-click Hugging Face Spaces)
├── audio_utils.py             # 16 kHz mono processing & Log-Mel spectrogram extractor
├── model.py                   # CNN Architecture (TensorFlow/Keras) & inference wrapper
├── alert_manager.py           # Stabilization engine (threshold, temporal queue, cooldown)
├── train.py                   # End-to-end model training & test sample generator
├── Dockerfile                 # Container image for Hugging Face Spaces / cloud hosting
├── requirements.txt           # Project dependencies
├── HUGGINGFACE_GUIDE.md       # Step-by-step Hugging Face deployment guide
├── models/
│   └── acousticguard.keras    # Serialized trained CNN model weights
├── samples/                   # Reference audio test clips (WAV)
│   ├── sample_siren.wav
│   ├── sample_car_horn.wav
│   ├── sample_fire_alarm.wav
│   ├── sample_glass_break.wav
│   ├── sample_dog_bark.wav
│   ├── sample_door_knock.wav
│   ├── sample_baby_cry.wav
│   └── sample_ambient.wav
├── templates/
│   └── index.html             # Accessible Web Dashboard (HTML5)
├── static/
│   ├── css/style.css          # WCAG AAA compliant dark styling & strobe animations
│   └── js/main.js             # Web Audio API streaming, Canvas visualizer & Vibration API
└── README.md                  # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/sahil007-coder/Acoustic-Guard-AI.git
cd "Acoustic-Guard-AI"
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
# Create and activate virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

*(Alternatively, to run the Streamlit version: `streamlit run streamlit_app.py`)*

### 4. (Optional) Retrain Model from Scratch
To regenerate the training dataset and train new weights:
```bash
python train.py
```

---

## ☁️ Hugging Face Spaces Deployment

You can deploy AcousticGuard AI to **Hugging Face Spaces** for free in under 3 minutes:

1. Create a New Space at [huggingface.co/new-space](https://huggingface.co/new-space).
2. Select **Docker SDK** (Blank).
3. Connect and push your code:
   ```bash
   git remote add space https://huggingface.co/spaces/<YOUR_USERNAME>/AcousticGuard-AI
   git push space main
   ```
4. Hugging Face builds the included `Dockerfile` and launches the application automatically!

*(Detailed instructions with screenshots and Streamlit alternatives can be found in [HUGGINGFACE_GUIDE.md](file:///c:/Users/Sahil%20Jasuja/Downloads/AcousticGuard%20AI/HUGGINGFACE_GUIDE.md)).*

---

## 👥 Authors & Project Credits

**Group 17 &bull; Medi-Caps University**
* **Sakina Tikiwala**
* **Sagar Sen**
* **Sahil Jasuja** ([@sahil007-coder](https://github.com/sahil007-coder))

*Bachelor of Technology (B.Tech) – Computer Science and Engineering*
