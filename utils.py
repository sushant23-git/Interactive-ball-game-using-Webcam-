"""
Utility functions for the Asteroid Destroyer game.
"""
import math
import time


class FPSCounter:
    """Calculate and smooth FPS display."""
    
    def __init__(self, smoothing=10):
        self.smoothing = smoothing
        self.frame_times = []
        self.last_time = time.time()
    
    def update(self):
        """Update FPS calculation."""
        current_time = time.time()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.smoothing:
            self.frame_times.pop(0)
        
        return self.get_fps()
    
    def get_fps(self):
        """Get current smoothed FPS."""
        if not self.frame_times:
            return 0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return int(1.0 / avg_frame_time) if avg_frame_time > 0 else 0


def distance(p1, p2):
    """Calculate Euclidean distance between two points.
    
    Args:
        p1: Tuple (x, y) for first point
        p2: Tuple (x, y) for second point
    
    Returns:
        Distance as float
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def clamp(value, min_value, max_value):
    """Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value
    
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))
