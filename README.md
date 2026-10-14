# 🛡️ AI HelmetGuard: Real-Time Helmet Detection & Traffic Safety System

An end-to-end Deep Learning & Computer Vision working model for automated helmet detection, compliance monitoring, and traffic violation logging.

---

## 🌟 Features

- **Multi-Mode Operation**:
  - ⚡ **1-Click Live Demonstration**: Preloaded scenarios for quick testing and presentations.
  - 📸 **Image Upload & Inspection**: Test any custom street or traffic image.
  - 🎥 **Video Stream Analysis**: Frame-by-frame processing with dynamic FPS and violation tracker.
  - 📹 **Real-Time Webcam**: Live feed detection using your computer camera.
- **Smart Visual Analytics**:
  - Color-coded bounding boxes (🟢 Green for Helmet, 🔴 Red for Safety Violation).
  - Dynamic HUD overlay with system status, real-time FPS, and warning banners.
  - KPI Metrics Cards: Total Tracked, Compliant Count, Violations, Compliance Rate (%).
- **Automated Evidence Vault**:
  - Automatically crops violator images with timestamped evidence headers.
  - Records incident logs in `snapshots/violations_log.csv`.
  - 1-Click CSV report download.
- **Academic Ready**:
  - Complete teacher presentation guide and Viva Q&A included.

---

## 🚀 How to Run the Project

### Method 1: 1-Click Windows Launcher (Easiest)
Simply double-click:
```cmd
run_demo.bat
```

### Method 2: Manual Terminal Run
1. Open PowerShell or Command Prompt in this folder (`C:\Users\hp\.gemini\antigravity\scratch\helmet_detection_system`).
2. Run the Streamlit web dashboard:
```bash
py -3.14 -m streamlit run app.py
```
3. Open your browser at `http://localhost:8501`.

---

## 📁 Directory Structure

```
helmet_detection_system/
├── app.py                      # Streamlit interactive web dashboard
├── detector.py                 # Core YOLOv8 AI inference engine
├── utils/
│   ├── visualizer.py           # Futuristic HUD & bounding box rendering
│   └── logger.py               # Incident logger & evidence snapshot vault
├── sample_data/                # Preloaded test images & demo traffic video
│   ├── sample_with_helmet.jpg
│   ├── sample_no_helmet.jpg
│   ├── sample_construction_workers.jpg
│   ├── sample_motorcycle_helmet.jpg
│   ├── sample_pedestrian_no_helmet.jpg
│   ├── demo_traffic.mp4
│   ├── generate_samples.py
│   └── generate_test_video.py
├── weights/                    # Neural network weights (YOLOv8 helmet model)
│   └── helmet_model.pt
├── snapshots/                  # Auto-saved violation evidence snapshots & CSV logs
├── run_demo.bat                # 1-Click Windows launcher script
├── requirements.txt            # Dependency list
├── README.md                   # Project overview & documentation
└── Viva_Presentation_Guide.md  # Teacher presentation & viva Q&A script
```

---

## 🛠️ Tech Stack
- **Deep Learning Model**: YOLOv8 (CSPDarknet53 + PANet + Anchor-free Decoupled Head)
- **Computer Vision**: OpenCV (cv2)
- **Frameworks**: PyTorch, Ultralytics, Streamlit
- **Data & Visualization**: Pandas, NumPy, PIL
