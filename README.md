# 🧠 Sentixcare — Mood-Driven Personalized Recommendation   System

##Live : https://sentixcare.gokul.software/

> **Your Intelligent Mental Health & Wellness Companion**  
> *Emotion Detection • Music Therapy • Reading Suggestions • Wellness Coaching • AI Chatbot Support* 

---

## 📖 Project Description

**Sentixcare** is an AI-powered mental health and wellness application that detects a user's emotional state in real time and delivers personalized recommendations to improve well-being. Built with Python and Streamlit, it bridges the gap between technology and emotional support by combining computer vision, natural language processing, and curated wellness content.

**What problem does it solve?**  
Mental health awareness is growing, but personalized, accessible support remains limited. Sentixcare provides an intelligent, non-clinical first layer of emotional support — detecting how someone feels and responding with targeted music, reading materials, breathing exercises, journaling prompts, and AI-driven conversation.

**Who is it for?**  
- Individuals seeking daily emotional check-ins
- Students and professionals managing stress and burnout
- Researchers exploring affective computing and emotion AI
- Mental health advocates building support tools

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎭 **Facial Emotion Detection** | Detects emotions from photos and webcam using a dual-pipeline: OpenCV Haar Cascade (primary) + YOLOv7-tiny (fallback) for face detection, followed by RepVGG-A0 and FER2013-trained deep models for emotion classification |
| 🎬 **Video Emotion Analysis** | Processes uploaded videos frame-by-frame, aggregating emotion scores over time and generating a comprehensive analysis dashboard |
| ✍️ **Text-Based Mood Input** | Keyword-based NLP engine that infers emotion from free-text mood descriptions, feeding the same recommendation pipeline |
| 🔀 **Multimodal Emotion Fusion** | Combines emotion inputs from multiple sources (photo, webcam, text) and fuses them using a confidence-weighted scoring algorithm to determine a dominant emotion |
| 🎵 **Music Recommendation Engine** | Curated YouTube-linked playlists mapped to each of the 8 recognized emotions, with mood-match scoring based on tempo, energy, valence, and genre |
| 📚 **Reading Recommendation Engine** | Book and article recommendations tailored to the user's detected emotion, with reading insights and mood-aligned content categories |
| 🧘 **Wellness & Breathing Exercises** | Guided breathing exercises (e.g., box breathing, 4-7-8, diaphragmatic) with animated prompts, scientifically referenced and matched to emotional state |
| 🎨 **Interactive Coloring Game** | A calming, interactive coloring activity for emotional regulation, particularly for high-stress states |
| 💬 **AI Wellness Chatbot** | Dual-mode chatbot: rule-based empathetic responses for all 8 emotions, with optional Google Gemini API integration for generative AI conversation |
| 📝 **Mood Journal** | Structured journaling with emotion-specific reflection prompts, mood tag selection, intensity rating, and exportable history (JSON / Excel) |
| 🆘 **Mental Health Resources** | Curated crisis helplines, mental health links, and quick-access support resources tailored to detected emotion and confidence level |
| 📊 **Emotion History Tracking** | Session-level emotional journey log displayed as a timestamped dataframe with source tracking |
| 🛡️ **ERS + AEISA Engine** | Emotion Regulation Score (ERS) computes a weighted rolling emotional state score; the Adaptive Emotional Intervention Selection Algorithm (AEISA) selects the optimal intervention type |

---

## 🏗️ System Architecture

```
User Input
  ├── 📸 Photo Upload
  ├── 📹 Webcam Capture (burst of 30 frames)
  ├── 🎬 Video Upload
  └── ✍️ Text Description
          │
          ▼
  ┌─────────────────────────────┐
  │   Emotion Detection Engine  │
  │  (src/core/emotion_engine)  │
  │                             │
  │  1. Face Detection:         │
  │     OpenCV Haar Cascade     │
  │     → YOLOv7-tiny (fallback)│
  │                             │
  │  2. Emotion Classification: │
  │     RepVGG-A0 (8 classes)   │
  │     FER2013 CNN detector    │
  │                             │
  │  3. Text NLP (keyword-based)│
  └────────────┬────────────────┘
               │
               ▼
  ┌─────────────────────────────┐
  │   ERS + AEISA Engine        │
  │  (src/ers/)                 │
  │                             │
  │  • Computes Emotion         │
  │    Regulation Score (ERS)   │
  │  • Selects best intervention│
  │    (breathing / content)    │
  └────────────┬────────────────┘
               │
               ▼
  ┌─────────────────────────────┐
  │   Recommendation Panel      │
  │  (src/ui/recommendation_    │
  │   panel.py)                 │
  │                             │
  │  🎵 Music  📚 Reading      │
  │  🧘 Wellness 🎨 Coloring   │
  │  💬 Chatbot 📝 Journal     │
  |  🆘 Support Resources      ||
  └─────────────────────────────┘
               │
               ▼
        Streamlit UI
       (Wide Layout)
```

