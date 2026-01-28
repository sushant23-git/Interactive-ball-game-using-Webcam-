"""
Test script for hand tracking functionality.
This script opens the webcam and displays detected hand landmarks in real-time.
"""
import cv2
import sys
sys.path.insert(0, '.')

from hand_tracker import HandTracker
import config


def main():
    """Test hand tracking with webcam."""
    print("Hand Tracking Test")
    print("==================")
    print("This will open your webcam and show detected hand landmarks.")
    print("Hold your hand in front of the camera.")
    print("Press 'q' to quit.")
    print()
    
    # Initialize components
    hand_tracker = HandTracker()
    camera = cv2.VideoCapture(config.CAMERA_INDEX)
    
    if not camera.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Camera opened successfully!")
    print("Detection confidence:", config.HAND_DETECTION_CONFIDENCE)
    print("Tracking confidence:", config.HAND_TRACKING_CONFIDENCE)
    print()
    
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Process frame
        results = hand_tracker.process_frame(frame)
        
        # Draw landmarks
        frame = hand_tracker.draw_landmarks(frame)
        
        # Get finger tip position
        finger_tip = hand_tracker.get_finger_tip()
        
        # Display info on frame
        if finger_tip:
            cv2.putText(frame, f"Finger Tip: ({finger_tip[0]:.2f}, {finger_tip[1]:.2f})", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw a circle at finger tip position
            h, w, _ = frame.shape
            x = int(finger_tip[0] * w)
            y = int(finger_tip[1] * h)
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
        else:
            cv2.putText(frame, "No hand detected", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show frame
        cv2.imshow("Hand Tracking Test", frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    camera.release()
    cv2.destroyAllWindows()
    hand_tracker.close()
    print("\nTest completed!")


if __name__ == "__main__":
    main()
