"""
Test script for coordinate mapping.
This script shows both camera view and mapped screen coordinates side by side.
"""
import cv2
import pygame
import sys
sys.path.insert(0, '.')

from hand_tracker import HandTracker
from coordinate_mapper import CoordinateMapper
import config


def main():
    """Test coordinate mapping."""
    print("Coordinate Mapping Test")
    print("=======================")
    print("This will show your hand in camera view and the mapped position on a virtual screen.")
    print("Press 'q' to quit.")
    print()
    
    # Initialize components
    hand_tracker = HandTracker()
    coord_mapper = CoordinateMapper()
    camera = cv2.VideoCapture(config.CAMERA_INDEX)
    
    # Initialize Pygame for screen visualization
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Coordinate Mapping Test - Screen View")
    clock = pygame.time.Clock()
    
    if not camera.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Test running...")
    running = True
    
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        
        # Read camera frame
        ret, frame = camera.read()
        if not ret:
            break
        
        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Process with hand tracker
        hand_tracker.process_frame(frame)
        frame_with_landmarks = hand_tracker.draw_landmarks(frame.copy())
        
        # Get finger tip
        finger_tip_normalized = hand_tracker.get_finger_tip()
        
        # Clear screen
        screen.fill((20, 20, 40))
        
        if finger_tip_normalized:
            # Map to screen coordinates
            screen_x, screen_y = coord_mapper.map_to_screen(*finger_tip_normalized)
            
            # Draw on pygame screen
            pygame.draw.circle(screen, (0, 255, 100), (screen_x, screen_y), 20)
            pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), 8)
            
            # Show coordinates
            font = pygame.font.Font(None, 36)
            coord_text = font.render(f"Screen: ({screen_x}, {screen_y})", True, (255, 255, 255))
            screen.blit(coord_text, (10, 10))
            
            norm_text = font.render(f"Normalized: ({finger_tip_normalized[0]:.2f}, {finger_tip_normalized[1]:.2f})", 
                                   True, (200, 200, 200))
            screen.blit(norm_text, (10, 50))
            
            # Draw on camera frame
            h, w, _ = frame_with_landmarks.shape
            cam_x = int(finger_tip_normalized[0] * w)
            cam_y = int(finger_tip_normalized[1] * h)
            cv2.circle(frame_with_landmarks, (cam_x, cam_y), 15, (0, 255, 0), -1)
            cv2.putText(frame_with_landmarks, f"Cam: ({cam_x}, {cam_y})", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            font = pygame.font.Font(None, 36)
            text = font.render("No hand detected", True, (255, 100, 100))
            screen.blit(text, (10, 10))
        
        # Update displays
        pygame.display.flip()
        cv2.imshow("Camera View", frame_with_landmarks)
        
        # Check for quit in OpenCV window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
        
        clock.tick(30)
    
    # Cleanup
    camera.release()
    cv2.destroyAllWindows()
    hand_tracker.close()
    pygame.quit()
    print("\nTest completed!")


if __name__ == "__main__":
    main()
