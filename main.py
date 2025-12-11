import cv2
import sys
from src.config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
from src.detector import DrowsinessDetector
from src.logic import DrowsinessLogic
from src.alerter import AudioAlerter
from src.visualizer import Visualizer


def main():
    """Main application loop."""
    print("Initializing Driver Drowsiness Detection System...")
    
    # Initialize components
    try:
        detector = DrowsinessDetector()
        logic = DrowsinessLogic()
        alerter = AudioAlerter()
        visualizer = Visualizer()
        print("✓ All components initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing components: {e}")
        return
    
    # Initialize camera
    print(f"Opening camera {CAMERA_INDEX}...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print("✗ Error: Could not open camera")
        return
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    print("✓ Camera opened successfully")
    
    print("\nStarting detection... Press 'q' to quit\n")
    
    try:
        while True:
            # Capture frame
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to grab frame")
                break
            
            # Run detection
            class_id, confidence, bbox = detector.detect(frame)
            
            # Update logic
            should_alert, alert_type, elapsed_time = logic.update(class_id)
            
            # Trigger alert if needed
            if should_alert:
                print(f"⚠ ALERT TRIGGERED: {alert_type.upper()}!")
                alerter.play_alert(alert_type)
            
            # Get status for visualization
            status = logic.get_status()
            
            # Visualize
            if class_id is not None:
                frame = visualizer.draw_detection(frame, class_id, confidence, bbox)
            
            if status['alert_triggered']:
                frame = visualizer.draw_alert(frame, alert_type)
            
            frame = visualizer.draw_status(frame, status['elapsed_time'], status['is_danger'])
            
            # Display frame
            visualizer.show_frame(frame)
            
            # Check for quit command
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nQuitting...")
                break
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError during execution: {e}")
    finally:
        # Cleanup
        print("Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
        alerter.cleanup()
        print("✓ Cleanup complete")


if __name__ == "__main__":
    main()
