import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Model configuration
MODEL_PATH = ROOT_DIR / "assets" / "models" / "best-2.pt"
CONFIDENCE_THRESHOLD = 0.5

# Class mapping
CLASS_NAMES = {
    0: 'awake',
    1: 'sleep',
    2: 'tired'
}

# Alert configuration
ALERT_THRESHOLD_SECONDS = 3  # Duration threshold for triggering alerts
SOUND_SLEEP = ROOT_DIR / "assets" / "sounds" / "sleep.wav"
SOUND_TIRED = ROOT_DIR / "assets" / "sounds" / "tired.wav"

# Camera configuration
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Visualization settings
BOX_COLOR_AWAKE = (0, 255, 0)    # Green
BOX_COLOR_TIRED = (0, 165, 255)  # Orange
BOX_COLOR_SLEEP = (0, 0, 255)    # Red
TEXT_COLOR = (255, 255, 255)     # White
ALERT_TEXT_COLOR = (0, 0, 255)   # Red
FONT_SCALE = 0.6
FONT_THICKNESS = 2
BOX_THICKNESS = 2
