/**
 * AcousticGuard AI - Accessible Client Controller & Audio Processor
 * Handles live Web Audio streaming, Canvas visualizer, Haptic API, Visual Strobe, and REST calls.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const strobeOverlay = document.getElementById("strobeOverlay");
  const strobeText = document.getElementById("strobeText");
  const strobeSubtext = document.getElementById("strobeSubtext");

  const mainAlertBanner = document.getElementById("mainAlertBanner");
  const bannerIcon = document.getElementById("bannerIcon");
  const bannerTitle = document.getElementById("bannerTitle");
  const bannerSubtitle = document.getElementById("bannerSubtitle");
  const bannerConfidence = document.getElementById("bannerConfidence");
  const bannerEngineStatus = document.getElementById("bannerEngineStatus");

  const micToggleBtn = document.getElementById("micToggleBtn");
  const micBtnText = document.getElementById("micBtnText");
  const micRecordingBadge = document.getElementById("micRecordingBadge");
  const micSecurityWarning = document.getElementById("micSecurityWarning");
  const waveformCanvas = document.getElementById("waveformCanvas");
  const canvasCtx = waveformCanvas.getContext("2d");

  // Check Secure Context on startup
  const isSecureOrigin = window.isSecureContext || 
    window.location.hostname === "localhost" || 
    window.location.hostname === "127.0.0.1";
  
  if (!isSecureOrigin && micSecurityWarning) {
    micSecurityWarning.classList.remove("hidden");
  }

  // Fast in-memory 16-bit PCM WAV Encoder for instant server compatibility
  function encodeWAV(samples, sampleRate = 16000) {
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);

    function writeString(offset, string) {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    }

    writeString(0, 'RIFF');
    view.setUint32(4, 36 + samples.length * 2, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM format
    view.setUint16(22, 1, true); // Mono channel
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true); // Byte rate
    view.setUint16(32, 2, true); // Block align
    view.setUint16(34, 16, true); // 16-bit
    writeString(36, 'data');
    view.setUint32(40, samples.length * 2, true);

    let offset = 44;
    for (let i = 0; i < samples.length; i++, offset += 2) {
      let s = Math.max(-1, Math.min(1, samples[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    return new Blob([buffer], { type: 'audio/wav' });
  }

  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const selectedFileInfo = document.getElementById("selectedFileInfo");
  const selectedFileName = document.getElementById("selectedFileName");
  const analyzeFileBtn = document.getElementById("analyzeFileBtn");

  const sampleButtons = document.querySelectorAll(".sample-btn");
  const sampleAudioPlayer = document.getElementById("sampleAudioPlayer");

  const toggleStrobe = document.getElementById("toggleStrobe");
  const toggleVibration = document.getElementById("toggleVibration");
  const thresholdSlider = document.getElementById("thresholdSlider");
  const thresholdVal = document.getElementById("thresholdVal");

  const telemStatus = document.getElementById("telemStatus");
  const telemTemporal = document.getElementById("telemTemporal");
  const telemReason = document.getElementById("telemReason");
  const historyTableBody = document.getElementById("historyTableBody");
  const clearHistoryBtn = document.getElementById("clearHistoryBtn");

  // State Variables
  let isListening = false;
  let audioContext = null;
  let mediaStream = null;
  let analyserNode = null;
  let audioProcessorNode = null;
  let pcmBuffer = [];
  let isSendingInference = false;
  let animationFrameId = null;
  let currentFile = null;
  let strobeTimeout = null;

  // 16-bit PCM WAV Encoder (universally decoded by Python soundfile & scipy)
  function encodeWAV(samples, sampleRate = 16000) {
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);

    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    writeString(0, 'RIFF');
    view.setUint32(4, 36 + samples.length * 2, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM
    view.setUint16(22, 1, true); // Mono channel
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true); // Byte rate
    view.setUint16(32, 2, true); // Block align
    view.setUint16(34, 16, true); // 16-bit
    writeString(36, 'data');
    view.setUint32(40, samples.length * 2, true);

    let offset = 44;
    for (let i = 0; i < samples.length; i++, offset += 2) {
      const s = Math.max(-1, Math.min(1, samples[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    return new Blob([buffer], { type: 'audio/wav' });
  }

  // Icons Mapping
  const classIcons = {
    "Siren (Emergency Vehicle)": "🚨",
    "Car Horn (Traffic)": "🚗",
    "Fire / Smoke Alarm": "🔥",
    "Glass Breaking": "🪟",
    "Dog Barking": "🐕",
    "Door Knock / Bell": "🚪",
    "Crying Baby": "👶",
    "Normal Ambient": "🌿"
  };

  // ==========================================
  // 1. Tab Navigation
  // ==========================================
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const targetTab = document.getElementById(btn.dataset.tab);
      if (targetTab) targetTab.classList.add("active");
    });
  });

  // ==========================================
  // 2. Settings Handlers
  // ==========================================
  thresholdSlider.addEventListener("input", (e) => {
    thresholdVal.textContent = `${e.target.value}%`;
  });

  // ==========================================
  // 3. Audio Visualizer (Canvas Waveform)
  // ==========================================
  function startVisualizer() {
    if (!audioContext || !analyserNode) return;
    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function draw() {
      animationFrameId = requestAnimationFrame(draw);
      analyserNode.getByteTimeDomainData(dataArray);

      canvasCtx.fillStyle = "#090d16";
      canvasCtx.fillRect(0, 0, waveformCanvas.width, waveformCanvas.height);

      canvasCtx.lineWidth = 2.5;
      canvasCtx.strokeStyle = isListening ? "#06b6d4" : "#334155";
      canvasCtx.beginPath();

      const sliceWidth = waveformCanvas.width / bufferLength;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = (v * waveformCanvas.height) / 2;

        if (i === 0) {
          canvasCtx.moveTo(x, y);
        } else {
          canvasCtx.lineTo(x, y);
        }
        x += sliceWidth;
      }

      canvasCtx.lineTo(waveformCanvas.width, waveformCanvas.height / 2);
      canvasCtx.stroke();
    }
    draw();
  }

  function stopVisualizer() {
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    canvasCtx.fillStyle = "#090d16";
    canvasCtx.fillRect(0, 0, waveformCanvas.width, waveformCanvas.height);
    // Draw idle centerline
    canvasCtx.strokeStyle = "#334155";
    canvasCtx.lineWidth = 1.5;
    canvasCtx.beginPath();
    canvasCtx.moveTo(0, waveformCanvas.height / 2);
    canvasCtx.lineTo(waveformCanvas.width, waveformCanvas.height / 2);
    canvasCtx.stroke();
  }
  stopVisualizer();

  // State Variables for Live PCM Capture
  let scriptProcessor = null;
  let pcmBuffer = [];
  let isInferring = false;
  const TARGET_SAMPLES = 48000; // 3.0 seconds at 16 kHz

  // ==========================================
  // 4. Live Microphone Real-Time Stream
  // ==========================================
  async function toggleMicrophone() {
    if (!isListening) {
      // 1. Validate Browser MediaDevices Availability (Secure Context Check)
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        if (micSecurityWarning) micSecurityWarning.classList.remove("hidden");
        alert(
          "🔒 Microphone Access Blocked by Browser Security!\n\n" +
          "Modern browsers disable microphone access on unencrypted IP addresses (http://" + window.location.hostname + ":5000).\n\n" +
          "👉 If on this laptop: Please open http://localhost:5000 (or http://127.0.0.1:5000).\n" +
          "📱 If on a phone: Run 'npx localtunnel --port 5000' for free HTTPS or enable the Chrome insecure origin flag."
        );
        return;
      }

      try {
        // Request single-channel 16 kHz audio without noise destruction
        mediaStream = await navigator.mediaDevices.getUserMedia({
          audio: {
            channelCount: 1,
            sampleRate: 16000,
            echoCancellation: false,
            noiseSuppression: false,
            autoGainControl: true
          },
          video: false
        });

        audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        const source = audioContext.createMediaStreamSource(mediaStream);

        // Visualizer Analyser Node
        analyserNode = audioContext.createAnalyser();
        analyserNode.fftSize = 2048;
        source.connect(analyserNode);

        // PCM Sample Collector via ScriptProcessor
        pcmBuffer = [];
        const bufferSize = 4096;
        scriptProcessor = audioContext.createScriptProcessor(bufferSize, 1, 1);
        source.connect(scriptProcessor);
        scriptProcessor.connect(audioContext.destination);

        scriptProcessor.onaudioprocess = async (e) => {
          if (!isListening) return;
          const inputData = e.inputBuffer.getChannelData(0);
          for (let i = 0; i < inputData.length; i++) {
            pcmBuffer.push(inputData[i]);
          }

          // When we accumulate 3 seconds of audio (48,000 samples)
          if (pcmBuffer.length >= TARGET_SAMPLES && !isInferring) {
            const chunk = pcmBuffer.slice(0, TARGET_SAMPLES);
            // 1.5-second slide for rapid continuous detection
            pcmBuffer = pcmBuffer.slice(24000);

            isInferring = true;
            try {
              const actualSr = audioContext.sampleRate || 16000;
              const wavBlob = encodeWAV(chunk, actualSr);
              await sendAudioForPrediction(wavBlob);
            } catch (err) {
              console.error("Live streaming inference error:", err);
            } finally {
              isInferring = false;
            }
          }
        };

        isListening = true;
        micToggleBtn.classList.add("btn-recording");
        micBtnText.textContent = "Stop Real-Time Listening";
        micRecordingBadge.classList.remove("hidden");
        if (micSecurityWarning) micSecurityWarning.classList.add("hidden");
        startVisualizer();

        bannerTitle.textContent = "Listening to Live Ambient Audio...";
        bannerSubtitle.textContent = "Streaming 3-second PCM windows to CNN inference pipeline";
      } catch (err) {
        console.error("Microphone Access Error:", err);
        alert("Microphone Access Error: " + err.message);
      }
    } else {
      // Stop listening
      isListening = false;
      if (scriptProcessor) {
        scriptProcessor.disconnect();
        scriptProcessor.onaudioprocess = null;
        scriptProcessor = null;
      }
      if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
      }
      if (audioContext && audioContext.state !== "closed") {
        audioContext.close();
        audioContext = null;
      }

      pcmBuffer = [];
      micToggleBtn.classList.remove("btn-recording");
      micBtnText.textContent = "Start Real-Time Listening";
      micRecordingBadge.classList.add("hidden");
      stopVisualizer();

      bannerTitle.textContent = "Monitoring Paused";
      bannerSubtitle.textContent = "Press Start Listening or select a sample above to resume.";
    }
  }

  micToggleBtn.addEventListener("click", toggleMicrophone);

  // ==========================================
  // 5. File Upload Handling
  // ==========================================
  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
      handleSelectedFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleSelectedFile(e.target.files[0]);
    }
  });

  function handleSelectedFile(file) {
    currentFile = file;
    selectedFileName.textContent = file.name;
    selectedFileInfo.classList.remove("hidden");
  }

  analyzeFileBtn.addEventListener("click", async () => {
    if (!currentFile) return;
    analyzeFileBtn.textContent = "Analyzing...";
    analyzeFileBtn.disabled = true;
    await sendAudioForPrediction(currentFile);
    analyzeFileBtn.textContent = "Analyze Audio";
    analyzeFileBtn.disabled = false;
  });

  // ==========================================
  // 6. 1-Click Test Samples
  // ==========================================
  sampleButtons.forEach(btn => {
    btn.addEventListener("click", async () => {
      const sampleFile = btn.dataset.sample;
      if (!sampleFile) return;

      // Play audio preview
      sampleAudioPlayer.src = `/api/sample/${sampleFile}`;
      sampleAudioPlayer.classList.remove("hidden");
      sampleAudioPlayer.play().catch(() => {});

      // Dispatch inference request
      try {
        bannerEngineStatus.textContent = "EVALUATING";
        const response = await fetch("/api/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ sample_name: sampleFile })
        });
        const result = await response.json();
        updateUIWithPrediction(result);
      } catch (err) {
        console.error("Sample prediction error:", err);
      }
    });
  });

  // ==========================================
  // 7. Prediction REST Dispatcher
  // ==========================================
  async function sendAudioForPrediction(audioBlobOrFile) {
    const formData = new FormData();
    const fileName = audioBlobOrFile.name || "live_stream.wav";
    formData.append("audio", audioBlobOrFile, fileName);

    try {
      bannerEngineStatus.textContent = "INFERENCE";
      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData
      });
      const result = await response.json();
      updateUIWithPrediction(result);
    } catch (err) {
      console.error("Inference Error:", err);
      bannerSubtitle.textContent = "Error during classification. Check server logs.";
    }
  }

  // ==========================================
  // 8. Update UI with Prediction & Stabilization
  // ==========================================
  function updateUIWithPrediction(result) {
    if (!result.success) {
      console.warn("Prediction returned error:", result.error);
      return;
    }

    const {
      predicted_class,
      confidence,
      is_hazard,
      is_awareness,
      status,
      alert_triggered,
      reason,
      all_probabilities
    } = result;

    const confPct = (confidence * 100).toFixed(1);
    const icon = classIcons[predicted_class] || "🔊";

    // Update Banner
    bannerIcon.textContent = icon;
    bannerTitle.textContent = predicted_class;
    bannerSubtitle.textContent = reason;
    bannerConfidence.textContent = `${confPct}%`;
    bannerEngineStatus.textContent = status;

    // Reset styles
    mainAlertBanner.classList.remove("alert-idle", "alert-danger-active", "alert-awareness-active", "alert-normal-active");

    const isAwarenessClass = is_awareness || [
      "Dog Barking", "Door Knock / Bell", "Crying Baby"
    ].includes(predicted_class);

    if (alert_triggered && is_hazard) {
      mainAlertBanner.classList.add("alert-danger-active");
      triggerMultiModalAlert(predicted_class, confPct);
    } else if (isAwarenessClass && confidence >= 0.5) {
      mainAlertBanner.classList.add("alert-awareness-active");
      // Gentle awareness haptic pulse on mobile devices
      if (toggleVibration && toggleVibration.checked && "vibrate" in navigator) {
        navigator.vibrate(200);
      }
    } else if (is_hazard) {
      mainAlertBanner.classList.add("alert-danger-active");
    } else {
      mainAlertBanner.classList.add("alert-normal-active");
    }

    // Update Probability Bars
    if (all_probabilities) {
      let idx = 0;
      for (const [cls, prob] of Object.entries(all_probabilities)) {
        const valElem = document.getElementById(`val-${idx}`);
        const barElem = document.getElementById(`bar-${idx}`);
        if (valElem && barElem) {
          const pct = (prob * 100).toFixed(1);
          valElem.textContent = `${pct}%`;
          barElem.style.width = `${pct}%`;

          // Hazard bar highlight
          const isHazardClass = [
            "Siren (Emergency Vehicle)", "Car Horn (Traffic)", "Fire / Smoke Alarm", "Glass Breaking"
          ].includes(cls);

          if (isHazardClass && prob >= 0.5) {
            barElem.classList.add("hazard-fill");
          } else {
            barElem.classList.remove("hazard-fill");
          }
        }
        idx++;
      }
    }

    // Update Telemetry
    telemStatus.textContent = status;
    telemTemporal.textContent = alert_triggered ? "VERIFIED (Passed)" : (status === "COOLDOWN_SUPPRESSED" ? "COOLDOWN (Active)" : "Tracking");
    telemReason.textContent = reason;

    // Refresh History Table
    fetchHistory();
  }

  // ==========================================
  // 9. Multi-Modal Alert (Strobe & Haptic)
  // ==========================================
  function triggerMultiModalAlert(hazardName, confPct) {
    // 1. Visual Strobe for Deaf/Hard of Hearing Users
    if (toggleStrobe.checked) {
      strobeText.textContent = `🚨 ${hazardName.toUpperCase()}!`;
      strobeSubtext.textContent = `Confidence: ${confPct}% • Alerting surroundings`;
      strobeOverlay.classList.add("active");

      if (strobeTimeout) clearTimeout(strobeTimeout);
      strobeTimeout = setTimeout(() => {
        strobeOverlay.classList.remove("active");
      }, 1400); // 1.4 seconds visual flash
    }

    // 2. Tactile / Haptic Vibration Pattern
    if (toggleVibration.checked && "vibrate" in navigator) {
      // SOS / Warning pulse pattern: vibrate 300ms, pause 100ms, vibrate 300ms, pause 100ms, vibrate 500ms
      navigator.vibrate([300, 100, 300, 100, 500]);
    }
  }

  // ==========================================
  // 10. History Audit Log Fetching
  // ==========================================
  async function fetchHistory() {
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      if (!data.history || data.history.length === 0) {
        historyTableBody.innerHTML = `
          <tr class="empty-row">
            <td colspan="5">No hazard incidents recorded yet. Trigger a sound above to test!</td>
          </tr>
        `;
        return;
      }

      historyTableBody.innerHTML = data.history.map(item => `
        <tr>
          <td><strong>#${item.id}</strong></td>
          <td>${item.timestamp}</td>
          <td><span class="badge-danger">${item.hazard}</span></td>
          <td><strong>${item.confidence}</strong></td>
          <td><span class="badge-dispatched">${item.status}</span></td>
        </tr>
      `).join("");
    } catch (e) {
      console.warn("Failed to fetch history:", e);
    }
  }

  clearHistoryBtn.addEventListener("click", async () => {
    await fetch("/api/clear_history", { method: "POST" });
    fetchHistory();
  });

  // Initial fetch
  fetchHistory();
});
