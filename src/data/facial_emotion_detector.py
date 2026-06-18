"""
Facial Emotion Detection using Geometric Features
Uses facial landmarks to analyze facial expressions for emotion detection
"""

import cv2
import numpy as np
from collections import Counter


class FacialEmotionDetector:
    """
    Emotion detection using facial geometry and landmark analysis.
    This approach analyzes facial landmark positions to determine emotions
    without requiring a trained neural network.
    """
    
    def __init__(self):
        # Define facial landmark indices for key facial features
        # Based on dlib's 68-point face landmark detector
        self.JAWLINE = list(range(0, 17))
        self.EYEBROWS = list(range(17, 27))
        self.NOSE = list(range(27, 36))
        self.EYES = list(range(36, 48))
        self.MOUTH = list(range(48, 68))
        
        # Eye landmark groups
        self.LEFT_EYE = list(range(36, 42))
        self.RIGHT_EYE = list(range(42, 48))
        
        # Mouth landmark groups
        self.MOUTH_OUTER = list(range(48, 60))
        self.MOUTH_INNER = list(range(60, 68))
        
        # Eyebrow groups
        self.LEFT_EYEBROW = list(range(17, 22))
        self.RIGHT_EYEBROW = list(range(22, 27))
        
    def detect_facial_landmarks(self, face_image, face_cascade):
        """
        Detect facial landmarks using OpenCV's built-in methods.
        Returns landmark points or None if detection fails.
        """
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        
        # Try to detect faces in the image
        faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(50, 50))
        
        if len(faces) == 0:
            return None
            
        # Use the first detected face
        x, y, w, h = faces[0]
        
        # Since we already have a face crop, let's use simpler geometric analysis
        # instead of full landmark detection
        
        return {
            'face_region': (x, y, w, h),
            'image': face_image,
            'gray': gray
        }
    
    def analyze_eye_aspect_ratio(self, eye_points, landmarks):
        """
        Calculate eye aspect ratio to detect if eyes are open or closed.
        EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
        """
        if landmarks is None:
            return 0.3  # Default value
            
        try:
            # Simplified EAR calculation using available points
            if len(eye_points) >= 6:
                # Get eye region
                eye_region = self.get_landmark_region(landmarks, eye_points)
                if eye_region is None:
                    return 0.3
                    
                h, w = eye_region.shape[:2]
                
                # Calculate darkness of upper vs lower eyelid area
                upper_half = eye_region[:h//2, :]
                lower_half = eye_region[h//2:, :]
                
                upper_mean = np.mean(upper_half)
                lower_mean = np.mean(lower_half)
                
                # If upper eyelid is significantly darker/lower, eyes might be droopy (tired/sad)
                # or if there's more white space, eyes might be open (surprise/happy)
                return abs(upper_mean - lower_mean) / 255.0
        except:
            pass
            
        return 0.3
    
    def get_landmark_region(self, landmarks, indices):
        """Extract region defined by landmark indices."""
        if landmarks is None or len(landmarks) == 0:
            return None
            
        points = landmarks[indices]
        
        if len(points) == 0:
            return None
            
        # Get bounding box
        x_min = max(0, int(np.min(points[:, 0])) - 5)
        x_max = int(np.max(points[:, 0])) + 5
        y_min = max(0, int(np.min(points[:, 1])) - 5)
        y_max = int(np.max(points[:, 1])) + 5
        
        h, w = landmarks.shape[:2]
        x_max = min(w, x_max)
        y_max = min(h, y_max)
        
        if x_max <= x_min or y_max <= y_min:
            return None
            
        return landmarks[y_min:y_max, x_min:x_max]
    
    def analyze_mouth(self, face_image):
        """
        Analyze mouth region to detect smile/frown.
        Uses contour analysis and symmetry.
        """
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # Define mouth region (lower third of face)
        mouth_y_start = int(h * 0.6)
        mouth_region = gray[mouth_y_start:, :]
        
        if mouth_region.size == 0:
            return {'smile_score': 0, 'openness': 0}
        
        # Apply threshold to find mouth contours
        _, thresh = cv2.threshold(mouth_region, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            return {'smile_score': 0, 'openness': 0}
        
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        # Calculate mouth bounding box
        x, y, cw, ch = cv2.boundingRect(largest_contour)
        
        # Calculate aspect ratio (wide = smile, tall = open mouth)
        aspect_ratio = cw / (ch + 1)
        
        # Calculate symmetry (more symmetric = more likely neutral/happy)
        # Split contour horizontally
        moments = cv2.moments(largest_contour)
        if moments['m00'] != 0:
            cx = int(moments['m10'] / moments['m00'])
            # Symmetry relative to center
            symmetry = 1 - abs(cx - cw/2) / (cw/2 + 1)
        else:
            symmetry = 0.5
        
        # Open mouth detection (yawning or surprise)
        mouth_openness = ch / (h * 0.4)  # Proportion of lower face
        
        return {
            'smile_score': aspect_ratio * symmetry,  # Higher = more smile-like
            'openness': mouth_openness,  # Higher = more open
            'width': cw,
            'height': ch
        }
    
    def analyze_eyebrows(self, face_image):
        """
        Analyze eyebrow position to detect emotions.
        - Raised eyebrows = surprise
        - Furrowed eyebrows = anger/fear
        - Neutral = happy/content
        """
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # Define eyebrow region (upper third of face)
        eyebrow_y_end = int(h * 0.35)
        eyebrow_region = gray[:eyebrow_y_end, :]
        
        if eyebrow_region.size == 0:
            return {'raise_score': 0, 'furrow_score': 0}
        
        # Edge detection for eyebrows
        edges = cv2.Canny(eyebrow_region, 50, 150)
        
        # Count edge pixels in upper vs lower half of eyebrow region
        upper_half = edges[:eyebrow_y_end//2, :]
        lower_half = edges[eyebrow_y_end//2:, :]
        
        upper_edges = np.sum(upper_half > 0)
        lower_edges = np.sum(lower_half > 0)
        
        # More edges in upper half = raised eyebrows (surprise)
        # More edges in lower half = furrowed (anger)
        total_edges = upper_edges + lower_edges + 1
        
        raise_score = upper_edges / total_edges
        furrow_score = lower_edges / total_edges
        
        return {
            'raise_score': raise_score,
            'furrow_score': furrow_score
        }
    
    def analyze_eyes(self, face_image):
        """
        Analyze eyes to detect emotions.
        - Wide open eyes = surprise/fear
        - Narrow/closed eyes = happy/content/tired
        """
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # Define eye regions
        left_eye_x_end = w // 2
        right_eye_x_start = w // 2
        
        left_eye_region = gray[:int(h*0.5), :left_eye_x_end]
        right_eye_region = gray[:int(h*0.5), right_eye_x_start:]
        
        results = {}
        
        for eye_name, eye_region in [('left', left_eye_region), ('right', right_eye_region)]:
            if eye_region.size == 0:
                results[eye_name] = {'openness': 0.5}
                continue
                
            # Calculate variance (high variance = more open eyes)
            variance = np.var(eye_region)
            
            # Normalize to 0-1 range (assuming typical variance 100-2000)
            openness = min(1.0, variance / 500)
            
            results[eye_name] = {
                'openness': openness,
                'mean_brightness': np.mean(eye_region)
            }
        
        # Average openness
        avg_openness = (results['left']['openness'] + results['right']['openness']) / 2
        
        return {
            'left': results['left'],
            'right': results['right'],
            'avg_openness': avg_openness
        }
    
    def detect_emotion(self, face_crops, face_cascade):
        """
        Main emotion detection function.
        
        Args:
            face_crops: List of face image arrays
            face_cascade: OpenCV face cascade classifier
            
        Returns:
            List of [emotion, confidence] pairs
        """
        results = []
        
        for face_image in face_crops:
            if face_image is None or face_image.size == 0:
                results.append(['neutral', 50.0])
                continue
            
            # Ensure image is valid
            if len(face_image.shape) == 2:
                face_image = cv2.cvtColor(face_image, cv2.COLOR_GRAY2BGR)
            
            if face_image.shape[2] == 4:  # RGBA
                face_image = cv2.cvtColor(face_image, cv2.COLOR_RGBA2BGR)
            
            # Resize to consistent size
            face_image = cv2.resize(face_image, (200, 200))
            
            # Analyze facial features
            mouth_analysis = self.analyze_mouth(face_image)
            eyebrow_analysis = self.analyze_eyebrows(face_image)
            eye_analysis = self.analyze_eyes(face_image)
            
            # Calculate emotion scores
            emotion_scores = {
                'happy': 0,
                'sad': 0,
                'anger': 0,
                'fear': 0,
                'surprise': 0,
                'neutral': 0,
                'disgust': 0,
                'contempt': 0
            }
            
            # Happy: Wide smile, slightly raised eyebrows, normal/open eyes
            if mouth_analysis['smile_score'] > 1.5:
                emotion_scores['happy'] += 3
            if eyebrow_analysis['raise_score'] > 0.45:
                emotion_scores['happy'] += 1
            if eye_analysis['avg_openness'] > 0.3:
                emotion_scores['happy'] += 1
            
            # Sad: Downward mouth corners (low smile score), lowered eyebrows
            if mouth_analysis['smile_score'] < 1.0:
                emotion_scores['sad'] += 2
            if eyebrow_analysis['raise_score'] < 0.4:
                emotion_scores['sad'] += 1
            
            # Anger: Furrowed eyebrows, tight lips (low smile, low openness)
            if eyebrow_analysis['furrow_score'] > 0.5:
                emotion_scores['anger'] += 3
            if mouth_analysis['smile_score'] < 1.2:
                emotion_scores['anger'] += 1
            
            # Fear: Wide open eyes, raised eyebrows, slightly open mouth
            if eye_analysis['avg_openness'] > 0.6:
                emotion_scores['fear'] += 2
            if eyebrow_analysis['raise_score'] > 0.55:
                emotion_scores['fear'] += 2
            if mouth_analysis['openness'] > 0.3:
                emotion_scores['fear'] += 1
            
            # Surprise: Very wide eyes, raised eyebrows, open mouth
            if eye_analysis['avg_openness'] > 0.7:
                emotion_scores['surprise'] += 3
            if eyebrow_analysis['raise_score'] > 0.6:
                emotion_scores['surprise'] += 2
            if mouth_analysis['openness'] > 0.4:
                emotion_scores['surprise'] += 2
            
            # Neutral: Medium scores across the board
            emotion_scores['neutral'] += 2
            
            # Disgust: Eye narrowing, mouth asymmetry (simplified)
            if eye_analysis['avg_openness'] < 0.25:
                emotion_scores['disgust'] += 1
            
            # Find the dominant emotion
            if max(emotion_scores.values()) == 0:
                detected_emotion = 'neutral'
                confidence = 50.0
            else:
                detected_emotion = max(emotion_scores, key=emotion_scores.get)
                max_score = emotion_scores[detected_emotion]
                # Convert score to confidence (0-100)
                confidence = min(95.0, max_score * 15 + 30)
            
            results.append([detected_emotion, confidence])
        
        return results


# Global instance for use in the app
facial_emotion_detector = FacialEmotionDetector()


def detect_emotion_geometric(face_crops, face_cascade):
    """
    Wrapper function for geometric emotion detection.
    This provides a simpler alternative when the neural network approach fails.
    """
    return facial_emotion_detector.detect_emotion(face_crops, face_cascade)

