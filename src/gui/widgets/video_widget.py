"""Video display widget for showing camera feed."""
import cv2
import numpy as np
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from src.config import VIDEO_DISPLAY_WIDTH, VIDEO_DISPLAY_HEIGHT


class VideoWidget(QLabel):
    """Widget for displaying video frames."""
    
    def __init__(self):
        """Initialize video widget."""
        super().__init__()
        
        self.setMinimumSize(VIDEO_DISPLAY_WIDTH, VIDEO_DISPLAY_HEIGHT)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #000000;
                border: 2px solid #555555;
                border-radius: 5px;
            }
        """)
        
        # Show placeholder text
        self.setText("Camera Preview\n\nPress START to begin detection")
        self.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #555555;
                border-radius: 5px;
                color: #888888;
                font-size: 16px;
            }
        """)
    
    def update_frame(self, frame: np.ndarray):
        """Update displayed frame.
        
        Args:
            frame: OpenCV frame (BGR format)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Get frame dimensions
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        
        # Convert to QImage
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Scale to widget size while maintaining aspect ratio
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.setPixmap(scaled_pixmap)
    
    def clear_frame(self):
        """Clear the video display and show placeholder."""
        self.clear()
        self.setText("Camera Preview\n\nPress START to begin detection")
        self.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #555555;
                border-radius: 5px;
                color: #888888;
                font-size: 16px;
            }
        """)
