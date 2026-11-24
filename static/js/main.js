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
  const waveformCanvas = document.getElementById("waveformCanvas");
  const canvasCtx = waveformCanvas.getContext("2d");

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
  let mediaRecorder = null;
  let animationFrameId = null;
  let currentFile = null;
  let strobeTimeout = null;

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

  // ==========================================
  // 4. Live Microphone Real-Time Stream
  // ==========================================
  async function toggleMicrophone() {
    if (!isListening) {
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        const source = audioContext.createMediaStreamSource(mediaStream);
        analyserNode = audioContext.createAnalyser();
        analyserNode.fftSize = 2048;
        source.connect(analyserNode);

        // MediaRecorder for chunk inference
        let recordedChunks = [];
        mediaRecorder = new MediaRecorder(mediaStream);

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            recordedChunks.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          if (recordedChunks.length > 0 && isListening) {
            const audioBlob = new Blob(recordedChunks, { type: "audio/webm" });
            recordedChunks = [];
            await sendAudioForPrediction(audioBlob);
            // Restart recording for next 3-second cycle
            if (isListening) mediaRecorder.start();
          }
        };

        // Start cycle: record 3 seconds chunks
        mediaRecorder.start();
        const recordInterval = setInterval(() => {
          if (!isListening) {
            clearInterval(recordInterval);
            return;
          }
          if (mediaRecorder.state === "recording") {
            mediaRecorder.stop();
          }
        }, 3000);

        isListening = true;
        micToggleBtn.classList.add("btn-recording");
        micBtnText.textContent = "Stop Real-Time Listening";
        micRecordingBadge.classList.remove("hidden");
        startVisualizer();

        bannerTitle.textContent = "Listening to Ambient Audio...";
        bannerSubtitle.textContent = "Streaming 3-second audio windows to CNN inference pipeline";
      } catch (err) {
        alert("Microphone Access Error: " + err.message);
      }
    } else {
      // Stop listening
      isListening = false;
      if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
      }
      if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
      }
      if (audioContext && audioContext.state !== "closed") {
        audioContext.close();
      }

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
    formData.append("audio", audioBlobOrFile);

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
    mainAlertBanner.classList.remove("alert-idle", "alert-danger-active", "alert-normal-active");

    if (alert_triggered) {
      mainAlertBanner.classList.add("alert-danger-active");
      triggerMultiModalAlert(predicted_class, confPct);
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