### Key Subsystems

| Layer | Files | Role |
|---|---|---|
| **Entry Point** | `src/app.py` | Page config, session init, model loading, mode routing |
| **Session State** | `src/state/session_state.py` | Centralized Streamlit session state defaults |
| **Model Manager** | `src/core/model_manager.py` | `@st.cache_resource` — loads all ML models once per session |
| **Emotion Engine** | `src/core/emotion_engine.py` | Detection pipeline, fusion, text NLP |
| **ERS Engine** | `src/ers/ers_engine.py` | Rolling emotion regulation scoring |
| **AEISA** | `src/ers/aeisa.py` | Adaptive intervention selection |
| **Features** | `src/features/` | Music recommender, reading recommender, wellness chatbot, wellness features, mental health resources |
| **UI Modules** | `src/ui/` | All Streamlit page components (single mode, multimodal, recommendation panel, music player, journal, etc.) |

---

## 📁 Project Folder Structure

```
ers-system/
│
├── src/                          # Main application source
│   ├── app.py                    # Application entry point
│   ├── core/                     # Core ML & detection logic
│   │   ├── emotion_detector.py   # RepVGG inference wrapper
│   │   ├── emotion_engine.py     # Detection pipeline & fusion
│   │   ├── fer_detector.py       # FER2013 CNN detector
│   │   ├── facial_emotion_detector.py  # Facial landmark detector
│   │   ├── deep_emotion_detector.py    # Deep model variant
│   │   ├── model_manager.py      # Cached model loader
│   │   ├── repvgg.py             # RepVGG architecture definition
│   │   ├── se_block.py           # Squeeze-and-Excitation block
│   │   ├── train_fer2013.py      # FER2013 training script
│   │   └── utils/                # YOLO utilities (NMS, coord scaling, etc.)
│   │
│   ├── ers/                      # Emotion Regulation System
│   │   ├── ers_engine.py         # ERS scoring (rolling weighted average)
│   │   └── aeisa.py              # Adaptive intervention selection
│   │
│   ├── features/                 # Recommendation & wellness features
│   │   ├── music_recommender.py  # Emotion-to-music mapping + YouTube playlists
│   │   ├── reading_recommender.py# Emotion-to-book/article recommendations
│   │   ├── wellness_features.py  # Wellness activity recommendations
│   │   ├── wellness_chatbot.py   # Rule-based + Gemini AI chatbot
│   │   └── mental_health_resources.py  # Curated crisis & support links
│   │
│   ├── ui/                       # Streamlit UI components
│   │   ├── single_mode_ui.py     # Single-input mode (photo/text/webcam/video)
│   │   ├── multimodal_ui.py      # Multi-source fusion mode UI
│   │   ├── recommendation_panel.py   # Unified tabbed recommendations panel
│   │   ├── music_player.py       # Enhanced music player UI
│   │   ├── breathing_exercises.py    # Animated breathing exercise UI
│   │   ├── coloring_display.py   # Interactive coloring game
│   │   ├── mood_journaling.py    # Mood journal form + history
│   │   ├── mental_health_display.py  # Resources, chatbot display
│   │   ├── reading_display.py    # Reading recommendations UI
│   │   ├── video_analysis_dashboard.py  # Video analysis results dashboard
│   │   ├── enhanced_ui.py        # Global styling, header, footer
│   │   ├── compact_sidebar.py    # Sidebar layout
│   │   └── resources_section.py  # Footer resource links
│   │
│   ├── state/
│   │   └── session_state.py      # Centralized session state management
│   │
│   ├── utils/
│   │   └── constants.py          # Shared constants (EMOTION_EMOJIS, EMOTION_COLORS, etc.)
│   │
│   ├── config/                   # Application configuration files
│   ├── content/                  # Content library (emotion-to-content mapping)
│   └── data/                     # Data assets
│
├── models/
│   ├── weights/
│   │   ├── repvgg.pth            # RepVGG-A0 emotion model weights (8 classes)
│   │   ├── yolov7-tiny-face.pt   # YOLOv7-tiny face detection weights
│   │   └── (fer2013 weights)     # FER2013 CNN model weights
│   └── hub/                      # Model hub cache
│
├── docs/                         # Documentation
│   ├── SCIENTIFIC_REFERENCES.md  # Evidence base for wellness exercises
│   ├── WELLNESS_README.md        # Wellness feature documentation
│   ├── COLORING_GAME_README.md   # Coloring game documentation
│   └── LICENSE                   # Project license
│
├── assests/                      # Static assets (images, icons)
├── fer2013/                      # FER2013 dataset directory
├── emotion/                      # Emotion dataset files
├── .streamlit/                   # Streamlit configuration
├── Dockerfile                    # Container deployment config
├── render.yaml                   # Render.com deployment config
├── runtime.txt                   # Python runtime specification
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core programming language |
| **Streamlit** | Interactive web UI framework |
| **PyTorch** | Deep learning inference (RepVGG, FER2013 CNN) |
| **TorchVision** | Image transforms and preprocessing |
| **OpenCV (`opencv-python-headless`)** | Face detection (Haar Cascade), image processing, webcam capture |
| **Pillow** | Image loading and manipulation |
| **NumPy** | Numerical array operations |
| **Pandas** | Emotion history dataframes, tabular exports |
| **Transformers / HuggingFace Hub** | NLP model support |
| **Google Generative AI (`google-generativeai`)** | Gemini API integration for AI chatbot |
| **Altair / Matplotlib / Seaborn** | Data visualization |
| **Scikit-learn** | ML utility functions |
| **SciPy** | Scientific computing utilities |
| **python-dotenv** | Environment variable management |
| **TensorBoard** | Training visualization |
| **openpyxl** | Excel export for mood journal |
| **YouTube Integration** | Curated YouTube video IDs for music playback |

---

## 🤖 AI Models Used

### 1. RepVGG-A0 — Emotion Classification
- **Architecture:** RepVGG-A0 (re-parameterizable VGG-style ConvNet)
- **Input:** 224×224 RGB face crop
- **Output:** 8-class emotion probabilities
- **Classes:** `anger`, `contempt`, `disgust`, `fear`, `happy`, `neutral`, `sad`, `surprise`
- **Mode:** Deploy mode (reparameterized single-path convolutions for fast inference)
- **Weights:** `models/weights/repvgg.pth`

### 2. YOLOv7-tiny — Face Detection (Fallback)
- **Architecture:** YOLOv7-tiny object detector
- **Role:** Detects face bounding boxes when Haar Cascade fails
- **Weights:** `models/weights/yolov7-tiny-face.pt`
- **Pipeline:** Image → resize 640×640 → YOLO inference → NMS → crop → emotion model

### 3. OpenCV Haar Cascade — Face Detection (Primary)
- **Type:** Classical computer vision (Viola-Jones)
- **Role:** Fast primary face detector; histogram equalization applied pre-detection
- **Model:** `haarcascade_frontalface_default.xml` (bundled with OpenCV)

### 4. FER2013 CNN — Emotion Detector (Secondary Path)
- **Type:** Custom CNN trained on the FER2013 dataset
- **Training script:** `src/core/train_fer2013.py`
- **Role:** Secondary emotion classifier for face crops

### 5. Text NLP — Keyword-Based Emotion Detector
- **Type:** Rule-based keyword scoring (no external model)
- **Role:** Classifies free text into one of the 8 emotion categories
- **Location:** `src/core/emotion_engine.py` → `detect_emotion_from_text_simple()`

### Detection Pipeline Flow

```
Image Input
    │
    ▼
