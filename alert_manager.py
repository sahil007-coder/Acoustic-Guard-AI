"""
AcousticGuard AI - Prediction Stabilization & Alert Engine
Implements multi-barrier stabilization: Confidence Gating, Temporal Majority Voting, and Cooldown Debouncing.
"""

import time
from collections import deque
from datetime import datetime
from typing import Dict, Any, List

# Stabilization Hyperparameters (matching System Design specifications)
CONFIDENCE_THRESHOLD = 0.70    # Minimum posterior probability required
QUEUE_SIZE = 3                 # Number of consecutive temporal frames required
COOLDOWN_SECONDS = 3.0         # Suppression interval between identical hazard triggers


class AlertManager:
    """
    Stabilizes CNN predictions to prevent false positives and jittery notifications.
    """
    def __init__(
        self,
        confidence_threshold: float = CONFIDENCE_THRESHOLD,
        queue_size: int = QUEUE_SIZE,
        cooldown_seconds: float = COOLDOWN_SECONDS
    ):
        self.confidence_threshold = confidence_threshold
        self.queue_size = queue_size
        self.cooldown_seconds = cooldown_seconds

        # Circular buffer storing recent (class_name, is_hazard, confidence)
        self.history_queue = deque(maxlen=queue_size)

        # Track timestamps of last alert fired for each hazard class
        self.last_alert_times: Dict[str, float] = {}

        # Log of recent alert events for user audit and history panel
        self.alert_audit_log: List[Dict[str, Any]] = []

    def process_prediction(self, raw_prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a raw CNN prediction against the 3-tier stabilization pipeline:
        1. Confidence Threshold Gate
        2. Temporal Majority Voting
        3. Cooldown Debounce Timer
        """
        predicted_class = raw_prediction["predicted_class"]
        confidence = raw_prediction["confidence"]
        is_hazard = raw_prediction["is_hazard"]
        current_time = time.time()
        iso_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        alert_triggered = False
        status = "MONITORING"
        reason = "Normal ambient listening"

        # Barrier 1: Confidence Gating
        if confidence < self.confidence_threshold:
            status = "LOW_CONFIDENCE"
            reason = f"Confidence {confidence:.2f} below threshold {self.confidence_threshold:.2f}"
            # Push non-decision to break streak
            self.history_queue.append(None)
        else:
            # Push valid detection to temporal sliding queue
            self.history_queue.append({
                "class": predicted_class,
                "is_hazard": is_hazard,
                "confidence": confidence,
                "timestamp": current_time
            })

            # Check if current class is a danger sound
            if is_hazard:
                # Barrier 2: Temporal Majority Voting
                # Check if recent frames consistently agree on this hazard
                valid_entries = [e for e in self.history_queue if e is not None and e["class"] == predicted_class]
                majority_agrees = len(valid_entries) >= (self.queue_size - 1)  # At least 2 of 3 (or 3 of 3)

                if majority_agrees:
                    # Barrier 3: Cooldown Debounce
                    last_time = self.last_alert_times.get(predicted_class, 0.0)
                    elapsed = current_time - last_time

                    if elapsed >= self.cooldown_seconds:
                        # ALL 3 BARRIERS PASSED: Fire Multi-Modal Alert!
                        alert_triggered = True
                        status = "ALERT"
                        reason = f"Verified hazard detection ({predicted_class}) with {confidence*100:.1f}% confidence"
                        self.last_alert_times[predicted_class] = current_time

                        # Append to audit log
                        event = {
                            "id": len(self.alert_audit_log) + 1,
                            "timestamp": iso_timestamp,
                            "hazard": predicted_class,
                            "confidence": f"{confidence * 100:.1f}%",
                            "status": "DISPATCHED"
                        }
                        self.alert_audit_log.insert(0, event)
                        if len(self.alert_audit_log) > 50:
                            self.alert_audit_log.pop()
                    else:
                        status = "COOLDOWN_SUPPRESSED"
                        remaining = self.cooldown_seconds - elapsed
                        reason = f"Alert suppressed by cooldown ({remaining:.1f}s remaining)"
                else:
                    status = "WAITING_CONFIRMATION"
                    reason = f"Waiting for temporal confirmation ({len(valid_entries)}/{self.queue_size} frames)"
            else:
                status = "NORMAL"
                reason = f"Detected non-hazard sound: {predicted_class}"

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "is_hazard": is_hazard,
            "status": status,
            "alert_triggered": alert_triggered,
            "reason": reason,
            "timestamp": iso_timestamp,
            "all_probabilities": raw_prediction["all_probabilities"]
        }

    def get_audit_log(self) -> List[Dict[str, Any]]:
        return self.alert_audit_log

    def clear_audit_log(self):
        self.alert_audit_log.clear()
        self.last_alert_times.clear()
        self.history_queue.clear()
