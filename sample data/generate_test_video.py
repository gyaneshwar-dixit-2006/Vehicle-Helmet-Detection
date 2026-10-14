import os
import cv2
import numpy as np

def create_demo_traffic_video(output_path="sample_data/demo_traffic.mp4", duration_sec=8, fps=25):
    """
    Generates a high-quality traffic video stream with riders passing by
    (both compliant with helmet and violators without helmet).
    """
    sample_dir = os.path.dirname(output_path)
    os.makedirs(sample_dir, exist_ok=True)
    
    w, h = 854, 480
    total_frames = duration_sec * fps
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    
    print(f"Rendering demo traffic video ({total_frames} frames)...")
    
    for i in range(total_frames):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        # Background: Sky & horizon
        frame[0:200] = (175, 160, 150)
        # Trees/city outline
        cv2.rectangle(frame, (0, 160), (w, 200), (90, 110, 80), -1)
        # Road
        frame[200:] = (48, 48, 52)
        
        # Lane markings (moving with offset)
        offset = (i * 12) % 100
        for x in range(-100 + offset, w + 100, 100):
            cv2.rectangle(frame, (x, 340), (x + 50, 350), (240, 240, 240), -1)
            
        # Rider 1: Compliant (Yellow Helmet) moving left to right
        r1_x = int(-100 + (i * 5.5))
        r1_y = 270
        if -80 < r1_x < w + 80:
            # Bike body
            cv2.circle(frame, (r1_x - 35, r1_y + 110), 28, (20, 20, 20), 6)
            cv2.circle(frame, (r1_x + 45, r1_y + 110), 28, (20, 20, 20), 6)
            cv2.rectangle(frame, (r1_x - 30, r1_y + 75), (r1_x + 40, r1_y + 100), (220, 50, 30), -1)
            # Rider jacket
            cv2.rectangle(frame, (r1_x - 15, r1_y + 20), (r1_x + 20, r1_y + 80), (60, 60, 180), -1)
            # Helmet (Bright Yellow shell)
            cv2.ellipse(frame, (r1_x + 2, r1_y), (18, 22), 0, 0, 360, (0, 215, 255), -1)
            cv2.rectangle(frame, (r1_x - 4, r1_y + 4), (r1_x + 14, r1_y + 12), (20, 20, 20), -1)
            
        # Rider 2: Violator (NO HELMET) entering from frame 60 onwards
        if i >= 40:
            r2_x = int(w + 80 - ((i - 40) * 6.5))
            r2_y = 240
            if -80 < r2_x < w + 80:
                # Bike body
                cv2.circle(frame, (r2_x - 30, r2_y + 100), 26, (20, 20, 20), 6)
                cv2.circle(frame, (r2_x + 40, r2_y + 100), 26, (20, 20, 20), 6)
                cv2.rectangle(frame, (r2_x - 25, r2_y + 70), (r2_x + 35, r2_y + 90), (30, 150, 40), -1)
                # Rider body
                cv2.rectangle(frame, (r2_x - 12, r2_y + 15), (r2_x + 18, r2_y + 75), (40, 100, 210), -1)
                # Head: Skin tone + Bare Hair (No Helmet)
                cv2.ellipse(frame, (r2_x + 3, r2_y), (16, 20), 0, 0, 360, (140, 180, 225), -1)
                cv2.ellipse(frame, (r2_x + 3, r2_y - 8), (16, 10), 0, 180, 360, (20, 15, 15), -1)

        out.write(frame)
        
    out.release()
    print(f"Demo video saved to {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    create_demo_traffic_video()
