"""Session panel widget with statistics and alert history."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QGroupBox, QHeaderView, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List, Dict


class SessionPanel(QWidget):
    """Panel for displaying session statistics and alert history."""
    
    # Signals
    export_requested = pyqtSignal()
    
    def __init__(self):
        """Initialize session panel."""
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Group box
        group_box = QGroupBox("Session Dashboard")
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
        
        # Statistics row
        stats_layout = QHBoxLayout()
        
        # Total time
        time_container = QVBoxLayout()
        time_label = QLabel("Total Time")
        time_label.setStyleSheet("font-size: 12px; color: #aaaaaa;")
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.time_value = QLabel("00:00:00")
        self.time_value.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #4CAF50;
        """)
        self.time_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        time_container.addWidget(time_label)
        time_container.addWidget(self.time_value)
        
        # Total alerts
        alert_container = QVBoxLayout()
        alert_label = QLabel("Total Alerts")
        alert_label.setStyleSheet("font-size: 12px; color: #aaaaaa;")
        alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.alert_value = QLabel("0")
        self.alert_value.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #F44336;
        """)
        self.alert_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        alert_container.addWidget(alert_label)
        alert_container.addWidget(self.alert_value)
        
        stats_layout.addLayout(time_container, 1)
        stats_layout.addLayout(alert_container, 1)
        
        # Alert history label
        history_label = QLabel("Alert History:")
        history_label.setStyleSheet("font-size: 13px; color: #ffffff; margin-top: 10px;")
        
        # Alert history table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Time", "State", "Duration", "Alert"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setMaximumHeight(200)
        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 3px;
                gridline-color: #444444;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #34495E;
                color: #ffffff;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Export button
        self.export_button = QPushButton("💾 EXPORT SESSION LOG")
        self.export_button.setMinimumHeight(35)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6bc2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.export_button.clicked.connect(self.export_requested.emit)
        self.export_button.setEnabled(False)
        
        # Add all to group layout
        group_layout.addLayout(stats_layout)
        group_layout.addWidget(history_label)
        group_layout.addWidget(self.history_table)
        group_layout.addWidget(self.export_button)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        self.setLayout(layout)
    
    def update_statistics(self, total_time: str, total_alerts: int):
        """Update session statistics.
        
        Args:
            total_time: Formatted time string (HH:MM:SS)
            total_alerts: Total number of alerts triggered
        """
        self.time_value.setText(total_time)
        self.alert_value.setText(str(total_alerts))
        
        # Enable export button if session has started
        if total_time != "00:00:00":
            self.export_button.setEnabled(True)
    
    def update_history(self, history: List[Dict]):
        """Update alert history table.
        
        Args:
            history: List of alert event dictionaries
        """
        self.history_table.setRowCount(len(history))
        
        for row, event in enumerate(history):
            # Time
            time_item = QTableWidgetItem(event['time'])
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 0, time_item)
            
            # State
            state_item = QTableWidgetItem(event['state'].upper())
            state_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Color code by state
            if event['state'] == 'sleep':
                state_item.setForeground(Qt.GlobalColor.red)
            elif event['state'] == 'tired':
                state_item.setForeground(Qt.GlobalColor.yellow)
            else:
                state_item.setForeground(Qt.GlobalColor.green)
            
            self.history_table.setItem(row, 1, state_item)
            
            # Duration
            duration_item = QTableWidgetItem(event['duration'])
            duration_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 2, duration_item)
            
            # Alert
            alert_item = QTableWidgetItem(event['alert'])
            alert_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            if event['alert'] == 'YES':
                alert_item.setForeground(Qt.GlobalColor.red)
                alert_item.setText("⚠️ YES")
            
            self.history_table.setItem(row, 3, alert_item)
        
        # Scroll to bottom to show latest alert
        self.history_table.scrollToBottom()
    
    def add_alert_to_history(self, event: Dict):
        """Add a single alert event to history table.
        
        Args:
            event: Alert event dictionary
        """
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        
        # Time
        time_item = QTableWidgetItem(event['time'])
        time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.history_table.setItem(row, 0, time_item)
        
        # State
        state_item = QTableWidgetItem(event['state'].upper())
        state_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Color code by state
        if event['state'] == 'sleep':
            state_item.setForeground(Qt.GlobalColor.red)
        elif event['state'] == 'tired':
            state_item.setForeground(Qt.GlobalColor.yellow)
        else:
            state_item.setForeground(Qt.GlobalColor.green)
        
        self.history_table.setItem(row, 1, state_item)
        
        # Duration
        duration_item = QTableWidgetItem(event['duration'])
        duration_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.history_table.setItem(row, 2, duration_item)
        
        # Alert
        alert_item = QTableWidgetItem(event['alert'])
        alert_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if event['alert'] == 'YES':
            alert_item.setForeground(Qt.GlobalColor.red)
            alert_item.setText("⚠️ YES")
        
        self.history_table.setItem(row, 3, alert_item)
        
        # Scroll to bottom
        self.history_table.scrollToBottom()
    
    def reset(self):
        """Reset session panel."""
        self.time_value.setText("00:00:00")
        self.alert_value.setText("0")
        self.history_table.setRowCount(0)
        self.export_button.setEnabled(False)
