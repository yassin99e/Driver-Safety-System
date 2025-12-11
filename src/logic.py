import time
from src.config import ALERT_THRESHOLD_SECONDS


class DrowsinessLogic:
    """Manages drowsiness state tracking and alert triggering logic."""
    
    def __init__(self, threshold_seconds=ALERT_THRESHOLD_SECONDS):
        """Initialize the logic tracker.
        
        Args:
            threshold_seconds: Time threshold for triggering alert
        """
        self.threshold = threshold_seconds
        self.danger_start_time = None
        self.current_state = None
        self.alert_triggered = False
        
    def update(self, class_id):
        """Update state based on new detection.
        
        Args:
            class_id: Detected class (0=awake, 1=sleep, 2=tired, None=no detection)
            
        Returns:
            tuple: (should_alert, alert_type, elapsed_time)
                   should_alert: True if alert should be triggered
                   alert_type: 'sleep' or 'tired' (None if no alert)
                   elapsed_time: Current accumulated danger time
        """
        current_time = time.time()
        
        # Determine if current state is dangerous (sleep or tired)
        is_danger = class_id in [1, 2]  # 1=sleep, 2=tired
        
        # If awake or no detection, reset
        if not is_danger:
            self.danger_start_time = None
            self.current_state = class_id
            self.alert_triggered = False
            return False, None, 0.0
        
        # Start tracking danger time if not already started
        if self.danger_start_time is None:
            self.danger_start_time = current_time
            self.alert_triggered = False
        
        # Update current state
        self.current_state = class_id
        
        # Calculate elapsed time in danger state
        elapsed_time = current_time - self.danger_start_time
        
        # Check if threshold exceeded and alert not yet triggered
        if elapsed_time >= self.threshold and not self.alert_triggered:
            self.alert_triggered = True
            alert_type = 'sleep' if class_id == 1 else 'tired'
            return True, alert_type, elapsed_time
        
        return False, None, elapsed_time
    
    def get_status(self):
        """Get current tracking status.
        
        Returns:
            dict: Status information including state and elapsed time
        """
        if self.danger_start_time is None:
            elapsed = 0.0
        else:
            elapsed = time.time() - self.danger_start_time
            
        return {
            'current_state': self.current_state,
            'elapsed_time': elapsed,
            'is_danger': self.current_state in [1, 2],
            'alert_triggered': self.alert_triggered
        }
