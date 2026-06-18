Sentixcare Emotion AI System Upgrade Plan (Target: 92–95% Accuracy)

Master roadmap for upgrading the Sentixcare Emotion Recognition System to achieve state-of-the-art performance (92–95% accuracy) while maintaining real-time usability.

This document outlines improvements across data, model architecture, preprocessing, inference pipeline, and system design.

🧠 Target Architecture (92–95%)
User Input
   │
   ▼
RetinaFace Face Detection
   │
   ▼
Face Alignment (landmarks)
   │
   ▼
Face Preprocessing
   │
   ▼
EfficientNet-B4 + CBAM Attention
   │
   ▼
Emotion Classification (8 classes)
   │
   ▼
Confidence Calibration
   │
   ▼
Temporal Emotion Smoothing
   │
   ▼
Multimodal Fusion (Face + Text + Voice)
   │
   ▼
Final Emotion Prediction
1️⃣ Dataset Improvements (Highest Impact)
Replace Single Dataset Training

Current dataset:

FER2013

Upgrade to multi-dataset training:

FER2013
+
RAF-DB
+
CK+
+
AffectNet
Recommended Training Set
RAF-DB + FER2013

Benefits:

RAF-DB provides cleaner labels

FER2013 provides dataset scale

improves model generalization

Expected accuracy gain:

+10–15%
Dataset Cleaning

Remove poor training samples:

mislabelled images
non-face images
extreme occlusions
low-resolution images

Dataset cleaning alone can increase accuracy:

+3–7%
Class Balancing

Emotion datasets are heavily imbalanced.

Example:

happy → many samples
disgust → few samples

Solutions:

Weighted CrossEntropy Loss
Focal Loss
Oversampling minority classes

Example:

loss = nn.CrossEntropyLoss(weight=class_weights)
2️⃣ Face Detection Upgrade

Current system:

Haar Cascade
YOLOv7 fallback

Replace with modern detector:

RetinaFace

Advantages:

detects rotated faces

robust to lighting

provides facial landmarks

high detection accuracy

Example:

from retinaface import RetinaFace

faces = RetinaFace.detect_faces(image)

Expected improvement:

+10–20%
3️⃣ Face Alignment

Emotion models perform best with aligned faces.

Use facial landmarks to normalize face orientation.

Key landmarks:

left eye
right eye
nose
mouth

Libraries:

RetinaFace landmarks
MediaPipe FaceMesh
dlib

Example pipeline:

detect face
detect landmarks
rotate image
align eyes horizontally
crop face

Expected improvement:

+5–10%
4️⃣ Face Preprocessing

Normalize face images before model inference.

Recommended preprocessing:

face cropping
resize to 224x224
contrast normalization
histogram equalization
noise reduction

Example:

face = cv2.equalizeHist(face)
face = cv2.resize(face, (224,224))

Benefits:

better performance in low light
more consistent model inputs
5️⃣ Emotion Model Upgrade

Current models:

RepVGG
FER2013 CNN

Upgrade to modern architectures.

Recommended backbone:

EfficientNet-B4

Alternative options:

ResNet50
ConvNeXt
MobileNetV3

EfficientNet provides the best balance between:

accuracy
speed
memory usage

Example:

model = torchvision.models.efficientnet_b4(pretrained=True)
model.classifier[1] = nn.Linear(1792, 8)
6️⃣ Attention Mechanisms

Add attention layers to improve emotion feature extraction.

Recommended modules:

CBAM (Convolutional Block Attention Module)
SE Blocks (Squeeze and Excitation)
Spatial Attention

Architecture example:

EfficientNet Backbone
↓
CBAM Attention Layer
↓
Classifier

Expected improvement:

+3–5%
7️⃣ Training Improvements
Transfer Learning

Use pretrained models:

ImageNet pretrained weights

Fine-tune final layers for emotion recognition.

Benefits:

faster training
better generalization
higher accuracy
Data Augmentation

Apply augmentation during training.

Recommended augmentations:

horizontal flip
random rotation
brightness variation
gaussian blur
random crop
noise injection

Example:

transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.3),
    transforms.GaussianBlur(3),
    transforms.ToTensor()
])

Expected improvement:

+5–8%
8️⃣ Test-Time Augmentation (TTA)

Improve prediction accuracy during inference.

Process multiple augmented versions of the same image:

original image
horizontal flip
slight rotation
brightness variation

Average predictions:

final_prediction = mean(all_predictions)

Expected improvement:

+3–5%
9️⃣ Temporal Emotion Smoothing

Webcam predictions fluctuate frame-to-frame.

Solution:

Store predictions across multiple frames.

Example:

last 15 frames

Final prediction:

majority voting
or
average probability

Example:

emotion_buffer.append(prediction)

if len(emotion_buffer) > 15:
    emotion_buffer.pop(0)

final_emotion = max(set(emotion_buffer), key=emotion_buffer.count)

Benefits:

stable predictions
reduced flickering
🔟 Confidence Calibration

Filter unreliable predictions.

Example:

if confidence < 0.45:
    emotion = "neutral"

Benefits:

reduces false positives
improves real-world reliability
11️⃣ Ensemble Models

Combine multiple models.

Example:

EfficientNet
+
ResNet

Final prediction:

average probabilities

Benefits:

more robust predictions
higher accuracy
12️⃣ Multimodal Emotion Detection

Facial emotion alone is imperfect.

Combine multiple signals:

facial emotion
text sentiment
voice emotion

Example fusion:

Face emotion weight → 0.6
Text sentiment weight → 0.25
Voice emotion weight → 0.15

Benefits:

better real-world accuracy
more robust predictions
13️⃣ Emotion Memory System

Track emotional trends across time.

Example database:

timestamp | emotion | confidence

Benefits:

emotion stability analysis
trend detection
personalized recommendations
📊 Expected Accuracy Improvements
Upgrade	Accuracy Gain
Dataset upgrade	+10–15%
RetinaFace detection	+10–20%
Face alignment	+5–10%
EfficientNet model	+8–12%
Attention layers	+3–5%
Data augmentation	+5–8%
Temporal smoothing	+5–10%
TTA inference	+3–5%
Final Expected Accuracy
92–95%
🚀 Implementation Priority

Recommended implementation order:

Phase 1 (Highest Priority)
RetinaFace face detection
Face alignment
EfficientNet model
Phase 2
Dataset upgrade (RAF-DB)
Data augmentation
Class balancing
Phase 3
CBAM attention module
Temporal smoothing
Confidence calibration
Phase 4
Test-time augmentation
Model ensembles
Multimodal emotion detection
Emotion memory tracking
🎯 Final System
RetinaFace
↓
Face Alignment
↓
EfficientNet + CBAM
↓
Confidence Filtering
↓
Temporal Smoothing
↓
Multimodal Emotion Fusion
↓
Recommendation Engine

Target:

92–95% emotion recognition accuracy