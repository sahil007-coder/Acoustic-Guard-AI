# AcousticGuard AI

> **Real-Time Environmental Sound Detection and Accessible Alert System**

AcousticGuard AI is an AI-powered accessibility solution designed to help individuals with hearing impairments remain aware of critical environmental sounds (such as sirens, vehicle horns, alarms, and glass breaking). The system captures ambient audio, extracts log-Mel spectrogram features, and classifies sounds in real time using a Convolutional Neural Network (CNN) to deliver visual and haptic/vibration notifications.

---

## 🚀 Key Features

- **Audio Preprocessing & Feature Extraction:** Standardizes audio inputs (mono, 16 kHz) and extracts log-Mel spectrogram representations.
- **Deep Learning Classifier:** CNN trained on environmental sound benchmarks (ESC-50 dataset) for target hazard/awareness classes.
- **Prediction Stabilization:** Employs confidence thresholds, temporal smoothing, and cooldown timers to prevent false or jittery alerts.
- **Accessible Multi-Modal Alerts:** Real-time visual status dashboard with vibration support on compatible devices.

---

## 🛠️ Proposed Tech Stack

- **Machine Learning & Audio:** Python, Librosa, NumPy, SciPy, TensorFlow / Keras
- **Dataset:** ESC-50 (Environmental Sound Classification)
- **Backend / API:** Python (Flask / FastAPI)
- **Frontend / Client:** React.js / Progressive Web App (PWA)
- **Version Control:** Git & GitHub

---

## 📁 Repository Structure

```text
AcousticGuard AI/
├── .gitattributes
├── .gitignore
├── README.md
├── data/              # Datasets & audio clips (git-ignored)
├── models/            # Trained weights & checkpoints (git-ignored)
├── notebooks/         # Exploratory data analysis & experiments
└── src/               # Application & pipeline source code
```

---

## 👥 Authors & Credits

- Sakina Tikiwala
- Sagar Sen
- Sahil Jasuja

*B.Tech – Computer Science and Engineering, Medi-Caps University (Group 17)*
