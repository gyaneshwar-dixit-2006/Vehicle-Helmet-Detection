import os
import time
import random
from datetime import datetime
import pandas as pd
import cv2

class ViolationLogger:
    def __init__(self, log_dir="snapshots", log_file="violations_log.csv"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.columns = [
            "Challan_ID",
            "Timestamp",
            "License_Plate",
            "Violation_Type",
            "Confidence",
            "Fine_Amount",
            "Status",
            "Snapshot_File"
        ]
        
        if os.path.exists(self.log_file):
            try:
                self.df = pd.read_csv(self.log_file)
                # Ensure all columns exist
                for col in self.columns:
                    if col not in self.df.columns:
                        self.df[col] = ""
            except Exception:
                self.df = pd.DataFrame(columns=self.columns)
        else:
            self.df = pd.DataFrame(columns=self.columns)
            self._save_df()
            
        self.last_log_times = {}
        self.cooldown_seconds = 2.0

    def _save_df(self):
        self.df.to_csv(self.log_file, index=False)

    def _generate_license_plate(self):
        """Generates a realistic simulated license plate number."""
        states = ["DL", "MH", "KA", "TN", "UP", "HR", "GJ", "WB", "TS"]
        state = random.choice(states)
        district = f"{random.randint(1, 14):02d}"
        letters = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ", k=2))
        number = f"{random.randint(1000, 9999)}"
        return f"{state}-{district}-{letters}-{number}"

    def log_violation(self, frame, bbox, confidence=0.85, violation_type="No Helmet Violation", rider_id=None, license_plate=None):
        """
        Logs a violation, creates an annotated evidence snapshot with header,
        generates an official E-Challan record, and returns the metadata.
        """
        now = time.time()
        track_key = rider_id if rider_id is not None else "gen"
        
        if track_key in self.last_log_times and (now - self.last_log_times[track_key]) < self.cooldown_seconds:
            return None
        
        self.last_log_times[track_key] = now
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
        challan_id = f"CHAL-{file_ts[-6:]}"
        snapshot_name = f"violation_{file_ts}.jpg"
        snapshot_path = os.path.join(self.log_dir, snapshot_name)
        
        plate = license_plate if license_plate else self._generate_license_plate()
        fine_amount = "₹1,000" if "Triple" not in violation_type else "₹2,500"
        
        # Crop violator image with safety margin
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = bbox
        pad_x = int((x2 - x1) * 0.20)
        pad_y = int((y2 - y1) * 0.20)
        
        crop_x1 = max(0, x1 - pad_x)
        crop_y1 = max(0, y1 - pad_y)
        crop_x2 = min(w, x2 + pad_x)
        crop_y2 = min(h, y2 + pad_y)
        
        crop_img = frame[crop_y1:crop_y2, crop_x1:crop_x2].copy()
        
        # Overlay evidence header
        if crop_img.shape[0] > 15 and crop_img.shape[1] > 15:
            header_h = 42
            overlay = cv2.copyMakeBorder(crop_img, header_h, 0, 0, 0, cv2.BORDER_CONSTANT, value=(20, 20, 200))
            cv2.putText(overlay, f"TRAFFIC POLICE EVIDENCE | {timestamp_str}", (10, 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(overlay, f"OFFENSE: {violation_type.upper()} | VEHICLE: {plate}", (10, 34),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.imwrite(snapshot_path, overlay)
        else:
            cv2.imwrite(snapshot_path, frame)
            
        new_entry = {
            "Challan_ID": challan_id,
            "Timestamp": timestamp_str,
            "License_Plate": plate,
            "Violation_Type": violation_type,
            "Confidence": f"{confidence * 100:.1f}%",
            "Fine_Amount": fine_amount,
            "Status": "PAYMENT PENDING",
            "Snapshot_File": snapshot_name
        }
        
        self.df = pd.concat([self.df, pd.DataFrame([new_entry])], ignore_index=True)
        self._save_df()
        
        return {
            "id": challan_id,
            "timestamp": timestamp_str,
            "plate": plate,
            "type": violation_type,
            "confidence": confidence,
            "fine": fine_amount,
            "status": "PAYMENT PENDING",
            "snapshot_path": snapshot_path,
            "snapshot_name": snapshot_name
        }

    def get_recent_violations(self, limit=12):
        return self.df.tail(limit).to_dict(orient="records")

    def get_total_violations(self):
        return len(self.df)

    def clear_logs(self):
        self.df = pd.DataFrame(columns=self.columns)
        self._save_df()
