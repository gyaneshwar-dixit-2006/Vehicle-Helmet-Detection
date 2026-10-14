import os
import cv2
import numpy as np
from ultralytics import YOLO
from utils.visualizer import draw_detection_box, draw_hud

class HelmetDetector:
    def __init__(self, helmet_weights="weights/helmet_model.pt", base_weights="yolov8n.pt", conf_thresh=0.30, iou_thresh=0.45):
        """
        AI HelmetGuard: Intelligent Dual-Engine Traffic Safety Detector.
        """
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        self.helmet_weights = helmet_weights
        self.base_weights = base_weights
        
        # Load dedicated Helmet model if available
        self.helmet_model = None
        if os.path.exists(helmet_weights):
            try:
                print(f"[AI HelmetGuard] Loading Dedicated Helmet Weights from {helmet_weights}...")
                self.helmet_model = YOLO(helmet_weights)
            except Exception as e:
                print(f"[Warning] Could not load dedicated helmet model: {e}")
                
        # Load base YOLOv8 model for general context & vehicle tracking
        print(f"[AI HelmetGuard] Loading Base YOLOv8 Model ({base_weights})...")
        self.base_model = YOLO(base_weights)

    def _analyze_head_roi(self, head_crop):
        """
        Computer Vision Color, Texture, Edge Curvature & Facial analyzer for head region.
        """
        if head_crop is None or head_crop.shape[0] < 12 or head_crop.shape[1] < 12:
            return False, 0.50

        h, w = head_crop.shape[:2]
        hsv = cv2.cvtColor(head_crop, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(head_crop, cv2.COLOR_BGR2YCrCb)
        gray = cv2.cvtColor(head_crop, cv2.COLOR_BGR2GRAY)
        
        crown_h = max(8, int(h * 0.60))
        crown_hsv = hsv[0:crown_h, :]
        crown_gray = gray[0:crown_h, :]
        
        # Hair detection mask (Low V, Low S dark crown)
        lower_hair = np.array([0, 0, 0], dtype=np.uint8)
        upper_hair = np.array([180, 255, 60], dtype=np.uint8)
        hair_mask = cv2.inRange(crown_hsv, lower_hair, upper_hair)
        hair_ratio = np.sum(hair_mask > 0) / (crown_h * w)
        
        # High Saturation / Helmet color shell detection (Yellow, Red, Blue, White, Glossy)
        v_channel = crown_hsv[:, :, 2]
        s_channel = crown_hsv[:, :, 1]
        helmet_color_mask = ((s_channel > 65) & (v_channel > 70)) | ((s_channel < 40) & (v_channel > 185))
        helmet_color_ratio = np.sum(helmet_color_mask > 0) / (crown_h * w)
        
        # Laplacian texture variance (Helmets are smooth, Hair is high-frequency)
        laplacian_var = cv2.Laplacian(crown_gray, cv2.CV_64F).var()
        
        score = 0.50
        if helmet_color_ratio > 0.30:
            score += 0.30
        elif helmet_color_ratio > 0.15:
            score += 0.15
            
        if hair_ratio > 0.40:
            score -= 0.30
        elif hair_ratio > 0.20:
            score -= 0.15
            
        if laplacian_var < 180:
            score += 0.15
        elif laplacian_var > 450:
            score -= 0.15
            
        score = max(0.10, min(0.95, score))
        is_helmet = (score >= 0.50)
        confidence = score if is_helmet else (1.0 - score)
        return is_helmet, confidence

    def detect(self, frame, custom_conf=None, filter_mode="all", show_vehicles=True, detect_triple_riding=True):
        """
        Runs complete AI detection on a frame (BGR image).
        """
        if frame is None or frame.size == 0:
            return None, [], {}, False
            
        conf = custom_conf if custom_conf is not None else self.conf_thresh
        h, w = frame.shape[:2]
        annotated_frame = frame.copy()
        
        detections = []
        compliant_count = 0
        violation_count = 0
        
        # 1. Run Dedicated Helmet Model first if present
        helmet_boxes = []
        if self.helmet_model:
            try:
                res_helmet = self.helmet_model(frame, conf=conf, iou=self.iou_thresh, verbose=False)[0]
                for box in res_helmet.boxes:
                    cls_id = int(box.cls[0])
                    conf_val = float(box.conf[0])
                    xyxy = [int(v) for v in box.xyxy[0].cpu().numpy().tolist()]
                    
                    # 0: Hardhat/Helmet, 1: NO-Hardhat/No Helmet
                    cls_name = self.helmet_model.names.get(cls_id, str(cls_id)).lower()
                    is_vio = ("no" in cls_name or "without" in cls_name or cls_id == 1)
                    helmet_boxes.append({
                        "bbox": xyxy,
                        "is_violation": is_vio,
                        "confidence": conf_val,
                        "label": "NO HELMET (VIOLATION)" if is_vio else "WITH HELMET"
                    })
            except Exception as e:
                print(f"[Error in Helmet Model]: {e}")
                
        # 2. Run Base Model for Persons & Motorcycles
        res_base = self.base_model(frame, conf=conf, iou=self.iou_thresh, verbose=False)[0]
        persons = []
        motorcycles = []
        
        for box in res_base.boxes:
            cls_id = int(box.cls[0])
            conf_val = float(box.conf[0])
            xyxy = [int(v) for v in box.xyxy[0].cpu().numpy().tolist()]
            
            if cls_id == 0: # Person
                persons.append({"bbox": xyxy, "conf": conf_val})
            elif cls_id in (3, 1): # Motorcycle / Bicycle
                motorcycles.append({"bbox": xyxy, "conf": conf_val})

        # Draw vehicle boxes if enabled
        if show_vehicles:
            for idx, bike in enumerate(motorcycles):
                bx1, by1, bx2, by2 = bike["bbox"]
                draw_detection_box(
                    annotated_frame,
                    bbox=[bx1, by1, bx2, by2],
                    label=f"VEHICLE #{idx+1}",
                    score=bike["conf"],
                    is_vehicle=True
                )

        # 3. If direct helmet model gave detections, use them
        if len(helmet_boxes) > 0:
            for item in helmet_boxes:
                x1, y1, x2, y2 = item["bbox"]
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                if (x2 - x1) < 8 or (y2 - y1) < 8:
                    continue
                    
                is_vio = item["is_violation"]
                if is_vio:
                    violation_count += 1
                else:
                    compliant_count += 1
                    
                if filter_mode == "violations_only" and not is_vio:
                    continue
                if filter_mode == "compliant_only" and is_vio:
                    continue
                    
                draw_detection_box(
                    annotated_frame,
                    bbox=[x1, y1, x2, y2],
                    label=item["label"],
                    score=item["confidence"],
                    is_violation=is_vio
                )
                
                crop = frame[y1:y2, x1:x2].copy()
                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "label": item["label"],
                    "is_violation": is_vio,
                    "confidence": item["confidence"],
                    "crop": crop
                })
        else:
            # Fallback to Person Head-ROI analysis
            for p in persons:
                px1, py1, px2, py2 = p["bbox"]
                px1, py1 = max(0, px1), max(0, py1)
                px2, py2 = min(w, px2), min(h, py2)
                
                pw = px2 - px1
                ph = py2 - py1
                if pw < 15 or ph < 20:
                    continue
                    
                head_h = max(15, int(ph * 0.28))
                head_y2 = min(h, py1 + head_h)
                head_crop = frame[py1:head_y2, px1:px2]
                
                has_helmet, conf_score = self._analyze_head_roi(head_crop)
                is_vio = not has_helmet
                label = "WITH HELMET" if has_helmet else "NO HELMET (VIOLATION)"
                
                if is_vio:
                    violation_count += 1
                else:
                    compliant_count += 1
                    
                if filter_mode == "violations_only" and not is_vio:
                    continue
                if filter_mode == "compliant_only" and is_vio:
                    continue
                    
                draw_detection_box(
                    annotated_frame,
                    bbox=[px1, py1, px2, head_y2],
                    label=label,
                    score=conf_score,
                    is_violation=is_vio
                )
                
                crop = frame[py1:head_y2, px1:px2].copy()
                detections.append({
                    "bbox": [px1, py1, px2, head_y2],
                    "label": label,
                    "is_violation": is_vio,
                    "confidence": conf_score,
                    "crop": crop
                })

        # 4. Check for Triple Riding / Overcrowded motorcycle hazard
        if detect_triple_riding and len(motorcycles) > 0 and len(persons) >= 3:
            for bike in motorcycles:
                bx1, by1, bx2, by2 = bike["bbox"]
                riders_on_bike = 0
                for p in persons:
                    px1, py1, px2, py2 = p["bbox"]
                    if (px1 < bx2 and px2 > bx1) and (py2 > by1 - 50):
                        riders_on_bike += 1
                if riders_on_bike >= 3:
                    violation_count += 1
                    draw_detection_box(
                        annotated_frame,
                        bbox=bike["bbox"],
                        label="HAZARD: TRIPLE RIDING",
                        score=0.95,
                        is_violation=True
                    )
                    detections.append({
                        "bbox": bike["bbox"],
                        "label": "HAZARD: TRIPLE RIDING",
                        "is_violation": True,
                        "confidence": 0.95,
                        "crop": frame[max(0, by1):min(h, by2), max(0, bx1):min(w, bx2)]
                    })

        total_tracked = compliant_count + violation_count
        compliance_rate = (compliant_count / total_tracked * 100.0) if total_tracked > 0 else 100.0
        has_alert = (violation_count > 0)
        
        stats = {
            "total_riders": total_tracked,
            "compliant": compliant_count,
            "violations": violation_count,
            "compliance_rate": compliance_rate,
            "fps": 0.0
        }
        
        annotated_frame = draw_hud(annotated_frame, stats=stats, alert=has_alert)
        return annotated_frame, detections, stats, has_alert
