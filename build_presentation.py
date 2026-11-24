import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

def build_presentation():
    # Base presentation
    base_path = "g17 project.pptx"
    prs = pptx.Presentation(base_path)
    
    # Slide dimensions
    prs.slide_width = Inches(20.0)
    prs.slide_height = Inches(11.25)
    blank_layout = prs.slide_layouts[6] # Blank slide layout
    
    # Theme Colors
    BG_COLOR = RGBColor(247, 247, 246)       # #F7F7F6 Warm off-white
    CARD_BG = RGBColor(255, 255, 255)        # #FFFFFF Pure white
    CARD_BORDER = RGBColor(226, 232, 240)    # #E2E8F0 Subtle gray
    TEXT_MAIN = RGBColor(17, 24, 39)         # #111827 Dark charcoal/black
    TEXT_MUTED = RGBColor(75, 85, 99)        # #4B5563 Slate gray
    ACCENT_BLUE = RGBColor(30, 58, 138)      # #1E3A8A Deep navy blue
    ACCENT_ORANGE = RGBColor(217, 119, 6)    # #D97706 Warm amber
    ACCENT_RED = RGBColor(220, 38, 38)       # #DC2626 Hazard red
    ACCENT_GREEN = RGBColor(22, 101, 52)     # #166534 Forest green

    slides_data = [
        {
            "title": "ALGORITHM",
            "subtitle": "Real-Time Environmental Audio Classification & Stabilization Pipeline",
            "diagram": "diagram_algorithm.png",
            "bullets": [
                ("Procedural Pipeline Execution", "Processes microphone audio through a deterministic 5-stage real-time execution loop with continuous temporal buffering."),
                ("Audio Ring Buffer Ingestion", "Captures ambient waveforms via microphone at 16 kHz mono in overlapping sliding windows (1.0s to 5.0s buffer with 50% step overlap)."),
                ("Log-Mel Feature Extraction", "Transforms temporal waveforms into time-frequency energy representations via Short-Time Fourier Transform (STFT, N_fft=2048, hop=512) and 128 Mel filterbanks with logarithmic scaling: S_log = log10(S_mel + 1e-6)."),
                ("Deep CNN Forward Inference", "Feeds spectrogram tensor (128 x T x 1) into CNN layers, computing posterior class probability distribution P = [p_1, ..., p_C] via Softmax."),
                ("Multi-Stage Prediction Stabilization", "Evaluates three sequential filtering barriers to eliminate false alarms:"),
                ("  • Confidence Gating", "Rejects indeterminate background sounds where max(P) < 0.70 threshold."),
                ("  • Temporal Majority Voting", "Maintains circular queue (W = 3 to 5 frames); requires consecutive agreement."),
                ("  • Cooldown Debounce Timer", "Suppresses duplicate notifications for continuous events (t_cooldown = 3.0s)."),
                ("Multi-Modal Alert Dispatch", "Fires concurrent high-contrast visual strobes and device tactile vibration patterns upon confirmed hazard.")
            ]
        },
        {
            "title": "FUNCTION ORIENTED DESIGN",
            "subtitle": "Procedural Structure Chart & Functional Module Decomposition",
            "diagram": "diagram_fod.png",
            "bullets": [
                ("Top-Down Functional Decomposition", "Organizes system logic into clear hierarchical modules with clean data couples and control flags:"),
                ("  • 0.0 Main Controller", "Central orchestrator coordinating application lifecycle, streaming threads, and event handling."),
                ("  • 1.0 Audio Capture Subsystem", "Initializes microphone hardware, reads continuous PCM buffer, and manages buffer overruns."),
                ("  • 2.0 Audio Preprocessing", "Downmixes stereo channels to mono, resamples audio to 16 kHz, and normalizes amplitude to [-1.0, 1.0]."),
                ("  • 3.0 Feature Extraction", "Executes STFT spectral analysis, applies Mel filterbanks, and computes logarithmic compression."),
                ("  • 4.0 CNN Inference Engine", "Loads trained Keras weights, aligns input tensor dimensions, and executes forward pass classification."),
                ("  • 5.0 Prediction Stabilization", "Applies confidence thresholding, sliding FIFO queue voting, and cooldown interval tracking."),
                ("  • 6.0 Multi-Modal Dispatcher", "Triggers visual UI banners, drives device haptic vibration motors, and refreshes status feeds."),
                ("  • 7.0 Storage & Telemetry", "Records detection logs, persists accessibility preferences, and purges expired audit trails."),
                ("Coupling & Cohesion Attributes", "Achieves high intra-module cohesion with low inter-module coupling via standardized numerical arrays and structured records.")
            ]
        },
        {
            "title": "DATA FLOW DIAGRAM (LEVEL 0)",
            "subtitle": "Context-Level System Boundary & External Entity Interactions",
            "diagram": "diagram_dfd0.png",
            "bullets": [
                ("System Boundary Definition", "Defines the high-level boundary of AcousticGuard AI interacting with external hardware, users, and storage layers:"),
                ("  • Hearing-Impaired User", "Configures detection sensitivity, selects visual alert themes (strobe/banner), enables haptic vibration, and perceives accessible notifications."),
                ("  • Microphone Hardware", "Continuous physical sensor capturing ambient environmental sound pressure and streaming uncompressed digital PCM audio."),
                ("  • Visual & Vibration Actuators", "Physical display screens and haptic vibration motors delivering real-time sensory alerts."),
                ("  • System Database Storage", "Local/cloud persistent repository storing user configuration profiles, trained CNN weights, and historical detection audit logs."),
                ("Core Information Exchanges", "Transforms continuous raw audio inputs into actionable visual/tactile outputs in under 200ms latency without requiring internet connectivity during edge inference.")
            ]
        },
        {
            "title": "DATA FLOW DIAGRAM (LEVEL 1)",
            "subtitle": "Functional Data Flow Decomposition & Internal Data Stores",
            "diagram": "diagram_dfd1.png",
            "bullets": [
                ("Process 1.0: Audio Ingestion", "Receives raw PCM stream from microphone, downmixes to mono, standardizes duration, and outputs 16 kHz audio."),
                ("Process 2.0: Feature Extraction", "Computes STFT and converts audio waveform into a 2D Log-Mel Spectrogram matrix (128 frequency bands)."),
                ("Process 3.0: CNN Classification", "Consumes spectrogram tensor and references Trained Model Weights (Data Store D1) to compute class probabilities."),
                ("Process 4.0: Prediction Filtering", "Reads and writes to Sliding Temporal Prediction Buffer (Data Store D2) to filter unstable noise and verify danger persistence."),
                ("Process 5.0: Alert Generation", "Dispatches prioritized visual warning signals and tactile haptic impulses upon verified hazard detection."),
                ("Process 6.0: Event Logging", "Commits detection event records (timestamp, class, confidence) to System Event DB (Data Store D3) and serves real-time status feeds to the user.")
            ]
        },
        {
            "title": "ACTIVITY DIAGRAM",
            "subtitle": "Operational Workflow with Swimlanes, Concurrency & Decision Branches",
            "diagram": "diagram_activity.png",
            "bullets": [
                ("User Swimlane", "User launches application, grants microphone permission, and configures alert sensitivity and vibration modes."),
                ("Audio Ingestion Swimlane", "Initializes audio stream, continuously captures 16 kHz PCM buffers, downmixes channels, and normalizes amplitudes."),
                ("Feature & Inference Swimlane", "Computes 128-band Log-Mel spectrograms and executes CNN forward pass to generate Softmax class probabilities."),
                ("Stabilization & Decision Swimlane", "Applies comprehensive multi-tier filtering logic:"),
                ("  • Threshold Gate", "Evaluates if top prediction confidence >= 0.70; discards indeterminate noise."),
                ("  • Danger Match", "Verifies if detected class matches target hazard list (Siren, Car Horn, Glass Breaking, Alarm)."),
                ("  • Temporal Smoothing", "Requires at least 3 consecutive matching predictions in sliding window."),
                ("  • Cooldown Check", "Validates cooldown timer (3.0s) has expired to avoid repetitive notification flooding."),
                ("Alert & Notification Swimlane", "Executes concurrent fork: renders high-contrast visual strobe, fires haptic vibration motor, and writes event log record.")
            ]
        },
        {
            "title": "SYSTEM FLOWCHART",
            "subtitle": "Runtime Execution Control Flow & Logic Branching Sequence",
            "diagram": "diagram_flowchart.png",
            "bullets": [
                ("System Boot & Initialization", "Loads dependencies, deserializes pretrained CNN weights (acousticguard.keras), retrieves user alert preferences, and opens microphone stream."),
                ("Real-Time Processing Loop", "Continuously executes while system monitoring is active:"),
                ("  1. Ingestion & Preprocessing", "Reads 5.0s audio buffer with 50% overlap, converts to mono, resamples to 16 kHz, and normalizes waveform [-1.0, 1.0]."),
                ("  2. Spectrogram Extraction", "Extracts 128 Mel-band Log-Mel Spectrogram matrix representation."),
                ("  3. Neural Inference", "Feeds spectrogram into CNN classifier; computes class probabilities vector P and identifies (C_max, P_max)."),
                ("  4. Confidence & Target Evaluation", "Checks P_max >= 0.70 and C_max in Target Danger Sounds; updates ambient status if non-hazard."),
                ("  5. Temporal & Cooldown Verification", "Requires >= 3 temporal agreement frames and verifies (t - t_last > 3.0s) cooldown debounce."),
                ("  6. Multi-Modal Dispatch", "Fires visual warning strobe, triggers vibration pulse sequence, persists audit record, and updates last alert timestamp t_last.")
            ]
        },
        {
            "title": "CLASS DIAGRAM",
            "subtitle": "Object-Oriented Architecture, Class Specifications & Structural Contracts",
            "diagram": "diagram_class.png",
            "bullets": [
                ("AudioStreamManager", "Encapsulates microphone hardware interface, audio sampling threads, ring buffer queues, and stream lifecycle."),
                ("AudioPreprocessor", "Performs channel reduction (stereo to mono), resampling to 16 kHz, and amplitude standardization."),
                ("FeatureExtractor", "Mathematical transformation service computing STFT and extracting 128-band Log-Mel spectrogram matrices."),
                ("CNNClassifier", "TensorFlow/Keras wrapper managing neural model weights, tensor reshaping, and forward inference execution."),
                ("PredictionStabilizer", "Implements rolling FIFO queue, sliding temporal majority voting, and cooldown interval tracking."),
                ("AlertDecisionEngine", "Policy evaluator checking hazard severity thresholds and dispatching multi-modal alert actions."),
                ("NotificationManager", "Controls UI flashing strobes, color themes, and drives Web Vibration / native haptic APIs."),
                ("DatabaseService", "Data access adapter handling CRUD persistence for detection logs, telemetry, and user preferences.")
            ]
        },
        {
            "title": "ENTITY-RELATIONSHIP DIAGRAM",
            "subtitle": "Conceptual Data Modeling, Relational Cardinalities & Keys",
            "diagram": "diagram_er.png",
            "bullets": [
                ("USERS Entity", "Stores user account information, authorization role, and creation timestamp (PK: user_id UUID)."),
                ("USER_PREFERENCES Entity", "Maintains 1:1 relationship with USERS, storing customized visual alert color schemes, vibration toggles, sensitivity thresholds, and cooldown durations."),
                ("SOUND_CLASSES Entity", "Master catalog of 50 ESC-50 categories with danger sound flags, hazard categories, and risk priority ratings (PK: class_id INT)."),
                ("DETECTION_EVENTS Entity", "Records every verified sound detection instance (PK: event_id UUID, FK: user_id, FK: class_id, confidence, timestamp, spectrogram path)."),
                ("ALERT_LOGS Entity", "Audits notification dispatches (PK: alert_id UUID, FK: event_id, channel, delivery status, latency in ms, acknowledged flag)."),
                ("DEVICE_CONFIG Entity", "Stores registered client device hardware specifications, microphone sample rates, and buffer durations (PK: device_id UUID, FK: user_id).")
            ]
        },
        {
            "title": "SEQUENCE DIAGRAM",
            "subtitle": "End-to-End Real-Time Detection Message Exchange & Object Lifelines",
            "diagram": "diagram_sequence.png",
            "bullets": [
                ("Session Activation", "Hearing-impaired user launches app; Audio Ingestion service initializes microphone hardware capture stream."),
                ("Continuous Frame Acquisition", "Microphone streams uncompressed PCM chunks (16 kHz mono) to Audio Ingestion & Preprocessor."),
                ("Feature Extraction Pipeline", "Preprocessor invokes FeatureExtractor.extractLogMelSpectrogram(), returning 2D Log-Mel spectrogram tensor."),
                ("Model Classification Call", "Preprocessor forwards spectrogram tensor to CNN Inference Engine; receives Softmax probability vector."),
                ("Prediction Stabilization Check", "Preprocessor pushes predicted class and confidence to PredictionStabilizer; validates threshold (>= 0.70), rolling queue, and cooldown."),
                ("Parallel Alert Dispatch (par)", "Upon hazard confirmation, Alert Decision Engine triggers concurrent actions:"),
                ("  • Visual Display", "Notification UI renders flashing high-contrast red warning banner."),
                ("  • Haptic Actuator", "Device triggers tactile vibration buzzer pattern (SOS cadence)."),
                ("  • Asynchronous Logging", "Persists event record with latency and confidence to System DB.")
            ]
        },
        {
            "title": "LOGICAL DATABASE DESIGN",
            "subtitle": "Normalized Relational Schema (3NF) & Integrity Constraints",
            "diagram": "diagram_db_logical.png",
            "bullets": [
                ("3NF Normalization Strategy", "Schema is strictly decomposed into Third Normal Form to ensure database integrity and eliminate redundancy:"),
                ("  • 1NF (Atomic Data)", "All attribute values are atomic; no repeating groups or composite columns."),
                ("  • 2NF (Full Key Dependency)", "All non-key attributes are fully functionally dependent on the entire primary key."),
                ("  • 3NF (No Transitive Dependencies)", "Eliminates non-prime attribute dependencies on other non-prime attributes."),
                ("Relational Schema Definitions", "Strictly structured normalized relations:"),
                ("  • T1: USERS", "user_id [PK], username, email, role, created_at"),
                ("  • T2: USER_PREFERENCES", "pref_id [PK], user_id [FK], visual_mode, vibration_enabled, min_confidence, cooldown_sec"),
                ("  • T3: SOUND_CLASSES", "class_id [PK], class_name, is_danger_sound, esc50_category, risk_priority"),
                ("  • T4: DETECTION_EVENTS", "event_id [PK], user_id [FK], class_id [FK], confidence, detected_at, is_verified"),
                ("  • T5: ALERT_DISPATCHES", "alert_id [PK], event_id [FK], channel, delivery_latency_ms, acknowledged"),
                ("Referential Integrity", "Foreign key constraints with ON DELETE CASCADE on user profiles and domain range checks.")
            ]
        },
        {
            "title": "PHYSICAL DATABASE DESIGN",
            "subtitle": "PostgreSQL & SQLite Physical Schema, Indexing & Storage Engine",
            "diagram": "diagram_db_physical.png",
            "bullets": [
                ("Hybrid Storage Architecture", "Optimized dual-storage deployment using PostgreSQL 16 for cloud synchronization and embedded SQLite 3 for zero-latency offline edge inference."),
                ("Optimized Physical Column Types", "UUID keys (gen_random_uuid()), VARCHAR(50), single-precision REAL floats for confidence, TIMESTAMPTZ, and BOOLEAN."),
                ("High-Performance Indexing Strategy:", ""),
                ("  • B-Tree Composite Index", "idx_user_events ON detection_events(user_id, detected_at DESC) for sub-5ms chronological query history."),
                ("  • Hash Index", "idx_sound_class_name ON sound_classes USING HASH (class_name) for O(1) class lookups during inference."),
                ("  • Partial Index", "idx_danger_alerts ON sound_classes(is_danger) WHERE is_danger = TRUE for instantaneous hazard filtering."),
                ("Storage Partitioning & TTL Purging", "detection_events table partitioned by monthly ranges; automated background worker prunes raw spectrogram paths after 30 days."),
                ("Zero-Persistence Audio Policy", "Raw microphone audio streams reside exclusively in RAM circular buffers to guarantee user privacy.")
            ]
        }
    ]

    # Create slides for each item
    for data in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        
        # Set solid background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR
        
        # Decorative top accent bar
        accent_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(1.0), Inches(0.55), Inches(0.4), Inches(1.1)
        )
        accent_bar.fill.solid()
        accent_bar.fill.fore_color.rgb = ACCENT_ORANGE
        accent_bar.line.color.rgb = ACCENT_ORANGE
        
        # Title Box
        title_box = slide.shapes.add_textbox(Inches(1.6), Inches(0.45), Inches(17.4), Inches(1.3))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_title = tf.paragraphs[0]
        p_title.text = data["title"]
        p_title.font.name = "Poppins"
        p_title.font.size = Pt(46)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN
        
        p_sub = tf.add_paragraph()
        p_sub.text = data["subtitle"]
        p_sub.font.name = "Poppins"
        p_sub.font.size = Pt(20)
        p_sub.font.color.rgb = TEXT_MUTED
        
        # Content Box (Left Column Card)
        content_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(1.0), Inches(1.95), Inches(9.2), Inches(8.75)
        )
        content_card.fill.solid()
        content_card.fill.fore_color.rgb = CARD_BG
        content_card.line.color.rgb = CARD_BORDER
        content_card.line.width = Pt(1.5)
        
        content_tf = content_card.text_frame
        content_tf.word_wrap = True
        content_tf.margin_left = Inches(0.4)
        content_tf.margin_right = Inches(0.4)
        content_tf.margin_top = Inches(0.4)
        content_tf.margin_bottom = Inches(0.4)
        
        for idx, (head, body) in enumerate(data["bullets"]):
            p = content_tf.add_paragraph() if idx > 0 else content_tf.paragraphs[0]
            p.space_after = Pt(6)
            
            run_head = p.add_run()
            run_head.text = head + (": " if body else "")
            run_head.font.name = "Poppins"
            run_head.font.size = Pt(17)
            run_head.font.bold = True
            if "•" in head:
                run_head.font.color.rgb = ACCENT_BLUE
            else:
                run_head.font.color.rgb = TEXT_MAIN
                
            if body:
                run_body = p.add_run()
                run_body.text = body
                run_body.font.name = "Poppins"
                run_body.font.size = Pt(16)
                run_body.font.color.rgb = TEXT_MUTED

        # Diagram Card (Right Column)
        diagram_path = data["diagram"]
        if os.path.exists(diagram_path):
            card_left = Inches(10.5)
            card_top = Inches(1.95)
            card_width = Inches(8.5)
            card_height = Inches(8.75)
            
            diag_card = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                card_left, card_top, card_width, card_height
            )
            diag_card.fill.solid()
            diag_card.fill.fore_color.rgb = CARD_BG
            diag_card.line.color.rgb = CARD_BORDER
            diag_card.line.width = Pt(1.5)
            
            # Open image to get aspect ratio
            im = Image.open(diagram_path)
            im_w, im_h = im.size
            aspect = im_w / im_h
            
            max_img_w = Inches(8.0)
            max_img_h = Inches(8.25)
            
            # Calculate fitted size
            if (max_img_w / max_img_h) > aspect:
                # height constrained
                target_h = max_img_h
                target_w = target_h * aspect
            else:
                # width constrained
                target_w = max_img_w
                target_h = target_w / aspect
                
            img_left = card_left + (card_width - target_w) / 2
            img_top = card_top + (card_height - target_h) / 2
            
            slide.shapes.add_picture(diagram_path, img_left, img_top, target_w, target_h)

    # Save presentation
    output_filename = "AcousticGuard_AI_System_Design.pptx"
    prs.save(output_filename)
    print(f"Successfully generated {output_filename} with {len(prs.slides)} slides!")
    
    # Also save a copy as 'g17 project.pptx' for the user convenience
    prs.save("g17 project.pptx")
    print("Also updated g17 project.pptx with all system design slides!")

if __name__ == "__main__":
    build_presentation()
