# 🚀 How to Deploy AcousticGuard AI to Hugging Face Spaces

This guide walks you through deploying **AcousticGuard AI** to **Hugging Face Spaces** for free public cloud hosting.

---

## 📋 Prerequisites

1. A free account on [huggingface.co](https://huggingface.co).
2. A **Hugging Face Access Token** (Write permission):
   - Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
   - Click **Create new token** &rarr; Select Type: **Write** &rarr; Copy your token.

---

## 🌟 Method 1: Docker SDK (Recommended for Full Accessible UI)

This deploys the complete accessible dashboard with the **Visual Strobe Alert**, **Haptic Vibration API**, **Live Mic Visualizer**, and **Sample Player**.

### Step 1: Create the Space on Hugging Face
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Set **Space Name**: `AcousticGuard-AI`.
3. Set **License**: `mit` or `apache-2.0`.
4. Select **Space SDK**: choose **Docker** &rarr; choose **Blank**.
5. Set Visibility: **Public**.
6. Click **Create Space**.

### Step 2: Push Your Code via Git

Open your terminal in the `AcousticGuard AI` project folder and run:

```bash
# 1. Add your Hugging Face Space as a new git remote (replace <YOUR_USERNAME> with your HF username)
git remote add space https://huggingface.co/spaces/<YOUR_USERNAME>/AcousticGuard-AI

# 2. Push the code to Hugging Face
git push space main
```

*(When Git prompts for credentials, enter your Hugging Face username and use your **Access Token** as the password).*

### Step 3: View Your Live App!
Hugging Face will automatically build the `Dockerfile` and launch your app at:
`https://huggingface.co/spaces/<YOUR_USERNAME>/AcousticGuard-AI`

---

## ⚡ Method 2: Streamlit SDK (Alternative 1-Click Deployment)

If you prefer using Hugging Face's native Streamlit environment:

### Step 1: Create the Space
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Set **Space Name**: `AcousticGuard-AI-Streamlit`.
3. Select **Space SDK**: **Streamlit**.
4. Click **Create Space**.

### Step 2: Push to Hugging Face
```bash
git remote add space-st https://huggingface.co/spaces/<YOUR_USERNAME>/AcousticGuard-AI-Streamlit
git push space-st main
```

### Step 3: Configure Entrypoint
In your Hugging Face Space settings, verify the entry file is set to `streamlit_app.py` (or rename `streamlit_app.py` to `app.py`).

---

## 🌐 Method 3: Drag & Drop via Web Browser (No Git Required)

1. Open your newly created Space on Hugging Face.
2. Go to the **Files and versions** tab.
3. Click **Add file** &rarr; **Upload files**.
4. Drag and drop all project files from this folder (`app.py`, `model.py`, `audio_utils.py`, `alert_manager.py`, `templates/`, `static/`, `models/`, `samples/`, `requirements.txt`, `Dockerfile`).
5. Click **Commit changes to main**.
6. Your Space will build and launch automatically!
