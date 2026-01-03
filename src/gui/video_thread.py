"""Video processing thread for real-time detection."""
# CRITICAL: Import torch-dependent modules BEFORE PyQt6 to avoid DLL conflicts on Windows
from src.detector import DrowsinessDetector
from src.logic import DrowsinessLogic
from src.alerter import AudioAlerter
from src.visualizer import Visualizer
from src.config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

# Now import PyQt6 after torch is loaded
import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from typing import Optional


class VideoThread(QThread):
    """Background thread for video capture and detection processing."""
    
    # Signals
    frame_ready = pyqtSignal(np.ndarray)  # Emits processed frame
    detection_result = pyqtSignal(int, float, float, bool)  # state_id, confidence, danger_time, alert_triggered
    error_occurred = pyqtSignal(str)  # Error message
    
    def __init__(self, camera_index: int = CAMERA_INDEX):
        """Initialize video thread.
        
        Args:
            camera_index: Camera device index
        """
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        self.paused = False
        
        # Components (initialized in run)
        self.cap: Optional[cv2.VideoCapture] = None
        self.detector: Optional[DrowsinessDetector] = None
        self.logic: Optional[DrowsinessLogic] = None
        self.alerter: Optional[AudioAlerter] = None
        self.visualizer: Optional[Visualizer] = None
    
    def run(self):
        """Main thread loop - captures and processes video frames."""
        try:
            # Initialize components
            self.detector = DrowsinessDetector()
            self.logic = DrowsinessLogic()
            self.alerter = AudioAlerter()
            self.visualizer = Visualizer()
            
            # Initialize camera
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                self.error_occurred.emit("Could not open camera")
                return
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            
            self.running = True
            
            while self.running:
                if self.paused:
                    self.msleep(100)  # Sleep when paused
                    continue
                
                # Capture frame
                ret, frame = self.cap.read()
                
                if not ret:
                    self.error_occurred.emit("Failed to grab frame")
                    break
                
                # Run detection
                class_id, confidence, bbox = self.detector.detect(frame)
                
                # Update logic
                should_alert, alert_type, elapsed_time = self.logic.update(class_id)
                
                # Get status
                status = self.logic.get_status()
                
                # Handle alerts
                if should_alert:
                    self.alerter.play_alert(alert_type)
                elif not status['is_danger']:
                    self.alerter.stop()
                
                # Visualize
                if class_id is not None:
                    frame = self.visualizer.draw_detection(frame, class_id, confidence, bbox)
                
                if status['alert_triggered']:
                    frame = self.visualizer.draw_alert(frame, alert_type)
                
                frame = self.visualizer.draw_status(frame, status['elapsed_time'], status['is_danger'])
                
                # Emit signals
                self.frame_ready.emit(frame)
                
                if class_id is not None:
                    self.detection_result.emit(
                        class_id,
                        confidence,
                        elapsed_time,
                        status['alert_triggered']
                    )
                
                # Small delay to control frame rate
                self.msleep(30)  # ~33 FPS
                
        except Exception as e:
            self.error_occurred.emit(f"Error in video thread: {str(e)}")
        finally:
            self.cleanup()
    
    def pause(self):
        """Pause video processing."""
        self.paused = True
        if self.alerter:
            self.alerter.stop()
    
    def resume(self):
        """Resume video processing."""
        self.paused = False
    
    def stop(self):
        """Stop video processing and cleanup."""
        self.running = False
        self.wait()  # Wait for thread to finish
    
    def cleanup(self):
        """Clean up resources."""
        if self.cap is not None:
            self.cap.release()
        
        if self.alerter is not None:
            self.alerter.cleanup()
