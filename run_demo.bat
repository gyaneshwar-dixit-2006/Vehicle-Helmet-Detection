@echo off
title AI HelmetGuard - Real-Time Helmet Detection System
color 0A
echo ==============================================================================
echo                 AI HELMETGUARD: REAL-TIME HELMET DETECTION SYSTEM             
echo                 Computer Vision & Deep Learning Traffic Safety Model          
echo ==============================================================================
echo.
echo [1/2] Verifying AI Models and Sample Data...
py -3.14 sample_data\generate_samples.py

echo.
echo [2/2] Launching Interactive Web Dashboard...
echo Dashboard will open automatically in your browser at http://localhost:8501
echo.
echo Tip: You can also launch the 60 FPS Native Desktop Camera window via Tab 4 or run_live_webcam.bat!
echo.
py -3.14 -m streamlit run app.py --server.headless false

pause
