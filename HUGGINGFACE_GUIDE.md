# 🚀 How to Deploy AcousticGuard AI to Hugging Face Spaces (100% Free Tier)

You do **NOT** need Docker or any paid subscription! Hugging Face Spaces provides completely free hosting using the **Gradio** SDK on their **Free CPU Basic Tier** (2 vCPU, 16 GB RAM).

---

## 📋 Quick 3-Minute Deployment Steps

### Step 1: Create a New Space on Hugging Face
1. Open your browser to: **[huggingface.co/new-space](https://huggingface.co/new-space)**
2. Enter **Space name**: `AcousticGuard-AI`
3. License: `mit` or `apache-2.0`
4. **Select Space SDK**: Choose **Gradio** 👈 *(100% Free!)*
5. **Space Hardware**: Keep default **CPU basic &bull; 2 vCPU &bull; 16GB &bull; Free**
6. Visibility: **Public**
7. Click **Create Space** at the bottom.

---

### Step 2: Push Your Project via Git

In your local project folder (`c:\Users\Sahil Jasuja\Downloads\AcousticGuard AI`), open PowerShell or your terminal and run:

```powershell
# 1. Connect your Hugging Face Space as a new git remote
# (Replace <YOUR_HF_USERNAME> with your Hugging Face username)
git remote add space https://huggingface.co/spaces/<YOUR_HF_USERNAME>/AcousticGuard-AI

# 2. Push all code and trained models to Hugging Face
git push space main
```

> **Note on Authentication:**
> When Git asks for your Password, use your **Hugging Face User Access Token**:
> 1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
> 2. Click **Create new token** &rarr; Select Type: **Write** &rarr; Copy the token.
> 3. Paste this token as your password in Git.

---

### Step 3: That's It! Your Space is Live! 🎉
Hugging Face will automatically install dependencies from `requirements.txt` and launch `app.py`.
Your live app will be accessible by anyone in the world at:
👉 **`https://huggingface.co/spaces/<YOUR_HF_USERNAME>/AcousticGuard-AI`**

---

## 🌐 Alternative: Browser Upload (No Terminal Needed!)
If you prefer not to use git commands:
1. Open your new Hugging Face Space page.
2. Click the **Files and versions** tab &rarr; **Add file** &rarr; **Upload files**.
3. Drag and drop the files from this folder (`app.py`, `model.py`, `audio_utils.py`, `alert_manager.py`, `models/`, `samples/`, `requirements.txt`, `README.md`).
4. Click **Commit changes to main**.
5. Hugging Face starts building immediately!
