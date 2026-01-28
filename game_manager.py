"""
Game manager handles game logic and state.
"""
import random
import config
from game_objects import Asteroid, Particle


class GameManager:
    """Manages the game state, asteroids, scoring, and difficulty."""
    
    def __init__(self, screen_width, screen_height):
        """Initialize game manager.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Game state
        self.score = 0
        self.lives = config.INITIAL_LIVES if config.ENABLE_LIVES else 999
        self.game_over = False
        
        # Asteroids and effects
        self.asteroids = []
        self.particles = []
        
        # Difficulty settings
        self.asteroid_speed = config.INITIAL_ASTEROID_SPEED
        self.spawn_rate = config.ASTEROID_SPAWN_RATE
        self.frames_since_spawn = 0
        
        # Difficulty scaling
        self.last_difficulty_increase = 0
    
    def spawn_asteroid(self):
        """Spawn a new asteroid at a random position."""
        x = random.randint(config.ASTEROID_MAX_SIZE, 
                          self.screen_width - config.ASTEROID_MAX_SIZE)
        y = -config.ASTEROID_MAX_SIZE
        radius = random.randint(config.ASTEROID_MIN_SIZE, config.ASTEROID_MAX_SIZE)
        speed = self.asteroid_speed + random.uniform(-0.5, 0.5)
        
        asteroid = Asteroid(x, y, radius, speed)
        self.asteroids.append(asteroid)
    
    def update_asteroids(self):
        """Update all asteroids and remove off-screen ones."""
        for asteroid in self.asteroids[:]:
            asteroid.update()
            
            # Check if asteroid is off screen (missed)
            if asteroid.is_off_screen(self.screen_height):
                self.asteroids.remove(asteroid)
                if config.ENABLE_LIVES and asteroid.alive:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
    
    def update_particles(self):
        """Update all particles and remove dead ones."""
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def check_collisions(self, finger_position):
        """Check for collisions between finger and asteroids.
        
        Args:
            finger_position: Tuple (x, y) of finger position, or None
        
        Returns:
            Number of asteroids destroyed this frame
        """
        if finger_position is None:
            return 0
        
        destroyed_count = 0
        for asteroid in self.asteroids[:]:
            if asteroid.check_collision(finger_position):
                # Destroy asteroid
                asteroid.alive = False
                self.asteroids.remove(asteroid)
                
                # Create explosion particles
                self.create_explosion(asteroid.x, asteroid.y)
                
                # Increase score
                self.score += 1
                destroyed_count += 1
        
        return destroyed_count
    
    def create_explosion(self, x, y):
        """Create particle explosion at position.
        
        Args:
            x: X position
            y: Y position
        """
        for _ in range(config.PARTICLE_COUNT):
            particle = Particle(x, y)
            self.particles.append(particle)
    
    def update_difficulty(self):
        """Increase difficulty based on score."""
        score_increase = self.score - self.last_difficulty_increase
        
        if score_increase >= config.DIFFICULTY_INCREASE_INTERVAL:
            self.asteroid_speed *= config.SPEED_INCREASE_FACTOR
            self.spawn_rate = max(20, self.spawn_rate - config.SPAWN_RATE_DECREASE)
            self.last_difficulty_increase = self.score
    
    def update(self, finger_position):
        """Update game state.
        
        Args:
            finger_position: Tuple (x, y) of finger position, or None
        """
        if self.game_over:
            return
        
        # Update existing asteroids
        self.update_asteroids()
        
        # Update particles
        self.update_particles()
        
        # Check collisions
        self.check_collisions(finger_position)
        
        # Spawn new asteroids
        self.frames_since_spawn += 1
        if self.frames_since_spawn >= self.spawn_rate:
            self.spawn_asteroid()
            self.frames_since_spawn = 0
        
        # Update difficulty
        self.update_difficulty()
    
    def reset(self):
        """Reset the game to initial state."""
        self.score = 0
        self.lives = config.INITIAL_LIVES if config.ENABLE_LIVES else 999
        self.game_over = False
        self.asteroids = []
        self.particles = []
        self.asteroid_speed = config.INITIAL_ASTEROID_SPEED
        self.spawn_rate = config.ASTEROID_SPAWN_RATE
        self.frames_since_spawn = 0
        self.last_difficulty_increase = 0
