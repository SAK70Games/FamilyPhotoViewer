@echo off
REM Optional: create logs folder if you want logging
if not exist "D:\FamilyPhotoViewer\logs" mkdir "D:\FamilyPhotoViewer\logs"

REM Run the Python script
python "D:\FamilyPhotoViewer\scripts\family_photo_viewer.py" >> "D:\FamilyPhotoViewer\logs\family_photo_viewer_log.txt" 2>&1

pause
