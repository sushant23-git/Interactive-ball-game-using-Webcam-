"""
Interactive Asteroid Destroyer Game
Main game loop and integration of all components.
"""
import pygame
import cv2
import sys
import os
import config
from object_tracker import ObjectTracker  # Swapped from hand_tracker
from coordinate_mapper import CoordinateMapper
from game_manager import GameManager
from game_objects import FingerCursor
from ui_renderer import UIRenderer
from utils import FPSCounter


class AsteroidGame:
    """Main game class integrating all components."""
    
    def __init__(self):
        """Initialize the game."""
        # Initialize Pygame
        pygame.init()
        
        # Set up display
        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.fullscreen = config.FULLSCREEN
        
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 
                                                  pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        pygame.display.set_caption("Asteroid Destroyer (Object Tracking Mode)")
        
        # Load background image
        bg_path = os.path.join(os.path.dirname(__file__), 'background.png')
        self.background_image = pygame.image.load(bg_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        # Initialize components
        self.object_tracker = ObjectTracker()
        self.coord_mapper = CoordinateMapper(self.screen_width, self.screen_height)
        self.game_manager = GameManager(self.screen_width, self.screen_height)
        self.finger_cursor = FingerCursor()
        self.ui_renderer = UIRenderer(self.screen)
        self.fps_counter = FPSCounter()
        
        # Initialize webcam
        self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        
        if not self.camera.isOpened():
            print("Error: Could not open camera")
            sys.exit(1)
        
        # Game state
        self.running = True
        self.game_state = "menu"  # menu, playing, game_over
        self.debug_mode = config.DEBUG_MODE
        self.last_frame = None
        self.clock = pygame.time.Clock()
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 
                                                  pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "menu":
                        self.running = False
                    else:
                        self.game_state = "menu"
                
                elif event.key == pygame.K_SPACE:
                    if self.game_state == "menu":
                        self.game_state = "playing"
                        self.game_manager.reset()
                    elif self.game_state == "game_over":
                        self.game_state = "playing"
                        self.game_manager.reset()
                
                elif event.key == pygame.K_f:
                    self.toggle_fullscreen()
                
                elif event.key == pygame.K_d:
                    self.debug_mode = not self.debug_mode
                    print(f"Debug Mode: {self.debug_mode}")
    
    def process_tracking(self):
        """Process webcam frame and detect object position.
        
        Returns:
            Screen coordinates (x, y) of object center, or None
        """
        ret, frame = self.camera.read()
        if not ret:
            return None
        
        # Flip frame horizontally for mirror effect (intuitive for screen interaction)
        frame = cv2.flip(frame, 1)
        self.last_frame = frame # Store for debug rendering
        
        # Process with object tracker
        normalized_pos = self.object_tracker.process_frame(frame)
        
        if normalized_pos:
            # Map to screen coordinates
            screen_pos = self.coord_mapper.map_to_screen(*normalized_pos)
            return screen_pos
        
        return None
    
    def update(self, cursor_position):
        """Update game state.
        
        Args:
            cursor_position: Tuple (x, y) or None
        """
        if self.game_state == "playing":
            # Update game manager
            self.game_manager.update(cursor_position)
            
            # Update cursor visual
            self.finger_cursor.update(cursor_position)
            
            # Check if game is over
            if self.game_manager.game_over:
                self.game_state = "game_over"
    
    def render(self):
        """Render the game."""
        # Draw background image
        self.screen.blit(self.background_image, (0, 0))
        
        if self.game_state == "menu":
            self.ui_renderer.draw_menu()
            # Add tip about debug mode
            font = pygame.font.Font(None, 24)
            debug_text = font.render("Press 'D' to show Camera View (Debug)", True, (150, 150, 150))
            self.screen.blit(debug_text, (10, self.screen_height - 30))
        
        elif self.game_state == "playing":
            # Draw asteroids
            for asteroid in self.game_manager.asteroids:
                asteroid.draw(self.screen)
            
            # Draw particles
            for particle in self.game_manager.particles:
                particle.draw(self.screen)
            
            # Draw cursor
            self.finger_cursor.draw(self.screen)
            
            # Draw UI
            self.ui_renderer.draw_score(self.game_manager.score)
            self.ui_renderer.draw_lives(self.game_manager.lives)
            
            # Draw FPS
            fps = self.fps_counter.get_fps()
            self.ui_renderer.draw_fps(fps)
        
        elif self.game_state == "game_over":
            # Still draw the game in background
            for asteroid in self.game_manager.asteroids:
                asteroid.draw(self.screen)
            
            for particle in self.game_manager.particles:
                particle.draw(self.screen)
            
            # Draw game over overlay
            self.ui_renderer.draw_game_over(self.game_manager.score)
            
        # Debug Overlay (Picture-in-Picture)
        if self.debug_mode and self.last_frame is not None:
             # Get debug image from tracker (shows mask)
            debug_img = self.object_tracker.get_debug_image(self.last_frame)
            
            # Resize for PiP
            pip_height = self.screen_height // 4
            pip_width = int(pip_height * (config.CAMERA_WIDTH / config.CAMERA_HEIGHT))
            debug_img_small = cv2.resize(debug_img, (pip_width, pip_height))
            
            # Convert to Pygame surface
            debug_img_rgb = cv2.cvtColor(debug_img_small, cv2.COLOR_BGR2RGB)
            debug_surface = pygame.surfarray.make_surface(debug_img_rgb.swapaxes(0, 1))
            
            # Draw box and image
            self.screen.blit(debug_surface, (self.screen_width - pip_width - 10, self.screen_height - pip_height - 10))
            pygame.draw.rect(self.screen, (255, 255, 0), 
                           (self.screen_width - pip_width - 10, self.screen_height - pip_height - 10, pip_width, pip_height), 2)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        print("Asteroid Destroyer Game Starting (Object Tracking)...")
        print("Position your webcam to see the PROJECTED SCREEN.")
        print("Use a WHITE OBJECT to aim.")
        print("Press 'D' to toggle debug view to see what the camera sees.")
        
        while self.running:
            # Handle events
            self.handle_events()
            
            # Process tracking
            cursor_position = self.process_tracking()
            
            # Update game
            self.update(cursor_position)
            
            # Render
            self.render()
            
            # Update FPS
            self.fps_counter.update()
            
            # Cap frame rate
            self.clock.tick(config.FPS_TARGET)
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        self.camera.release()
        self.object_tracker.close()
        pygame.quit()
        print("Game closed. Thanks for playing!")


def main():
    """Entry point for the game."""
    game = AsteroidGame()
    game.run()


if __name__ == "__main__":
    main()
