"""Control panel widget with Start/Pause/Stop buttons."""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal


class ControlPanel(QWidget):
    """Control panel with action buttons."""
    
    # Signals
    start_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    
    def __init__(self):
        """Initialize control panel."""
        super().__init__()
        self.is_running = False
        self.is_paused = False
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Start button
        self.start_button = QPushButton("▶ START DETECTION")
        self.start_button.setMinimumHeight(50)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.start_button.clicked.connect(self._on_start_clicked)
        
        # Pause button
        self.pause_button = QPushButton("⏸ PAUSE")
        self.pause_button.setMinimumHeight(50)
        self.pause_button.setEnabled(False)
        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
            QPushButton:pressed {
                background-color: #cc7a00;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.pause_button.clicked.connect(self._on_pause_clicked)
        
        # Stop button
        self.stop_button = QPushButton("⏹ STOP")
        self.stop_button.setMinimumHeight(50)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #ba160a;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        
        # Settings button
        self.settings_button = QPushButton("⚙ SETTINGS")
        self.settings_button.setMinimumHeight(50)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
            QPushButton:pressed {
                background-color: #455A64;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.settings_button.clicked.connect(self.settings_clicked.emit)
        
        # Add buttons to layout
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(self.settings_button)
        
        self.setLayout(layout)
    
    def _on_start_clicked(self):
        """Handle start button click."""
        self.is_running = True
        self.is_paused = False
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.settings_button.setEnabled(False)
        self.start_clicked.emit()
    
    def _on_pause_clicked(self):
        """Handle pause button click."""
        if self.is_paused:
            # Resume
            self.is_paused = False
            self.pause_button.setText("⏸ PAUSE")
            self.pause_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #e68900;
                }
                QPushButton:pressed {
                    background-color: #cc7a00;
                }
            """)
        else:
            # Pause
            self.is_paused = True
            self.pause_button.setText("▶ RESUME")
            self.pause_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #0b7dda;
                }
                QPushButton:pressed {
                    background-color: #0a6bc2;
                }
            """)
        
        self.pause_clicked.emit()
    
    def _on_stop_clicked(self):
        """Handle stop button click."""
        self.is_running = False
        self.is_paused = False
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("⏸ PAUSE")
        self.stop_button.setEnabled(False)
        self.settings_button.setEnabled(True)
        self.stop_clicked.emit()
    
    def reset(self):
        """Reset control panel to initial state."""
        self._on_stop_clicked()