OpenCV Haar Cascade
    ├── Faces found → crop → resize 224×224 → RepVGG-A0 → emotion
    └── No faces → YOLOv7-tiny → crop → resize 224×224 → FER detector → emotion
                                                                │
                                                                ▼
                                                    Confidence normalization
                                                    → Result dict {bbox, emotion, confidence}
```

---

## ⚙️ Installation Guide

### Prerequisites
- Python 3.9 or higher
- Git
- GPU (optional, but recommended for faster inference)
- A `GEMINI_API_KEY` (optional, for AI chatbot functionality)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/ers-system.git
cd ers-system
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Download Model Weights

Place the following files in the `models/weights/` directory:

| File | Description |
|---|---|
| `repvgg.pth` | RepVGG-A0 emotion classifier weights (8 emotion classes) |
| `yolov7-tiny-face.pt` | YOLOv7-tiny face detection weights |

> **Note:** The FER2013 model can be trained locally using `src/core/train_fer2013.py` if weights are not available.

### Step 5 — Configure Environment Variables (Optional)

Create a `.env` file in the project root for the Gemini chatbot:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 6 — Run the Application

```bash
streamlit run src/app.py
```

The application will open at `http://localhost:8501` in your browser.

### Docker Deployment (Alternative)

```bash
docker build -t sentixcare .
docker run -p 8501:8501 sentixcare
```

---

## 🚀 How to Use the Application

### Step 1 — Load AI Models
On first launch, click the **"🚀 Load AI Models"** button in the sidebar. This loads the RepVGG, YOLOv7, and FER2013 models into memory (cached for the session).

### Step 2 — Select Input Mode

