import sys
import time
import cv2
import winsound
from detector import HelmetDetector
from utils.logger import ViolationLogger

def main():
    print("=" * 70)
    print("      AI HELMETGUARD - REAL-TIME DESKTOP WEBCAM SURVEILLANCE         ")
    print("=" * 70)
    print("  Controls:")
    print("    [Q] / [ESC] : Quit application")
    print("    [S]         : Manually save high-res evidence snapshot")
    print("    [+] / [-]   : Increase / Decrease confidence threshold")
    print("    [V]         : Toggle vehicle bounding boxes")
    print("=" * 70)

    detector = HelmetDetector(conf_thresh=0.35)
    logger = ViolationLogger()
    
    # Try default camera index 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("[!] Trying default DirectShow failed, trying standard index 0...")
        cap = cv2.VideoCapture(0)
        
    if not cap.isOpened():
        print("[ERROR] Could not open webcam (Device Index 0). Please ensure your camera is plugged in and not used by another app.")
        input("Press Enter to exit...")
        return

    # Set camera resolution to 1280x720 or 640x480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    cv2.namedWindow("AI HelmetGuard - Live Traffic Safety Monitor", cv2.WINDOW_NORMAL)
    
    prev_time = time.time()
    show_vehicles = True
    last_beep_time = 0

    print("[AI HelmetGuard] Live Camera Feed Started. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Warning] Could not read frame from webcam.")
            break
            
        current_time = time.time()
        fps = 1.0 / (current_time - prev_time) if (current_time - prev_time) > 0 else 30.0
        prev_time = current_time
        
        # Run detection
        annotated_frame, dets, stats, has_alert = detector.detect(
            frame,
            show_vehicles=show_vehicles
        )
        stats['fps'] = fps
        
        # Audio Alert & Auto-Logging on violation
        if has_alert:
            # Sound buzzer beep (non-blocking gap)
            if (current_time - last_beep_time) > 1.5:
                try:
                    winsound.Beep(1000, 180) # 1000Hz for 180ms
                    last_beep_time = current_time
                except Exception:
                    pass
                    
            for d in dets:
                if d["is_violation"]:
                    logger.log_violation(frame, d["bbox"], confidence=d["confidence"])
                    
        # Redraw HUD with updated live FPS
        annotated_frame = detector.helmet_model and annotated_frame # keeps frame
        
        # Display window
        cv2.imshow("AI HelmetGuard - Live Traffic Safety Monitor", annotated_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), ord('Q'), 27): # 'q' or ESC
            break
        elif key in (ord('s'), ord('S')):
            snap_name = f"manual_snapshot_{int(time.time())}.jpg"
            cv2.imwrite(f"snapshots/{snap_name}", annotated_frame)
            print(f"[Evidence Saved] Saved screenshot to snapshots/{snap_name}")
        elif key == ord('+') or key == ord('='):
            detector.conf_thresh = min(0.95, detector.conf_thresh + 0.05)
            print(f"[Setting] Confidence Threshold increased to: {detector.conf_thresh:.2f}")
        elif key == ord('-') or key == ord('_'):
            detector.conf_thresh = max(0.10, detector.conf_thresh - 0.05)
            print(f"[Setting] Confidence Threshold decreased to: {detector.conf_thresh:.2f}")
        elif key in (ord('v'), ord('V')):
            show_vehicles = not show_vehicles
            print(f"[Setting] Show Vehicles toggled: {show_vehicles}")

    cap.release()
    cv2.destroyAllWindows()
    print("[AI HelmetGuard] Application closed successfully.")

if __name__ == "__main__":
    main()
