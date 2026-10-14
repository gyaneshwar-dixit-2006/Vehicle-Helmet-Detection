# 🛡️ AI HelmetGuard – Vehicle Helmet Detection System

**AI-Powered Helmet Detection and Traffic Safety Monitoring System**

## 📌 Project Overview

AI HelmetGuard is an AI-based project designed to improve road safety by detecting helmet usage among two-wheeler riders using Computer Vision and Deep Learning.

The system analyzes images, videos, and live webcam feeds to identify helmet-related safety violations. It provides visual detection results through bounding boxes and supports violation logging for further review.

The project uses YOLOv8 for object detection, OpenCV for image and video processing, and Streamlit to provide an interactive web dashboard.

## 🎯 Project Objectives

- Detect helmet usage among two-wheeler riders.
- Analyze traffic images and videos.
- Perform real-time detection using a webcam.
- Display detection results using bounding boxes.
- Save snapshots of detected safety violations.
- Maintain violation records in CSV format.
- Support automated traffic safety monitoring.

## ✨ Key Features

### 1. Helmet Detection
Uses an AI-based object detection model to identify helmet-related objects and potential safety violations.

### 2. Image Detection
Upload traffic images and analyze them for helmet-related detections.

### 3. Video Analysis
Process video frames to detect helmets and display the results visually.

### 4. Live Webcam Detection
Use a connected webcam to perform real-time detection.

### 5. Visual Detection Results
- Green bounding boxes for helmet detections.
- Red bounding boxes for potential safety violations.

*Note: The actual colors and labels depend on the implementation in the detection code.*

### 6. Interactive Dashboard
Provides a Streamlit interface for selecting detection modes, viewing results, and monitoring available detection metrics.

### 7. Violation Logging
Save snapshots and records of detected violations for further analysis.

### 8. CSV Reports
Store incident information in CSV format for reviewing and analyzing recorded violations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLOv8 | Object detection |
| OpenCV | Image and video processing |
| PyTorch | Deep learning framework |
| Ultralytics | YOLO model implementation |
| Streamlit | Interactive web dashboard |
| NumPy | Numerical operations |
| Pandas | Data handling and CSV reports |
| PIL | Image processing |

## 🔄 Project Workflow

1. **Input Collection:** Provide an image, video, or live webcam feed.
2. **Frame Processing:** OpenCV processes the input images or video frames.
3. **Object Detection:** The YOLOv8 model analyzes the input and detects the classes it was trained to recognize.
4. **Result Visualization:** Display detected objects with bounding boxes and labels.
5. **Violation Logging:** Save relevant snapshots and incident records when configured.
6. **Report Generation:** Review recorded incidents using CSV reports.

## 📁 Project Structure

```text
Vehicle-Helmet-Detection/
│
├── app.py
├── detector.py
├── live_webcam.py
├── requirements.txt
├── yolov8n.pt
├── run_demo.bat
├── run_live_webcam.bat
│
├── sample data/
├── snapshots/
├── utils/
├── weights/
│
├── README.md
└── Viva_Presentation_Guide.md
```

### Important Files

- `app.py` – Main Streamlit dashboard.
- `detector.py` – Detection and inference logic.
- `live_webcam.py` – Webcam-based detection.
- `requirements.txt` – Required Python dependencies.
- `yolov8n.pt` – YOLOv8 model weights, if used by the application.
- `weights/` – Directory for model weights.
- `snapshots/` – Directory for saving detection snapshots and related records.
- `run_demo.bat` – Windows demo launcher.
- `run_live_webcam.bat` – Windows webcam launcher.
- `Viva_Presentation_Guide.md` – Project presentation and viva preparation guide.

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/gyaneshwar-dixit-2006/Vehicle-Helmet-Detection.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Vehicle-Helmet-Detection
```

### Step 3: Create a Virtual Environment

```bash
py -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

Open the following address in your browser:

```text
http://localhost:8501
```

**Alternative:** On Windows, you can use `run_demo.bat` if it is configured to launch the application.

## 🚀 How to Use

1. Install the required dependencies.
2. Launch the Streamlit application.
3. Select the available detection mode.
4. Upload an image or video, or choose live webcam detection.
5. Run the detection process.
6. View the results and detected objects.
7. Review saved snapshots and CSV records, if generated.

## 🌍 Applications

- Road safety monitoring.
- Helmet compliance analysis.
- Smart traffic surveillance.
- Computer Vision research.
- AI and Deep Learning demonstrations.
- Academic projects and prototypes.

## 🔮 Future Enhancements

- Vehicle number plate recognition using OCR.
- Linking detected violations with vehicle information.
- Automated incident report generation.
- Improved detection accuracy in different lighting conditions.
- Database integration for storing historical records.
- Detection of additional traffic rule violations.

## ⚠️ Limitations

Detection accuracy depends on image quality, lighting conditions, camera angle, traffic density, and the training data used by the model.

The system should be validated under real-world conditions before being used for official traffic enforcement. Human verification may be necessary to avoid incorrect violation classifications.

## 👨‍💻 Developer

**Gyaneshwar Dixit**

GitHub Profile: https://github.com/gyaneshwar-dixit-2006

Project Repository: https://github.com/gyaneshwar-dixit-2006/Vehicle-Helmet-Detection

## 📄 License

Check the repository for the applicable license before redistributing or modifying the project.

---

⭐ If you find this project useful, consider giving the repository a star!

**Built with Python, Computer Vision, and Deep Learning.**
