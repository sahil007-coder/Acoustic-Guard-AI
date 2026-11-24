# AcousticGuard AI - Dockerfile for Hugging Face Spaces (Docker SDK)
FROM python:3.11-slim

# Install system dependencies for audio decoding
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application assets
COPY . .

# Hugging Face Spaces listens on port 7860
ENV PORT=7860
EXPOSE 7860

# Launch application
CMD ["python", "app.py"]
