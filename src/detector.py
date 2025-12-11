from ultralytics import YOLO
import cv2
import numpy as np
from src.config import MODEL_PATH, CONFIDENCE_THRESHOLD, CLASS_NAMES


class DrowsinessDetector:
    """YOLOv8-based drowsiness detector."""
    
    def __init__(self, model_path=MODEL_PATH):
        """Initialize the YOLO model.
        
        Args:
            model_path: Path to the trained YOLOv8 model weights
        """
        self.model = YOLO(model_path)
        self.confidence_threshold = CONFIDENCE_THRESHOLD
        
    def detect(self, frame):
        """Run detection on a single frame.
        
        Args:
            frame: OpenCV image (BGR format)
            
        Returns:
            tuple: (class_id, confidence, bbox) or (None, None, None) if no detection
                   class_id: 0 (awake), 1 (sleep), 2 (tired)
                   confidence: detection confidence score
                   bbox: (x1, y1, x2, y2) bounding box coordinates
        """
        results = self.model(frame, verbose=False)
        
        # Get the first result (single image)
        result = results[0]
        
        if len(result.boxes) == 0:
            return None, None, None
            
        # Get the detection with highest confidence
        boxes = result.boxes
        confidences = boxes.conf.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)
        bboxes = boxes.xyxy.cpu().numpy()
        
        # Find highest confidence detection
        max_idx = np.argmax(confidences)
        
        if confidences[max_idx] < self.confidence_threshold:
            return None, None, None
            
        class_id = classes[max_idx]
        confidence = confidences[max_idx]
        bbox = bboxes[max_idx].astype(int)
        
        return class_id, confidence, bbox
    
    def get_class_name(self, class_id):
        """Convert class ID to class name.
        
        Args:
            class_id: Integer class ID
            
        Returns:
            str: Class name ('awake', 'sleep', or 'tired')
        """
        return CLASS_NAMES.get(class_id, 'unknown')
