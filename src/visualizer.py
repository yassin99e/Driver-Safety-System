import cv2
import numpy as np
from src.config import (
    BOX_COLOR_AWAKE, BOX_COLOR_TIRED, BOX_COLOR_SLEEP,
    TEXT_COLOR, ALERT_TEXT_COLOR,
    FONT_SCALE, FONT_THICKNESS, BOX_THICKNESS,
    CLASS_NAMES
)


class Visualizer:
    """Handles video frame visualization with detections and alerts."""
    
    def __init__(self):
        """Initialize the visualizer."""
        self.color_map = {
            0: BOX_COLOR_AWAKE,  # awake - green
            1: BOX_COLOR_SLEEP,  # sleep - red
            2: BOX_COLOR_TIRED   # tired - orange
        }
        
    def draw_detection(self, frame, class_id, confidence, bbox):
        """Draw bounding box and label on frame.
        
        Args:
            frame: OpenCV image
            class_id: Detected class ID
            confidence: Detection confidence
            bbox: (x1, y1, x2, y2) bounding box coordinates
            
        Returns:
            frame: Modified frame with annotations
        """
        if class_id is None or bbox is None:
            return frame
            
        x1, y1, x2, y2 = bbox
        color = self.color_map.get(class_id, (255, 255, 255))
        class_name = CLASS_NAMES.get(class_id, 'unknown')
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, BOX_THICKNESS)
        
        # Draw label background
        label = f"{class_name}: {confidence:.2f}"
        (label_w, label_h), baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS
        )
        
        cv2.rectangle(
            frame,
            (x1, y1 - label_h - 10),
            (x1 + label_w, y1),
            color,
            -1
        )
        
        # Draw label text
        cv2.putText(
            frame,
            label,
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            FONT_SCALE,
            TEXT_COLOR,
            FONT_THICKNESS
        )
        
        return frame
    
    def draw_alert(self, frame, alert_type):
        """Draw alert message on frame.
        
        Args:
            frame: OpenCV image
            alert_type: 'sleep' or 'tired'
            
        Returns:
            frame: Modified frame with alert message
        """
        h, w = frame.shape[:2]
        
        if alert_type == 'sleep':
            message = "ALERT: SLEEPING!"
        elif alert_type == 'tired':
            message = "ALERT: TIRED!"
        else:
            return frame
            
        # Get text size
        font_scale = 1.5
        thickness = 3
        (text_w, text_h), baseline = cv2.getTextSize(
            message, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
        )
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(
            overlay,
            (0, 0),
            (w, text_h + 30),
            (0, 0, 0),
            -1
        )
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        
        # Draw alert text
        text_x = (w - text_w) // 2
        text_y = text_h + 10
        cv2.putText(
            frame,
            message,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            ALERT_TEXT_COLOR,
            thickness
        )
        
        return frame
    
    def draw_status(self, frame, elapsed_time, is_danger):
        """Draw status information on frame.
        
        Args:
            frame: OpenCV image
            elapsed_time: Time in danger state
            is_danger: Whether currently in danger state
            
        Returns:
            frame: Modified frame with status info
        """
        h, w = frame.shape[:2]
        
        if is_danger:
            status_text = f"Danger Time: {elapsed_time:.1f}s"
            color = (0, 0, 255)  # Red
        else:
            status_text = "Status: Safe"
            color = (0, 255, 0)  # Green
            
        # Draw status text at bottom
        cv2.putText(
            frame,
            status_text,
            (10, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            FONT_SCALE,
            color,
            FONT_THICKNESS
        )
        
        return frame
    
    def show_frame(self, frame, window_name="Driver Drowsiness Detection"):
        """Display frame in window.
        
        Args:
            frame: OpenCV image
            window_name: Name of display window
        """
        cv2.imshow(window_name, frame)
