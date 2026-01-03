"""
Driver Safety System - PyQt GUI Application

A real-time drowsiness detection system with modern GUI interface.
This application uses YOLOv8 for detecting driver states (awake/tired/sleep)
and provides visual alerts and session tracking.

Author: Yassine Ben Akki
Institution: ENSA Oujda
Year: 2025-2026
"""

import sys
import os

# CRITICAL FIX for Windows DLL loading issue:
# Force torch to load BEFORE PyQt6 to avoid DLL conflicts
# This must happen before any GUI imports
try:
    import torch
    _ = torch.tensor([1.0])  # Initialize torch to load all DLLs
except Exception as e:
    print(f"Warning: Could not pre-load torch: {e}")

# Add DLL directory to PATH for Windows (helps with missing dependencies)
if sys.platform == "win32":
    torch_lib_path = os.path.join(os.path.dirname(torch.__file__), "lib")
    if os.path.exists(torch_lib_path):
        os.add_dll_directory(torch_lib_path)

from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow


def main():
    """Main entry point for the GUI application."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Driver Safety System")
    app.setOrganizationName("ENSA Oujda")
    
    # Set application-wide stylesheet for dark theme
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
