import cv2
import numpy as np

# Futuristic Color Palette (BGR)
COLOR_HELMET = (46, 204, 113)     # Emerald Green
COLOR_NO_HELMET = (35, 35, 235)   # Vivid Red
COLOR_PILLION = (0, 140, 255)     # Deep Orange / Warning
COLOR_MOTORCYCLE = (235, 175, 40) # Bright Cyan / Sky Blue
COLOR_BG_DARK = (15, 20, 28)      # Slate Dark
COLOR_ALERT = (20, 20, 220)       # Flashing Red

def draw_hud(frame, stats=None, alert=False, show_title=True):
    """
    Draws a sleek, modern HUD status bar on the top and alert banner on the bottom.
    """
    h, w = frame.shape[:2]
    annotated = frame.copy()
    
    if show_title:
        # Top HUD Bar
        overlay = annotated.copy()
        cv2.rectangle(overlay, (0, 0), (w, 44), COLOR_BG_DARK, -1)
        cv2.addWeighted(overlay, 0.82, annotated, 0.18, 0, annotated)
        
        # System Title & Live Status Indicator
        status_dot_color = (0, 0, 255) if alert else (0, 255, 0)
        cv2.circle(annotated, (20, 22), 6, status_dot_color, -1)
        cv2.putText(annotated, "AI HELMETGUARD | SMART TRAFFIC SURVEILLANCE", (34, 27),
                    cv2.FONT_HERSHEY_DUPLEX, 0.58, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Stats on right
        if stats:
            fps_val = stats.get('fps', 0.0)
            compliant = stats.get('compliant', 0)
            violations = stats.get('violations', 0)
            rate = stats.get('compliance_rate', 100.0)
            
            stat_str = f"FPS: {fps_val:.1f}  |  Compliant: {compliant}  |  Violations: {violations}  |  Rate: {rate:.0f}%"
            (tw, _), _ = cv2.getTextSize(stat_str, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            cv2.putText(annotated, stat_str, (max(10, w - tw - 15), 27),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 230, 240), 1, cv2.LINE_AA)
            
    # Bottom Alert Banner if Violation Detected
    if alert:
        banner_h = 36
        banner_overlay = annotated.copy()
        cv2.rectangle(banner_overlay, (0, h - banner_h), (w, h), COLOR_ALERT, -1)
        cv2.addWeighted(banner_overlay, 0.88, annotated, 0.12, 0, annotated)
        alert_msg = " [!] WARNING: NO-HELMET VIOLATION DETECTED - E-CHALLAN LOGGED "
        (atw, _), _ = cv2.getTextSize(alert_msg, cv2.FONT_HERSHEY_DUPLEX, 0.52, 1)
        cv2.putText(annotated, alert_msg, (max(10, (w - atw) // 2), h - 12),
                    cv2.FONT_HERSHEY_DUPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)
        
    return annotated

def draw_detection_box(frame, bbox, label, score=None, is_violation=False, is_vehicle=False, show_score=True):
    """
    Draws a modern high-contrast bounding box with corner brackets and filled label badge.
    """
    x1, y1, x2, y2 = [int(v) for v in bbox]
    h_frame, w_frame = frame.shape[:2]
    
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w_frame, x2), min(h_frame, y2)
    
    if is_vehicle:
        color = COLOR_MOTORCYCLE
    elif is_violation:
        color = COLOR_NO_HELMET
    else:
        color = COLOR_HELMET
        
    # Main Rectangle
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)
    
    # Corner brackets for tactical aesthetic
    b_len = max(8, min(22, int((x2 - x1) * 0.2), int((y2 - y1) * 0.2)))
    t = 3
    # Top-Left
    cv2.line(frame, (x1, y1), (x1 + b_len, y1), color, t)
    cv2.line(frame, (x1, y1), (x1, y1 + b_len), color, t)
    # Top-Right
    cv2.line(frame, (x2, y1), (x2 - b_len, y1), color, t)
    cv2.line(frame, (x2, y1), (x2, y1 + b_len), color, t)
    # Bottom-Left
    cv2.line(frame, (x1, y2), (x1 + b_len, y2), color, t)
    cv2.line(frame, (x1, y2), (x1, y2 - b_len), color, t)
    # Bottom-Right
    cv2.line(frame, (x2, y2), (x2 - b_len, y2), color, t)
    cv2.line(frame, (x2, y2), (x2, y2 - b_len), color, t)
    
    # Label text
    if score is not None and show_score:
        text = f"{label} ({int(score * 100)}%)"
    else:
        text = label
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.46
    font_thickness = 1
    (tw, th), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    
    # Label badge position
    pill_y1 = max(0, y1 - th - 8)
    pill_y2 = y1
    pill_x1 = x1
    pill_x2 = min(w_frame, x1 + tw + 12)
    
    cv2.rectangle(frame, (pill_x1, pill_y1), (pill_x2, pill_y2), color, -1)
    cv2.putText(frame, text, (pill_x1 + 5, pill_y2 - 4),
                font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
    
    return frame
