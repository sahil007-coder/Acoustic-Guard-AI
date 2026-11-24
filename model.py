"""
AcousticGuard AI - CNN Classifier Architecture & Inference Engine
Defines the Convolutional Neural Network for environmental hazard sound classification.
"""

import os
import sys
import warnings
import tempfile

# Complete suppression of backend stderr warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib")
warnings.filterwarnings("ignore")

import numpy as np
import tensorflow as tf
tf.get_logger().setLevel("ERROR")

# Enable dynamic GPU memory growth to prevent ZeroGPU VRAM overload
try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
except Exception:
    pass

from tensorflow import keras
from keras import layers

# Defined Target Classes (aligned with ESC-50 Environmental Benchmarks & Accessibility Needs)
CLASSES = [
    "Siren (Emergency Vehicle)",
    "Car Horn (Traffic)",
    "Fire / Smoke Alarm",
    "Glass Breaking",
    "Dog Barking",
    "Door Knock / Bell",
    "Crying Baby",
    "Normal Ambient"
]

# High-priority danger classes that trigger emergency visual strobes & haptic alerts
HAZARD_CLASSES = {
    "Siren (Emergency Vehicle)",
    "Car Horn (Traffic)",
    "Fire / Smoke Alarm",
    "Glass Breaking"
}

NUM_CLASSES = len(CLASSES)
INPUT_SHAPE = (128, 94, 1)  # (n_mels, time_frames, channels)
DEFAULT_WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "models", "acousticguard.keras")


def build_acousticguard_cnn(input_shape=INPUT_SHAPE, num_classes=NUM_CLASSES) -> keras.Model:
    """
    Constructs a high-accuracy 2D Convolutional Neural Network
    for real-time inference on Log-Mel Spectrogram inputs.
    """
    model = keras.Sequential([
        layers.Input(shape=input_shape),

        # Conv Block 1
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.20),

        # Conv Block 2
        layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.25),

        # Conv Block 3
        layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.30),

        # Dense Head
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.35),
        layers.Dense(num_classes, activation='softmax', name="posterior_probabilities")
    ], name="AcousticGuard_CNN")

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


class AcousticGuardModel:
    """
    Inference wrapper for loading trained weights and executing forward passes.
    """
    def __init__(self, weights_path: str = DEFAULT_WEIGHTS_PATH):
        self.weights_path = weights_path
        self.model = None
        self._load_or_build()

    def _load_or_build(self):
        if os.path.exists(self.weights_path):
            try:
                self.model = keras.models.load_model(self.weights_path)
                print(f"[AcousticGuardModel] Loaded trained model weights from {self.weights_path}")
                return
            except Exception as e:
                print(f"[AcousticGuardModel] Failed to load {self.weights_path} ({e}). Retraining...")

        # Auto-train and export weights if missing
        print("[AcousticGuardModel] Training model weights on initial startup...")
        try:
            from train import train_and_export
            train_and_export()
            self.model = keras.models.load_model(self.weights_path)
            print(f"[AcousticGuardModel] Model trained and loaded successfully from {self.weights_path}")
        except Exception as e:
            print(f"[AcousticGuardModel] Fallback to direct model compilation: {e}")
            self.model = build_acousticguard_cnn()

    def predict(self, spectrogram: np.ndarray) -> dict:
        """
        Runs inference on a single spectrogram of shape (128, 94, 1) or batch (N, 128, 94, 1).
        """
        if spectrogram.ndim == 3:
            spectrogram = np.expand_dims(spectrogram, axis=0)

        probs = self.model.predict(spectrogram, verbose=0)[0]

        top_idx = int(np.argmax(probs))
        top_class = CLASSES[top_idx]
        confidence = float(probs[top_idx])
        is_hazard = top_class in HAZARD_CLASSES

        probabilities_dict = {
            CLASSES[i]: round(float(probs[i]), 4)
            for i in range(len(CLASSES))
        }

        return {
            "predicted_class": top_class,
            "class_index": top_idx,
            "confidence": round(confidence, 4),
            "is_hazard": is_hazard,
            "all_probabilities": probabilities_dict
        }
