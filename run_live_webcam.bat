@echo off
title AI HelmetGuard - Real-Time 60 FPS Native Camera
color 0B
echo ==============================================================================
echo            AI HELMETGUARD: REAL-TIME 60 FPS CAMERA MONITOR                   
echo ==============================================================================
echo.
echo Starting Native OpenCV Camera Window with Audio Alerts...
echo.
echo Controls:
echo   [Q] / [ESC] : Close Camera Window
echo   [S]         : Save Snapshot
echo   [+] / [-]   : Sensitivity Adjust
echo.
py -3.14 live_webcam.py
pause
