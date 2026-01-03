"""Main window for Driver Safety System GUI."""
# CRITICAL: Import torch-dependent modules BEFORE PyQt6 to avoid DLL conflicts on Windows
from src.gui.video_thread import VideoThread
from src.gui.session_manager import SessionManager

# Now import PyQt6 after torch is loaded
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QMessageBox, QFileDialog, QDialog, QLabel, QSpinBox, 
    QPushButton, QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QCloseEvent
import numpy as np
from pathlib import Path

from src.config import (
    GUI_WINDOW_TITLE, GUI_WINDOW_WIDTH, GUI_WINDOW_HEIGHT,
    GUI_MIN_WIDTH, GUI_MIN_HEIGHT, GUI_BACKGROUND, CAMERA_INDEX,
    ALERT_THRESHOLD_SECONDS
)
from src.gui.widgets.video_widget import VideoWidget
from src.gui.widgets.control_panel import ControlPanel
from src.gui.widgets.status_panel import StatusPanel
from src.gui.widgets.session_panel import SessionPanel


class SettingsDialog(QDialog):
    """Dialog for adjusting application settings."""
    
    def __init__(self, parent=None, current_threshold=ALERT_THRESHOLD_SECONDS, current_camera=CAMERA_INDEX):
        """Initialize settings dialog."""
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(300)
        
        # Create form layout
        layout = QFormLayout()
        
        # Alert threshold setting
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setMinimum(1)
        self.threshold_spin.setMaximum(10)
        self.threshold_spin.setValue(int(current_threshold))
        self.threshold_spin.setSuffix(" seconds")
        layout.addRow("Alert Threshold:", self.threshold_spin)
        
        # Camera index setting
        self.camera_spin = QSpinBox()
        self.camera_spin.setMinimum(0)
        self.camera_spin.setMaximum(5)
        self.camera_spin.setValue(current_camera)
        layout.addRow("Camera Index:", self.camera_spin)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
        
        self.setLayout(layout)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QSpinBox {
                background-color: #34495E;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
            }
        """)
    
    def get_settings(self):
        """Get selected settings.
        
        Returns:
            tuple: (threshold_seconds, camera_index)
        """
        return self.threshold_spin.value(), self.camera_spin.value()


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        # Initialize components
        self.video_thread = None
        self.session_manager = SessionManager()
        self.current_camera_index = CAMERA_INDEX
        self.current_threshold = ALERT_THRESHOLD_SECONDS
        
        # Timer for updating session statistics
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_session_stats)
        self.stats_timer.setInterval(1000)  # Update every second
        
        # Track last alert to avoid duplicates
        self.last_alert_state = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle(GUI_WINDOW_TITLE)
        self.setMinimumSize(GUI_MIN_WIDTH, GUI_MIN_HEIGHT)
        self.resize(GUI_WINDOW_WIDTH, GUI_WINDOW_HEIGHT)
        
        # Apply dark theme
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {GUI_BACKGROUND};
            }}
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("🚗 Driver Safety System")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            padding: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Video widget
        self.video_widget = VideoWidget()
        
        # Control panel
        self.control_panel = ControlPanel()
        self.control_panel.start_clicked.connect(self.start_detection)
        self.control_panel.pause_clicked.connect(self.pause_detection)
        self.control_panel.stop_clicked.connect(self.stop_detection)
        self.control_panel.settings_clicked.connect(self.show_settings)
        
        # Bottom section - Status and Session panels side by side
        bottom_layout = QHBoxLayout()
        
        # Status panel
        self.status_panel = StatusPanel()
        
        # Session panel
        self.session_panel = SessionPanel()
        self.session_panel.export_requested.connect(self.export_session)
        
        bottom_layout.addWidget(self.status_panel, 1)
        bottom_layout.addWidget(self.session_panel, 1)
        
        # Add all to main layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.video_widget, 2)
        main_layout.addWidget(self.control_panel)
        main_layout.addLayout(bottom_layout, 1)
        
        central_widget.setLayout(main_layout)
    
    def start_detection(self):
        """Start video detection."""
        try:
            # Create and configure video thread
            self.video_thread = VideoThread(self.current_camera_index)
            self.video_thread.frame_ready.connect(self.update_video_frame)
            self.video_thread.detection_result.connect(self.handle_detection_result)
            self.video_thread.error_occurred.connect(self.handle_error)
            
            # Start session
            self.session_manager.start_session()
            self.stats_timer.start()
            
            # Reset displays
            self.status_panel.reset()
            self.session_panel.reset()
            self.last_alert_state = None
            
            # Start thread
            self.video_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start detection: {str(e)}")
            self.control_panel.reset()
    
    def pause_detection(self):
        """Pause or resume detection."""
        if self.video_thread is None:
            return
        
        if self.control_panel.is_paused:
            self.video_thread.pause()
            self.stats_timer.stop()
        else:
            self.video_thread.resume()
            self.stats_timer.start()
    
    def stop_detection(self):
        """Stop video detection."""
        if self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread = None
        
        self.stats_timer.stop()
        self.session_manager.stop_session()
        
        # Clear video display
        self.video_widget.clear_frame()
        
        # Update final stats
        self.update_session_stats()
    
    def update_video_frame(self, frame: np.ndarray):
        """Update video display with new frame.
        
        Args:
            frame: OpenCV frame
        """
        self.video_widget.update_frame(frame)
    
    def handle_detection_result(self, state_id: int, confidence: float, danger_time: float, alert_triggered: bool):
        """Handle detection result from video thread.
        
        Args:
            state_id: Detected state ID
            confidence: Detection confidence
            danger_time: Time in danger state
            alert_triggered: Whether alert was triggered
        """
        # Update status panel
        self.status_panel.update_status(state_id, confidence, danger_time, alert_triggered)
        
        # Update session manager
        self.session_manager.update_state(state_id)
        
        # Add to alert history if significant event
        if danger_time > 0.5:  # Only log events > 0.5 seconds
            # Avoid duplicate entries - only add if state changed or alert triggered
            current_key = (state_id, alert_triggered)
            if current_key != self.last_alert_state:
                self.session_manager.add_alert(state_id, danger_time, alert_triggered)
                
                # Update session panel with new alert
                history = self.session_manager.get_alert_history()
                if history:
                    self.session_panel.add_alert_to_history(history[-1])
                
                self.last_alert_state = current_key
    
    def update_session_stats(self):
        """Update session statistics display."""
        stats = self.session_manager.get_statistics()
        self.session_panel.update_statistics(
            stats['total_duration'],
            stats['total_alerts']
        )
    
    def handle_error(self, error_message: str):
        """Handle error from video thread.
        
        Args:
            error_message: Error message to display
        """
        QMessageBox.critical(self, "Error", error_message)
        self.stop_detection()
        self.control_panel.reset()
    
    def show_settings(self):
        """Show settings dialog."""
        dialog = SettingsDialog(self, self.current_threshold, self.current_camera_index)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            threshold, camera = dialog.get_settings()
            self.current_threshold = threshold
            self.current_camera_index = camera
            
            QMessageBox.information(
                self,
                "Settings Updated",
                f"Settings saved!\nAlert Threshold: {threshold}s\nCamera Index: {camera}\n\nChanges will take effect on next detection session."
            )
    
    def export_session(self):
        """Export session log to CSV file."""
        try:
            # Open file dialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Session Log",
                str(Path.home() / f"driver_session_{self.session_manager.start_time:.0f}.csv"),
                "CSV Files (*.csv)"
            )
            
            if file_path:
                # Export to CSV
                saved_path = self.session_manager.export_to_csv(Path(file_path))
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Session log exported to:\n{saved_path}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Failed to export session log:\n{str(e)}")
    
    def closeEvent(self, a0: QCloseEvent):
        """Handle window close event."""
        if self.video_thread is not None and self.video_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "Detection is still running. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.stop_detection()
                a0.accept()
            else:
                a0.ignore()
        else:
            a0.accept()
