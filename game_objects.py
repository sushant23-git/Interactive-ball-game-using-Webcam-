"""
Game objects: Asteroids, Particles, and Finger Cursor.
"""
import random
import pygame
import math
import os
import config
from utils import distance

# Cache for asteroid image
_asteroid_image_cache = None

def get_asteroid_image():
    """Load and cache the asteroid image."""
    global _asteroid_image_cache
    if _asteroid_image_cache is None:
        image_path = os.path.join(os.path.dirname(__file__), 'aestroid.png')
        _asteroid_image_cache = pygame.image.load(image_path).convert_alpha()
    return _asteroid_image_cache


class Asteroid:
    """Represents a falling asteroid."""
    
    def __init__(self, x, y, radius, speed):
        """Initialize an asteroid.
        
        Args:
            x: X position
            y: Y position
            radius: Asteroid radius
            speed: Falling speed (pixels per frame)
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = config.ASTEROID_COLOR
        self.alive = True
        
        # Load and scale the asteroid image based on radius
        original_image = get_asteroid_image()
        size = radius * 2  # Diameter
        self.image = pygame.transform.smoothscale(original_image, (size, size))
    
    def update(self):
        """Move asteroid downward."""
        self.y += self.speed
    
    def draw(self, surface):
        """Draw the asteroid on a Pygame surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        if self.alive:
            # Draw the asteroid image centered on the position
            image_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, image_rect)
    
    def check_collision(self, point):
        """Check if a point collides with this asteroid.
        
        Args:
            point: Tuple (x, y) representing the point to test
        
        Returns:
            True if collision detected, False otherwise
        """
        if not self.alive:
            return False
        
        if point is None:
            return False
        
        dist = distance(point, (self.x, self.y))
        return dist <= self.radius
    
    def is_off_screen(self, screen_height):
        """Check if asteroid has fallen off the screen.
        
        Args:
            screen_height: Height of the screen
        
        Returns:
            True if off screen, False otherwise
        """
        return self.y - self.radius > screen_height


class Particle:
    """Particle effect for explosions."""
    
    def __init__(self, x, y):
        """Initialize a particle.
        
        Args:
            x: Initial X position
            y: Initial Y position
        """
        self.x = x
        self.y = y
        
        # Random velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*config.PARTICLE_SPEED_RANGE)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        self.lifetime = config.PARTICLE_LIFETIME
        self.max_lifetime = config.PARTICLE_LIFETIME
        self.color = random.choice(config.PARTICLE_COLORS)
        self.size = random.randint(2, 5)
    
    def update(self):
        """Update particle position and lifetime."""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
    
    def draw(self, surface):
        """Draw the particle.
        
        Args:
            surface: Pygame surface to draw on
        """
        if self.lifetime > 0:
            # Fade out based on lifetime
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            # Create a surface with alpha for fading effect
            temp_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(temp_surface, color_with_alpha, (self.size, self.size), self.size)
            surface.blit(temp_surface, (int(self.x) - self.size, int(self.y) - self.size))
    
    def is_alive(self):
        """Check if particle is still alive.
        
        Returns:
            True if alive, False otherwise
        """
        return self.lifetime > 0


class FingerCursor:
    """Visual representation of the finger position."""
    
    def __init__(self):
        """Initialize finger cursor."""
        self.position = None
        self.trail = []
        self.color = config.FINGER_CURSOR_COLOR
        self.radius = config.CURSOR_RADIUS
    
    def update(self, position):
        """Update cursor position.
        
        Args:
            position: Tuple (x, y) or None
        """
        self.position = position
        
        if position:
            self.trail.append(position)
            if len(self.trail) > config.CURSOR_TRAIL_LENGTH:
                self.trail.pop(0)
    
    def draw(self, surface):
        """Draw the cursor and its trail.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = int(255 * ((i + 1) / len(self.trail)))
            size = int(self.radius * 0.5 * ((i + 1) / len(self.trail)))
            temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(temp_surface, color_with_alpha, (size, size), size)
            surface.blit(temp_surface, (int(pos[0]) - size, int(pos[1]) - size))
        
        # Draw main cursor
        if self.position:
            pygame.draw.circle(surface, self.color, 
                             (int(self.position[0]), int(self.position[1])), self.radius)
            # Add a white center for better visibility
            pygame.draw.circle(surface, (255, 255, 255), 
                             (int(self.position[0]), int(self.position[1])), self.radius // 3)
