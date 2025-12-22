# Driver Drowsiness Detection System 🚗💤

A real-time driver drowsiness detection system using YOLOv8 and computer vision to enhance road safety by monitoring driver alertness and triggering audio alerts when signs of fatigue are detected.

## 📋 Informations du Projet

- **Author**: Yassine Ben Akki
- **Supervisor**: Prof. Kamal AZGHIOU
- **Institution**: ENSA Oujda
- **Academic Year**: 2025-2026


## 📋 Overview

This system uses a fine-tuned YOLOv8 model to detect three driver states:
- **Awake** - Driver is alert and focused
- **Tired** - Driver shows signs of fatigue
- **Sleep** - Driver is falling asleep

When the system detects continuous danger states (tired or sleeping) for 5 seconds, it triggers an audio alarm to alert the driver.

## ✨ Features

- **Real-time Detection**: Processes webcam feed in real-time using YOLOv8
- **Smart State Tracking**: Accumulates danger time across tired and sleep states
- **Audio Alerts**: Continuous alarm playback until driver returns to awake state
- **Visual Feedback**: 
  - Color-coded bounding boxes (Green/Orange/Red)
  - Alert banners ("ALERT: SLEEPING!" / "ALERT: TIRED!")
  - Real-time danger timer display
- **Modular Architecture**: Clean, maintainable code structure

## 🚀 How It Works

1. **Capture**: OpenCV captures video frames from webcam
2. **Detect**: Fine-tuned YOLOv8 model analyzes each frame
3. **Track**: Logic module accumulates time spent in danger states (tired/sleep)
4. **Alert**: After 5 seconds in danger state, triggers continuous audio alarm
5. **Reset**: Returns to monitoring when driver becomes awake again

### State Logic
- **Tired → Sleep**: Counter continues (both are danger states)
- **Sleep → Tired**: Counter continues (both are danger states)
- **Awake detected**: Counter resets, alarm stops

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Webcam

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yassin99e/Driver-Safety-System.git
cd Driver-Safety-System
```

2. **Create virtual environment** (recommended)
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 📦 Project Structure

```
driver_safety_system/
│
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
│
├── assets/
│   ├── models/
│   │   └── best-2.pt      # Fine-tuned YOLOv8 model weights
│   └── sounds/
│       ├── sleep.wav      # Sleep alert audio
│       └── tired.wav      # Tired alert audio
│
└── src/
    ├── __init__.py
    ├── config.py          # Configuration settings
    ├── detector.py        # YOLOv8 detection module
    ├── logic.py           # State tracking and alert logic
    ├── alerter.py         # Audio playback management
    └── visualizer.py      # OpenCV visualization
```

## 💻 Usage

Run the application:
```bash
python main.py
```

**Controls:**
- Press `q` to quit the application

**What you'll see:**
- Live webcam feed with detection bounding boxes
- Current state labels with confidence scores
- Danger timer (when in tired/sleep state)
- Alert banners when threshold exceeded
- Audio alarms playing continuously until awake

## ⚙️ Configuration

Edit `src/config.py` to customize:

```python
# Alert threshold (seconds)
ALERT_THRESHOLD_SECONDS = 5.0

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Detection confidence
CONFIDENCE_THRESHOLD = 0.5

# Colors and visualization
BOX_COLOR_AWAKE = (0, 255, 0)
BOX_COLOR_TIRED = (0, 165, 255)
BOX_COLOR_SLEEP = (0, 0, 255)
```

## 📊 Model Details

- **Framework**: YOLOv8 (Ultralytics)
- **Training**: Fine-tuned on custom drowsiness detection dataset
- **Classes**: 3 (awake, sleep, tired)
- **Model File**: `assets/models/best-2.pt`

## 📋 Requirements

- ultralytics>=8.0.0
- opencv-python>=4.8.0
- torch>=2.0.0
- torchvision>=0.15.0
- pygame>=2.5.0
- numpy>=1.24.0
- Pillow>=10.0.0

## 🎯 Use Cases

- Driver monitoring systems in vehicles
- Fleet management safety
- Research on driver attention and fatigue
- Educational demonstrations of computer vision applications

## ⚠️ Limitations

- Requires good lighting conditions
- Camera must have clear view of driver's face
- Performance depends on model accuracy
- Not a substitute for proper rest

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is open source and available for educational and research purposes.

## 📧 Contact

- **GitHub**: [@yassin99e](https://github.com/yassin99e)
- **Author**: Yassine Ben Akki
- **Email**: [yassine.benakki@ump.ac.ma](mailto:yassine.benakki@ump.ac.ma)
- **Institution**: ENSA Oujda
- **Academic Year**: 2025–2026

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- OpenCV community
- Dataset contributors

---

**⚡ Stay Alert, Stay Safe!** 


