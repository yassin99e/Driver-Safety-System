"""Status panel widget for displaying live detection status."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QGroupBox
from PyQt6.QtCore import Qt
from src.config import (
    GUI_COLOR_AWAKE, GUI_COLOR_TIRED, GUI_COLOR_SLEEP,
    GUI_COLOR_SAFE, GUI_COLOR_DANGER, GUI_COLOR_WARNING,
    ALERT_THRESHOLD_SECONDS, CLASS_NAMES
)


class StatusPanel(QWidget):
    """Panel for displaying live detection status."""
    
    def __init__(self):
        """Initialize status panel."""
        super().__init__()
        self.current_state = None
        self.confidence = 0.0
        self.danger_time = 0.0
        self.alert_triggered = False
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Group box
        group_box = QGroupBox("Live Status")
        group_box.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        group_layout = QVBoxLayout()
        
        # Current state display
        state_layout = QHBoxLayout()
        state_label = QLabel("Current State:")
        state_label.setStyleSheet("font-size: 13px; color: #ffffff;")
        
        self.state_value = QLabel("WAITING...")
        self.state_value.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #888888;
            padding: 5px 10px;
            border-radius: 3px;
            background-color: #2a2a2a;
        """)
        self.state_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        state_layout.addWidget(state_label)
        state_layout.addWidget(self.state_value, 1)
        
        # Confidence display
        conf_layout = QHBoxLayout()
        conf_label = QLabel("Confidence:")
        conf_label.setStyleSheet("font-size: 13px; color: #ffffff;")
        
        self.conf_value = QLabel("0%")
        self.conf_value.setStyleSheet("font-size: 14px; color: #ffffff; font-weight: bold;")
        self.conf_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        conf_layout.addWidget(conf_label)
        conf_layout.addWidget(self.conf_value, 1)
        
        # Danger timer
        timer_layout = QVBoxLayout()
        timer_label = QLabel("Danger Timer:")
        timer_label.setStyleSheet("font-size: 13px; color: #ffffff;")
        
        self.timer_value = QLabel("0.0s / 3.0s")
        self.timer_value.setStyleSheet("font-size: 14px; color: #ffffff; font-weight: bold;")
        self.timer_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(int(ALERT_THRESHOLD_SECONDS * 10))  # Use tenths of seconds
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 5px;
                background-color: #2a2a2a;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        
        timer_layout.addWidget(timer_label)
        timer_layout.addWidget(self.timer_value)
        timer_layout.addWidget(self.progress_bar)
        
        # Alert status
        self.alert_label = QLabel("")
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alert_label.setMinimumHeight(40)
        self.alert_label.hide()
        
        # Add all to group layout
        group_layout.addLayout(state_layout)
        group_layout.addLayout(conf_layout)
        group_layout.addLayout(timer_layout)
        group_layout.addWidget(self.alert_label)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        self.setLayout(layout)
    
    def update_status(self, state_id: int, confidence: float, danger_time: float, alert_triggered: bool):
        """Update status display.
        
        Args:
            state_id: Detected state (0=awake, 1=sleep, 2=tired)
            confidence: Detection confidence (0-1)
            danger_time: Time in danger state (seconds)
            alert_triggered: Whether alert threshold exceeded
        """
        self.current_state = state_id
        self.confidence = confidence
        self.danger_time = danger_time
        self.alert_triggered = alert_triggered
        
        # Update state display
        state_name = CLASS_NAMES.get(state_id, 'unknown').upper()
        self.state_value.setText(state_name)
        
        # Update state color
        if state_id == 0:  # awake
            color = GUI_COLOR_AWAKE
        elif state_id == 1:  # sleep
            color = GUI_COLOR_SLEEP
        elif state_id == 2:  # tired
            color = GUI_COLOR_TIRED
        else:
            color = "#888888"
        
        self.state_value.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {color};
            padding: 5px 10px;
            border-radius: 3px;
            background-color: #2a2a2a;
        """)
        
        # Update confidence
        self.conf_value.setText(f"{confidence * 100:.1f}%")
        
        # Update danger timer
        self.timer_value.setText(f"{danger_time:.1f}s / {ALERT_THRESHOLD_SECONDS:.1f}s")
        
        # Update progress bar
        progress_value = int(danger_time * 10)  # Convert to tenths
        self.progress_bar.setValue(min(progress_value, self.progress_bar.maximum()))
        
        # Update progress bar color based on danger level
        if danger_time > ALERT_THRESHOLD_SECONDS:
            chunk_color = GUI_COLOR_DANGER
        elif danger_time > ALERT_THRESHOLD_SECONDS * 0.7:
            chunk_color = GUI_COLOR_WARNING
        else:
            chunk_color = GUI_COLOR_SAFE
        
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #555555;
                border-radius: 5px;
                background-color: #2a2a2a;
                height: 25px;
            }}
            QProgressBar::chunk {{
                background-color: {chunk_color};
                border-radius: 3px;
            }}
        """)
        
        # Update alert status
        if alert_triggered:
            if state_id == 1:  # sleep
                self.alert_label.setText("⚠️ ALERT: DRIVER SLEEPING!")
                self.alert_label.setStyleSheet(f"""
                    background-color: {GUI_COLOR_SLEEP};
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                """)
            elif state_id == 2:  # tired
                self.alert_label.setText("⚠️ ALERT: DRIVER TIRED!")
                self.alert_label.setStyleSheet(f"""
                    background-color: {GUI_COLOR_TIRED};
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                """)
            self.alert_label.show()
        else:
            self.alert_label.hide()
    
    def reset(self):
        """Reset status display."""
        self.state_value.setText("WAITING...")
        self.state_value.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #888888;
            padding: 5px 10px;
            border-radius: 3px;
            background-color: #2a2a2a;
        """)
        self.conf_value.setText("0%")
        self.timer_value.setText(f"0.0s / {ALERT_THRESHOLD_SECONDS:.1f}s")
        self.progress_bar.setValue(0)
        self.alert_label.hide()
