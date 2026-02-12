"""
Ball tracking module using Machine Learning (MobileNet-SSD).
"""
import cv2
import numpy as np
import config
import os

class ObjectTracker:
    """Tracks a ball using ML-based object detection (MobileNet-SSD)."""
    
    def __init__(self):
        """Initialize the ML-based ball tracker."""
        self.use_ml = config.USE_ML_DETECTION
        self.confidence_threshold = config.CONFIDENCE_THRESHOLD
        self.target_class = config.TARGET_CLASS_ID
        
        # Color filter settings (optional)
        self.use_color_filter = config.USE_COLOR_FILTER
        if self.use_color_filter:
            self.ball_color = config.BALL_COLOR
            self.color_ranges = config.BALL_COLOR_RANGES.get(self.ball_color, config.BALL_COLOR_RANGES['ANY'])
        
        # Current position and size
        self.position = None
        self.bbox = None  # (x, y, w, h)
        self.confidence = 0.0
        
        # Debug info
        self.detections = []
        self.mask = None
        
        # Load ML model
        if self.use_ml:
            self._load_model()
    
    def _load_model(self):
        """Load the MobileNet-SSD model."""
        prototxt = config.MODEL_PROTOTXT
        weights = config.MODEL_WEIGHTS
        
        # Check if model files exist
        if not os.path.exists(prototxt):
            raise FileNotFoundError(f"Model prototxt not found: {prototxt}")
        if not os.path.exists(weights):
            raise FileNotFoundError(f"Model weights not found: {weights}")
        
        print(f"Loading MobileNet-SSD model...")
        self.net = cv2.dnn.readNetFromCaffe(prototxt, weights)
        print(f"✅ Model loaded successfully!")
        
        # COCO class labels (simplified - we only care about index 37)
        self.class_labels = [
            "background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor", "background", "background",
            "background", "background", "background", "background",
            "background", "background", "background", "background",
            "background", "background", "background", "background",
            "background", "background", "sports ball"  # Index 37
        ]
    
    def process_frame(self, frame):
        """Process a frame and detect a ball using ML.
        
        Args:
            frame: BGR image from OpenCV
        
        Returns:
            Tuple (x, y) in normalized coordinates (0-1), or None if not detected
        """
        if not self.use_ml:
            return None
        
        height, width = frame.shape[:2]
        
        # Prepare frame for DNN
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),  # MobileNet-SSD expects 300x300
            0.007843,  # Scale factor
            (300, 300),
            127.5  # Mean subtraction
        )
        
        # Run inference
        self.net.setInput(blob)
        detections = self.net.forward()
        
        # Store all detections for debug
        self.detections = []
        
        # Find the best ball detection
        best_detection = None
        best_confidence = 0.0
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            class_id = int(detections[0, 0, i, 1])
            
            # Check if it's a sports ball with sufficient confidence
            if class_id == self.target_class and confidence > self.confidence_threshold:
                # Get bounding box coordinates
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x1, y1, x2, y2) = box.astype("int")
                
                # Store detection info
                detection_info = {
                    'class_id': class_id,
                    'confidence': float(confidence),
                    'bbox': (x1, y1, x2, y2)
                }
                self.detections.append(detection_info)
                
                # Optional: Apply color filter
                if self.use_color_filter:
                    if not self._check_color_match(frame, (x1, y1, x2, y2)):
                        continue
                
                # Keep the most confident detection
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_detection = detection_info
        
        # Process best detection
        if best_detection:
            x1, y1, x2, y2 = best_detection['bbox']
            
            # Calculate center
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            
            # Store info
            self.position = (cx, cy)
            self.bbox = (x1, y1, x2 - x1, y2 - y1)  # (x, y, w, h)
            self.confidence = best_confidence
            
            # Return normalized coordinates
            return (cx / width, cy / height)
        
        # No ball detected
        self.position = None
        self.bbox = None
        self.confidence = 0.0
        return None
    
    def _check_color_match(self, frame, bbox):
        """Check if the detected region matches the target color.
        
        Args:
            frame: BGR image
            bbox: (x1, y1, x2, y2)
            
        Returns:
            True if color matches, False otherwise
        """
        x1, y1, x2, y2 = bbox
        
        # Extract ROI
        roi = frame[y1:y2, x1:x2]
        if roi.size == 0:
            return False
        
        # Convert to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Create mask
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in self.color_ranges:
            color_mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.bitwise_or(mask, color_mask)
        
        # Check if enough pixels match the color
        color_ratio = np.sum(mask > 0) / mask.size
        return color_ratio > 0.2  # At least 20% of the region should match
    
    def get_debug_image(self, frame):
        """Get a debug image showing detections and tracking info.
        
        Args:
            frame: Original BGR frame
            
        Returns:
            Debug visualization image
        """
        debug_frame = frame.copy()
        
        # Draw all detections (lower confidence in yellow)
        for det in self.detections:
            x1, y1, x2, y2 = det['bbox']
            conf = det['confidence']
            
            # Draw bounding box
            cv2.rectangle(debug_frame, (x1, y1), (x2, y2), (0, 255, 255), 1)
            
            # Draw confidence
            label = f"{conf:.2f}"
            cv2.putText(debug_frame, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        # Draw the final tracked ball (if any)
        if self.position and self.bbox:
            x, y, w, h = self.bbox
            cx, cy = self.position
            
            # Draw green bounding box for tracked ball
            cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Draw center point
            cv2.circle(debug_frame, (cx, cy), 8, (0, 0, 255), -1)
            cv2.circle(debug_frame, (cx, cy), 10, (255, 255, 255), 2)
            
            # Draw confidence and info
            label = f"Ball: {self.confidence:.2f}"
            cv2.putText(debug_frame, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Show tracking mode
        mode_text = "ML Detection: ON"
        if self.use_color_filter:
            mode_text += f" + {self.ball_color} color filter"
        cv2.putText(debug_frame, mode_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show detection count
        cv2.putText(debug_frame, f"Detections: {len(self.detections)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return debug_frame
    
    def close(self):
        """Cleanup resources."""
        pass
