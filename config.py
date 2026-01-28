"""
Configuration settings for the Asteroid Destroyer game.
"""
import cv2
import numpy as np

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS_TARGET = 60
FULLSCREEN = True

# Camera settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Object tracking settings (White Color Detection)
# HSV Color Space Thresholds
# For white/bright objects, Saturation is low, Value (Brightness) is high
TRACK_COLOR_LOWER = np.array([0, 0, 200])   # Low saturation, very high brightness
TRACK_COLOR_UPPER = np.array([180, 50, 255]) # Any hue, low saturation, max brightness

# Detection parameters
MIN_CONTOUR_AREA = 100  # Minimum size of object to detect
SMOOTHING_FACTOR = 0.5  # 0.0 to 1.0 (higher = more smoothing, lower latency)

# Debug mode (to see what the camera sees)
DEBUG_MODE = False

# Game settings
INITIAL_ASTEROID_SPEED = 2
ASTEROID_SPAWN_RATE = 60  # frames between spawns
ASTEROID_MIN_SIZE = 20
ASTEROID_MAX_SIZE = 50
DIFFICULTY_INCREASE_INTERVAL = 10  # score points
SPEED_INCREASE_FACTOR = 1.1
SPAWN_RATE_DECREASE = 5  # decrease frames between spawns

# Lives system
ENABLE_LIVES = True
INITIAL_LIVES = 3

# Colors (R, G, B)
BG_COLOR = (10, 10, 30)
ASTEROID_COLOR = (200, 50, 50)
FINGER_CURSOR_COLOR = (0, 255, 100)
TEXT_COLOR = (255, 255, 255)
PARTICLE_COLORS = [(255, 200, 0), (255, 150, 0), (255, 100, 0), (200, 50, 0)]

# UI settings
FONT_SIZE_SCORE = 48
FONT_SIZE_NORMAL = 36
FONT_SIZE_SMALL = 24

# Particle effects
PARTICLE_COUNT = 15
PARTICLE_LIFETIME = 30  # frames
PARTICLE_SPEED_RANGE = (2, 6)

# Cursor settings
CURSOR_RADIUS = 30
CURSOR_TRAIL_LENGTH = 10
