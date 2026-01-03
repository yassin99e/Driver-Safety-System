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

# GUI Configuration
GUI_WINDOW_TITLE = "Driver Safety System - Drowsiness Detection"
GUI_WINDOW_WIDTH = 1200
GUI_WINDOW_HEIGHT = 800
GUI_MIN_WIDTH = 800
GUI_MIN_HEIGHT = 600

# GUI Colors (RGB for PyQt)
GUI_COLOR_AWAKE = "#00FF00"      # Green
GUI_COLOR_TIRED = "#FFA500"      # Orange
GUI_COLOR_SLEEP = "#FF0000"      # Red
GUI_COLOR_SAFE = "#4CAF50"       # Material Green
GUI_COLOR_DANGER = "#F44336"     # Material Red
GUI_COLOR_WARNING = "#FF9800"    # Material Orange
GUI_BACKGROUND = "#2C3E50"       # Dark blue-gray
GUI_PANEL_BACKGROUND = "#34495E" # Lighter blue-gray
GUI_TEXT_PRIMARY = "#FFFFFF"     # White
GUI_TEXT_SECONDARY = "#BDC3C7"   # Light gray

# Session settings
SESSION_LOG_DIRECTORY = ROOT_DIR / "logs"
SESSION_LOG_FORMAT = "session_%Y%m%d_%H%M%S.csv"

# Video display settings
VIDEO_DISPLAY_WIDTH = 640
VIDEO_DISPLAY_HEIGHT = 480
VIDEO_UPDATE_INTERVAL_MS = 30  # ~33 FPS
