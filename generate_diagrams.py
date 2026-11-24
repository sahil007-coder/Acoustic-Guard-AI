import plantuml
import time
import os

server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')

diagrams = {}

# 1. ALGORITHM
diagrams['diagram_algorithm'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 12
skinparam roundCorner 8
skinparam arrowColor #444444

skinparam activity {
  BackgroundColor #FEF9E7
  BorderColor #D4AC0D
  FontColor #1A1A1A
  FontSize 12
}
skinparam activityDiamond {
  BackgroundColor #FFF2CC
  BorderColor #D6B656
  FontColor #1A1A1A
  FontSize 12
}
skinparam note {
  BackgroundColor #FFEAE8
  BorderColor #E74C3C
  FontColor #900C3F
  FontSize 11
}

title AcousticGuard AI: Real-Time Audio Recognition Algorithm

start
:Initialize Audio Stream;
note right
  - Format: Mono, 16 kHz PCM
  - Buffer Window: 1.0s to 5.0s
  - Overlap: 50% Sliding Step
end note

while (Audio Ingestion Active?) is (yes)
  :Capture Audio Window w(t);
  
  :Standardize & Preprocess Audio;
  note right
    - Cast to float32
    - Amplitude Normalize to [-1.0, 1.0]
    - Resample to 16 kHz
  end note
  
  :Extract Log-Mel Spectrogram;
  note right
    - STFT (N_fft=2048, hop=512)
    - Mel Filterbank (M=128 bands)
    - Log Scaling: S_log = log10(S_mel + eps)
  end note
  
  :CNN Forward Inference;
  note right
    - Input Tensor: [128 x T x 1]
    - Softmax Output: P = [p_1, ..., p_C]
  end note
  
  :Extract Best Class C* and Confidence p*;
  
  if (p* >= Confidence Threshold (0.70)?) then (yes)
    :Push (C*, p*) to Temporal Queue;
    note right: Queue Size W = 3 to 5 frames
    
    if (Temporal Majority Matches Danger Class?) then (yes)
      if (Cooldown Expired (t - t_last > 3.0s)?) then (yes)
        :Generate Visual Strobe Alert;
        :Trigger Device Haptic Vibration;
        :Persist Alert Telemetry to DB;
        :Update Last Alert Timestamp t_last;
      else (no)
        :Suppress Duplicate Alert;
      endif
    else (no)
      :Wait for Consecutive Frame Agreement;
    endif
  else (no)
    :Filter Out / Discard Low-Confidence Frame;
  endif
  
  :Refresh Dashboard Monitoring Status;
endwhile (no)

:Release Audio Hardware & Exit;
stop
@enduml
"""

# 2. FUNCTION ORIENTED DESIGN (Structure Chart)
diagrams['diagram_fod'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam roundCorner 6
skinparam arrowColor #333333

skinparam rectangle {
  BackgroundColor #F8F9FA
  BorderColor #495057
  FontColor #212529
}

title AcousticGuard AI: Function-Oriented Design (Structure Chart)

rectangle "0.0 AcousticGuard Main Controller\\n(Procedural Process Orchestration)" as ROOT #D9E1F2

rectangle "1.0 Audio Capture\\nSubsystem" as M1 #FFF2CC
rectangle "2.0 Audio Preprocessing\\nSubsystem" as M2 #FFF2CC
rectangle "3.0 Feature Extraction\\nSubsystem" as M3 #FFF2CC
rectangle "4.0 CNN Inference\\nEngine" as M4 #E2F0D9
rectangle "5.0 Prediction Filtering\\n& Stabilization" as M5 #E2F0D9
rectangle "6.0 Multi-Modal Alert\\nDispatcher" as M6 #FCE4D6
rectangle "7.0 Persistent Storage\\n& Telemetry" as M7 #E8E8E8

ROOT -down-> M1 : [cmd: start/stop]
ROOT -down-> M2 : [raw PCM stream]
ROOT -down-> M3 : [resampled audio]
ROOT -down-> M4 : [log-Mel tensor]
ROOT -down-> M5 : [raw probabilities]
ROOT -down-> M6 : [verified danger event]
ROOT -down-> M7 : [telemetry data]

rectangle "1.1 Init_Audio_Device()\\n1.2 Read_PCM_Buffer()\\n1.3 Check_Buffer_Overrun()" as S1 #FFFFFF
rectangle "2.1 Convert_To_Mono()\\n2.2 Resample_16kHz()\\n2.3 Normalize_Amplitude()" as S2 #FFFFFF
rectangle "3.1 Compute_STFT()\\n3.2 Apply_Mel_Filterbank()\\n3.3 Log_Compression()" as S3 #FFFFFF
rectangle "4.1 Load_Keras_Model()\\n4.2 Execute_Forward_Pass()\\n4.3 Compute_Softmax()" as S4 #FFFFFF
rectangle "5.1 Gate_Confidence_Score()\\n5.2 Update_Temporal_Buffer()\\n5.3 Check_Cooldown_Timer()" as S5 #FFFFFF
rectangle "6.1 Trigger_Visual_Banner()\\n6.2 Fire_Haptic_Pattern()\\n6.3 Update_Status_UI()" as S6 #FFFFFF
rectangle "7.1 Insert_Event_Record()\\n7.2 Load_User_Preferences()\\n7.3 Purge_Expired_Logs()" as S7 #FFFFFF

M1 -down-> S1
M2 -down-> S2
M3 -down-> S3
M4 -down-> S4
M5 -down-> S5
M6 -down-> S6
M7 -down-> S7
@enduml
"""

# 3. DATA FLOW DIAGRAM (Level 0 - Context Diagram)
diagrams['diagram_dfd0'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 12
skinparam roundCorner 8
skinparam arrowColor #333333

skinparam rectangle {
  BackgroundColor #E9ECEF
  BorderColor #495057
  FontColor #212529
}

title AcousticGuard AI: Data Flow Diagram (Level 0 - Context Diagram)

rectangle "Hearing-Impaired\\nUser" as USER #E2F0D9
rectangle "Microphone\\nHardware" as MIC #FCE4D6
rectangle "Visual Display &\\nVibration Actuators" as ACTUATOR #FFF2CC
rectangle "Persistent Database\\n(Local / Cloud Storage)" as DB #EDEDED

rectangle "\\n       [ Process 0.0 ]       \\nAcousticGuard AI\\nReal-Time Environmental\\nSound Recognition System\\n" as SYS #CFE2FF

MIC -down-> SYS : Continuous Raw Audio Stream\\n(Ambient Acoustic Waveforms)
USER -right-> SYS : Sensitivity & Alert Preferences,\\nAcknowledgment Inputs
SYS -left-> USER : Accessible Alert Visuals,\\nConfidence Score & Status
SYS -down-> ACTUATOR : High-Contrast Color Strobes,\\nHaptic Vibration Pulses
SYS -right-> DB : Detection Event Logs,\\nLatency & Telemetry Metrics
DB -left-> SYS : User Configuration Profile,\\nTrained CNN Weights
@enduml
"""

# 4. DATA FLOW DIAGRAM (Level 1)
diagrams['diagram_dfd1'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam roundCorner 6
skinparam arrowColor #333333

title AcousticGuard AI: Data Flow Diagram (Level 1)

skinparam rectangle {
  BackgroundColor #F8F9FA
  BorderColor #495057
  FontColor #212529
}

rectangle "Microphone Hardware" as MIC #FCE4D6
rectangle "Hearing-Impaired User" as USER #E2F0D9
rectangle "Display & Vibration Actuators" as UI #FFF2CC

rectangle "1.0\\nAudio Ingestion &\\nPreprocessing" as P1 #D9E1F2
rectangle "2.0\\nLog-Mel Spectrogram\\nExtraction" as P2 #D9E1F2
rectangle "3.0\\nCNN Sound\\nClassification" as P3 #D9E1F2
rectangle "4.0\\nPrediction Filtering\\n& Stabilization" as P4 #D9E1F2
rectangle "5.0\\nMulti-Modal Alert\\nGeneration" as P5 #D9E1F2
rectangle "6.0\\nEvent Logging &\\nState Management" as P6 #D9E1F2

database "D1: Trained CNN Model (.keras)" as D1 #E8F4F8
database "D2: Temporal Prediction Buffer" as D2 #FEF9E7
database "D3: System Event & Preferences DB" as D3 #E2E3E5

MIC -down-> P1 : Raw PCM Audio Stream
P1 -down-> P2 : Resampled 16 kHz Mono Audio
P2 -right-> P3 : Log-Mel Spectrogram Matrix
D1 -down-> P3 : Model Weights & Target Classes
P3 -right-> P4 : Raw Class Predictions & Confidences
P4 <-> D2 : Read / Write Sliding Window Predictions
P4 -down-> P5 : Validated Danger Sound Event
P5 -right-> UI : Trigger High-Priority Visual & Haptic Alerts
P5 -down-> P6 : Alert Log Record (Time, Class, Conf)
P6 -right-> D3 : Commit Audit Trail Record
USER -down-> P6 : Set Thresholds & Alert Mode
P6 -up-> USER : Real-Time Sound Status Feed
@enduml
"""

# 5. ACTIVITY DIAGRAM
diagrams['diagram_activity'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam roundCorner 8
skinparam arrowColor #333333

skinparam activity {
  BackgroundColor #FEF9E7
  BorderColor #D4AC0D
  FontColor #1A1A1A
}
skinparam activityDiamond {
  BackgroundColor #FFF2CC
  BorderColor #D6B656
  FontColor #1A1A1A
}

title AcousticGuard AI: Activity Diagram

|User|
start
:Launch AcousticGuard AI App;
:Grant Microphone Permissions;
:Configure Thresholds & Haptic Mode;

|Audio Ingestion|
:Initialize Audio Stream;
repeat
  :Capture Audio Buffer (PCM 16 kHz);
  :Standardize Duration & Convert to Mono;

|Feature & Inference Engine|
  :Compute Log-Mel Spectrogram (128 Bands);
  :Execute CNN Forward Pass;
  :Generate Softmax Probabilities;

|Stabilization & Decision Engine|
  if (Confidence >= Threshold (0.70)?) then (yes)
    :Push (Class, Conf) to Sliding Window;
    if (Matches Target Danger Sound?) then (yes)
      if (Consecutive Identical Predictions >= 3?) then (yes)
        if (Cooldown Timer Expired (3.0s)?) then (yes)
          |Alert & Notification|
          fork
            :Render High-Contrast Visual Strobe;
          fork again
            :Trigger Device Haptic Vibration;
          fork again
            :Log Detection Event into Database;
          end fork
          :Reset Cooldown Timer;
        else (no)
          :Suppress Redundant Alert (Debounce);
        endif
      else (no)
        :Accumulate Temporal Votes;
      endif
    else (no)
      :Update Ambient Category Display;
    endif
  else (no)
    :Discard Unstable / Noise Prediction;
  endif

|Audio Ingestion|
repeat while (Session Active?) is (yes)
->no;

|User|
:Close Application;
stop
@enduml
"""

# 6. SYSTEM FLOWCHART
diagrams['diagram_flowchart'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam roundCorner 8
skinparam arrowColor #333333

skinparam activity {
  BackgroundColor #F4F6F7
  BorderColor #34495E
  FontColor #1A252F
}
skinparam activityDiamond {
  BackgroundColor #FFF3CD
  BorderColor #856404
  FontColor #856404
  FontSize 11
}

title AcousticGuard AI: System Execution Flowchart

start
:Start System & Load Dependencies;
:Load Pretrained CNN Classifier;
:Load User Alert Sensitivity & Preferences;
:Initialize Microphone Audio Stream;

while (System Monitoring Active?) is (True)
  :Read Audio Buffer (5.0s window, 50% overlap);
  :Resample to 16 kHz Mono & Normalize Waveform;
  :Extract Log-Mel Spectrogram Matrix;
  :Execute CNN Model Forward Inference;
  :Obtain Class Probabilities Vector P;
  :Select Class C_max with Highest Confidence P_max;
  
  if (P_max >= Confidence Threshold (0.70)?) then (Yes)
    :Store (C_max, P_max) in Temporal Window;
    if (C_max in Target Danger Sounds List?) then (Yes)
      if (Temporal Agreement >= 3 Frames?) then (Yes)
        if (Cooldown Expired (t - t_last > 3.0s)?) then (Yes)
          :Generate Visual Strobe Warning Banner;
          :Trigger Tactile Vibration Pulse;
          :Persist Detection Record to DB;
          :Update Last Alert Timestamp t_last;
        else (No)
          :Suppress Duplicate Alert (In Cooldown);
        endif
      else (No)
        :Await Consecutive Frame Confirmation;
      endif
    else (No)
      :Display Ambient Sound Category;
    endif
  else (No)
    :Classify as Indeterminate Noise;
  endif
  
  :Update UI Dashboard Status;
endwhile (False)

:Stop Audio Stream & Release Microphone;
:Persist Session Summary Logs;
stop
@enduml
"""

# 7. CLASS DIAGRAM
diagrams['diagram_class'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 10
skinparam roundCorner 6
skinparam arrowColor #2C3E50

skinparam class {
  BackgroundColor #F8F9FA
  BorderColor #2C3E50
  ArrowColor #2C3E50
  HeaderBackgroundColor #E9ECEF
  FontSize 10
  AttributeFontSize 9
  MethodFontSize 9
}

title AcousticGuard AI: Class Diagram

class AudioStreamManager {
  - sampleRate : int
  - channels : int
  - bufferSize : int
  - isListening : bool
  + startStream() : void
  + stopStream() : void
  + readBuffer() : ndarray
}

class AudioPreprocessor {
  - targetSampleRate : int
  - clipDuration : float
  + convertToMono(audio: ndarray) : ndarray
  + resample(audio: ndarray) : ndarray
  + normalize(audio: ndarray) : ndarray
}

class FeatureExtractor {
  - nMels : int
  - nFft : int
  - hopLength : int
  + computeSTFT(audio: ndarray) : ndarray
  + extractLogMelSpectrogram(audio: ndarray) : ndarray
}

class CNNClassifier {
  - modelPath : string
  - classes : List<string>
  - confidenceThreshold : float
  + loadModel() : bool
  + predict(spectrogram: ndarray) : PredictionResult
}

class PredictionStabilizer {
  - windowSize : int
  - historyBuffer : Deque<PredictionResult>
  - cooldownPeriodSec : float
  - lastAlertTime : float
  + pushPrediction(pred: PredictionResult) : void
  + getMajorityClass() : string
  + isStableDanger() : bool
  + isCooldownActive() : bool
}

class AlertDecisionEngine {
  - dangerClasses : Set<string>
  - minConfidence : float
  + evaluateAlert(pred: PredictionResult) : AlertAction
  + dispatchNotification(action: AlertAction) : void
}

class NotificationManager {
  - visualAlertActive : bool
  - vibrationSupported : bool
  + showVisualStrobe(label: string, conf: float) : void
  + triggerHapticVibration(pattern: int[]) : void
  + clearAlert() : void
}

class DatabaseService {
  - dbConnectionUri : string
  + logDetectionEvent(event: DetectionRecord) : bool
  + getUserPreferences(userId: string) : UserConfig
  + saveUserPreferences(config: UserConfig) : bool
}

AudioStreamManager --> AudioPreprocessor : passes raw audio
AudioPreprocessor --> FeatureExtractor : passes clean audio
FeatureExtractor --> CNNClassifier : passes spectrogram tensor
CNNClassifier --> PredictionStabilizer : passes raw predictions
PredictionStabilizer --> AlertDecisionEngine : passes stabilized state
AlertDecisionEngine --> NotificationManager : triggers multi-modal alerts
AlertDecisionEngine --> DatabaseService : records detection telemetry
@enduml
"""

# 8. ENTITY-RELATIONSHIP DIAGRAM
diagrams['diagram_er'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam roundCorner 6
skinparam arrowColor #333333

hide circle
hide methods

skinparam class {
  BackgroundColor #FDFEFE
  BorderColor #34495E
  HeaderBackgroundColor #D5D8DC
  FontSize 11
  AttributeFontSize 10
}

title AcousticGuard AI: Entity-Relationship (ER) Diagram

class "USERS" as USERS {
  * user_id : UUID [PK]
  --
  username : VARCHAR(50)
  email : VARCHAR(100)
  role : VARCHAR(20)
  created_at : TIMESTAMPTZ
}

class "USER_PREFERENCES" as PREFS {
  * pref_id : UUID [PK]
  --
  * user_id : UUID [FK]
  visual_alert_theme : VARCHAR(30)
  vibration_enabled : BOOLEAN
  min_confidence_threshold : FLOAT
  cooldown_interval_sec : INT
  updated_at : TIMESTAMPTZ
}

class "SOUND_CLASSES" as SOUNDS {
  * class_id : INT [PK]
  --
  class_name : VARCHAR(60)
  is_danger_sound : BOOLEAN
  esc50_category : VARCHAR(50)
  risk_level : VARCHAR(20)
  description : TEXT
}

class "DETECTION_EVENTS" as EVENTS {
  * event_id : UUID [PK]
  --
  * user_id : UUID [FK]
  * class_id : INT [FK]
  confidence_score : FLOAT
  detected_at : TIMESTAMPTZ
  spectrogram_path : VARCHAR(255)
  is_verified : BOOLEAN
}

class "ALERT_LOGS" as ALERTS {
  * alert_id : UUID [PK]
  --
  * event_id : UUID [FK]
  channel : VARCHAR(30)
  delivery_status : VARCHAR(20)
  latency_ms : INT
  triggered_at : TIMESTAMPTZ
}

class "DEVICE_CONFIG" as DEVICES {
  * device_id : UUID [PK]
  --
  * user_id : UUID [FK]
  device_name : VARCHAR(100)
  platform : VARCHAR(50)
  sample_rate : INT
  buffer_duration_sec : FLOAT
  last_active_at : TIMESTAMPTZ
}

USERS ||--o| PREFS : "has configuration"
USERS ||--o{ DEVICES : "operates"
USERS ||--o{ EVENTS : "records"
SOUNDS ||--o{ EVENTS : "classified_as"
EVENTS ||--|{ ALERTS : "dispatches"
@enduml
"""

# 9. SEQUENCE DIAGRAM
diagrams['diagram_sequence'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam roundCorner 6
skinparam arrowColor #2C3E50

skinparam sequence {
  ParticipantBackgroundColor #E8F4F8
  ParticipantBorderColor #2C3E50
  LifeLineBorderColor #7F8C8D
  LifeLineBackgroundColor #BDC3C7
  ArrowColor #2C3E50
  ActorBackgroundColor #E2F0D9
  ActorBorderColor #27AE60
}

title AcousticGuard AI: End-to-End Real-Time Detection Sequence

actor "Hearing-Impaired\\nUser" as User
participant "Microphone\\nHardware" as Mic
participant "Audio Ingestion\\n& Preprocessor" as Prep
participant "Feature\\nExtractor" as Feat
participant "CNN Inference\\nEngine" as CNN
participant "Prediction\\nStabilizer" as Stab
participant "Alert Decision\\nEngine" as Engine
participant "Notification\\nUI & Haptics" as AlertUI
database "System DB\\n(Storage)" as DB

User -> Prep : Start Monitoring Session
activate Prep
Prep -> Mic : Start Audio Capture Stream()
activate Mic

loop Real-Time Audio Loop (Overlapping Windows)
  Mic --> Prep : Deliver PCM Buffer (16 kHz, Mono)
  Prep -> Feat : extractLogMelSpectrogram(pcmBuffer)
  activate Feat
  Feat --> Prep : Log-Mel Spectrogram Tensor
  deactivate Feat
  
  Prep -> CNN : predict(spectrogramTensor)
  activate CNN
  CNN --> Prep : Probabilities [Siren: 0.89, Car Horn: 0.05, ...]
  deactivate CNN
  
  Prep -> Stab : pushPrediction(Class: "Siren", Conf: 0.89)
  activate Stab
  Stab -> Stab : Validate Threshold (0.89 >= 0.70)
  Stab -> Stab : Check Rolling Queue & Cooldown
  
  alt Stable Danger Sound Confirmed & Cooldown Inactive
    Stab -> Engine : onDangerDetected("Siren", 0.89)
    activate Engine
    
    par Multi-Modal Alerting
      Engine -> AlertUI : showVisualStrobe("EMERGENCY SIREN DETECTED")
      AlertUI --> User : Display Flashing Red Warning Banner
      Engine -> AlertUI : triggerHapticVibration(SOS_Pattern)
      AlertUI --> User : Tactile Vibration Buzz
    else Background Logging
      Engine -> DB : logAlertEvent(eventId, "Siren", 0.89, timestamp)
    end
    
    Engine --> Stab : Alert Dispatched
    deactivate Engine
  else Below Threshold or Cooldown Active
    Stab -> AlertUI : updateStatus("Monitoring / Ambient Normal")
    AlertUI --> User : Update Ambient UI Indicator
  end
  deactivate Stab
end
deactivate Mic
deactivate Prep
@enduml
"""

# 10. LOGICAL DATABASE DESIGN
diagrams['diagram_db_logical'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam roundCorner 6
skinparam arrowColor #333333

skinparam class {
  BackgroundColor #FDFEFE
  BorderColor #5D6D7E
  HeaderBackgroundColor #EAEDED
  FontSize 11
  AttributeFontSize 10
}

title AcousticGuard AI: Logical Database Schema (3NF Normalized)

class "T1: USERS" as T1 {
  + PK: user_id : UUID
  --
  username : VARCHAR(50) [UNIQUE, NOT NULL]
  email : VARCHAR(100) [UNIQUE, NOT NULL]
  role : VARCHAR(20) [DEFAULT 'client']
  created_at : TIMESTAMPTZ [NOT NULL]
}

class "T2: USER_PREFERENCES" as T2 {
  + PK: pref_id : UUID
  --
  * FK: user_id : UUID [REFERENCES USERS]
  visual_mode : VARCHAR(20) [CHECK in ('STROBE','BANNER')]
  vibration_enabled : BOOLEAN [DEFAULT TRUE]
  min_confidence : NUMERIC(3,2) [CHECK >= 0.50]
  cooldown_sec : NUMERIC(3,1) [DEFAULT 3.0]
}

class "T3: SOUND_CLASSES" as T3 {
  + PK: class_id : SMALLINT
  --
  class_name : VARCHAR(60) [NOT NULL, UNIQUE]
  is_danger_sound : BOOLEAN [NOT NULL]
  esc50_category : VARCHAR(50) [NOT NULL]
  risk_priority : VARCHAR(15) [CHECK in ('HIGH','MED','LOW')]
}

class "T4: DETECTION_EVENTS" as T4 {
  + PK: event_id : UUID
  --
  * FK: user_id : UUID [REFERENCES USERS]
  * FK: class_id : SMALLINT [REFERENCES SOUND_CLASSES]
  confidence : NUMERIC(4,3) [CHECK between 0 and 1]
  detected_at : TIMESTAMPTZ [NOT NULL]
  is_verified : BOOLEAN [DEFAULT FALSE]
}

class "T5: ALERT_DISPATCHES" as T5 {
  + PK: alert_id : UUID
  --
  * FK: event_id : UUID [REFERENCES DETECTION_EVENTS]
  channel : VARCHAR(20) [CHECK in ('VISUAL','HAPTIC','BOTH')]
  delivery_latency_ms : INTEGER [CHECK >= 0]
  acknowledged : BOOLEAN [DEFAULT FALSE]
}

T1 "1" -- "1" T2 : Has Configuration >
T1 "1" -- "0..*" T4 : Generates History >
T3 "1" -- "0..*" T4 : Categorizes >
T4 "1" -- "1..*" T5 : Triggers >

note bottom of T1
  Normalized to 3NF:
  - Atomic attributes (1NF)
  - No partial key dependencies (2NF)
  - No transitive dependencies (3NF)
  - Strict Foreign Key integrity
end note
@enduml
"""

# 11. PHYSICAL DATABASE DESIGN
diagrams['diagram_db_physical'] = """@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam roundCorner 6
skinparam arrowColor #333333

skinparam class {
  BackgroundColor #FAFAFA
  BorderColor #37474F
  HeaderBackgroundColor #CFD8DC
  FontSize 11
  AttributeFontSize 10
}

title AcousticGuard AI: Physical Database Design (PostgreSQL / Edge SQLite)

class "users (Table)" as P1 {
  + user_id : uuid PRIMARY KEY DEFAULT gen_random_uuid()
  username : varchar(50) NOT NULL UNIQUE
  email : varchar(100) NOT NULL UNIQUE
  role : varchar(20) DEFAULT 'user'
  created_at : timestamptz DEFAULT CURRENT_TIMESTAMP
  --
  INDEX: btree (email)
}

class "user_preferences (Table)" as P2 {
  + pref_id : uuid PRIMARY KEY DEFAULT gen_random_uuid()
  user_id : uuid NOT NULL REFERENCES users(user_id) ON DELETE CASCADE
  visual_theme : varchar(30) DEFAULT 'high_contrast_red'
  vibration_enabled : boolean DEFAULT true
  confidence_threshold : real DEFAULT 0.70
  cooldown_sec : smallint DEFAULT 3
  --
  INDEX: btree (user_id)
}

class "sound_classes (Lookup Table)" as P3 {
  + class_id : smallint PRIMARY KEY
  class_name : varchar(60) NOT NULL
  is_danger : boolean NOT NULL DEFAULT false
  esc50_category : varchar(50) NOT NULL
  risk_level : varchar(20) NOT NULL
  --
  INDEX: hash (class_name)
  INDEX: btree (is_danger)
}

class "detection_events (Partitioned by Month)" as P4 {
  + event_id : uuid DEFAULT gen_random_uuid()
  user_id : uuid NOT NULL REFERENCES users(user_id)
  class_id : smallint NOT NULL REFERENCES sound_classes(class_id)
  confidence : real NOT NULL
  detected_at : timestamptz NOT NULL
  spectrogram_path : varchar(255)
  --
  PRIMARY KEY (event_id, detected_at)
  INDEX: btree (user_id, detected_at DESC)
  PARTITION BY RANGE (detected_at)
  TTL: Auto-purge after 30 days
}

class "alert_logs (Table)" as P5 {
  + alert_id : uuid PRIMARY KEY DEFAULT gen_random_uuid()
  event_id : uuid NOT NULL
  event_time : timestamptz NOT NULL
  alert_channel : varchar(30) NOT NULL
  latency_ms : integer NOT NULL
  acknowledged : boolean DEFAULT false
  --
  INDEX: btree (event_id)
  FOREIGN KEY (event_id, event_time) REFERENCES detection_events(event_id, detected_at)
}

P1 ||--|| P2
P1 ||--o{ P4
P3 ||--o{ P4
P4 ||--o{ P5

note right of P4
  Optimized Storage Engine:
  - Range Partitioning by month
  - In-Memory Circular Buffer on Edge
  - Sub-10ms lookup query latency
  - Raw audio stream kept strictly in RAM
end note
@enduml
"""

print(f"Total diagrams to generate: {len(diagrams)}")
for name, code in diagrams.items():
    print(f"Generating {name}...")
    try:
        raw_png = server.processes(code)
        out_path = f"{name}.png"
        with open(out_path, "wb") as f:
            f.write(raw_png)
        print(f"Successfully generated {out_path} ({len(raw_png)} bytes)")
    except Exception as e:
        print(f"Failed to generate {name}: {e}")
    time.sleep(0.5)

print("Diagram generation completed.")
