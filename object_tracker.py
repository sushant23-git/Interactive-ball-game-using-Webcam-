"""
Object tracking module using OpenCV Color Detection.
"""
import cv2
import numpy as np
import config

class ObjectTracker:
    """Tracks a specific colored object (e.g., white) in the video frame."""
    
    def __init__(self):
        """Initialize the object tracker."""
        self.lower_color = config.TRACK_COLOR_LOWER
        self.upper_color = config.TRACK_COLOR_UPPER
        self.min_area = config.MIN_CONTOUR_AREA
        
        # Current position
        self.position = None
        
        # Debug info
        self.mask = None
        self.contours = None
    
    def process_frame(self, frame):
        """Process a frame and detect the largest object matching the color settings.
        
        Args:
            frame: BGR image from OpenCV
        
        Returns:
            Tuple (x, y) in normalized coordinates (0-1), or None if not detected
        """
        # Convert to HSV color space (better for color tracking)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask based on the color thresholds
        self.mask = cv2.inRange(hsv, self.lower_color, self.upper_color)
        
        # Clean up the mask (remove noise)
        kernel = np.ones((5, 5), np.uint8)
        self.mask = cv2.erode(self.mask, kernel, iterations=1)
        self.mask = cv2.dilate(self.mask, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contours
        
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest_contour) > self.min_area:
                # Find the center of the contour
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Store current position
                    self.position = (cx, cy)
                    
                    # Return normalized coordinates (0-1)
                    height, width = frame.shape[:2]
                    return (cx / width, cy / height)
        
        self.position = None
        return None
    
    def get_debug_image(self, frame):
        """Get a debug image showing the mask and detected object.
        
        Args:
            frame: Original BGR frame
            
        Returns:
            Composite debug image
        """
        if self.mask is None:
            return frame
            
        # Create a visual representation of what the tracker sees
        debug_frame = frame.copy()
        
        # Draw all contours in fine yellow
        cv2.drawContours(debug_frame, self.contours, -1, (0, 255, 255), 1)
        
        if self.position:
            # Draw the detected center
            cv2.circle(debug_frame, self.position, 10, (0, 0, 255), -1)
            cv2.circle(debug_frame, self.position, 12, (255, 255, 255), 2)
            
        # Convert mask to BGR so we can stack it or blend it
        mask_bgr = cv2.cvtColor(self.mask, cv2.COLOR_GRAY2BGR)
        
        # Blend original frame and mask for visualization
        # Or just return the mask side-by-side? simpler to just show the mask overlay
        # Let's verify what the camera sees: Show the MASKED part of the image
        result = cv2.bitwise_and(frame, frame, mask=self.mask)
        
        # Draw marker on result too
        if self.position:
            cv2.circle(result, self.position, 10, (0, 255, 0), -1)
            
        return result

    def close(self):
        """Cleanup resources."""
        pass
