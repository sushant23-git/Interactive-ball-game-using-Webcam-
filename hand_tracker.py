"""
Hand tracking module using MediaPipe Hands.
"""
import cv2
import os
import urllib.request
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import config


class HandTracker:
    """Wrapper for MediaPipe Hands solution."""
    
    def __init__(self):
        """Initialize MediaPipe Hands."""
        # Download model if not exists
        model_path = self._get_model_path()
        
        # Create hand landmarker with IMAGE mode (simpler than VIDEO mode)
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,  # Changed from VIDEO to IMAGE
            num_hands=config.MAX_HANDS,
            min_hand_detection_confidence=config.HAND_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=config.HAND_TRACKING_CONFIDENCE,
            min_tracking_confidence=config.HAND_TRACKING_CONFIDENCE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        # Store latest detection
        self.results = None
        self.landmarks = []
    
    def _get_model_path(self):
        """Download and return the path to the hand landmarker model."""
        model_url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
        model_dir = os.path.join(os.path.dirname(__file__), "models")
        model_path = os.path.join(model_dir, "hand_landmarker.task")
        
        # Create models directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
        
        # Download model if it doesn't exist
        if not os.path.exists(model_path):
            print(f"Downloading hand tracking model...")
            urllib.request.urlretrieve(model_url, model_path)
            print(f"Model downloaded to {model_path}")
        
        return model_path
    
    def process_frame(self, frame):
        """Process a frame and detect hands.
        
        Args:
            frame: BGR image from OpenCV
        
        Returns:
            Processed results from MediaPipe
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image from numpy array
        # For IMAGE mode, we need to use the mp.Image constructor properly
        import mediapipe as mp
        
        # Create image using format and data
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )
        
        # Detect hands using IMAGE mode (no timestamp needed)
        self.results = self.detector.detect(mp_image)
        self.landmarks = self.results.hand_landmarks if self.results.hand_landmarks else []
        
        return self.results
    
    def get_finger_tip(self, hand_landmarks=None):
        """Get the index finger tip position.
        
        Args:
            hand_landmarks: Optional specific hand landmarks, otherwise uses first detected hand
        
        Returns:
            Tuple (x, y) in normalized coordinates (0-1), or None if not detected
        """
        if hand_landmarks is None:
            if self.landmarks:
                hand_landmarks = self.landmarks[0]
            else:
                return None
        
        if hand_landmarks:
            # Index finger tip is landmark 8
            finger_tip = hand_landmarks[8]
            return (finger_tip.x, finger_tip.y)
        
        return None
    
    def get_all_landmarks(self):
        """Get all detected hand landmarks.
        
        Returns:
            List of hand landmarks, or empty list if none detected
        """
        return self.landmarks
    
    def draw_landmarks(self, frame):
        """Draw hand landmarks on the frame for debugging.
        
        Args:
            frame: BGR image to draw on
        
        Returns:
            Frame with landmarks drawn
        """
        if self.landmarks:
            h, w, c = frame.shape
            for hand_landmarks in self.landmarks:
                # Draw landmarks
                for landmark in hand_landmarks:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
                
                # Draw connections
                connections = [
                    (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
                    (0, 5), (5, 6), (6, 7), (7, 8),  # Index
                    (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
                    (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
                    (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
                    (5, 9), (9, 13), (13, 17)  # Palm
                ]
                
                for start_idx, end_idx in connections:
                    start = hand_landmarks[start_idx]
                    end = hand_landmarks[end_idx]
                    start_point = (int(start.x * w), int(start.y * h))
                    end_point = (int(end.x * w), int(end.y * h))
                    cv2.line(frame, start_point, end_point, (255, 0, 0), 2)
        
        return frame
    
    def close(self):
        """Release MediaPipe resources."""
        if hasattr(self, 'detector'):
            self.detector.close()
