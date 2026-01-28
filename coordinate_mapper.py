"""
Coordinate mapping between camera space and screen space.
"""
import config
from utils import clamp


class CoordinateMapper:
    """Maps coordinates from camera view to screen coordinates."""
    
    def __init__(self, screen_width=None, screen_height=None):
        """Initialize coordinate mapper.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
        """
        self.screen_width = screen_width or config.SCREEN_WIDTH
        self.screen_height = screen_height or config.SCREEN_HEIGHT
        
        # Calibration points (for future calibration feature)
        self.calibrated = False
        self.calibration_matrix = None
    
    def map_to_screen(self, normalized_x, normalized_y):
        """Convert normalized camera coordinates (0-1) to screen pixel coordinates.
        
        Args:
            normalized_x: X coordinate from MediaPipe (0-1, left to right)
            normalized_y: Y coordinate from MediaPipe (0-1, top to bottom)
        
        Returns:
            Tuple (screen_x, screen_y) in pixels
        """
        # MediaPipe returns normalized coordinates where (0,0) is top-left
        # and (1,1) is bottom-right, same as screen coordinates
        
        # Simple proportional scaling
        screen_x = int(normalized_x * self.screen_width)
        screen_y = int(normalized_y * self.screen_height)
        
        # Clamp to screen bounds
        screen_x = clamp(screen_x, 0, self.screen_width - 1)
        screen_y = clamp(screen_y, 0, self.screen_height - 1)
        
        return (screen_x, screen_y)
    
    def inverse_map(self, screen_x, screen_y):
        """Convert screen coordinates back to normalized coordinates.
        
        Args:
            screen_x: X coordinate in pixels
            screen_y: Y coordinate in pixels
        
        Returns:
            Tuple (normalized_x, normalized_y) in range 0-1
        """
        normalized_x = screen_x / self.screen_width
        normalized_y = screen_y / self.screen_height
        
        return (normalized_x, normalized_y)
    
    def calibrate(self, corner_points):
        """Calibrate using detected corner points (future feature).
        
        Args:
            corner_points: List of (camera_x, camera_y, screen_x, screen_y) tuples
        """
        # Placeholder for future calibration implementation
        # Could use perspective transform or homography
        self.calibrated = True
        pass