| Mode | Description |
|---|---|
| **Single** | Analyze one input (photo, video, webcam, or text description) |
| **Multimodal** | Collect inputs from multiple sources, then fuse them for a combined analysis |

### Step 3 — Provide Your Input

- **📸 Photo:** Upload a JPG/PNG image containing a face
- **🎬 Video:** Upload a video file for frame-by-frame emotion analysis
- **📹 Webcam:** Capture 30 frames from your webcam for a burst analysis
- **✍️ Text:** Describe how you're feeling in your own words

### Step 4 — Get Recommendations

After emotion detection, the app displays a tabbed recommendation panel:

| Tab | Content |
|---|---|
| 🎵 **Music** | 5 YouTube-linked tracks matched to your emotion, with mood scores |
| 📚 **Reading** | Book and article suggestions with reading insights |
| 🧘 **Wellness** | Breathing exercises and mindfulness activities |
| 🎨 **Coloring Game** | Interactive calming coloring activity |
| 💬 **AI Chatbot** | Conversation with your wellness companion |
| 📝 **Mood Journal** | Guided journaling with reflection prompts |
| 🆘 **Support** | Crisis resources and mental health helplines |

### Step 5 — Track Your Emotional Journey

Your emotional history is stored for the session. Expand **"📈 Your Emotional Journey History"** at the bottom of the page to see a timestamped log of all your detected emotions.

---

## 💡 Example Workflow

```
1. User opens the application at localhost:8501

2. Clicks "🚀 Load AI Models" → RepVGG, YOLOv7, FER2013 load

3. Selects "Single" mode → chooses "📸 Photo"

4. Uploads a selfie → clicks "Analyze Photo"

5. System pipeline:
   OpenCV Haar detects face → crops region → RepVGG classifies → "sad" (78.3%)

6. ERS Engine:
   Computes rolling emotion score → ERS = -1.2 (slightly negative)

7. AEISA:
   ERS < 0 + emotion = "sad" → recommends music & reading content

8. Recommendation Panel displays:
   • 🎵 Music: Lewis Capaldi, Taylor Swift, Simon & Garfunkel playlists
   • 📚 Reading: Introspective and healing book recommendations
   • 🧘 Wellness: Breathing exercises for relaxation
   • 💬 Chatbot: "I can see you're feeling sad. It's okay to feel this way..."

9. User logs a journal entry reflecting on their feelings

10. Emotion added to session history log
```

---

## 🔮 Future Improvements

- **🎤 Voice Emotion Detection** — Analyze vocal tone and speech patterns to detect emotion from audio input
- **🧠 Emotion Memory & Trends** — Persistent cross-session emotion tracking with mood trend charts across days/weeks
- **📱 Mobile App Integration** — React Native or Flutter app wrapping the backend API
- **🤗 Advanced NLP Models** — Replace keyword-based text detection with transformer models (e.g., `roberta-base-go_emotions`) for nuanced text emotion classification
- **🔗 Spotify API Integration** — Real-time music streaming via Spotify API instead of YouTube links
- **🏥 Clinician Dashboard** — Anonymized aggregate emotion data view for mental health professionals or researchers
- **🌐 Multi-Language Support** — Internationalization of the UI and text emotion detection
- **🎯 Personalized Recommendation Learning** — Track user feedback on recommendations to improve future suggestions over time
- **🔐 User Authentication** — Persistent profiles with secure login for long-term mood tracking

---

## 🤝 Contributing Guidelines

Contributions are welcome! To contribute:

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow code structure** — UI logic in `src/ui/`, ML logic in `src/core/`, recommendation logic in `src/features/`

3. **Keep UI and logic separated** — do not embed ML calls directly in Streamlit pages

4. **Write clear docstrings** for all functions

5. **Test your changes** by running the Streamlit app and verifying the affected feature

6. **Commit with clear messages:**
   ```bash
   git commit -m "feat: add voice emotion detection module"
   ```

7. **Open a Pull Request** with a description of what was changed and why

### Code Style
- Follow PEP 8 formatting
- Use type hints where applicable
- Keep modules focused — each file should have a single clear responsibility

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.  
See [`docs/LICENSE`](docs/LICENSE) for full license text.

---

## 👤 Author

**Gokul** — Final Year Project, 2026  
🔗 GitHub: [Gokul7904231/ERS-System](https://github.com/Gokul7904231/Sentixcare)

---

## 📚 Scientific References

All breathing exercises and wellness interventions in this application are evidence-based and clinically referenced.  
See [`docs/SCIENTIFIC_REFERENCES.md`](docs/SCIENTIFIC_REFERENCES.md) for detailed citations.

---

<div align="center">

Made with ❤️ for mental health awareness

*"Technology in service of human well-being"*

</div>
