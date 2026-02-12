"""
Configuration settings for the Asteroid Destroyer game.
"""
import cv2
import numpy as np

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS_TARGET = 60
FULLSCREEN = False

# Camera settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Ball Detection Settings - Machine Learning Based
# Uses pre-trained MobileNet-SSD model to detect actual ball objects

# ML Model Configuration
USE_ML_DETECTION = True  # Use ML-based ball detection
MODEL_PROTOTXT = "models/MobileNetSSD_deploy.prototxt"
MODEL_WEIGHTS = "models/MobileNetSSD_deploy.caffemodel"

# Detection Parameters
CONFIDENCE_THRESHOLD = 0.3  # Minimum confidence for ball detection (0.0 - 1.0)
TARGET_CLASS_ID = 37  # COCO class ID for "sports ball"
# MobileNet-SSD COCO classes: person, bicycle, car, ..., sports ball (37), ...

# Color filter (optional, for additional filtering after ML detection)
USE_COLOR_FILTER = False  # Set to True to combine ML + color filtering
BALL_COLOR = 'ANY'  # Used only if USE_COLOR_FILTER is True

# HSV Color ranges (used if USE_COLOR_FILTER is enabled)
BALL_COLOR_RANGES = {
    'RED': [(np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))],
    'GREEN': [(np.array([40, 50, 50]), np.array([80, 255, 255]))],
    'BLUE': [(np.array([100, 100, 70]), np.array([130, 255, 255]))],
    'ORANGE': [(np.array([10, 100, 100]), np.array([25, 255, 255]))],
    'YELLOW': [(np.array([20, 100, 100]), np.array([35, 255, 255]))],
    'ANY': [(np.array([0, 50, 50]), np.array([180, 255, 255]))]
}

# Detection parameters
MIN_CONTOUR_AREA = 300  # Minimum size of ball bounding box area
SMOOTHING_FACTOR = 0.5  # 0.0 to 1.0 (higher = more smoothing, lower latency)

# Debug mode (to see what the camera sees)
DEBUG_MODE = False

# Game settings
INITIAL_ASTEROID_SPEED = 2
ASTEROID_SPAWN_RATE = 60  # frames between spawns
ASTEROID_MIN_SIZE = 50
ASTEROID_MAX_SIZE = 100
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
