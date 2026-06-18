SentixCare – Next Generation Emotion AI Architecture

This document describes the advanced AI architecture used in the SentixCare Emotion Recognition System.

The architecture is designed to achieve:

92–95% emotion recognition accuracy

Real-time inference

Multimodal emotion understanding

Stable emotion prediction

Personalized recommendations

🚀 System Overview

The SentixCare system processes emotional signals using multiple AI layers.

User Input
   │
   ▼
Face Detection
   │
   ▼
Face Alignment
   │
   ▼
Face Preprocessing
   │
   ▼
Emotion Recognition Model
   │
   ▼
Confidence Calibration
   │
   ▼
Temporal Emotion Smoothing
   │
   ▼
Emotion Intelligence Layer
   │
   ▼
Recommendation Engine
   │
   ▼
User Experience Layer
1️⃣ Input Layer

The system accepts multiple user inputs.

Supported inputs
Webcam Video
Image Upload
Text Input
Voice Input (future)

Primary emotional signal:

Facial expressions

Future signals:

Voice tone
User text sentiment
Emotion history
2️⃣ Face Detection Layer

Detects faces in the camera frame.

Current implementation
Haar Cascade
YOLOv7 fallback
Upgraded system
RetinaFace

Advantages:

higher detection accuracy

detects rotated faces

robust under poor lighting

provides facial landmarks

Example detection pipeline:

Camera Frame
   ↓
RetinaFace
   ↓
Detected Face + Landmarks
3️⃣ Face Alignment Layer

Faces must be aligned before emotion recognition.

Misaligned faces reduce model accuracy.

Alignment uses facial landmarks:

Left eye
Right eye
Nose
Mouth

Steps:

Detect landmarks
Rotate face
Align eyes horizontally
Crop face

Output:

Aligned facial image

Benefits:

Improves emotion model accuracy
Reduces noise in predictions
4️⃣ Face Preprocessing Layer

Standardizes face images before inference.

Processing steps
Face cropping
Resize to 224x224
Contrast normalization
Histogram equalization
Noise reduction

Example:

Raw Face
   ↓
Lighting normalization
   ↓
Resized face
   ↓
Model input tensor

Benefits:

Better performance in different lighting conditions
Improved model stability
5️⃣ Emotion Recognition Model

Core AI model that predicts emotions.

Current models
FER2013 CNN
RepVGG
Upgraded model
EfficientNet-B4

EfficientNet provides:

Higher accuracy
Better feature extraction
Efficient inference

Emotion classes:

Happy
Sad
Angry
Fear
Surprise
Disgust
Neutral
Contempt

Model output example:

Happy → 0.82
Neutral → 0.10
Surprise → 0.05
Others → <0.03
6️⃣ Attention Mechanism

Emotion features are concentrated in:

Eyes
Mouth
Eyebrows

Attention modules help the model focus on these areas.

Used modules
CBAM (Convolutional Block Attention Module)

Architecture:

EfficientNet Backbone
      ↓
CBAM Attention
      ↓
Emotion Classifier

Benefits:

Better facial feature understanding
Improved emotion detection accuracy
7️⃣ Confidence Calibration

Low-confidence predictions are filtered.

Example prediction:

Happy → 35%
Sad → 33%
Neutral → 30%

System response:

Emotion = Neutral

Example threshold:

Confidence threshold = 0.45

Benefits:

Reduces incorrect predictions
Improves reliability
8️⃣ Temporal Emotion Smoothing

Emotion predictions fluctuate across frames.

Example:

Frame 1 → Happy
Frame 2 → Neutral
Frame 3 → Sad
Frame 4 → Happy

Solution:

Emotion buffer (last 15 frames)

Final emotion:

Majority voting

Example:

[Happy, Happy, Happy, Neutral, Happy]
→ Final = Happy

Benefits:

Stable emotion prediction
Better real-time experience
9️⃣ Emotion Intelligence Layer

Transforms raw emotion predictions into insights.

Components
Emotion memory
Emotion stability analysis
Mood tracking
Emotion trends

Example:

User emotion over 5 minutes

Happy → 30%
Neutral → 50%
Sad → 20%

System understands the dominant emotional state.

🔟 Multimodal Emotion Fusion

Facial emotion alone can be inaccurate.

Future architecture integrates:

Face Emotion
Text Sentiment
Voice Emotion

Fusion example:

Face → Sad
Text → Frustrated
Voice → Angry

Final emotion → Distress

Weights example:

Face → 0.6
Text → 0.25
Voice → 0.15

Benefits:

Higher real-world accuracy
More reliable emotion understanding
11️⃣ Recommendation Engine

Based on detected emotion, the system generates:

Music recommendations
Mental health resources
Wellness tips
AI chatbot support

Example:

Emotion → Sad

System actions:

Play calming music
Show mental health resources
Activate supportive chatbot
12️⃣ User Experience Layer

The final layer presents results to the user.

Features
Emotion visualization
Emotion confidence chart
Music recommendations
Mental health support resources
AI wellness chatbot

Built using:

Streamlit UI

Future upgrade:

React Native mobile app
📊 Target System Performance
Metric	Target
Emotion Accuracy	92–95%
Inference Speed	Real-time
Face Detection Accuracy	>98%
Emotion Stability	High
🧩 Future Architecture Extensions

Planned improvements:

Vision Transformer emotion models
Voice emotion recognition
Emotion trend prediction
Personalized AI therapist
Mobile app integration
🏆 Final AI Pipeline
User Input
   ↓
RetinaFace Face Detection
   ↓
Face Alignment
   ↓
Face Preprocessing
   ↓
EfficientNet + CBAM
   ↓
Confidence Filtering
   ↓
Temporal Smoothing
   ↓
Emotion Intelligence
   ↓
Recommendation Engine
   ↓
User Interface