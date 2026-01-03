"""Session manager for tracking statistics and alert history."""
import time
from datetime import datetime
from typing import List, Dict, Optional
import csv
from pathlib import Path
from src.config import SESSION_LOG_DIRECTORY, SESSION_LOG_FORMAT, CLASS_NAMES


class AlertEvent:
    """Represents a single alert event."""
    
    def __init__(self, timestamp: float, state: str, duration: float, alert_triggered: bool):
        """Initialize alert event.
        
        Args:
            timestamp: Unix timestamp when event occurred
            state: State name ('awake', 'tired', 'sleep')
            duration: Duration in danger state (seconds)
            alert_triggered: Whether alert was triggered
        """
        self.timestamp = timestamp
        self.state = state
        self.duration = duration
        self.alert_triggered = alert_triggered
        self.datetime = datetime.fromtimestamp(timestamp)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'time': self.datetime.strftime('%H:%M:%S'),
            'state': self.state,
            'duration': f"{self.duration:.1f}s",
            'alert': 'YES' if self.alert_triggered else 'No'
        }


class SessionManager:
    """Manages session statistics and alert history."""
    
    def __init__(self):
        """Initialize session manager."""
        self.start_time: Optional[float] = None
        self.alert_history: List[AlertEvent] = []
        self.total_alerts = 0
        self.current_session_active = False
        
        # Statistics
        self.time_awake = 0.0
        self.time_tired = 0.0
        self.time_sleep = 0.0
        self.last_update_time: Optional[float] = None
        self.last_state: Optional[int] = None
    
    def start_session(self):
        """Start a new session."""
        self.start_time = time.time()
        self.alert_history = []
        self.total_alerts = 0
        self.current_session_active = True
        self.time_awake = 0.0
        self.time_tired = 0.0
        self.time_sleep = 0.0
        self.last_update_time = time.time()
        self.last_state = None
    
    def stop_session(self):
        """Stop the current session."""
        self.current_session_active = False
        self._update_state_time()
    
    def add_alert(self, state_id: int, duration: float, alert_triggered: bool):
        """Add an alert event to history.
        
        Args:
            state_id: State class ID (0=awake, 1=sleep, 2=tired)
            duration: Duration in danger state
            alert_triggered: Whether alert threshold was exceeded
        """
        state_name = CLASS_NAMES.get(state_id, 'unknown')
        event = AlertEvent(time.time(), state_name, duration, alert_triggered)
        self.alert_history.append(event)
        
        if alert_triggered:
            self.total_alerts += 1
    
    def update_state(self, state_id: Optional[int]):
        """Update state timing statistics.
        
        Args:
            state_id: Current state ID (0=awake, 1=sleep, 2=tired, None=no detection)
        """
        if not self.current_session_active:
            return
        
        self._update_state_time()
        self.last_state = state_id
        self.last_update_time = time.time()
    
    def _update_state_time(self):
        """Update time spent in current state."""
        if self.last_update_time is None or self.last_state is None:
            return
        
        elapsed = time.time() - self.last_update_time
        
        if self.last_state == 0:  # awake
            self.time_awake += elapsed
        elif self.last_state == 1:  # sleep
            self.time_sleep += elapsed
        elif self.last_state == 2:  # tired
            self.time_tired += elapsed
    
    def get_session_duration(self) -> float:
        """Get total session duration in seconds.
        
        Returns:
            Duration in seconds, or 0 if no active session
        """
        if self.start_time is None:
            return 0.0
        
        if self.current_session_active:
            return time.time() - self.start_time
        else:
            return self.last_update_time - self.start_time if self.last_update_time else 0.0
    
    def get_formatted_duration(self) -> str:
        """Get formatted session duration as HH:MM:SS.
        
        Returns:
            Formatted duration string
        """
        duration = self.get_session_duration()
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_alert_history(self) -> List[Dict]:
        """Get alert history as list of dictionaries.
        
        Returns:
            List of alert event dictionaries
        """
        return [event.to_dict() for event in self.alert_history]
    
    def get_statistics(self) -> Dict:
        """Get session statistics.
        
        Returns:
            Dictionary with session statistics
        """
        self._update_state_time()
        
        total_time = self.get_session_duration()
        
        return {
            'total_duration': self.get_formatted_duration(),
            'total_alerts': self.total_alerts,
            'time_awake': self.time_awake,
            'time_tired': self.time_tired,
            'time_sleep': self.time_sleep,
            'awake_percentage': (self.time_awake / total_time * 100) if total_time > 0 else 0,
            'tired_percentage': (self.time_tired / total_time * 100) if total_time > 0 else 0,
            'sleep_percentage': (self.time_sleep / total_time * 100) if total_time > 0 else 0,
        }
    
    def export_to_csv(self, filepath: Optional[Path] = None) -> Path:
        """Export session data to CSV file.
        
        Args:
            filepath: Optional custom filepath. If None, uses default naming
            
        Returns:
            Path to created CSV file
        """
        if filepath is None:
            # Create logs directory if it doesn't exist
            SESSION_LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            filename = datetime.now().strftime(SESSION_LOG_FORMAT)
            filepath = SESSION_LOG_DIRECTORY / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Session Summary'])
            writer.writerow(['Total Duration', self.get_formatted_duration()])
            writer.writerow(['Total Alerts', self.total_alerts])
            writer.writerow([])
            
            # Write alert history
            writer.writerow(['Time', 'State', 'Duration', 'Alert Triggered'])
            for event in self.alert_history:
                data = event.to_dict()
                writer.writerow([data['time'], data['state'], data['duration'], data['alert']])
        
        return filepath
